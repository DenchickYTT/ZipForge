from dataclasses import dataclass
from datetime import datetime


@dataclass
class ArchiveEntry:
    name: str              # путь внутри архива, например "docs/readme.txt"
    size: int              # исходный размер в байтах
    compressed_size: int   # сжатый размер в байтах
    mtime: datetime        # дата изменения
    is_dir: bool = False
    crc: int = 0
    encrypted: bool = False

    @property
    def ratio(self) -> float:
        """Коэффициент сжатия: 0.0 = не сжалось, 1.0 = сжалось в ноль."""
        if self.size == 0:
            return 0.0
        return 1.0 - (self.compressed_size / self.size)

    @property
    def basename(self) -> str:
        """Имя файла без пути."""
        return self.name.rstrip("/").rsplit("/", 1)[-1]