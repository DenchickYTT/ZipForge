import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPlainTextEdit, 
    QDialogButtonBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

TEXT_EXTENSIONS = {".txt", ".md", ".py", ".json", ".csv", ".xml", ".html", ".css", ".js", ".log", ".ini", ".cfg", ".yaml", ".yml"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp"}

class PreviewDialog(QDialog):
    def __init__(self, filename: str, data: bytes, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Предпросмотр: {filename}")
        self.resize(700, 500)

        layout = QVBoxLayout(self)

        ext = os.path.splitext(filename)[1].lower()

        if ext in IMAGE_EXTENSIONS:
            # Предпросмотр картинки
            label = QLabel()
            pixmap = QPixmap()
            if pixmap.loadFromData(data):
                # Масштабируем, сохраняя пропорции. 
                # Отнимаем по 20 пикселей с каждой стороны для отступов (чтобы не прилипало)
                target_size = self.size() - self.minimumSizeHint() # грубый расчет
                max_w = 680
                max_h = 450
                
                scaled = pixmap.scaled(
                    max_w, max_h,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                label.setPixmap(scaled)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            else:
                label.setText("Не удалось загрузить изображение (возможно, формат не поддерживается).")
            layout.addWidget(label)
        
        elif ext in TEXT_EXTENSIONS or not ext:
            # Предпросмотр текста
            text_edit = QPlainTextEdit()
            text_edit.setReadOnly(True)
            
            # Ограничение на размер, чтобы не убить память (первые 2 МБ)
            preview_data = data[:2 * 1024 * 1024]
            
            try:
                text = preview_data.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    text = preview_data.decode("cp1251")
                except UnicodeDecodeError:
                    text = preview_data.decode("utf-8", errors="replace")
            
            if len(data) > 2 * 1024 * 1024:
                text += "\n\n... [Файл слишком большой. Показаны первые 2 МБ] ..."

            text_edit.setPlainText(text)
            layout.addWidget(text_edit)
            
        else:
            # Если это exe, mp3, zip и т.д. — предлагаем распаковать
            msg = QLabel(f"Для файлов формата *{ext}* предпросмотр недоступен.\n\nХотите извлечь его на диск?")
            msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(msg)
            
            bb = QDialogButtonBox()
            extract_btn = bb.addButton("Извлечь...", QDialogButtonBox.ButtonRole.ActionRole)
            close_btn = bb.addButton("Закрыть", QDialogButtonBox.ButtonRole.RejectRole)
            
            extract_btn.clicked.connect(lambda: self.done(1)) # 1 = код извлечения
            close_btn.clicked.connect(self.reject)
            layout.addWidget(bb)
            return # Выходим, чтобы не добавлять нижнюю кнопку "Закрыть"

        # Нижняя кнопка "Закрыть" для текста и картинок
        bb = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)