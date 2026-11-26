import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QFileDialog, QComboBox,
    QLineEdit, QMessageBox, QDialogButtonBox,
)


class CreateArchiveDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Создать архив")
        self.resize(620, 460)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Что архивировать:"))

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(
            QListWidget.SelectionMode.ExtendedSelection
        )
        layout.addWidget(self.list_widget, stretch=1)

        buttons_row = QHBoxLayout()
        add_files_btn = QPushButton("Добавить файлы…")
        add_files_btn.clicked.connect(self._add_files)
        add_dir_btn = QPushButton("Добавить папку…")
        add_dir_btn.clicked.connect(self._add_dir)
        remove_btn = QPushButton("Убрать из списка")
        remove_btn.clicked.connect(self._remove_selected)
        buttons_row.addWidget(add_files_btn)
        buttons_row.addWidget(add_dir_btn)
        buttons_row.addWidget(remove_btn)
        buttons_row.addStretch()
        layout.addLayout(buttons_row)

        layout.addWidget(QLabel("Сохранить как:"))
        out_row = QHBoxLayout()
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("Путь к новому .zip файлу")
        browse_btn = QPushButton("Обзор…")
        browse_btn.clicked.connect(self._browse_output)
        out_row.addWidget(self.output_edit, stretch=1)
        out_row.addWidget(browse_btn)
        layout.addLayout(out_row)

        level_row = QHBoxLayout()
        level_row.addWidget(QLabel("Уровень сжатия:"))
        self.level_combo = QComboBox()
        for lvl, label in [
            (0, "0 — без сжатия (быстро)"),
            (1, "1 — минимальный"),
            (3, "3 — лёгкий"),
            (6, "6 — обычный (по умолчанию)"),
            (9, "9 — максимальный (медленно)"),
        ]:
            self.level_combo.addItem(label, lvl)
        self.level_combo.setCurrentIndex(3)
        level_row.addWidget(self.level_combo)
        level_row.addStretch()
        layout.addLayout(level_row)

        pass_row = QHBoxLayout()
        pass_row.addWidget(QLabel("Пароль (опционально):"))
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("Оставьте пустым, если не нужен")
        pass_row.addWidget(self.password_edit, stretch=1)
        layout.addLayout(pass_row)

        bb = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        bb.accepted.connect(self._on_ok)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

    def _add_files(self) -> None:
        paths, _ = QFileDialog.getOpenFileNames(self, "Выберите файлы")
        for p in paths:
            self._append_path(p)

    def _add_dir(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if path:
            self._append_path(path)

    def _append_path(self, path: str) -> None:
        for i in range(self.list_widget.count()):
            if self.list_widget.item(i).data(Qt.ItemDataRole.UserRole) == path:
                return
        item = QListWidgetItem(path)
        item.setData(Qt.ItemDataRole.UserRole, path)
        self.list_widget.addItem(item)

    def _remove_selected(self) -> None:
        for item in self.list_widget.selectedItems():
            self.list_widget.takeItem(self.list_widget.row(item))

    def _browse_output(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить архив", "", "ZIP-архив (*.zip)"
        )
        if path:
            if not path.lower().endswith(".zip"):
                path += ".zip"
            self.output_edit.setText(path)

    def _on_ok(self) -> None:
        if self.list_widget.count() == 0:
            QMessageBox.warning(self, "ZipForge", "Добавьте хотя бы один файл или папку.")
            return
        output = self.output_edit.text().strip()
        if not output:
            QMessageBox.warning(self, "ZipForge", "Укажите путь для сохранения архива.")
            return
        if not output.lower().endswith(".zip"):
            output += ".zip"
            self.output_edit.setText(output)

        if os.path.exists(output):
            answer = QMessageBox.question(
                self, "Файл существует",
                f"Файл уже существует:\n{output}\nПерезаписать?",
            )
            if answer != QMessageBox.StandardButton.Yes:
                return

        self.accept()

    def sources(self) -> list[str]:
        return [
            self.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(self.list_widget.count())
        ]

    def output_path(self) -> str:
        return self.output_edit.text().strip()

    def compression_level(self) -> int:
        return int(self.level_combo.currentData())

    def password(self) -> str:
        return self.password_edit.text()