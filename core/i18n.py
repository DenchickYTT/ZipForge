from core.settings import settings


TRANSLATIONS = {
    "ru": {
        # Тулбар
        "open": "📂 Открыть",
        "create": "📦 Создать",
        "extract": "📤 Извлечь",
        "add": "➕ Добавить",
        "delete": "🗑️ Удалить",
        "rename": "✏️ Переименовать",
        # Меню
        "menu_file": "Файл",
        "menu_settings": "Настройки",
        "menu_help": "Справка",
        "menu_exit": "Выход",
        "menu_preferences": "Параметры…",
        "menu_about": "О программе",
        # Диалоги
        "dlg_open_title": "Открыть архив",
        "dlg_open_filter": "ZIP-архивы (*.zip);;Все файлы (*)",
        "dlg_extract_where": "Куда извлечь?",
        "dlg_extract_q": "Извлечь выбранное ({n} шт.) или весь архив?",
        "dlg_delete_q": "Удалить из архива ({n} шт.)?",
        "dlg_rename_title": "Переименовать",
        "dlg_password_title": "Архив защищён паролем",
        "dlg_password_label": "Введите пароль:",
        "dlg_settings_title": "Настройки",
        "dlg_about_title": "О программе",
        # Статусы
        "status_ready": "Готово",
        "status_no_archive": "Архив не открыт",
        "status_files": "Файлов: {n}",
        "status_original": "Исходно: {size}",
        "status_in_archive": "В архиве: {size}",
        "status_done": "Готово",
        # Сообщения
        "msg_open_first": "Сначала откройте архив.",
        "msg_error": "Ошибка",
        "msg_open_failed": "Не удалось открыть архив:\n{err}",
        "msg_archive_created": "Архив создан:\n{path}",
        "msg_extracted_to": "Архив извлечён в:\n{path}",
        "msg_deleted": "Выбранное удалено из архива.",
        "msg_renamed": "Переименовано:\n{old} → {new}",
        "msg_added": "Добавлено в архив:\n{path}",
        "msg_folder_in_itself": "Нельзя переместить папку внутрь самой себя.",
        "msg_select_for_delete": "Выберите файлы или папки для удаления.",
        "msg_select_one_rename": "Для переименования выберите ровно один файл или папку.",
        # Настройки
        "settings_language": "Язык интерфейса:",
        "settings_theme": "Тема:",
        "settings_theme_dark": "Тёмная",
        "settings_theme_light": "Светлая",
        "settings_apply": "Применить",
        "settings_cancel": "Отмена",
        "settings_restart_hint": "Изменения языка применяются сразу.",
        # О программе
        "about_text": (
            "ZipForge — простой и быстрый архиватор.\n\n"
            "Версия: 1.0.0\n"
            "Работает полностью офлайн. Не собирает и не передаёт "
            "никаких данных.\n\n"
            "Технологии: Python, PyQt6, pyzipper."
        ),
        # Заголовки колонок
        "col_name": "Имя",
        "col_size": "Размер",
        "col_compressed": "Сжатый",
        "col_ratio": "Коэф.",
        "col_date": "Дата",
    },
    "en": {
        "open": "📂 Open",
        "create": "📦 Create",
        "extract": "📤 Extract",
        "add": "➕ Add",
        "delete": "🗑️ Delete",
        "rename": "✏️ Rename",
        "menu_file": "File",
        "menu_settings": "Settings",
        "menu_help": "Help",
        "menu_exit": "Exit",
        "menu_preferences": "Preferences…",
        "menu_about": "About",
        "dlg_open_title": "Open archive",
        "dlg_open_filter": "ZIP archives (*.zip);;All files (*)",
        "dlg_extract_where": "Extract to…",
        "dlg_extract_q": "Extract selected ({n}) or whole archive?",
        "dlg_delete_q": "Delete from archive ({n} items)?",
        "dlg_rename_title": "Rename",
        "dlg_password_title": "Archive is password-protected",
        "dlg_password_label": "Enter password:",
        "dlg_settings_title": "Settings",
        "dlg_about_title": "About",
        "status_ready": "Ready",
        "status_no_archive": "No archive open",
        "status_files": "Files: {n}",
        "status_original": "Original: {size}",
        "status_in_archive": "In archive: {size}",
        "status_done": "Done",
        "msg_open_first": "Open an archive first.",
        "msg_error": "Error",
        "msg_open_failed": "Failed to open archive:\n{err}",
        "msg_archive_created": "Archive created:\n{path}",
        "msg_extracted_to": "Extracted to:\n{path}",
        "msg_deleted": "Selected items deleted from archive.",
        "msg_renamed": "Renamed:\n{old} → {new}",
        "msg_added": "Added to archive:\n{path}",
        "msg_folder_in_itself": "Cannot move a folder into itself.",
        "msg_select_for_delete": "Select files or folders to delete.",
        "msg_select_one_rename": "Select exactly one file or folder to rename.",
        "settings_language": "Interface language:",
        "settings_theme": "Theme:",
        "settings_theme_dark": "Dark",
        "settings_theme_light": "Light",
        "settings_apply": "Apply",
        "settings_cancel": "Cancel",
        "settings_restart_hint": "Language changes apply immediately.",
        "about_text": (
            "ZipForge — a simple and fast archiver.\n\n"
            "Version: 1.0.0\n"
            "Runs fully offline. Does not collect or transmit any data.\n\n"
            "Built with Python, PyQt6, pyzipper."
        ),
        "col_name": "Name",
        "col_size": "Size",
        "col_compressed": "Compressed",
        "col_ratio": "Ratio",
        "col_date": "Date",
    },
}


def tr(key: str, **kwargs) -> str:
    lang = settings.get("language", "ru")
    table = TRANSLATIONS.get(lang, TRANSLATIONS["ru"])
    text = table.get(key, TRANSLATIONS["ru"].get(key, key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text