import sys
import os
import winreg
import glob

APP_NAME = "ZipForge"
PROG_ID = "ZipForge.zip"
EXE_NAME = "ZipForge.exe"

def get_exe_path() -> str:
    """Возвращает путь к текущему .exe или .py файлу."""
    if getattr(sys, 'frozen', False):
        return sys.executable
    else:
        return f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}"'

def _register_base() -> tuple[bool, str]:
    """Базовая регистрация (OpenWith)."""
    exe_path = get_exe_path()
    icon_path = sys.executable if getattr(sys, 'frozen', False) else ""
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{PROG_ID}") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "ZipForge Archive")
        if icon_path:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{PROG_ID}\DefaultIcon") as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f"{icon_path},0")
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\{PROG_ID}\shell\open\command") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'{exe_path} "%1"')
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\Applications\{EXE_NAME}") as key:
            winreg.SetValueEx(key, "FriendlyAppName", 0, winreg.REG_SZ, "ZipForge")
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"Software\Classes\Applications\{EXE_NAME}\shell\open\command") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, f'{exe_path} "%1"')
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.zip\OpenWithProgids") as key:
            winreg.SetValueEx(key, PROG_ID, 0, winreg.REG_SZ, "")
        return True, "ZipForge успешно зарегистрирован в списке 'Открыть с помощью'."
    except Exception as e:
        return False, f"Ошибка при записи в реестр:\n{e}"

def register_context_menu() -> tuple[bool, str]:
    return _register_base()

def set_as_default() -> tuple[bool, str]:
    """Делает ZipForge программой по умолчанию для .zip."""
    ok, msg = _register_base()
    if not ok: return False, msg
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.zip") as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, PROG_ID)
        return True, "ZipForge назначен программой по умолчанию для ZIP-файлов.\n\nWindows может показать уведомление о смене ассоциации — это нормально."
    except Exception as e:
        return False, f"Ошибка при назначении по умолчанию:\n{e}"

def unregister_context_menu() -> tuple[bool, str]:
    def delete_key_recursive(key_path):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, 0)
                        delete_key_recursive(f"{key_path}\\{subkey_name}")
                    except OSError:
                        break
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
        except (FileNotFoundError, OSError):
            pass
    try:
        delete_key_recursive(rf"Software\Classes\{PROG_ID}")
        delete_key_recursive(rf"Software\Classes\Applications\{EXE_NAME}")
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.zip\OpenWithProgids", 0, winreg.KEY_ALL_ACCESS) as key:
                winreg.DeleteValue(key, PROG_ID)
        except (FileNotFoundError, OSError):
            pass
        # Сбрасываем ассоциацию по умолчанию, если она была
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.zip", 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "")
        except (FileNotFoundError, OSError):
            pass
        return True, "ZipForge удалён из системы (OpenWith и ассоциации)."
    except Exception as e:
        return False, f"Ошибка при удалении:\n{e}"

def clean_temp_files() -> tuple[bool, str, int]:
    """Ищет и удаляет файлы .zipforge_*.tmp в текущей папке с программой и в профиле."""
    count = 0
    dirs_to_check = [
        os.path.dirname(get_exe_path().strip('"')),
        os.path.expanduser("~"),
    ]
    for d in set(dirs_to_check):
        if not os.path.isdir(d): continue
        for f in glob.glob(os.path.join(d, "*.zipforge_*.tmp")):
            try:
                os.remove(f)
                count += 1
            except OSError:
                pass
    if count > 0:
        return True, f"Очищено временных файлов: {count}", count
    else:
        return True, "Временные файлы не найдены.", 0