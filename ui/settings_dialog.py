from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QDialogButtonBox,
)
from core.settings import settings
from core.i18n import tr


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("dlg_settings_title"))
        self.resize(420, 200)

        layout = QVBoxLayout(self)

        # Язык
        lang_row = QHBoxLayout()
        lang_row.addWidget(QLabel(tr("settings_language")))
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("Русский", "ru")
        self.lang_combo.addItem("English", "en")
        idx = self.lang_combo.findData(settings.get("language", "ru"))
        self.lang_combo.setCurrentIndex(max(0, idx))
        lang_row.addWidget(self.lang_combo, stretch=1)
        layout.addLayout(lang_row)

        # Тема
        theme_row = QHBoxLayout()
        theme_row.addWidget(QLabel(tr("settings_theme")))
        self.theme_combo = QComboBox()
        self.theme_combo.addItem(tr("settings_theme_dark"), "dark")
        self.theme_combo.addItem(tr("settings_theme_light"), "light")
        idx = self.theme_combo.findData(settings.get("theme", "dark"))
        self.theme_combo.setCurrentIndex(max(0, idx))
        theme_row.addWidget(self.theme_combo, stretch=1)
        layout.addLayout(theme_row)

        hint = QLabel(tr("settings_restart_hint"))
        hint.setStyleSheet("color: #858585; font-size: 9pt;")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        layout.addStretch()

        bb = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        bb.button(QDialogButtonBox.StandardButton.Ok).setText(tr("settings_apply"))
        bb.button(QDialogButtonBox.StandardButton.Cancel).setText(tr("settings_cancel"))
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

    def selected_language(self) -> str:
        return self.lang_combo.currentData()

    def selected_theme(self) -> str:
        return self.theme_combo.currentData()