import os
import sys

from PyQt6.QtGui import QIcon


def resource_path(relative: str) -> str:
    """Возвращает путь к ресурсу и в исходниках, и в собранном .exe."""
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS  # PyInstaller распаковывает сюда
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)


def app_icon() -> QIcon:
    path = resource_path(os.path.join("resources", "icon.ico"))
    if os.path.exists(path):
        return QIcon(path)
    # fallback на png
    png = resource_path(os.path.join("resources", "icon.png"))
    return QIcon(png) if os.path.exists(png) else QIcon()


def set_windows_app_id() -> None:
    """Чтобы панель задач Windows показывала нашу иконку, а не Python."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "ZipForge.ArchiveTool.1"
        )
    except Exception:
        pass