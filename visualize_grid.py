from PIL import Image, ImageDraw, ImageFont
import itertools # Pour l'itération sur les positions des repères
import math # Pour math.sqrt

# Le script est à la racine, src est un package au même niveau
from src.core.hex_grid import AxialPos, PixelCoord, HexgridLayout, Hexagon
from src.core.constants import FINDER_POS_TL, FINDER_POS_TR, FINDER_POS_BL
from src.core.drawing import draw_finder_pattern

def draw_grid_visualization(
    image_path: str = "grid_visualization.png",
    image_size: tuple[int, int] = (850, 850), # Ajusté
    hex_radius: float = 30.0,
    grid_range_q: tuple[int, int] = (-10, 10), # Peut être ajusté si nécessaire
    grid_range_r: tuple[int, int] = (-10, 10), # Peut être ajusté si nécessaire
    draw_coords: bool = True,
    draw_finders: bool = True,
    target_center_axial: AxialPos = AxialPos(-5, 0) # Nouveau paramètre pour centrer
) -> None:
    """Génère une image visualisant une grille d'hexagones avec les repères d'alignement."""

    img_width, img_height = image_size
    background_color = (255, 255, 255) # Blanc
    line_color = (0, 0, 0)       # Noir
    text_color = (50, 50, 50)    # Gris foncé

    # Calculer le grid_origin pour que target_center_axial soit au centre de l'image
    # grid_origin est la coordonnée pixel de AxialPos(0,0)
    origin_x = (img_width / 2) - (hex_radius * (3/2 * target_center_axial.q))
    origin_y = (img_height / 2) - (hex_radius * (math.sqrt(3)/2 * target_center_axial.q + math.sqrt(3) * target_center_axial.r))
    grid_origin_pixel = PixelCoord(origin_x, origin_y)
    
    layout = HexgridLayout(size=hex_radius, origin=grid_origin_pixel)
    image = Image.new("RGB", image_size, background_color)
    draw = ImageDraw.Draw(image)
    font = None
    if draw_coords:
        try:
            font_size = int(hex_radius / 3)
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            print(f"Police arial.ttf non trouvée, les coordonnées ne seront pas dessinées.")
            font = ImageFont.load_default()

    # --- Calculer les positions des hexagones des finder patterns --- 
    finder_pattern_centers = [FINDER_POS_TL, FINDER_POS_TR, FINDER_POS_BL]
    finder_pattern_positions: set[AxialPos] = set(finder_pattern_centers)
    if draw_finders:
        # Utiliser un layout temporaire juste pour créer les objets Hexagon et trouver les voisins
        temp_layout_for_neighbors = HexgridLayout(size=1.0, origin=PixelCoord(0,0)) # size/origin non importants ici
        for center_pos in finder_pattern_centers:
            center_hex = Hexagon(pos=center_pos, layout=temp_layout_for_neighbors)
            for neighbor_hex in center_hex.get_neighbors():
                finder_pattern_positions.add(neighbor_hex.pos)

    print(f"Dessin de la grille avec q de {grid_range_q[0]} à {grid_range_q[1]} et r de {grid_range_r[0]} à {grid_range_r[1]}")

    # --- Dessin de la Grille de Base --- 
    for q_coord in range(grid_range_q[0], grid_range_q[1] + 1):
        for r_coord in range(grid_range_r[0], grid_range_r[1] + 1):
            current_pos = AxialPos(q_coord, r_coord)
            current_hex = Hexagon(pos=current_pos, layout=layout)
            hex_center_pixel = current_hex.get_pixel_center()
            
            if not ((-hex_radius < hex_center_pixel.x < img_width + hex_radius) and \
                    (-hex_radius < hex_center_pixel.y < img_height + hex_radius)):
                continue

            # Vérifier si l'hexagone actuel fait partie d'un finder pattern
            is_part_of_finder = draw_finders and (current_pos in finder_pattern_positions)

            # Dessiner le contour seulement si ce n'est PAS une partie d'un finder pattern
            if not is_part_of_finder:
                vertices_pixels = current_hex.get_vertices()
                drawable_vertices = [(v.x, v.y) for v in vertices_pixels]
                draw.polygon(drawable_vertices, outline=line_color, fill=None)

            # Dessiner les coordonnées seulement si ce n'est PAS une partie d'un finder pattern
            if draw_coords and font and not is_part_of_finder:
                coord_text = f"{q_coord},{r_coord}"
                try:
                    bbox = draw.textbbox((0,0), coord_text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                except AttributeError:
                    text_width, text_height = draw.textsize(coord_text, font=font) # type: ignore
                
                text_x = hex_center_pixel.x - text_width / 2
                text_y = hex_center_pixel.y - text_height / 2
                draw.text((text_x, text_y), coord_text, fill=text_color, font=font)

    # --- Dessin des Repères d'Alignement --- 
    if draw_finders:
        print("Dessin des repères d'alignement...")
        # Ces appels vont redessiner les 7 hexagones de chaque repère avec leurs couleurs et contours
        draw_finder_pattern(draw, layout, FINDER_POS_TL, "origin")
        draw_finder_pattern(draw, layout, FINDER_POS_TR, "xaxis")
        draw_finder_pattern(draw, layout, FINDER_POS_BL, "yaxis")
    
    # --- Sauvegarde --- 
    image.save(image_path)
    print(f"Image sauvegardée sous : {image_path}")

if __name__ == '__main__':
    draw_grid_visualization(
        image_path="hex_grid_visualization.png", 
        image_size=(850, 850), # Ajusté ici aussi
        hex_radius=25.0, 
        grid_range_q=(-12, 12), # Gardé pour couvrir une zone suffisante
        grid_range_r=(-12, 12), # Gardé pour couvrir une zone suffisante
        draw_coords=False, 
        draw_finders=True,
        target_center_axial=AxialPos(-5,0) # Passer le centre cible
    ) 