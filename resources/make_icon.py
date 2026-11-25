<<<<<<< HEAD
"""
Генерирует resources/icon.ico и resources/icon.png
с простым логотипом ZipForge: тёмный квадрат + буква Z бирюзового цвета.
Запуск: python resources/make_icon.py
"""
import os
from PIL import Image, ImageDraw, ImageFont


def make_icon(size: int = 256) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Скруглённый тёмный квадрат
    margin = size // 16
    radius = size // 6
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        fill=(30, 30, 30, 255),
        outline=(78, 201, 176, 255),
        width=max(2, size // 64),
    )

    # Буква Z
    try:
        font = ImageFont.truetype("arialbd.ttf", int(size * 0.55))
    except OSError:
        font = ImageFont.load_default()

    text = "Z"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pos = ((size - tw) // 2 - bbox[0], (size - th) // 2 - bbox[1])
    draw.text(pos, text, font=font, fill=(78, 201, 176, 255))

    return img


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))

    base = make_icon(256)
    png_path = os.path.join(here, "icon.png")
    base.save(png_path, "PNG")
    print(f"Сохранено: {png_path}")

    ico_path = os.path.join(here, "icon.ico")
    base.save(
        ico_path, "ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    print(f"Сохранено: {ico_path}")


if __name__ == "__main__":
=======
"""
Генерирует resources/icon.ico и resources/icon.png
с простым логотипом ZipForge: тёмный квадрат + буква Z бирюзового цвета.
Запуск: python resources/make_icon.py
"""
import os
from PIL import Image, ImageDraw, ImageFont


def make_icon(size: int = 256) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Скруглённый тёмный квадрат
    margin = size // 16
    radius = size // 6
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        fill=(30, 30, 30, 255),
        outline=(78, 201, 176, 255),
        width=max(2, size // 64),
    )

    # Буква Z
    try:
        font = ImageFont.truetype("arialbd.ttf", int(size * 0.55))
    except OSError:
        font = ImageFont.load_default()

    text = "Z"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pos = ((size - tw) // 2 - bbox[0], (size - th) // 2 - bbox[1])
    draw.text(pos, text, font=font, fill=(78, 201, 176, 255))

    return img


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))

    base = make_icon(256)
    png_path = os.path.join(here, "icon.png")
    base.save(png_path, "PNG")
    print(f"Сохранено: {png_path}")

    ico_path = os.path.join(here, "icon.ico")
    base.save(
        ico_path, "ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    print(f"Сохранено: {ico_path}")


if __name__ == "__main__":
>>>>>>> 7518772216c1d981bbfd5895f875ea24751d8bd0
    main()