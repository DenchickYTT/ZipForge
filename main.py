import sys
import os

# --- КОСТЫЛЬ ДЛЯ PYINSTALLER ---
# Явно импортируем все локальные модули, чтобы PyInstaller их увидел
import core.zip_engine
import core.updater
import core.windows_integration
import core.settings
import core.i18n
import core.password
import core.archive_model
import ui.main_window
import ui.archive_tree
import ui.settings_dialog
import ui.create_dialog
import ui.preview_dialog
import ui.progress_dialog
import ui.password_dialog
import ui.rename_dialog
import ui.about_dialog
import features.atomic_rebuild
# ------------------------------

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def resource_path(relative: str) -> str:
    """Возвращает путь к ресурсу, работает и в .exe, и в исходниках."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("ZipForge")
    app.setOrganizationName("ZipForge")

    icon_path = resource_path("resources/icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()

    # --- ОБРАБОТКА АРГУМЕНТОВ КОМАНДНОЙ СТРОКИ ---
    if len(sys.argv) > 1:
        file_path = sys.argv[-1]
        if os.path.isfile(file_path) and file_path.lower().endswith(".zip"):
            window._open_archive_from_path(file_path)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())