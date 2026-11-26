import json
import urllib.request
import time
from packaging.version import Version, InvalidVersion
from core.settings import settings, APP_VERSION

GITHUB_REPO = "DenchickYTT/ZipForge"
API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

def check_for_updates(force: bool = False) -> tuple[bool, str, str]:
    """
    Проверяет обновления на GitHub.
    Возвращает (есть_обновление, последняя_версия, ссылка_на_релиз).
    Кэширует результат на 24 часа (если не force).
    """
    # Проверка кэша
    now = int(time.time())
    last_check = settings.get("last_update_check", 0)
    if not force and (now - last_check) < 86400:  # 24 часа
        cached_ver = settings.get("cached_latest_version", "")
        cached_url = settings.get("cached_release_url", "")
        if cached_ver and cached_url:
            return _compare_versions(cached_ver), cached_ver, cached_url

    try:
        req = urllib.request.Request(API_URL, headers={"User-Agent": "ZipForge-Updater"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            latest_version = data.get("tag_name", "")
            html_url = data.get("html_url", "")
            
            # Сохраняем в кэш
            settings.set("last_update_check", now)
            settings.set("cached_latest_version", latest_version)
            settings.set("cached_release_url", html_url)
            
            return _compare_versions(latest_version), latest_version, html_url
    except Exception:
        # Если ошибка сети — возвращаем False, чтобы не мешать пользователю
        return False, "", ""

def _compare_versions(latest: str) -> bool:
    """Возвращает True, если latest > текущей версии."""
    try:
        current = Version(APP_VERSION)
        latest_ver = Version(latest.lstrip("v"))
        return latest_ver > current
    except (InvalidVersion, ValueError):
        return False