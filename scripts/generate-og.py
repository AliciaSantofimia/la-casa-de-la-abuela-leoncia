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


def main() -> None:
    canvas = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)

    # --- Texto (columna izquierda ~40%) ---
    left = 58
    text_max = 420
    y = 96

    kicker_font = load_font(FONT_SANS_SB, 17)
    kicker = "TORRECAMPO · CÓRDOBA"
    spacing = 4.2
    x = left
    for ch in kicker:
        draw.text((x, y), ch, font=kicker_font, fill=SAGE)
        x += draw.textlength(ch, font=kicker_font) + spacing
    y += 44

    title_font = load_font(FONT_SERIF, 52)
    title_lines = ["La Casa de la", "Abuela Leoncia"]
    for line in title_lines:
        draw.text((left, y), line, font=title_font, fill=INK)
        bbox = draw.textbbox((left, y), line, font=title_font)
        y = bbox[3] + 4
    y += 20

    body_font = load_font(FONT_SANS, 21)
    body = (
        "Casa tradicional con 248 m² construidos, patio, huerto "
        "y una amplia buhardilla llena de posibilidades."
    )
    for line in wrap_text(draw, body, body_font, text_max):
        draw.text((left, y), line, font=body_font, fill=MUTED)
        y += 29
    y += 26

    meta_font = load_font(FONT_SANS, 15)
    meta = "248 m² · Patio · Huerto · Buhardilla"
    draw.text((left, y), meta, font=meta_font, fill=OLIVE)

    # --- Ilustración (~58% derecho, bien grande) ---
    hero = Image.open(HERO).convert("RGBA")
    target_h = H - 24
    scale = target_h / hero.height
    new_w = int(hero.width * scale)
    new_h = int(hero.height * scale)
    hero = hero.resize((new_w, new_h), Image.Resampling.LANCZOS)

    paste_x = W - new_w + 36
    paste_y = H - new_h + 4

    fade_w = 110
    fade = Image.new("L", (new_w, new_h), 255)
    fade_draw = ImageDraw.Draw(fade)
    for i in range(fade_w):
        alpha = int(255 * (i / fade_w))
        fade_draw.line([(i, 0), (i, new_h)], fill=alpha)
    r, g, b, a = hero.split()
    hero.putalpha(Image.composite(a, fade, fade))

    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba.alpha_composite(hero, (paste_x, paste_y))
    result = canvas_rgba.convert("RGB")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    result.save(OUT, "PNG", optimize=True)
    print(f"Guardado {OUT} ({result.size[0]}x{result.size[1]}, {OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
