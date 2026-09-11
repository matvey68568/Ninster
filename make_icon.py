"""Генерирует assets/icon.ico для Ninster (запускается один раз)."""

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
OUT = ROOT / "assets" / "icon.ico"


def make_icon(size: int = 256) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    m = size // 16  # margin
    r = size // 4   # corner radius
    d.rounded_rectangle(
        [m, m, size - m, size - m], radius=r, fill=(43, 108, 200, 255))

    w = size // 6
    cx = size // 2
    top_y = int(size * 0.30)
    bottom_y = int(size * 0.72)
    d.line([(cx, top_y), (cx, bottom_y)], fill="white", width=w)
    d.line([(cx - w, bottom_y - w), (cx, bottom_y), (cx + w, bottom_y - w)],
           fill="white", width=w, joint="curve")
    d.line([(cx - w, top_y - w // 2), (cx + w, top_y - w // 2)],
           fill="white", width=w)
    return img


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img = make_icon()
    img.save(OUT, format="ICO",
             sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(f"Иконка сохранена: {OUT}")


if __name__ == "__main__":
    main()
