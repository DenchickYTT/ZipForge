from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox,
)


class RenameDialog(QDialog):
    def __init__(self, current_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Переименовать")
        self.resize(450, 120)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Текущее имя:\n{current_name}"))

        self.edit = QLineEdit(current_name)
        layout.addWidget(self.edit)

        bb = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

    def new_name(self) -> str:
        return self.edit.text().strip()