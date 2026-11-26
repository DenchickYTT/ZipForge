import os
import sys
from PyQt6.QtGui import QAction, QKeySequence, QIcon
from PyQt6.QtWidgets import (
    QMainWindow, QToolBar, QStatusBar, QWidget, QVBoxLayout,
    QLabel, QFileDialog, QMessageBox, QHBoxLayout, QDialog, QLineEdit,
    QStyle,
)
from PyQt6.QtCore import QTimer, Qt

from core.zip_engine import (
    read_entries, extract_all, extract_selected, create_archive,
    add_to_archive, delete_from_archive, rename_in_archive, move_in_archive,
    read_file_data, test_archive_integrity
)
from core.password import is_encrypted_zip
from core.archive_model import ArchiveEntry
from core.settings import settings, APP_VERSION
from core.i18n import tr
from core.updater import check_for_updates
from ui.archive_tree import ArchiveTreeView, human_size
from ui.progress_dialog import ProgressDialog
from ui.create_dialog import CreateArchiveDialog
from ui.rename_dialog import RenameDialog
from ui.password_dialog import PasswordDialog
from ui.settings_dialog import SettingsDialog
from ui.about_dialog import AboutDialog
from ui.preview_dialog import PreviewDialog

DARK_STYLE = """
QMainWindow, QWidget { background-color: #1e1e1e; color: #d4d4d4; font-family: "Segoe UI", "Ubuntu", sans-serif; font-size: 10pt; }
QToolBar { background-color: #252526; border-bottom: 1px solid #3c3c3c; padding: 4px; spacing: 4px; }
QToolBar QToolButton { color: #d4d4d4; padding: 6px 10px; border-radius: 4px; }
QToolBar QToolButton:hover { background-color: #3a3d41; }
QToolBar QToolButton:pressed { background-color: #094771; }
QTreeView { background-color: #1e1e1e; alternate-background-color: #232323; border: 1px solid #3c3c3c; color: #d4d4d4; }
QTreeView::item:selected { background-color: #094771; }
QHeaderView::section { background-color: #252526; color: #d4d4d4; padding: 4px; border: none; border-right: 1px solid #3c3c3c; }
QStatusBar { background-color: #007acc; color: white; }
QLabel#pathLabel { color: #858585; padding: 4px 8px; }
QListWidget, QLineEdit, QComboBox { background-color: #252526; color: #d4d4d4; border: 1px solid #3c3c3c; padding: 4px; border-radius: 4px; }
QPushButton { background-color: #3a3d41; color: #d4d4d4; border: 1px solid #3c3c3c; padding: 6px 12px; border-radius: 4px; }
QPushButton:hover { background-color: #4a4d51; }
QPushButton:pressed { background-color: #094771; }
QDialog { background-color: #1e1e1e; }
QMenuBar { background-color: #252526; color: #d4d4d4; }
QMenuBar::item:selected { background-color: #094771; }
QMenu { background-color: #252526; color: #d4d4d4; border: 1px solid #3c3c3c; }
QMenu::item:selected { background-color: #094771; }
QTabWidget::pane { border: 1px solid #3c3c3c; background: #1e1e1e; }
QTabBar::tab { background: #252526; color: #d4d4d4; padding: 8px 16px; border: 1px solid #3c3c3c; border-bottom: none; }
QTabBar::tab:selected { background: #094771; }
QProgressBar { border: 1px solid #3c3c3c; background-color: #252526; text-align: center; color: white; border-radius: 4px; }
QProgressBar::chunk { background-color: #007acc; border-radius: 3px; }
"""

LIGHT_STYLE = """
QMainWindow, QWidget { background-color: #f3f3f3; color: #1e1e1e; font-family: "Segoe UI", "Ubuntu", sans-serif; font-size: 10pt; }
QToolBar { background-color: #e8e8e8; border-bottom: 1px solid #c8c8c8; padding: 4px; spacing: 4px; }
QToolBar QToolButton { color: #1e1e1e; padding: 6px 10px; border-radius: 4px; }
QToolBar QToolButton:hover { background-color: #d0d0d0; }
QToolBar QToolButton:pressed { background-color: #b0d4f1; }
QTreeView { background-color: #ffffff; alternate-background-color: #f7f7f7; border: 1px solid #c8c8c8; color: #1e1e1e; }
QTreeView::item:selected { background-color: #cce4f7; color: #1e1e1e; }
QHeaderView::section { background-color: #e8e8e8; color: #1e1e1e; padding: 4px; border: none; border-right: 1px solid #c8c8c8; }
QStatusBar { background-color: #007acc; color: white; }
QLabel#pathLabel { color: #666666; padding: 4px 8px; }
QListWidget, QLineEdit, QComboBox { background-color: #ffffff; color: #1e1e1e; border: 1px solid #c8c8c8; padding: 4px; border-radius: 4px; }
QPushButton { background-color: #e8e8e8; color: #1e1e1e; border: 1px solid #c8c8c8; padding: 6px 12px; border-radius: 4px; }
QPushButton:hover { background-color: #d0d0d0; }
QPushButton:pressed { background-color: #b0d4f1; }
QDialog { background-color: #f3f3f3; }
QMenuBar { background-color: #e8e8e8; color: #1e1e1e; }
QMenuBar::item:selected { background-color: #cce4f7; }
QMenu { background-color: #ffffff; color: #1e1e1e; border: 1px solid #c8c8c8; }
QMenu::item:selected { background-color: #cce4f7; }
QTabWidget::pane { border: 1px solid #c8c8c8; background: #f3f3f3; }
QTabBar::tab { background: #e8e8e8; color: #1e1e1e; padding: 8px 16px; border: 1px solid #c8c8c8; border-bottom: none; }
QTabBar::tab:selected { background: #cce4f7; }
QProgressBar { border: 1px solid #c8c8c8; background-color: #ffffff; text-align: center; color: black; border-radius: 4px; }
QProgressBar::chunk { background-color: #007acc; border-radius: 3px; }
"""


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.current_archive: str | None = None
        self.current_entries: list[ArchiveEntry] = []
        self.current_password: str | None = None

        self._apply_style()
        self.setWindowTitle("ZipForge")
        self.resize(1000, 650)

        self._build_menu()
        self._build_toolbar()
        self._build_central()
        self._build_statusbar()

        QTimer.singleShot(2000, self._check_updates_on_startup)

    def _apply_style(self) -> None:
        theme = settings.get("theme", "dark")
        if theme == "system":
            if self.palette().color(self.backgroundRole()).lightness() > 128:
                theme = "light"
            else:
                theme = "dark"
        self.setStyleSheet(DARK_STYLE if theme == "dark" else LIGHT_STYLE)

    def _get_icon(self, standard_pixmap) -> QIcon:
        return self.style().standardIcon(standard_pixmap)

    def _build_menu(self) -> None:
        menubar = self.menuBar()
        file_menu = menubar.addMenu(tr("menu_file"))
        open_act = QAction(tr("open"), self)
        open_act.setShortcut(QKeySequence.StandardKey.Open)
        open_act.setIcon(self._get_icon(QStyle.StandardPixmap.SP_DialogOpenButton))
        open_act.triggered.connect(self._on_open)
        file_menu.addAction(open_act)

        create_act = QAction(tr("create"), self)
        create_act.setShortcut(QKeySequence.StandardKey.New)
        create_act.setIcon(self._get_icon(QStyle.StandardPixmap.SP_FileDialogNewFolder))
        create_act.triggered.connect(self._on_create)
        file_menu.addAction(create_act)

        file_menu.addSeparator()
        exit_act = QAction(tr("menu_exit"), self)
        exit_act.setShortcut(QKeySequence.StandardKey.Quit)
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)

        settings_menu = menubar.addMenu(tr("menu_settings"))
        prefs_act = QAction(tr("menu_preferences"), self)
        prefs_act.setIcon(self._get_icon(QStyle.StandardPixmap.SP_ComputerIcon))
        prefs_act.triggered.connect(self._on_settings)
        settings_menu.addAction(prefs_act)

        help_menu = menubar.addMenu(tr("menu_help"))
        about_act = QAction(tr("menu_about"), self)
        about_act.triggered.connect(self._on_about)
        help_menu.addAction(about_act)

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Main")
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)

        open_action = QAction(tr("open"), self)
        open_action.setIcon(self._get_icon(QStyle.StandardPixmap.SP_DialogOpenButton))
        open_action.triggered.connect(self._on_open)
        toolbar.addAction(open_action)

        create_action = QAction(tr("create"), self)
        create_action.setIcon(self._get_icon(QStyle.StandardPixmap.SP_FileDialogNewFolder))
        create_action.triggered.connect(self._on_create)
        toolbar.addAction(create_action)

        toolbar.addSeparator()

        extract_action = QAction(tr("extract"), self)
        extract_action.setIcon(self._get_icon(QStyle.StandardPixmap.SP_DialogSaveButton))
        extract_action.triggered.connect(self._on_extract)
        toolbar.addAction(extract_action)

        add_action = QAction(tr("add"), self)
        add_action.setIcon(self._get_icon(QStyle.StandardPixmap.SP_FileIcon))
        add_action.triggered.connect(self._on_add)
        toolbar.addAction(add_action)

        delete_action = QAction(tr("delete"), self)
        delete_action.setIcon(self._get_icon(QStyle.StandardPixmap.SP_TrashIcon))
        delete_action.setShortcut(QKeySequence(QKeySequence.StandardKey.Delete))
        delete_action.triggered.connect(self._on_delete)
        toolbar.addAction(delete_action)

        rename_action = QAction(tr("rename"), self)
        rename_action.setIcon(self._get_icon(QStyle.StandardPixmap.SP_FileDialogDetailedView))
        rename_action.setShortcut(QKeySequence("F2"))
        rename_action.triggered.connect(self._on_rename)
        toolbar.addAction(rename_action)

        toolbar.addSeparator()

        check_action = QAction(tr("btn_check"), self)
        check_action.setIcon(self._get_icon(QStyle.StandardPixmap.SP_DialogApplyButton))
        check_action.triggered.connect(self._on_check_integrity)
        toolbar.addAction(check_action)

    def _build_central(self) -> None:
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        path_bar = QHBoxLayout()
        path_bar.setContentsMargins(8, 4, 8, 4)
        self.path_label = QLabel(tr("status_no_archive"))
        self.path_label.setObjectName("pathLabel")
        path_bar.addWidget(self.path_label)
        path_bar.addStretch()

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText(tr("search_placeholder"))
        self.search_edit.setFixedWidth(250)
        self.search_edit.textChanged.connect(self._on_search_changed)
        path_bar.addWidget(self.search_edit)

        layout.addLayout(path_bar)

        self.tree = ArchiveTreeView()
        self.tree.set_drop_handler(self._on_tree_drop)
        self.tree.doubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.tree)

        self.setCentralWidget(central)

    def _build_statusbar(self) -> None:
        status = QStatusBar()
        self.setStatusBar(status)
        status.showMessage(tr("status_ready"))

    def _reload_archive(self) -> None:
        if not self.current_archive: return
        try:
            entries = read_entries(self.current_archive, self.current_password)
        except Exception as exc:
            QMessageBox.critical(self, tr("msg_error"), tr("msg_open_failed", err=exc))
            return
        self.current_entries = entries
        self.tree.load_entries(entries)
        self._update_status(entries)
        self.search_edit.clear()

    def _update_status(self, entries: list[ArchiveEntry]) -> None:
        total_size = sum(e.size for e in entries if not e.is_dir)
        total_comp = sum(e.compressed_size for e in entries if not e.is_dir)
        file_count = sum(1 for e in entries if not e.is_dir)
        self.statusBar().showMessage(
            f"{tr('status_files', n=file_count)} │ "
            f"{tr('status_original', size=human_size(total_size))} │ "
            f"{tr('status_in_archive', size=human_size(total_comp))}"
        )

    def _require_archive(self) -> bool:
        if not self.current_archive:
            QMessageBox.information(self, "ZipForge", tr("msg_open_first"))
            return False
        return True

    def _confirm_and_run(self, title: str, func) -> None:
        dlg = ProgressDialog(title, func, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._reload_archive()

    def _ask_password_if_needed(self, path: str) -> tuple[bool, str | None]:
        if not is_encrypted_zip(path): return True, None
        dlg = PasswordDialog(tr("dlg_password_title"), self)
        if dlg.exec() != QDialog.DialogCode.Accepted: return False, None
        return True, dlg.password()

    def _on_search_changed(self, text: str) -> None:
        self.tree.apply_filter(text)

    def _on_tree_drop(self, source_paths: list[str], target_dir: str) -> None:
        if not self._require_archive() or not source_paths: return
        for src in source_paths:
            if src.endswith("/") and target_dir.startswith(src):
                QMessageBox.warning(self, "ZipForge", tr("msg_folder_in_itself"))
                return
        archive = self.current_archive
        pw = self.current_password

        def task(cb):
            for src in source_paths:
                move_in_archive(archive, src, target_dir, pw, cb)
        self._confirm_and_run("Move", task)

    def _on_item_double_clicked(self, index) -> None:
        node = index.internalPointer()
        if node is None or node.entry is None or node.entry.is_dir: return
        parts = []
        cur = node
        while cur is not None and cur.name:
            parts.append(cur.name)
            cur = cur.parent
        file_path_in_zip = "/".join(reversed(parts))

        try:
            data = read_file_data(self.current_archive, file_path_in_zip, self.current_password)
        except Exception as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось прочитать файл:\n{exc}")
            return

        dlg = PreviewDialog(file_path_in_zip, data, self)
        result = dlg.exec()

        if result == 1:
            dest_dir = QFileDialog.getExistingDirectory(self, tr("dlg_extract_where"))
            if dest_dir:
                archive = self.current_archive
                pw = self.current_password
                task = lambda cb: extract_selected(archive, [file_path_in_zip], dest_dir, pw, cb)
                prog_dlg = ProgressDialog("Извлечение", task, self)
                if prog_dlg.exec() == QDialog.DialogCode.Accepted:
                    QMessageBox.information(self, "ZipForge", tr("msg_extracted_to", path=dest_dir))

    def _on_open(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, tr("dlg_open_title"), "", tr("dlg_open_filter"))
        if not path: return
        self._open_archive_from_path(path)

    def _open_archive_from_path(self, path: str) -> None:
        ok, password = self._ask_password_if_needed(path)
        if not ok: return
        try:
            entries = read_entries(path, password)
        except Exception as exc:
            QMessageBox.critical(self, tr("msg_error"), tr("msg_open_failed", err=exc))
            return
        self.current_archive = path
        self.current_password = password
        self.current_entries = entries
        self.tree.load_entries(entries)
        self.path_label.setText(path)
        self.setWindowTitle(f"ZipForge — {os.path.basename(path)}")
        self._update_status(entries)
        self.search_edit.clear()

    def _on_create(self) -> None:
        dlg = CreateArchiveDialog(self)
        dlg.level_combo.setCurrentIndex(settings.get("default_compression", 6))

        if dlg.exec() != QDialog.DialogCode.Accepted: return
        sources = dlg.sources()
        output = dlg.output_path()
        level = dlg.compression_level()
        password = dlg.password() or None

        task = lambda cb: create_archive(sources, output, level, password, cb)
        progress = ProgressDialog(tr("create"), task, self)
        if progress.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "ZipForge", tr("msg_archive_created", path=output))
            self._open_archive_from_path(output)

    def _on_extract(self) -> None:
        if not self._require_archive(): return
        selected = self.tree.selected_names()
        if selected:
            answer = QMessageBox.question(self, tr("extract"), tr("dlg_extract_q", n=len(selected)),
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
            if answer == QMessageBox.StandardButton.Cancel: return
            mode_selected = answer == QMessageBox.StandardButton.Yes
        else:
            mode_selected = False
        dest_dir = QFileDialog.getExistingDirectory(self, tr("dlg_extract_where"))
        if not dest_dir: return
        archive = self.current_archive
        pw = self.current_password
        if mode_selected:
            task = lambda cb: extract_selected(archive, selected, dest_dir, pw, cb)
        else:
            task = lambda cb: extract_all(archive, dest_dir, pw, cb)
        dlg = ProgressDialog(tr("extract"), task, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "ZipForge", tr("msg_extracted_to", path=dest_dir))

    def _on_add(self) -> None:
        if not self._require_archive(): return
        files, _ = QFileDialog.getOpenFileNames(self, tr("add"), "", "All files (*)")
        if not files:
            answer = QMessageBox.question(self, "ZipForge", "Add a folder?")
            if answer == QMessageBox.StandardButton.Yes:
                folder = QFileDialog.getExistingDirectory(self, tr("add"))
                if folder: files = [folder]
            if not files: return
        archive = self.current_archive
        pw = self.current_password
        self._confirm_and_run(tr("add"), lambda cb: add_to_archive(archive, files, pw, cb))
        QMessageBox.information(self, "ZipForge", tr("msg_added", path=archive))

    def _on_delete(self) -> None:
        if not self._require_archive(): return
        selected = self.tree.selected_names()
        if not selected:
            QMessageBox.information(self, "ZipForge", tr("msg_select_for_delete"))
            return
        
        if settings.get("confirm_delete", True):
            answer = QMessageBox.question(self, tr("delete"), tr("dlg_delete_q", n=len(selected)))
            if answer != QMessageBox.StandardButton.Yes: return
            
        archive = self.current_archive
        pw = self.current_password
        self._confirm_and_run(tr("delete"), lambda cb: delete_from_archive(archive, selected, pw, cb))
        QMessageBox.information(self, "ZipForge", tr("msg_deleted"))

    def _on_rename(self) -> None:
        if not self._require_archive(): return
        selected = self.tree.selected_names()
        if len(selected) != 1:
            QMessageBox.information(self, "ZipForge", tr("msg_select_one_rename"))
            return
        old_name = selected[0]
        is_dir = old_name.endswith("/")
        dlg = RenameDialog(old_name.rstrip("/"), self)
        if dlg.exec() != QDialog.DialogCode.Accepted: return
        new_name = dlg.new_name()
        if not new_name or new_name == old_name.rstrip("/"): return
        if is_dir: new_name += "/"
        archive = self.current_archive
        pw = self.current_password
        self._confirm_and_run(tr("rename"), lambda cb: rename_in_archive(archive, old_name, new_name, pw, cb))
        QMessageBox.information(self, "ZipForge", tr("msg_renamed", old=old_name, new=new_name))

    def _check_updates_on_startup(self) -> None:
        has_update, latest_ver, url = check_for_updates(force=False)
        if has_update:
            msg = tr("update_available", ver=latest_ver, current=APP_VERSION)
            reply = QMessageBox.question(
                self, tr("update_title"), msg,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                import webbrowser
                webbrowser.open(url)

    def _on_check_integrity(self) -> None:
        if not self._require_archive(): return
        archive = self.current_archive
        pw = self.current_password
        try:
            ok, bad_file = test_archive_integrity(archive, pw)
            if ok:
                QMessageBox.information(self, "ZipForge", tr("msg_check_ok"))
            else:
                QMessageBox.warning(self, "ZipForge", tr("msg_check_bad", name=bad_file))
        except Exception as e:
            QMessageBox.critical(self, "ZipForge", f"Ошибка проверки:\n{e}")

    def _on_settings(self) -> None:
        dlg = SettingsDialog(self)
        if dlg.exec() != QDialog.DialogCode.Accepted: return
        new_lang = dlg.selected_language()
        new_theme = dlg.selected_theme()
        new_comp = dlg.selected_compression()
        new_hidden = dlg.selected_show_hidden()
        new_confirm = dlg.selected_confirm_delete()
        new_preview = dlg.selected_preview_size()

        changed_lang = new_lang != settings.get("language", "ru")
        changed_theme = new_theme != settings.get("theme", "dark")

        settings.set("language", new_lang)
        settings.set("theme", new_theme)
        settings.set("default_compression", new_comp)
        settings.set("show_hidden", new_hidden)
        settings.set("confirm_delete", new_confirm)
        settings.set("preview_max_size", new_preview)

        if changed_theme: self._apply_style()
        if changed_lang:
            self.menuBar().clear()
            self._build_menu()
            for tb in self.findChildren(QToolBar):
                self.removeToolBar(tb)
                tb.deleteLater()
            self._build_toolbar()
            self.statusBar().showMessage(tr("status_ready"))
            if self.current_archive:
                self._update_status(self.current_entries)
            else:
                self.path_label.setText(tr("status_no_archive"))
            self.tree.header().reset()
            self.tree.viewport().update()
            self.search_edit.setPlaceholderText(tr("search_placeholder"))

    def _on_about(self) -> None:
        AboutDialog(self).exec()