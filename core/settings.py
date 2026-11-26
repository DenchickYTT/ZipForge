import os
import json
from pathlib import Path

# Текущая версия приложения
APP_VERSION = "1.2.1"

DEFAULTS = {
    "language": "ru",
    "theme": "dark",
    "default_compression": 6,
    "last_update_check": 0,
    "show_hidden": False,           # Новая настройка
    "confirm_delete": True,         # Новая настройка
    "preview_max_size": 2 * 1024 * 1024,  # Новая настройка (2 МБ по умолчанию)
}

def _settings_dir() -> Path:
    base = os.environ.get("APPDATA") or os.path.expanduser("~/.config")
    d = Path(base) / "ZipForge"
    d.mkdir(parents=True, exist_ok=True)
    return d

def _settings_file() -> Path:
    return _settings_dir() / "settings.json"

class Settings:
    def __init__(self) -> None:
        self._data = dict(DEFAULTS)
        self.load()

    def load(self) -> None:
        path = _settings_file()
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                for k, v in loaded.items():
                    if k in DEFAULTS:
                        self._data[k] = v
            except Exception:
                pass

    def save(self) -> None:
        try:
            with open(_settings_file(), "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value) -> None:
        self._data[key] = value
        self.save()

settings = Settings()