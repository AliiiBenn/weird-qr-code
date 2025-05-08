from typing import Literal, Sequence
from PIL import ImageDraw

# Imports relatifs car drawing.py est dans core/
from .hex_grid import Hexagon, AxialPos, HexgridLayout, PixelCoord
from .constants import ProtocolColor, FINDER_COLORS, ColorTuple

def draw_hexagon(
    draw: ImageDraw.ImageDraw,
    hexagon: Hexagon,
    fill_color: ProtocolColor | None = None,
    outline_color: ProtocolColor = ProtocolColor.BLACK
) -> None:
    """Dessine un seul hexagone sur l'objet ImageDraw fourni.

    Args:
        draw: L'objet Pillow ImageDraw sur lequel dessiner.
        hexagon: L'objet Hexagon à dessiner.
        fill_color: La couleur de remplissage (membre de ProtocolColor) ou None pour aucun remplissage.
        outline_color: La couleur du contour (membre de ProtocolColor).
    """
    vertices: list[PixelCoord] = hexagon.get_vertices()
    # Convertir les PixelCoord en une liste de tuples (x, y) pour Pillow
    drawable_vertices: Sequence[tuple[float, float]] = [(v.x, v.y) for v in vertices]
    
    fill_rgb: ColorTuple | None = fill_color.rgb if fill_color else None
    outline_rgb: ColorTuple = outline_color.rgb
    
    draw.polygon(drawable_vertices, fill=fill_rgb, outline=outline_rgb)

# --- Implémentation de draw_finder_pattern à venir --- 

def draw_finder_pattern(
    draw: ImageDraw.ImageDraw,
    layout: HexgridLayout,
    center_pos: AxialPos,
    pattern_type: Literal["origin", "xaxis", "yaxis"]
) -> None:
    """Dessine un repère d'alignement (finder pattern) complet.

    Args:
        draw: L'objet Pillow ImageDraw sur lequel dessiner.
        layout: Le layout de la grille.
        center_pos: La position axiale du centre du repère.
        pattern_type: Le type de repère ("origin", "xaxis" ou "yaxis") pour déterminer les couleurs.
    """
    # Vérifier que le type de pattern est valide (bien que Literal devrait aider)
    if pattern_type not in FINDER_COLORS:
        raise ValueError(f"Type de pattern invalide : {pattern_type}")

    colors = FINDER_COLORS[pattern_type]
    center_color = colors["center"]
    ring_color = colors["ring"]

    # Créer l'hexagone central
    center_hex = Hexagon(pos=center_pos, layout=layout)
    
    # Dessiner l'hexagone central
    draw_hexagon(draw, center_hex, fill_color=center_color, outline_color=ProtocolColor.BLACK)

    # Obtenir et dessiner les voisins (l'anneau)
    neighbors = center_hex.get_neighbors()
    for neighbor_hex in neighbors:
        draw_hexagon(draw, neighbor_hex, fill_color=ring_color, outline_color=ProtocolColor.BLACK)
