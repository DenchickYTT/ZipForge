<<<<<<< HEAD
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QProgressBar, QMessageBox,
)


class Worker(QThread):
    """
    Выполняет функцию в фоне.
    func(progress_cb) — функция, которая принимает колбэк (done, total, name).
    """
    progress = pyqtSignal(int, int, str)
    finished_ok = pyqtSignal()
    failed = pyqtSignal(str)

    def __init__(self, func, parent=None):
        super().__init__(parent)
        self.func = func

    def run(self):
        try:
            self.func(self._cb)
            self.finished_ok.emit()
        except Exception as exc:
            self.failed.emit(str(exc))

    def _cb(self, done: int, total: int, name: str) -> None:
        self.progress.emit(done, total, name)


class ProgressDialog(QDialog):
    """Модальный диалог с прогресс-баром и фоновым потоком."""

    def __init__(self, title: str, func, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(500, 140)

        layout = QVBoxLayout(self)

        self.label = QLabel("Подготовка…")
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        layout.addWidget(self.bar)

        self.worker = Worker(func, self)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished_ok.connect(self.accept)
        self.worker.failed.connect(self._on_failed)

        self.worker.start()

    def _on_progress(self, done: int, total: int, name: str) -> None:
        if total > 0:
            self.bar.setRange(0, total)
            self.bar.setValue(done)
        short = name if len(name) <= 60 else "…" + name[-57:]
        self.label.setText(f"[{done}/{total}] {short}")

    def _on_failed(self, message: str) -> None:
        self.label.setText(f"Ошибка: {message}")
        self.bar.setRange(0, 1)
        self.bar.setValue(1)
        QMessageBox.critical(self, "Ошибка", message)
=======
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QProgressBar, QMessageBox,
)


class Worker(QThread):
    """
    Выполняет функцию в фоне.
    func(progress_cb) — функция, которая принимает колбэк (done, total, name).
    """
    progress = pyqtSignal(int, int, str)
    finished_ok = pyqtSignal()
    failed = pyqtSignal(str)

    def __init__(self, func, parent=None):
        super().__init__(parent)
        self.func = func

    def run(self):
        try:
            self.func(self._cb)
            self.finished_ok.emit()
        except Exception as exc:
            self.failed.emit(str(exc))

    def _cb(self, done: int, total: int, name: str) -> None:
        self.progress.emit(done, total, name)


class ProgressDialog(QDialog):
    """Модальный диалог с прогресс-баром и фоновым потоком."""

    def __init__(self, title: str, func, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(500, 140)

        layout = QVBoxLayout(self)

        self.label = QLabel("Подготовка…")
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        layout.addWidget(self.bar)

        self.worker = Worker(func, self)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished_ok.connect(self.accept)
        self.worker.failed.connect(self._on_failed)

        self.worker.start()

    def _on_progress(self, done: int, total: int, name: str) -> None:
        if total > 0:
            self.bar.setRange(0, total)
            self.bar.setValue(done)
        short = name if len(name) <= 60 else "…" + name[-57:]
        self.label.setText(f"[{done}/{total}] {short}")

    def _on_failed(self, message: str) -> None:
        self.label.setText(f"Ошибка: {message}")
        self.bar.setRange(0, 1)
        self.bar.setValue(1)
        QMessageBox.critical(self, "Ошибка", message)
>>>>>>> 7518772216c1d981bbfd5895f875ea24751d8bd0
        self.reject()