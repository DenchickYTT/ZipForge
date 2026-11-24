from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QDialogButtonBox,
)
from PyQt6.QtCore import Qt
from core.i18n import tr


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("dlg_about_title"))
        self.resize(420, 220)

        layout = QVBoxLayout(self)

        text = QLabel(tr("about_text"))
        text.setWordWrap(True)
        text.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(text)

        layout.addStretch()

        bb = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        bb.accepted.connect(self.accept)
        layout.addWidget(bb)