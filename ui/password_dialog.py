<<<<<<< HEAD
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox,
)


class PasswordDialog(QDialog):
    def __init__(self, title: str = "Пароль", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(420, 110)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Введите пароль:"))

        self.edit = QLineEdit()
        self.edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.edit)

        bb = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

    def password(self) -> str:
=======
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox,
)


class PasswordDialog(QDialog):
    def __init__(self, title: str = "Пароль", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(420, 110)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Введите пароль:"))

        self.edit = QLineEdit()
        self.edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.edit)

        bb = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

    def password(self) -> str:
>>>>>>> 7518772216c1d981bbfd5895f875ea24751d8bd0
        return self.edit.text()