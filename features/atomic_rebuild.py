import os
import tempfile
import zipfile
import shutil
from datetime import datetime


def atomic_rebuild(
    zip_path: str,
    add_files: list[tuple[str, str]] | None = None,
    delete_names: list[str] | None = None,
    rename_map: dict[str, str] | None = None,
    password: str | None = None,
    progress_cb=None,
) -> None:
    add_files = add_files or []
    delete_names = set(delete_names or [])
    rename_map = rename_map or {}

    dir_name = os.path.dirname(os.path.abspath(zip_path))
    fd, tmp_path = tempfile.mkstemp(
        prefix=".zipforge_", suffix=".zip.tmp", dir=dir_name
    )
    os.close(fd)

    try:
        if password:
            import pyzipper
            src = pyzipper.AESZipFile(zip_path, "r")
            src.setpassword(password.encode("utf-8"))
            dst = pyzipper.AESZipFile(
                tmp_path, "w",
                compression=pyzipper.ZIP_DEFLATED,
                encryption=pyzipper.WZ_AES,
            )
            dst.setpassword(password.encode("utf-8"))
        else:
            src = zipfile.ZipFile(zip_path, "r")
            dst = zipfile.ZipFile(
                tmp_path, "w",
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=6,
            )

        with src, dst:
            src_infos = src.infolist()
            total = len(src_infos) + len(add_files)
            done = 0

            for info in src_infos:
                old_name = info.filename
                if old_name in delete_names:
                    done += 1
                    if progress_cb:
                        progress_cb(done, total, f"удаление: {old_name}")
                    continue

                new_name = rename_map.get(old_name, old_name)
                for old_prefix, new_prefix in rename_map.items():
                    if old_prefix.endswith("/") and old_name.startswith(old_prefix):
                        new_name = new_prefix + old_name[len(old_prefix):]
                        break

                if info.is_dir():
                    if new_name != old_name:
                        zi = zipfile.ZipInfo(new_name)
                        zi.date_time = info.date_time
                        zi.external_attr = info.external_attr
                        dst.writestr(zi, b"")
                else:
                    with src.open(info) as fsrc:
                        new_info = zipfile.ZipInfo(new_name)
                        new_info.date_time = info.date_time
                        new_info.compress_type = zipfile.ZIP_DEFLATED
                        new_info.external_attr = info.external_attr
                        with dst.open(new_info, "w") as fdst:
                            shutil.copyfileobj(fsrc, fdst, length=65536)

                done += 1
                if progress_cb:
                    msg = old_name if new_name == old_name else f"{old_name} → {new_name}"
                    progress_cb(done, total, msg)

            for abs_path, arcname in add_files:
                if progress_cb:
                    progress_cb(done + 1, total, f"добавление: {arcname}")
                dst.write(abs_path, arcname=arcname)
                done += 1

        os.replace(tmp_path, zip_path)

    except Exception:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        raise