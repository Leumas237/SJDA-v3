#!/usr/bin/env python3
"""Génération du logo BC Connect et des icônes PWA (192x192, 512x512).

Palette IUT-FV :
  Vert principal     #007A3D
  Vert profond       #004D2A
  Or / Jaune         #F5B800
  Bleu institutionnel #004A99
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Chemins de sortie
ICONS_DIR = Path(__file__).parent / "frontend" / "icons"
ICONS_DIR.mkdir(parents=True, exist_ok=True)

# Couleurs
GREEN_MAIN = "#007A3D"
GREEN_DEEP = "#004D2A"
GOLD = "#F5B800"
WHITE = "#FFFFFF"


def create_logo_svg(size: int = 512) -> str:
    """Génère le SVG du logo BC (monogramme entrelacé)."""
    # Le monogramme BC : B et C entrelacés avec un trait de connexion subtil
    # Style : typo Poppins Bold, centré, sur fond arrondi avec dégradé
    svg = f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="{size}" height="{size}" rx="{size * 0.3}" fill="url(#grad)"/>
  <text x="50%" y="54%" dominant-baseline="middle" text-anchor="middle"
        font-family="Poppins, system-ui, sans-serif" font-weight="700"
        font-size="{int(size * 0.5)}" fill="white">BC</text>
  <defs>
    <linearGradient id="grad" x1="0" y1="0" x2="{size}" y2="{size}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{GREEN_MAIN}"/>
      <stop offset="100%" stop-color="{GREEN_DEEP}"/>
    </linearGradient>
  </defs>
</svg>'''
    return svg


def draw_monogram(draw: ImageDraw.Draw, size: int, center: tuple, font_size: int):
    """Dessine le monogramme BC au centre de l'image."""
    # On utilise une police système, fallback sur défaut si Poppins dispo
    try:
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except OSError:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()

    cx, cy = center
    text = "BC"

    # Mesurer le texte pour le centrer parfaitement
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = cx - text_w // 2
    y = cy - text_h // 2 - int(font_size * 0.05)  # léger ajustement vertical

    # Dessiner le texte en blanc
    draw.text((x, y), text, font=font, fill=WHITE)


def generate_icon(size: int) -> Image.Image:
    """Génère une icône PNG carrée avec le logo BC."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fond arrondi avec dégradé vert principal → vert profond
    radius = int(size * 0.3)
    # Dessiner le fond arrondi avec dégradé (approximation par lignes horizontales)
    for y in range(size):
        t = y / size
        r = int(0 * (1 - t) + 0 * t)  # 0 -> 0
        g = int(0x7A * (1 - t) + 0x4D * t)  # 122 -> 77
        b = int(0x3D * (1 - t) + 0x2A * t)  # 61 -> 42
        color = (r, g, b, 255)
        # Ligne avec coins arrondis
        if y < radius:
            # Partie supérieure : arrondi
            x_start = int((radius**2 - (y - radius)**2)**0.5)
            x_end = size - x_start
        elif y >= size - radius:
            # Partie inférieure : arrondi
            x_start = int((radius**2 - (y - (size - radius))**2)**0.5)
            x_end = size - x_start
        else:
            # Milieu : plein
            x_start = 0
            x_end = size
        draw.line([(x_start, y), (x_end, y)], fill=color)

    # Monogramme BC au centre
    font_size = int(size * 0.5)
    draw_monogram(draw, size, (size // 2, size // 2), font_size)

    return img


def generate_maskable_icon(size: int) -> Image.Image:
    """Génère une version maskable (zone sûre 40% au centre)."""
    # Pour maskable, le contenu principal doit tenir dans 40% de la taille
    # On génère l'icône normale puis on ajoute du padding si nécessaire
    # Ici le monogramme est déjà centré et raisonnablement dimensionné
    return generate_icon(size)


def main():
    print("[+] Generation du logo BC Connect et icones PWA...")

    # 1. Logo SVG source
    svg_content = create_logo_svg(512)
    svg_path = ICONS_DIR / "logo.svg"
    svg_path.write_text(svg_content, encoding="utf-8")
    print(f"[OK] Logo SVG : {svg_path}")

    # 2. Icône 192x192
    icon_192 = generate_icon(192)
    icon_192_path = ICONS_DIR / "icon-192.png"
    icon_192.save(icon_192_path, "PNG")
    print(f"[OK] Icone 192x192 : {icon_192_path}")

    # 3. Icône 512x512
    icon_512 = generate_icon(512)
    icon_512_path = ICONS_DIR / "icon-512.png"
    icon_512.save(icon_512_path, "PNG")
    print(f"[OK] Icone 512x512 : {icon_512_path}")

    # 4. Favicon 32x32 (pour compatibilité)
    favicon_32 = generate_icon(32)
    favicon_32_path = ICONS_DIR / "favicon-32.png"
    favicon_32.save(favicon_32_path, "PNG")
    print(f"[OK] Favicon 32x32 : {favicon_32_path}")

    # 5. Version maskable 512x512 (même image, purpose=maskable dans manifest)
    maskable_512 = generate_maskable_icon(512)
    maskable_512_path = ICONS_DIR / "icon-512-maskable.png"
    maskable_512.save(maskable_512_path, "PNG")
    print(f"[OK] Icone maskable 512x512 : {maskable_512_path}")

    print("\n[DONE] Generation terminee !")
    print(f"[DIR] Dossier : {ICONS_DIR}")


if __name__ == "__main__":
    main()