import sys
import os
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

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())