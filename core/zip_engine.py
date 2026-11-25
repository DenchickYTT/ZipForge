import os
import zipfile
from datetime import datetime
from core.archive_model import ArchiveEntry
from features.atomic_rebuild import atomic_rebuild
from core.password import open_zip
from core.i18n import tr


def read_entries(zip_path: str, password: str | None = None) -> list[ArchiveEntry]:
    entries: list[ArchiveEntry] = []
    with open_zip(zip_path, "r", password) as zf:
        for info in zf.infolist():
            is_dir = info.is_dir()
            try:
                mtime = datetime(*info.date_time)
            except (ValueError, OverflowError):
                mtime = datetime.now()

            entries.append(ArchiveEntry(
                name=info.filename,
                size=info.file_size,
                compressed_size=info.compress_size,
                mtime=mtime,
                is_dir=is_dir,
                crc=info.CRC,
                encrypted=bool(info.flag_bits & 0x1),
            ))
    return entries


def _safe_target(dest_dir: str, arcname: str) -> str:
    dest_dir_abs = os.path.abspath(dest_dir)
    target = os.path.abspath(os.path.join(dest_dir_abs, arcname))
    if not (target == dest_dir_abs or target.startswith(dest_dir_abs + os.sep)):
        raise ValueError(f"Небезопасный путь в архиве: {arcname}")
    return target


def extract_all(zip_path: str, dest_dir: str, password: str | None = None, progress_cb=None) -> None:
    with open_zip(zip_path, "r", password) as zf:
        infos = zf.infolist()
        total = len(infos)
        for i, info in enumerate(infos, start=1):
            target = _safe_target(dest_dir, info.filename)
            if info.is_dir():
                os.makedirs(target, exist_ok=True)
            else:
                parent = os.path.dirname(target)
                if parent: os.makedirs(parent, exist_ok=True)
                with zf.open(info) as src, open(target, "wb") as dst:
                    while True:
                        chunk = src.read(65536)
                        if not chunk: break
                        dst.write(chunk)
            if progress_cb:
                progress_cb(i, total, info.filename)


def extract_selected(zip_path: str, names: list[str], dest_dir: str, password: str | None = None, progress_cb=None) -> None:
    if not names: return
    with open_zip(zip_path, "r", password) as zf:
        all_infos = zf.infolist()
        def matches(info_name: str) -> bool:
            for n in names:
                if info_name == n: return True
                if info_name.startswith(n.rstrip("/") + "/"): return True
            return False

        selected = [i for i in all_infos if matches(i.filename)]
        total = len(selected)
        for i, info in enumerate(selected, start=1):
            target = _safe_target(dest_dir, info.filename)
            if info.is_dir():
                os.makedirs(target, exist_ok=True)
            else:
                parent = os.path.dirname(target)
                if parent: os.makedirs(parent, exist_ok=True)
                with zf.open(info) as src, open(target, "wb") as dst:
                    while True:
                        chunk = src.read(65536)
                        if not chunk: break
                        dst.write(chunk)
            if progress_cb:
                progress_cb(i, total, info.filename)


def _collect_files(sources: list[str]) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for src in sources:
        src = os.path.abspath(src)
        if os.path.isfile(src):
            result.append((src, os.path.basename(src)))
        elif os.path.isdir(src):
            base_parent = os.path.dirname(src)
            for root, _dirs, files in os.walk(src):
                for f in files:
                    full = os.path.join(root, f)
                    arcname = os.path.relpath(full, base_parent).replace(os.sep, "/")
                    result.append((full, arcname))
    return result


def create_archive(sources: list[str], output_zip: str, compression_level: int = 6, password: str | None = None, progress_cb=None) -> None:
    files = _collect_files(sources)
    total = len(files)
    if total == 0: raise ValueError("Нечего архивировать: источники пусты.")

    if password:
        import pyzipper
        zf = pyzipper.AESZipFile(output_zip, "w", compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES)
        zf.setpassword(password.encode("utf-8"))
    else:
        zf = zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=max(0, min(9, compression_level)))

    with zf:
        for i, (full_path, arcname) in enumerate(files, start=1):
            zf.write(full_path, arcname=arcname)
            if progress_cb: progress_cb(i, total, arcname)


def add_to_archive(zip_path: str, sources: list[str], password: str | None = None, progress_cb=None) -> None:
    add_files = _collect_files(sources)
    atomic_rebuild(zip_path, add_files=add_files, password=password, progress_cb=progress_cb)


def delete_from_archive(zip_path: str, names: list[str], password: str | None = None, progress_cb=None) -> None:
    with open_zip(zip_path, "r", password) as zf:
        existing = [i.filename for i in zf.infolist()]
    delete_set: set[str] = set()
    for name in names:
        is_dir = name.endswith("/")
        base = name.rstrip("/")
        if is_dir:
            prefix = base + "/"
            for f in existing:
                if f == name or f == base or f.startswith(prefix): delete_set.add(f)
        else:
            if name in existing: delete_set.add(name)
    atomic_rebuild(zip_path, delete_names=list(delete_set), password=password, progress_cb=progress_cb)


def rename_in_archive(zip_path: str, old_name: str, new_name: str, password: str | None = None, progress_cb=None) -> None:
    rename_map: dict[str, str] = {}
    if old_name.endswith("/") and new_name.endswith("/"):
        rename_map[old_name] = new_name
    else:
        rename_map[old_name] = new_name
    atomic_rebuild(zip_path, rename_map=rename_map, password=password, progress_cb=progress_cb)


def move_in_archive(zip_path: str, source_name: str, target_dir: str, password: str | None = None, progress_cb=None) -> None:
    base = source_name.rstrip("/").rsplit("/", 1)[-1]
    is_dir = source_name.endswith("/")
    if target_dir:
        new_name = target_dir.rstrip("/") + "/" + base
    else:
        new_name = base
    if is_dir: new_name += "/"
    if new_name == source_name: return
    rename_in_archive(zip_path, source_name, new_name, password, progress_cb)


# --- НОВАЯ ФУНКЦИЯ ДЛЯ ПРЕДПРОСМОТРА ---
def read_file_data(zip_path: str, name: str, password: str | None = None, max_size: int = 10 * 1024 * 1024) -> bytes:
    """Читает байты файла из архива (до max_size), не извлекая его на диск."""
    with open_zip(zip_path, "r", password) as zf:
        try:
            info = zf.getinfo(name)
            if info.file_size > max_size:
                # Читаем частично
                with zf.open(info) as f:
                    return f.read(max_size)
            else:
                return zf.read(info)
        except KeyError:
            raise ValueError(f"Файл {name} не найден в архиве.")