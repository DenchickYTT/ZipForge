<<<<<<< HEAD
import os
from PyQt6.QtCore import Qt, QAbstractItemModel, QModelIndex, QFileInfo
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtWidgets import QTreeView, QAbstractItemView, QFileIconProvider

from core.archive_model import ArchiveEntry
from core.i18n import tr


def human_size(num: int) -> str:
    for unit in ("Б", "КБ", "МБ", "ГБ", "ТБ"):
        if abs(num) < 1024.0:
            return f"{num:.1f} {unit}" if unit != "Б" else f"{num} {unit}"
        num /= 1024.0
    return f"{num:.1f} ПБ"


class TreeNode:
    def __init__(self, name: str, entry: ArchiveEntry | None = None, parent=None):
        self.name = name
        self.entry = entry
        self.parent: TreeNode | None = parent
        self.children: list[TreeNode] = []
        self.is_visible = True  # Для фильтрации

    def row(self) -> int:
        if self.parent:
            return self.parent.children.index(self)
        return 0


class ArchiveTreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._root = TreeNode("")
        self._entries: list[ArchiveEntry] = []
        self._icon_provider = QFileIconProvider()

    def _columns(self) -> list[str]:
        return [
            tr("col_name"), tr("col_size"), tr("col_compressed"),
            tr("col_ratio"), tr("col_date"),
        ]

    def load_entries(self, entries: list[ArchiveEntry]) -> None:
        self.beginResetModel()
        self._entries = entries
        self._root = TreeNode("")
        self._build_tree(entries)
        self.endResetModel()

    def _build_tree(self, entries: list[ArchiveEntry]) -> None:
        for entry in entries:
            if entry.is_dir:
                self._ensure_path(entry.name.rstrip("/").split("/"), entry)
        for entry in entries:
            if not entry.is_dir:
                parts = entry.name.split("/")
                folder_parts, file_name = parts[:-1], parts[-1]
                parent = self._ensure_path(folder_parts, None) if folder_parts else self._root
                node = TreeNode(file_name, entry, parent)
                parent.children.append(node)

        self._sort_recursive(self._root)

    def _ensure_path(self, parts: list[str], entry: ArchiveEntry | None) -> TreeNode:
        node = self._root
        for i, part in enumerate(parts):
            found = None
            for c in node.children:
                if c.name == part and (c.entry is None or c.entry.is_dir):
                    found = c
                    break
            if found is None:
                node_entry = entry if i == len(parts) - 1 else None
                found = TreeNode(part, node_entry, node)
                node.children.append(found)
            node = found
        return node

    def _sort_recursive(self, node: TreeNode) -> None:
        node.children.sort(key=lambda n: (n.entry is not None, n.name.lower()))
        for child in node.children:
            self._sort_recursive(child)

    # --- Поиск и фильтрация ---
    def apply_filter(self, text: str) -> None:
        text = text.lower().strip()

        def _filter_node(node: TreeNode) -> bool:
            # Если это файл — проверяем его имя
            if node.entry is not None and not node.entry.is_dir:
                match = text in node.name.lower()
                node.is_visible = match
                return match

            # Если это папка (или корень) — проверяем детей
            any_child_visible = False
            for child in node.children:
                if _filter_node(child):
                    any_child_visible = True
            
            # Папка видима, если она сама совпадает по имени ИЛИ внутри есть совпадения
            match_self = text in node.name.lower() if node.name else False
            node.is_visible = any_child_visible or match_self
            return node.is_visible

        self.layoutAboutToBeChanged.emit()
        _filter_node(self._root)
        self.layoutChanged.emit()

    # --- Модель ---
    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        parent_node = parent.internalPointer() if parent.isValid() else self._root
        
        # Берем только видимых детей
        visible_children = [c for c in parent_node.children if c.is_visible]
        if row >= len(visible_children):
            return QModelIndex()
            
        child = visible_children[row]
        return self.createIndex(row, column, child)

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        node: TreeNode = index.internalPointer()
        parent_node = node.parent
        if parent_node is None or parent_node is self._root:
            return QModelIndex()
        return self.createIndex(parent_node.row(), 0, parent_node)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0
        node = parent.internalPointer() if parent.isValid() else self._root
        return len([c for c in node.children if c.is_visible])

    def columnCount(self, parent=QModelIndex()):
        return 5

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        node: TreeNode = index.internalPointer()
        entry = node.entry
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0: return node.name
            if entry is None: return ""
            if col == 1: return human_size(entry.size)
            if col == 2: return human_size(entry.compressed_size)
            if col == 3: return f"{entry.ratio * 100:.0f}%"
            if col == 4: return entry.mtime.strftime("%d.%m.%Y %H:%M")

        if role == Qt.ItemDataRole.TextAlignmentRole and col > 0:
            return int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        if role == Qt.ItemDataRole.ForegroundRole:
            if entry is None: return QColor("#4ec9b0")
            if entry.encrypted: return QColor("#dcdcaa")

        # Иконки
        if role == Qt.ItemDataRole.DecorationRole and col == 0:
            if entry is None:
                return self._icon_provider.icon(QFileIconProvider.IconType.Folder)
            else:
                # Создаем фиктивный файл, чтобы Windows выдала иконку
                # (для exe, mp3, txt и т.д.)
                fake_path = f"dummy{os.path.splitext(node.name)[1]}"
                return self._icon_provider.icon(QFileInfo(fake_path))

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            cols = self._columns()
            if 0 <= section < len(cols):
                return cols[section]
        return None

    def flags(self, index):
        base = super().flags(index)
        if not index.isValid():
            return base | Qt.ItemFlag.ItemIsDropEnabled
        node: TreeNode = index.internalPointer()
        if node.entry is None or node.entry.is_dir:
            return base | Qt.ItemFlag.ItemIsDropEnabled | Qt.ItemFlag.ItemIsDragEnabled
        return base | Qt.ItemFlag.ItemIsDragEnabled

    def supportedDropActions(self):
        return Qt.DropAction.MoveAction

    def mimeTypes(self):
        return ["application/x-zipforge-entry"]

    def mimeData(self, indexes):
        from PyQt6.QtCore import QMimeData
        data = QMimeData()
        paths = []
        for idx in indexes:
            if idx.column() != 0: continue
            node = idx.internalPointer()
            parts = []
            cur = node
            while cur is not None and cur.name:
                parts.append(cur.name)
                cur = cur.parent
            full = "/".join(reversed(parts))
            if node.entry is None:
                full += "/"
            paths.append(full)
        data.setData("application/x-zipforge-entry", "\n".join(paths).encode("utf-8"))
        return data


class ArchiveTreeView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = ArchiveTreeModel(self)
        self.setModel(self._model)
        self.setAlternatingRowColors(True)
        self.setUniformRowHeights(True)
        self.setSortingEnabled(False)
        self.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        self.setColumnWidth(0, 400)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 70)
        self.setColumnWidth(4, 140)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self._drop_handler = None

    def set_drop_handler(self, handler):
        self._drop_handler = handler

    def load_entries(self, entries: list[ArchiveEntry]) -> None:
        self._model.load_entries(entries)
        self.expandToDepth(0)
        self.header().reset()

    def apply_filter(self, text: str) -> None:
        self._model.apply_filter(text)
        if text:
            self.expandAll()

    def selected_names(self) -> list[str]:
        names: list[str] = []
        indexes = self.selectionModel().selectedIndexes()
        seen = set()
        for idx in indexes:
            if idx.column() != 0: continue
            node = idx.internalPointer()
            parts = []
            cur = node
            while cur is not None and cur.name:
                parts.append(cur.name)
                cur = cur.parent
            full = "/".join(reversed(parts))
            if node.entry is None: full += "/"
            if full not in seen:
                seen.add(full)
                names.append(full)
        return names

    def dropEvent(self, event):
        if event.source() is not self:
            event.ignore()
            return
        mime = event.mimeData()
        if not mime.hasFormat("application/x-zipforge-entry"):
            event.ignore()
            return
        raw = bytes(mime.data("application/x-zipforge-entry")).decode("utf-8")
        source_paths = [p for p in raw.split("\n") if p]
        idx = self.indexAt(event.position().toPoint())
        target_dir = ""
        if idx.isValid():
            node = idx.internalPointer()
            if node.entry is not None and not node.entry.is_dir:
                node = node.parent
            if node is not None and node is not self._model._root:
                parts = []
                cur = node
                while cur is not None and cur.name:
                    parts.append(cur.name)
                    cur = cur.parent
                target_dir = "/".join(reversed(parts)) + "/"
        if self._drop_handler:
            self._drop_handler(source_paths, target_dir)
=======
from PyQt6.QtCore import Qt, QAbstractItemModel, QModelIndex
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTreeView, QAbstractItemView

from core.archive_model import ArchiveEntry
from core.i18n import tr


def human_size(num: int) -> str:
    for unit in ("Б", "КБ", "МБ", "ГБ", "ТБ"):
        if abs(num) < 1024.0:
            return f"{num:.1f} {unit}" if unit != "Б" else f"{num} {unit}"
        num /= 1024.0
    return f"{num:.1f} ПБ"


class TreeNode:
    def __init__(self, name: str, entry: ArchiveEntry | None = None, parent=None):
        self.name = name
        self.entry = entry
        self.parent: TreeNode | None = parent
        self.children: list[TreeNode] = []

    def row(self) -> int:
        if self.parent:
            return self.parent.children.index(self)
        return 0


class ArchiveTreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._root = TreeNode("")
        self._entries: list[ArchiveEntry] = []

    def _columns(self) -> list[str]:
        return [
            tr("col_name"), tr("col_size"), tr("col_compressed"),
            tr("col_ratio"), tr("col_date"),
        ]

    def load_entries(self, entries: list[ArchiveEntry]) -> None:
        self.beginResetModel()
        self._entries = entries
        self._root = TreeNode("")
        self._build_tree(entries)
        self.endResetModel()

    def _build_tree(self, entries: list[ArchiveEntry]) -> None:
        for entry in entries:
            if entry.is_dir:
                self._ensure_path(entry.name.rstrip("/").split("/"), entry)
        for entry in entries:
            if not entry.is_dir:
                parts = entry.name.split("/")
                folder_parts, file_name = parts[:-1], parts[-1]
                parent = self._ensure_path(folder_parts, None) if folder_parts else self._root
                node = TreeNode(file_name, entry, parent)
                parent.children.append(node)

        self._sort_recursive(self._root)

    def _ensure_path(self, parts: list[str], entry: ArchiveEntry | None) -> TreeNode:
        node = self._root
        for i, part in enumerate(parts):
            found = None
            for c in node.children:
                if c.name == part and (c.entry is None or c.entry.is_dir):
                    found = c
                    break
            if found is None:
                node_entry = entry if i == len(parts) - 1 else None
                found = TreeNode(part, node_entry, node)
                node.children.append(found)
            node = found
        return node

    def _sort_recursive(self, node: TreeNode) -> None:
        node.children.sort(key=lambda n: (n.entry is not None, n.name.lower()))
        for child in node.children:
            self._sort_recursive(child)

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        parent_node = parent.internalPointer() if parent.isValid() else self._root
        child = parent_node.children[row]
        return self.createIndex(row, column, child)

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        node: TreeNode = index.internalPointer()
        parent_node = node.parent
        if parent_node is None or parent_node is self._root:
            return QModelIndex()
        return self.createIndex(parent_node.row(), 0, parent_node)

    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0
        node = parent.internalPointer() if parent.isValid() else self._root
        return len(node.children)

    def columnCount(self, parent=QModelIndex()):
        return 5

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        node: TreeNode = index.internalPointer()
        entry = node.entry
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return node.name
            if entry is None:
                return ""
            if col == 1:
                return human_size(entry.size)
            if col == 2:
                return human_size(entry.compressed_size)
            if col == 3:
                return f"{entry.ratio * 100:.0f}%"
            if col == 4:
                return entry.mtime.strftime("%d.%m.%Y %H:%M")

        if role == Qt.ItemDataRole.TextAlignmentRole and col > 0:
            return int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        if role == Qt.ItemDataRole.ForegroundRole:
            if entry is None:
                return QColor("#4ec9b0")
            if entry.encrypted:
                return QColor("#dcdcaa")

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            cols = self._columns()
            if 0 <= section < len(cols):
                return cols[section]
        return None

    def flags(self, index):
        base = super().flags(index)
        if not index.isValid():
            return base | Qt.ItemFlag.ItemIsDropEnabled
        node: TreeNode = index.internalPointer()
        if node.entry is None or node.entry.is_dir:
            return base | Qt.ItemFlag.ItemIsDropEnabled | Qt.ItemFlag.ItemIsDragEnabled
        return base | Qt.ItemFlag.ItemIsDragEnabled

    def supportedDropActions(self):
        return Qt.DropAction.MoveAction

    def mimeTypes(self):
        return ["application/x-zipforge-entry"]

    def mimeData(self, indexes):
        from PyQt6.QtCore import QMimeData
        data = QMimeData()
        paths = []
        for idx in indexes:
            if idx.column() != 0:
                continue
            node = idx.internalPointer()
            parts = []
            cur = node
            while cur is not None and cur.name:
                parts.append(cur.name)
                cur = cur.parent
            full = "/".join(reversed(parts))
            if node.entry is None:
                full += "/"
            paths.append(full)
        data.setData("application/x-zipforge-entry", "\n".join(paths).encode("utf-8"))
        return data


class ArchiveTreeView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = ArchiveTreeModel(self)
        self.setModel(self._model)
        self.setAlternatingRowColors(True)
        self.setUniformRowHeights(True)
        self.setSortingEnabled(False)
        self.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        self.setColumnWidth(0, 400)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 70)
        self.setColumnWidth(4, 140)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self._drop_handler = None

    def set_drop_handler(self, handler):
        self._drop_handler = handler

    def load_entries(self, entries: list[ArchiveEntry]) -> None:
        self._model.load_entries(entries)
        self.expandToDepth(0)
        self.header().reset()

    def selected_names(self) -> list[str]:
        names: list[str] = []
        indexes = self.selectionModel().selectedIndexes()
        seen = set()
        for idx in indexes:
            if idx.column() != 0:
                continue
            node = idx.internalPointer()
            parts = []
            cur = node
            while cur is not None and cur.name:
                parts.append(cur.name)
                cur = cur.parent
            full = "/".join(reversed(parts))
            if node.entry is None:
                full += "/"
            if full not in seen:
                seen.add(full)
                names.append(full)
        return names

    def dropEvent(self, event):
        if event.source() is not self:
            event.ignore()
            return
        mime = event.mimeData()
        if not mime.hasFormat("application/x-zipforge-entry"):
            event.ignore()
            return
        raw = bytes(mime.data("application/x-zipforge-entry")).decode("utf-8")
        source_paths = [p for p in raw.split("\n") if p]
        idx = self.indexAt(event.position().toPoint())
        target_dir = ""
        if idx.isValid():
            node = idx.internalPointer()
            if node.entry is not None and not node.entry.is_dir:
                node = node.parent
            if node is not None and node is not self._model._root:
                parts = []
                cur = node
                while cur is not None and cur.name:
                    parts.append(cur.name)
                    cur = cur.parent
                target_dir = "/".join(reversed(parts)) + "/"
        if self._drop_handler:
            self._drop_handler(source_paths, target_dir)
>>>>>>> 7518772216c1d981bbfd5895f875ea24751d8bd0
        event.acceptProposedAction()