from typing import Literal, TypeAlias, cast, TYPE_CHECKING
from ..utils.validators import OneOf, Validator
from dataclasses import dataclass
import math

AxialCoordinatesValues: TypeAlias = Literal[-1, 0, 1]

class AxialCoordinates:
    """Représente un déplacement unitaire ou une direction sur la grille hexagonale."""
    _q = OneOf[AxialCoordinatesValues](-1, 0, 1)
    _r = OneOf[AxialCoordinatesValues](-1, 0, 1)

    def __init__(self, q: AxialCoordinatesValues, r: AxialCoordinatesValues):
        self._q = q
        self._r = r

    @property
    def q(self) -> AxialCoordinatesValues:
        return cast(AxialCoordinatesValues, self._q)

    @property
    def r(self) -> AxialCoordinatesValues:
        return cast(AxialCoordinatesValues, self._r)

    @property
    def value(self) -> tuple[AxialCoordinatesValues, AxialCoordinatesValues]:
        return (self.q, self.r)

    def __str__(self) -> str:
        return f"AxialCoordinates(q={self.q}, r={self.r})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AxialCoordinates):
            return NotImplemented
        return self.q == other.q and self.r == other.r
    
    def __hash__(self) -> int:
        return hash((self.q, self.r))


@dataclass(frozen=True)
class AxialPos:
    """Représente une position absolue (q, r) sur la grille hexagonale."""
    q: int
    r: int

    def to_tuple(self) -> tuple[int, int]:
        return (self.q, self.r)

    def __add__(self, other: AxialCoordinates) -> 'AxialPos':
        """Additionne une direction (AxialCoordinates) à cette position."""
        if not isinstance(other, AxialCoordinates):
            return NotImplemented
        return AxialPos(self.q + other.q, self.r + other.r)
    
    # __sub__ pourrait être utile pour trouver la direction entre deux positions
    def __sub__(self, other: 'AxialPos') -> AxialCoordinates:
        """Calcule la direction (AxialCoordinates) d'une autre position vers celle-ci.
           Attention: le résultat doit être un déplacement unitaire valide pour AxialCoordinates.
           Cette méthode suppose que 'other' est un voisin direct pour un résultat valide pour AxialCoordinates.
           Pour une différence générale, le type de retour serait AxialPos ou un nouveau type Vector.
        """
        # Ceci est une simplification. Une vraie soustraction de vecteurs donnerait un (int, int)
        # qui ne serait pas nécessairement un AxialCoordinates valide. 
        # Pour l'instant, on lève une exception si le résultat n'est pas un déplacement valide.
        # Ou, on pourrait retourner un AxialPos représentant le vecteur différence.
        # Alternative: ne pas implémenter __sub__ ici si son usage est ambigu.
        dq = self.q - other.q
        dr = self.r - other.r
        # Tentative de créer une AxialCoordinates, lèvera ValueError si dq/dr n'est pas dans [-1,0,1]
        # Cela fait l'hypothèse que __sub__ est utilisé pour trouver une direction unitaire.
        try:
            return AxialCoordinates(dq, dr) # type: ignore
        except ValueError:
            # Si on veut une différence générale, on retournerait AxialPos(dq, dr)
            # ou on lèverait une erreur plus spécifique indiquant que le résultat n'est pas une direction unitaire.
            raise ValueError(f"La différence ({dq},{dr}) ne forme pas une direction unitaire valide.")

# Directions Axiales Constantes pour une grille "flat-top"
# (q, r) -> voir https://www.redblobgames.com/grids/hexagons/#coordinates-axial
# Pour flat-top, les axes sont souvent définis ainsi:
# q: horizontal (vers la droite)
# r: diagonal (vers le bas-droite)
# s (implicite, s = -q-r): diagonal (vers le bas-gauche)

HEX_DIRECTIONS_FLAT_TOP: dict[str, AxialCoordinates] = {
    "east":      AxialCoordinates(1, 0),
    "northeast": AxialCoordinates(1, -1),
    "northwest": AxialCoordinates(0, -1),
    "west":      AxialCoordinates(-1, 0),
    "southwest": AxialCoordinates(-1, 1),
    "southeast": AxialCoordinates(0, 1),
}

# Optionnel: une liste ordonnée si l'ordre est important pour certaines opérations
# L'ordre ici est arbitraire (commençant à l'Est et allant dans le sens anti-horaire)
ORDERED_HEX_DIRECTIONS_FLAT_TOP: list[AxialCoordinates] = [
    HEX_DIRECTIONS_FLAT_TOP["east"],
    HEX_DIRECTIONS_FLAT_TOP["northeast"],
    HEX_DIRECTIONS_FLAT_TOP["northwest"],
    HEX_DIRECTIONS_FLAT_TOP["west"],
    HEX_DIRECTIONS_FLAT_TOP["southwest"],
    HEX_DIRECTIONS_FLAT_TOP["southeast"],
]

@dataclass(frozen=True)
class RelativePixelX:
    """Calcule la coordonnée X relative d'un hexagone par rapport à son layout."""
    size: float
    q_coord: int # Renommé pour éviter confusion avec une éventuelle propriété nommée q

    @property
    def value(self) -> float:
        """Retourne la valeur du pixel X relatif."""
        return self.size * (3/2 * self.q_coord)


@dataclass(frozen=True)
class RelativePixelY:
    """Calcule la coordonnée Y relative d'un hexagone par rapport à son layout (orientation flat-top)."""
    size: float
    q_coord: int
    r_coord: int

    @property
    def value(self) -> float:
        """Retourne la valeur du pixel Y relatif."""
        return self.size * (math.sqrt(3)/2 * self.q_coord + math.sqrt(3) * self.r_coord)


@dataclass(frozen=True)
class PixelCoord:
    """Représente une coordonnée en pixels (x, y)."""
    x: float
    y: float

    @classmethod
    def from_axial(cls, axial_pos: 'AxialPos', layout: 'HexgridLayout') -> 'PixelCoord': # Utilisation de 'AxialPos' en string si défini après
        """Factory method pour créer un PixelCoord à partir de coordonnées axiales et d'un layout.
        Pour une orientation "flat-top".
        """
        pixel_x_relative = RelativePixelX(layout.size, axial_pos.q)
        pixel_y_relative = RelativePixelY(layout.size, axial_pos.q, axial_pos.r)
        
        pixel_x_final = pixel_x_relative.value + layout.origin.x
        pixel_y_final = pixel_y_relative.value + layout.origin.y
        
        return cls(x=pixel_x_final, y=pixel_y_final)


@dataclass(frozen=True)
class HexgridLayout:
    """Définit les paramètres de layout pour une grille d'hexagones "flat-top".

    Attributs:
        size: La distance du centre d'un hexagone à l'un de ses sommets.
        origin: Les coordonnées en pixels du centre de l'hexagone AxialPos(0,0).
    """
    size: float
    origin: PixelCoord

    def get_hexagon_vertices(self, hex_pos: 'AxialPos') -> list[PixelCoord]:
        """Calcule les coordonnées des 6 sommets d'un hexagone "flat-top" donné par sa position AxialPos."""
        center: PixelCoord = PixelCoord.from_axial(hex_pos, self) # Appel direct à la factory method
        vertices: list[PixelCoord] = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
            vertex_x = center.x + self.size * math.cos(angle_rad)
            vertex_y = center.y + self.size * math.sin(angle_rad)
            vertices.append(PixelCoord(x=vertex_x, y=vertex_y))
        return vertices

CubeCoord: TypeAlias = tuple[int, int, int]

def axial_to_cube(axial_pos: AxialPos) -> CubeCoord:
    """Convertit les coordonnées axiales en coordonnées cubiques."""
    q = axial_pos.q
    r = axial_pos.r
    x = q
    z = r
    y = -x - z # Car x + y + z = 0
    return (x, y, z)

@dataclass(frozen=False)
class Hexagon:
    """Représente un hexagone individuel sur la grille.

    Combine une position logique (AxialPos) avec le layout de la grille (HexgridLayout)
    pour permettre des opérations géométriques spécifiques à cet hexagone.
    """
    pos: AxialPos
    layout: HexgridLayout
    # data: Any = None # Placeholder pour des données futures (couleur, type, etc.)

    def __post_init__(self):
        # Validation potentielle ou initialisation dérivée si nécessaire
        pass

    def get_pixel_center(self) -> PixelCoord:
        """Retourne le centre de cet hexagone en coordonnées pixels."""
        return PixelCoord.from_axial(self.pos, self.layout)

    def get_vertices(self) -> list[PixelCoord]:
        """Retourne la liste des 6 sommets de cet hexagone en coordonnées pixels."""
        return self.layout.get_hexagon_vertices(self.pos)

    def __repr__(self) -> str:
        # Une représentation simple pour le débogage
        return f"Hexagon(pos={self.pos})"

    def __eq__(self, other: object) -> bool:
        """Deux hexagones sont égaux s'ils ont la même position et le même layout."""
        if not isinstance(other, Hexagon):
            return NotImplemented
        return self.pos == other.pos and self.layout == other.layout

    def __hash__(self) -> int:
        """Calcule le hash basé sur la position et le layout."""
        # Le layout est aussi un dataclass, donc hashable par défaut s'il est frozen.
        # Si HexgridLayout n'est pas frozen, il faudra une autre stratégie de hash.
        return hash((self.pos, self.layout))

    def get_neighbors(self) -> list['Hexagon']:
        """Retourne la liste des 6 hexagones voisins."""
        neighbors: list[Hexagon] = []
        for direction in ORDERED_HEX_DIRECTIONS_FLAT_TOP:
            neighbor_pos = self.pos + direction # Utilise AxialPos.__add__
            # Crée un nouvel objet Hexagon pour chaque voisin, partageant le même layout
            neighbors.append(Hexagon(pos=neighbor_pos, layout=self.layout))
        return neighbors
    
    def distance_to(self, other: 'Hexagon') -> int:
        """Calcule la distance (en nombre d'hexagones) à un autre hexagone."""
        # Vérifier si les layouts sont compatibles ? Pour l'instant, on suppose qu'ils le sont
        # ou que la distance ne dépend que des positions logiques.
        if not isinstance(other, Hexagon):
            raise TypeError("L'autre objet doit être une instance de Hexagon")
        
        cube1 = axial_to_cube(self.pos)
        cube2 = axial_to_cube(other.pos)
        
        distance = (abs(cube1[0] - cube2[0]) + 
                    abs(cube1[1] - cube2[1]) + 
                    abs(cube1[2] - cube2[2])) // 2
        return distance




