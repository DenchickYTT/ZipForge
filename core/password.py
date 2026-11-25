import zipfile
import pyzipper


def open_zip(path: str, mode: str = "r", password: str | None = None):
    """
    Открывает ZIP с поддержкой AES-паролей.
    Если password задан — используем pyzipper.AESZipFile.
    Иначе — стандартный zipfile (быстрее и без зависимостей).
    """
    if password:
        zf = pyzipper.AESZipFile(
            path, mode,
            compression=pyzipper.ZIP_DEFLATED,
            encryption=pyzipper.WZ_AES,
        )
        zf.setpassword(password.encode("utf-8"))
        return zf
    return zipfile.ZipFile(path, mode, zipfile.ZIP_DEFLATED)


def is_encrypted_zip(path: str) -> bool:
    """Проверяет, есть ли в архиве зашифрованные записи."""
    try:
        with zipfile.ZipFile(path, "r") as zf:
            return any(i.flag_bits & 0x1 for i in zf.infolist())
    except Exception:
        return False