<<<<<<< HEAD
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QDialogButtonBox, QTabWidget, QWidget, QPushButton, QCheckBox,
    QMessageBox, QFormLayout
)
from core.settings import settings
from core.i18n import tr
from core.windows_integration import (
    register_context_menu, set_as_default, unregister_context_menu, clean_temp_files
)


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("dlg_settings_title"))
        self.resize(480, 400)

        layout = QVBoxLayout(self)
        
        # Создаем вкладки
        self.tabs = QTabWidget()
        
        # --- Вкладка 1: Основные ---
        self.tab_main = QWidget()
        main_layout = QFormLayout(self.tab_main)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("Русский", "ru")
        self.lang_combo.addItem("English", "en")
        self.lang_combo.addItem("Беларуская", "be")
        self.lang_combo.addItem("Deutsch", "de")
        idx = self.lang_combo.findData(settings.get("language", "ru"))
        self.lang_combo.setCurrentIndex(max(0, idx))
        main_layout.addRow(tr("settings_language"), self.lang_combo)

        self.theme_combo = QComboBox()
        self.theme_combo.addItem(tr("settings_theme_dark"), "dark")
        self.theme_combo.addItem(tr("settings_theme_light"), "light")
        idx = self.theme_combo.findData(settings.get("theme", "dark"))
        self.theme_combo.setCurrentIndex(max(0, idx))
        main_layout.addRow(tr("settings_theme"), self.theme_combo)
        
        self.tabs.addTab(self.tab_main, tr("menu_settings")) # Используем "Настройки" как заголовок основной вкладки
        
        # --- Вкладка 2: Архивы ---
        self.tab_archives = QWidget()
        arch_layout = QFormLayout(self.tab_archives)
        
        self.level_combo = QComboBox()
        for lvl in range(10):
            self.level_combo.addItem(str(lvl), lvl)
        self.level_combo.setCurrentIndex(settings.get("default_compression", 6))
        arch_layout.addRow("Уровень сжатия:", self.level_combo)
        
        self.tabs.addTab(self.tab_archives, "Архивы" if settings.get("language") == "ru" else "Archives")
        
        # --- Вкладка 3: Система ---
        self.tab_system = QWidget()
        sys_layout = QVBoxLayout(self.tab_system)
        
        # Интеграция
        sys_layout.addWidget(QLabel("<b>Интеграция с Windows</b>"))
        
        btn_reg = QPushButton("Зарегистрировать в 'Открыть с помощью'")
        btn_reg.clicked.connect(self._on_register)
        sys_layout.addWidget(btn_reg)
        
        btn_default = QPushButton("Сделать программой по умолчанию для ZIP")
        btn_default.clicked.connect(self._on_set_default)
        sys_layout.addWidget(btn_default)
        
        btn_unreg = QPushButton("Удалить из системы")
        btn_unreg.clicked.connect(self._on_unregister)
        sys_layout.addWidget(btn_unreg)
        
        sys_layout.addSpacing(15)
        
        # Очистка
        sys_layout.addWidget(QLabel("<b>Обслуживание</b>"))
        btn_clean = QPushButton("Очистить временные файлы (.tmp)")
        btn_clean.clicked.connect(self._on_clean_temp)
        sys_layout.addWidget(btn_clean)
        
        sys_layout.addStretch()
        self.tabs.addTab(self.tab_system, "Система" if settings.get("language") == "ru" else "System")

        layout.addWidget(self.tabs)

        # Кнопки OK/Cancel
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
        
    def selected_compression(self) -> int:
        return int(self.level_combo.currentData())

    def _on_register(self):
        ok, msg = register_context_menu()
        if ok: QMessageBox.information(self, "ZipForge", msg)
        else: QMessageBox.critical(self, "ZipForge", msg)

    def _on_set_default(self):
        ok, msg = set_as_default()
        if ok: QMessageBox.information(self, "ZipForge", msg)
        else: QMessageBox.critical(self, "ZipForge", msg)

    def _on_unregister(self):
        ok, msg = unregister_context_menu()
        if ok: QMessageBox.information(self, "ZipForge", msg)
        else: QMessageBox.critical(self, "ZipForge", msg)

    def _on_clean_temp(self):
        ok, msg, count = clean_temp_files()
        if ok: QMessageBox.information(self, "ZipForge", msg)
        else: QMessageBox.critical(self, "ZipForge", msg)
=======
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
>>>>>>> 7518772216c1d981bbfd5895f875ea24751d8bd0
