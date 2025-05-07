from PIL import Image, ImageDraw, ImageFont

# Le script est à la racine, src est un package au même niveau
from src.core.hex_grid import AxialPos, PixelCoord, HexgridLayout, Hexagon

def draw_grid_visualization(
    image_path: str = "grid_visualization.png",
    image_size: tuple[int, int] = (600, 600),
    hex_radius: float = 30.0,
    grid_range_q: tuple[int, int] = (-5, 5),
    grid_range_r: tuple[int, int] = (-5, 5),
    draw_coords: bool = True
) -> None:
    """Génère une image visualisant une grille d'hexagones."""

    img_width, img_height = image_size
    background_color = (255, 255, 255) # Blanc
    line_color = (0, 0, 0)       # Noir
    text_color = (50, 50, 50)    # Gris foncé

    # Centre l'origine de la grille au milieu de l'image
    grid_origin = PixelCoord(img_width / 2, img_height / 2)
    layout = HexgridLayout(size=hex_radius, origin=grid_origin)

    image = Image.new("RGB", image_size, background_color)
    draw = ImageDraw.Draw(image)

    try:
        # Essayer de charger une police par défaut. Peut nécessiter d'ajuster le chemin ou le nom.
        font_size = int(hex_radius / 3)
        font = ImageFont.truetype("arial.ttf", font_size) # ou "DejaVuSans.ttf"
    except IOError:
        print(f"Police arial.ttf non trouvée, les coordonnées ne seront pas dessinées.")
        font = ImageFont.load_default() # Police par défaut très basique
        draw_coords = False # Forcer la désactivation si la police n'est pas bonne

    print(f"Dessin de la grille avec q de {grid_range_q[0]} à {grid_range_q[1]} et r de {grid_range_r[0]} à {grid_range_r[1]}")

    for q_coord in range(grid_range_q[0], grid_range_q[1] + 1):
        for r_coord in range(grid_range_r[0], grid_range_r[1] + 1):
            # Contrainte optionnelle pour ne dessiner que les hexagones dans une forme globalement hexagonale
            # s_coord = -q_coord - r_coord
            # if max(abs(q_coord), abs(r_coord), abs(s_coord)) > max(abs(grid_range_q[0]), abs(grid_range_r[0])):
            #     continue
            
            current_pos = AxialPos(q_coord, r_coord)
            # Créer l'objet Hexagon
            current_hex = Hexagon(pos=current_pos, layout=layout)
            
            hex_center_pixel = current_hex.get_pixel_center() # Utiliser la méthode de Hexagon
            
            # Ne dessiner que si l'hexagone est grossièrement dans les limites de l'image
            # (avec une marge pour les sommets)
            if not ((-hex_radius < hex_center_pixel.x < img_width + hex_radius) and \
                    (-hex_radius < hex_center_pixel.y < img_height + hex_radius)):
                continue

            vertices_pixels = current_hex.get_vertices() # Utiliser la méthode de Hexagon
            # Convertir les PixelCoord en une liste de tuples (x,y) pour Pillow
            drawable_vertices = [(v.x, v.y) for v in vertices_pixels]
            
            draw.polygon(drawable_vertices, outline=line_color, fill=None) # fill peut être une couleur

            if draw_coords:
                # Préparer le texte des coordonnées
                coord_text = f"{q_coord},{r_coord}"
                # Obtenir la bounding box du texte pour le centrer
                try:
                    # textbbox est disponible dans les versions plus récentes de Pillow
                    bbox = draw.textbbox((0,0), coord_text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                except AttributeError:
                    # Fallback pour les anciennes versions de Pillow
                    text_width, text_height = draw.textsize(coord_text, font=font) # type: ignore
                
                text_x = hex_center_pixel.x - text_width / 2
                text_y = hex_center_pixel.y - text_height / 2
                draw.text((text_x, text_y), coord_text, fill=text_color, font=font)
    
    image.save(image_path)
    print(f"Image sauvegardée sous : {image_path}")

if __name__ == '__main__':
    draw_grid_visualization(
        image_path="hex_grid_visualization.png", 
        hex_radius=25.0, 
        grid_range_q=(-7, 7),
        grid_range_r=(-7, 7),
        draw_coords=True
    ) 