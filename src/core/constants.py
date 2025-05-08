from enum import Enum
from typing import Final, TypeAlias
from .hex_grid import AxialPos # Import relatif car constants.py est dans core/

# Type alias pour la clarté
ColorTuple: TypeAlias = tuple[int, int, int]

class ProtocolColor(Enum):
    """Enumération des couleurs de base utilisées dans le protocole."""
    # Membre = Valeur (Tuple RGB)
    BLACK = (0, 0, 0)
    RED   = (255, 0, 0)
    BLUE  = (0, 0, 255)
    WHITE = (255, 255, 255)
    
    @property
    def rgb(self) -> ColorTuple:
        """Retourne la valeur RGB de la couleur."""
        return self.value

# Couleurs pour les Repères d'Alignement (Finder Patterns)
FINDER_COLORS: Final[dict[str, dict[str, ProtocolColor]]] = {
    "origin": {"center": ProtocolColor.WHITE, "ring": ProtocolColor.RED}, # Repère TL (Origine)
    "xaxis":  {"center": ProtocolColor.WHITE, "ring": ProtocolColor.RED}, # Repère TR (Axe X)
    "yaxis":  {"center": ProtocolColor.WHITE, "ring": ProtocolColor.BLUE}, # Repère BL (Axe Y)
}

# --- Configuration de la Grille de Référence (Taille/Version Initiale) ---
# Basé sur une grille de référence où q et r varient de -10 à +10.
# Ces positions pourront être affinées après visualisation.
GRID_RADIUS_REF: Final[int] = 10 

# Positions des centres des 3 Repères d'Alignement pour la grille de référence
# Ajustées pour être un peu rentrées des bords.
FINDER_POS_TL: Final[AxialPos] = AxialPos(-8, 0)  # Haut-Gauche logique
FINDER_POS_TR: Final[AxialPos] = AxialPos(0, -8)  # Haut-Droit logique
FINDER_POS_BL: Final[AxialPos] = AxialPos(-8, 8)  # Bas-Gauche logique

# On pourrait ajouter ici d'autres constantes liées au protocole à l'avenir.
