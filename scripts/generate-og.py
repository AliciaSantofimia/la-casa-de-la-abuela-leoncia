"""Genera public/og-casa-leoncia.png (1200×630) con estética editorial."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "og-casa-leoncia.png"
HERO = ROOT / "images" / "hero-ilustracion-casa.png"

W, H = 1200, 630
PAPER = (243, 244, 240)  # --paper
INK = (26, 28, 24)  # --ink
MUTED = (90, 95, 84)  # --text-muted
SAGE = (138, 148, 120)  # --sage
OLIVE = (63, 74, 52)  # --olive

FONT_SERIF = Path(r"C:\Windows\Fonts\georgia.ttf")
FONT_SANS = Path(r"C:\Windows\Fonts\segoeui.ttf")
FONT_SANS_SB = Path(r"C:\Windows\Fonts\seguisb.ttf")


def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def crop_cream_margins(im: Image.Image, threshold: int = 38) -> Image.Image:
    """Recorta márgenes crema sin tocar la fachada."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    pix = rgb.load()
    xs: list[int] = []
    ys: list[int] = []
    for y in range(h):
        for x in range(w):
            r, g, b = pix[x, y]
            if abs(r - 243) + abs(g - 244) + abs(b - 240) > threshold:
                xs.append(x)
                ys.append(y)
    if not xs:
        return im
    pad = 4
    left = max(0, min(xs) - pad)
    top = max(0, min(ys) - pad)
    right = min(w, max(xs) + pad)
    bottom = min(h, max(ys) + pad)
    return im.crop((left, top, right, bottom))


def main() -> None:
    canvas = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)

    # Texto ~+20% respecto a la versión anterior
    left = 44
    text_max = 390
    y = 72

    kicker_font = load_font(FONT_SANS_SB, 20)
    kicker = "TORRECAMPO · CÓRDOBA"
    spacing = 5.0
    x = left
    for ch in kicker:
        draw.text((x, y), ch, font=kicker_font, fill=SAGE)
        x += draw.textlength(ch, font=kicker_font) + spacing
    y += 48

    title_font = load_font(FONT_SERIF, 62)
    for line in ("La Casa de la", "Abuela Leoncia"):
        draw.text((left, y), line, font=title_font, fill=INK)
        bbox = draw.textbbox((left, y), line, font=title_font)
        y = bbox[3] + 2
    y += 16

    body_font = load_font(FONT_SANS, 25)
    body = (
        "Casa tradicional con 248 m² construidos, patio, huerto "
        "y una amplia buhardilla llena de posibilidades."
    )
    for line in wrap_text(draw, body, body_font, text_max):
        draw.text((left, y), line, font=body_font, fill=MUTED)
        y += 33
    y += 22

    meta_font = load_font(FONT_SANS, 18)
    draw.text((left, y), "248 m² · Patio · Huerto · Buhardilla", font=meta_font, fill=OLIVE)

    # Ilustración más grande (~+35% de presencia), fachada completa
    hero = crop_cream_margins(Image.open(HERO).convert("RGBA"))
    max_h = H - 6
    max_w = int(W * 0.66)
    scale = min(max_h / hero.height, max_w / hero.width)
    new_w = int(hero.width * scale)
    new_h = int(hero.height * scale)
    hero = hero.resize((new_w, new_h), Image.Resampling.LANCZOS)

    text_right = left + text_max
    desired_gap = 32
    paste_x = min(W - new_w - 4, max(text_right + desired_gap, W - new_w - 4))
    # Cerrar hueco: preferir acercar al texto si cabe entera
    paste_x = text_right + desired_gap
    if paste_x + new_w > W - 2:
        paste_x = W - new_w - 2
    paste_y = (H - new_h) // 2

    fade_w = 44
    fade = Image.new("L", (new_w, new_h), 255)
    fade_draw = ImageDraw.Draw(fade)
    for i in range(fade_w):
        alpha = int(255 * (i / fade_w))
        fade_draw.line([(i, 0), (i, new_h)], fill=alpha)
    _r, _g, _b, a = hero.split()
    hero.putalpha(Image.composite(a, fade, fade))

    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba.alpha_composite(hero, (paste_x, paste_y))
    result = canvas_rgba.convert("RGB")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    result.save(OUT, "PNG", optimize=True)
    print(
        f"Guardado {OUT} ({result.size[0]}x{result.size[1]}, "
        f"ilustración {new_w}x{new_h} @x={paste_x}, {OUT.stat().st_size} bytes)"
    )


if __name__ == "__main__":
    main()
