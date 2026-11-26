from PIL import Image, ImageDraw, ImageFont

def make_icon(size: int, path: str) -> None:
    img = Image.new("RGBA", (size, size), (30, 30, 30, 255))
    draw = ImageDraw.Draw(img)

    margin = size // 10
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=size // 6,
        fill=(37, 37, 38, 255),
        outline=(0, 122, 204, 255),
        width=max(2, size // 32),
    )

    try:
        font = ImageFont.truetype("arialbd.ttf", int(size * 0.55))
    except OSError:
        font = ImageFont.load_default()

    text = "Z"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        ((size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1]),
        text, font=font, fill=(0, 122, 204, 255),
    )

    img.save(path)


if __name__ == "__main__":
    import os
    os.makedirs("resources", exist_ok=True)
    make_icon(256, "resources/icon.png")
    img = Image.open("resources/icon.png")
    img.save("resources/icon.ico",
             sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("Готово: resources/icon.png, resources/icon.ico")