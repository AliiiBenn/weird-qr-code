import unittest
import math # Pour les calculs de référence dans les tests
from src.core.hex_grid import (
    AxialCoordinates, AxialCoordinatesValues, AxialPos, PixelCoord, HexgridLayout,
    ORDERED_HEX_DIRECTIONS_FLAT_TOP, # Importer les directions pour les tests
    axial_to_cube, # Importer la fonction à tester
    CubeCoord, # Importer le TypeAlias pour l'utiliser dans les tests si besoin
    RelativePixelX, # Importer les nouvelles classes
    RelativePixelY,
    Hexagon # Importer la nouvelle classe
)

class TestAxialCoordinates(unittest.TestCase):

    def test_valid_instantiation(self):
        """Tests successful instantiation with valid q and r values."""
        # Explicitly type the list to match the expected Literal type
        coords: list[AxialCoordinatesValues] = [-1, 0, 1]
        for q_val in coords:
            for r_val in coords:
                with self.subTest(q=q_val, r=r_val):
                    try:
                        ax = AxialCoordinates(q=q_val, r=r_val)
                        self.assertEqual(ax.q, q_val, "q attribute not set correctly")
                        self.assertEqual(ax.r, r_val, "r attribute not set correctly")
                        self.assertEqual(ax.value, (q_val, r_val), "value property incorrect")
                    except ValueError:
                        self.fail(f"AxialCoordinates raised ValueError unexpectedly for q={q_val}, r={r_val}")

    def test_invalid_q_value(self):
        """Tests that an invalid q value raises a ValueError."""
        invalid_q_values = [-2, 2, 10] # These are int, which is fine for testing invalid inputs
        for q_invalid in invalid_q_values:
            with self.subTest(q_invalid=q_invalid):
                # The validator will handle the type mismatch at runtime if types were strictly enforced beyond Literal
                with self.assertRaisesRegex(ValueError, f"La valeur {q_invalid}.*n'est pas l'une des options valides"):
                    AxialCoordinates(q=q_invalid, r=0) # type: ignore

    def test_invalid_r_value(self):
        """Tests that an invalid r value raises a ValueError."""
        invalid_r_values = [-2, 2, 10] # These are int
        for r_invalid in invalid_r_values:
            with self.subTest(r_invalid=r_invalid):
                with self.assertRaisesRegex(ValueError, f"La valeur {r_invalid}.*n'est pas l'une des options valides"):
                    AxialCoordinates(q=0, r=r_invalid) # type: ignore

    def test_string_representation(self):
        """Tests the __str__ method."""
        ax = AxialCoordinates(q=1, r=-1)
        self.assertEqual(str(ax), "AxialCoordinates(q=1, r=-1)")

        ax_zero = AxialCoordinates(q=0, r=0)
        self.assertEqual(str(ax_zero), "AxialCoordinates(q=0, r=0)")

    def test_properties_return_correct_values(self):
        """Test that properties q, r, and value return expected values after instantiation."""
        ax = AxialCoordinates(q=1, r=0)
        self.assertEqual(ax.q, 1)
        self.assertEqual(ax.r, 0)
        self.assertEqual(ax.value, (1,0))

class TestRelativePixelUtils(unittest.TestCase):
    def test_relative_pixel_x(self):
        """Teste RelativePixelX."""
        rp_x1 = RelativePixelX(size=10.0, q_coord=0)
        self.assertAlmostEqual(rp_x1.value, 0.0)

        rp_x2 = RelativePixelX(size=10.0, q_coord=1)
        self.assertAlmostEqual(rp_x2.value, 15.0) # 10 * 1.5 * 1

        rp_x3 = RelativePixelX(size=20.0, q_coord=2)
        self.assertAlmostEqual(rp_x3.value, 60.0) # 20 * 1.5 * 2

        rp_x4 = RelativePixelX(size=10.0, q_coord=-1)
        self.assertAlmostEqual(rp_x4.value, -15.0) # 10 * 1.5 * -1

    def test_relative_pixel_y(self):
        """Teste RelativePixelY."""
        # q=0, r=0
        rp_y1 = RelativePixelY(size=10.0, q_coord=0, r_coord=0)
        self.assertAlmostEqual(rp_y1.value, 0.0)

        # q=1, r=0
        rp_y2 = RelativePixelY(size=10.0, q_coord=1, r_coord=0)
        self.assertAlmostEqual(rp_y2.value, 10.0 * math.sqrt(3)/2)

        # q=0, r=1
        rp_y3 = RelativePixelY(size=10.0, q_coord=0, r_coord=1)
        self.assertAlmostEqual(rp_y3.value, 10.0 * math.sqrt(3))

        # q=1, r=1
        rp_y4 = RelativePixelY(size=10.0, q_coord=1, r_coord=1)
        self.assertAlmostEqual(rp_y4.value, 10.0 * (math.sqrt(3)/2 + math.sqrt(3)))
        self.assertAlmostEqual(rp_y4.value, 10.0 * 1.5 * math.sqrt(3))

        # q=-1, r=-1
        rp_y5 = RelativePixelY(size=10.0, q_coord=-1, r_coord=-1)
        self.assertAlmostEqual(rp_y5.value, 10.0 * (-math.sqrt(3)/2 - math.sqrt(3)))
        self.assertAlmostEqual(rp_y5.value, -10.0 * 1.5 * math.sqrt(3))

class TestHexgridLayout(unittest.TestCase):

    def test_pixel_coord_from_axial_origin_zero(self):
        """Teste PixelCoord.from_axial avec l'origine à (0,0)."""
        layout = HexgridLayout(size=10.0, origin=PixelCoord(0.0, 0.0))
        
        center_0_0 = PixelCoord.from_axial(AxialPos(0,0), layout)
        self.assertAlmostEqual(center_0_0.x, 0.0)
        self.assertAlmostEqual(center_0_0.y, 0.0)

        center_1_0 = PixelCoord.from_axial(AxialPos(1,0), layout)
        self.assertAlmostEqual(center_1_0.x, 15.0)
        self.assertAlmostEqual(center_1_0.y, 10.0 * math.sqrt(3)/2)

        center_0_1 = PixelCoord.from_axial(AxialPos(0,1), layout)
        self.assertAlmostEqual(center_0_1.x, 0.0)
        self.assertAlmostEqual(center_0_1.y, 10.0 * math.sqrt(3))

        center_1_1 = PixelCoord.from_axial(AxialPos(1,1), layout)
        self.assertAlmostEqual(center_1_1.x, 15.0)
        self.assertAlmostEqual(center_1_1.y, 10.0 * 1.5 * math.sqrt(3))

    def test_pixel_coord_from_axial_with_offset_origin(self):
        """Teste PixelCoord.from_axial avec une origine décalée."""
        origin_offset = PixelCoord(100.0, 50.0)
        layout = HexgridLayout(size=10.0, origin=origin_offset)
        
        center_0_0 = PixelCoord.from_axial(AxialPos(0,0), layout)
        self.assertAlmostEqual(center_0_0.x, origin_offset.x)
        self.assertAlmostEqual(center_0_0.y, origin_offset.y)

        center_1_0 = PixelCoord.from_axial(AxialPos(1,0), layout)
        self.assertAlmostEqual(center_1_0.x, 15.0 + origin_offset.x)
        self.assertAlmostEqual(center_1_0.y, (10.0 * math.sqrt(3)/2) + origin_offset.y)

    def test_get_hexagon_vertices_origin_zero(self):
        """Teste get_hexagon_vertices avec l'origine à (0,0)."""
        layout = HexgridLayout(size=10.0, origin=PixelCoord(0.0, 0.0))
        hex_pos_center = AxialPos(0,0)
        center_pixel = PixelCoord.from_axial(hex_pos_center, layout)
        vertices = layout.get_hexagon_vertices(hex_pos_center)

        self.assertEqual(len(vertices), 6)

        expected_vertices = []
        for i in range(6):
            angle_rad = math.radians(60 * i)
            expected_x = center_pixel.x + layout.size * math.cos(angle_rad)
            expected_y = center_pixel.y + layout.size * math.sin(angle_rad)
            expected_vertices.append(PixelCoord(expected_x, expected_y))
        
        for i in range(6):
            with self.subTest(vertex_index=i):
                self.assertAlmostEqual(vertices[i].x, expected_vertices[i].x)
                self.assertAlmostEqual(vertices[i].y, expected_vertices[i].y)
    
    def test_get_hexagon_vertices_offset_hex_and_origin(self):
        """Teste get_hexagon_vertices pour un hexagone décalé et une origine décalée."""
        layout = HexgridLayout(size=20.0, origin=PixelCoord(50.0, 75.0))
        hex_pos_offset = AxialPos(1,-1)
        
        center_pixel = PixelCoord.from_axial(hex_pos_offset, layout)
        vertices = layout.get_hexagon_vertices(hex_pos_offset)

        self.assertEqual(len(vertices), 6)

        expected_vertices = []
        for i in range(6):
            angle_rad = math.radians(60 * i)
            expected_x = center_pixel.x + layout.size * math.cos(angle_rad)
            expected_y = center_pixel.y + layout.size * math.sin(angle_rad)
            expected_vertices.append(PixelCoord(expected_x, expected_y))
        
        for i in range(6):
            with self.subTest(vertex_index=i):
                self.assertAlmostEqual(vertices[i].x, expected_vertices[i].x, places=5)
                self.assertAlmostEqual(vertices[i].y, expected_vertices[i].y, places=5)

class TestHexagon(unittest.TestCase):
    def setUp(self): # Méthode pour configurer un layout commun pour les tests
        self.origin = PixelCoord(0.0, 0.0)
        self.size = 10.0
        self.layout = HexgridLayout(size=self.size, origin=self.origin)
        self.hex_center = Hexagon(pos=AxialPos(0,0), layout=self.layout)
        self.hex_offset = Hexagon(pos=AxialPos(5,-3), layout=self.layout)

    def test_hexagon_instantiation_and_properties(self):
        """Teste l'instanciation de Hexagon et l'accès aux propriétés pos/layout."""
        self.assertEqual(self.hex_center.pos, AxialPos(0,0))
        self.assertEqual(self.hex_center.layout, self.layout)
        self.assertEqual(self.hex_offset.pos, AxialPos(5,-3))
        self.assertEqual(self.hex_offset.layout, self.layout)

    def test_hexagon_get_pixel_center(self):
        """Teste que get_pixel_center délègue correctement."""
        expected_center = PixelCoord.from_axial(AxialPos(0,0), self.layout)
        self.assertEqual(self.hex_center.get_pixel_center(), expected_center)
        
        expected_offset_center = PixelCoord.from_axial(AxialPos(5,-3), self.layout)
        self.assertEqual(self.hex_offset.get_pixel_center(), expected_offset_center)

    def test_hexagon_get_vertices(self):
        """Teste que get_vertices délègue correctement."""
        expected_vertices = self.layout.get_hexagon_vertices(AxialPos(0,0))
        self.assertEqual(self.hex_center.get_vertices(), expected_vertices)
        
        expected_offset_vertices = self.layout.get_hexagon_vertices(AxialPos(5,-3))
        self.assertEqual(self.hex_offset.get_vertices(), expected_offset_vertices)

    def test_hexagon_get_neighbors(self):
        """Teste la méthode get_neighbors."""
        neighbors = self.hex_center.get_neighbors()
        self.assertEqual(len(neighbors), 6)
        
        # Vérifie que les positions des voisins sont correctes
        neighbor_positions = [n.pos for n in neighbors]
        expected_neighbor_positions = [
            AxialPos(d.q, d.r) for d in ORDERED_HEX_DIRECTIONS_FLAT_TOP
        ]
        self.assertListEqual(neighbor_positions, expected_neighbor_positions)
        
        # Vérifie que les voisins ont le bon layout
        for neighbor in neighbors:
            self.assertEqual(neighbor.layout, self.layout)
            
        # Test pour une position décalée
        offset_neighbors = self.hex_offset.get_neighbors()
        self.assertEqual(len(offset_neighbors), 6)
        offset_neighbor_positions = [n.pos for n in offset_neighbors]
        expected_offset_neighbor_positions = [
             self.hex_offset.pos + d for d in ORDERED_HEX_DIRECTIONS_FLAT_TOP
        ]
        # Utiliser assertCountEqual ici car l'ordre pourrait être moins critique, 
        # mais notre implémentation suit ORDERED_HEX_DIRECTIONS_FLAT_TOP
        # self.assertCountEqual(offset_neighbor_positions, expected_offset_neighbor_positions)
        self.assertListEqual(offset_neighbor_positions, expected_offset_neighbor_positions)
        self.assertEqual(len(set(offset_neighbor_positions)), 6)
        
    def test_hexagon_equality_and_hash(self):
        """Teste l'égalité et le hash des objets Hexagon."""
        h1 = Hexagon(pos=AxialPos(1,2), layout=self.layout)
        h2 = Hexagon(pos=AxialPos(1,2), layout=self.layout)
        h3 = Hexagon(pos=AxialPos(3,4), layout=self.layout)
        # Créer un layout différent (même s'il a les mêmes valeurs)
        layout2 = HexgridLayout(size=self.size, origin=self.origin) 
        h4 = Hexagon(pos=AxialPos(1,2), layout=layout2)
        
        self.assertEqual(h1, h2) # Mêmes pos et layout
        self.assertNotEqual(h1, h3) # pos différentes
        self.assertEqual(h1, h4) # Mêmes valeurs de layout, donc égaux par défaut pour dataclass
        # Si on voulait qu'ils soient différents s'ils n'ont pas la MÊME instance de layout,
        # il faudrait changer la logique __eq__.
        
        # Test Hash
        self.assertEqual(hash(h1), hash(h2))
        self.assertEqual(hash(h1), hash(h4)) # Car les layouts sont égaux
        # Mettre h1 et h3 dans un set
        hex_set = {h1, h3}
        self.assertIn(h2, hex_set) # h2 est égal à h1
        self.assertIn(h4, hex_set) # h4 est égal à h1

    def test_hexagon_distance_to(self):
        """Teste la méthode distance_to."""
        # Utilise le layout défini dans setUp
        h0 = Hexagon(AxialPos(0,0), self.layout)
        h1 = Hexagon(AxialPos(1,0), self.layout)
        h2 = Hexagon(AxialPos(0,1), self.layout)
        h3 = Hexagon(AxialPos(1,-1), self.layout)
        h10_0 = Hexagon(AxialPos(10,0), self.layout)
        h0_10 = Hexagon(AxialPos(0,10), self.layout)
        h5_5 = Hexagon(AxialPos(5,5), self.layout)
        h1_2 = Hexagon(AxialPos(1,2), self.layout)
        h4_2 = Hexagon(AxialPos(4,2), self.layout)
        h2_2 = Hexagon(AxialPos(2,2), self.layout)
        h_neg1_neg2 = Hexagon(AxialPos(-1,-2), self.layout)
        h_3_1 = Hexagon(AxialPos(3,1), self.layout)
        
        test_cases = [
            (h0, h0, 0),
            (h0, h1, 1),
            (h0, h2, 1),
            (h0, h3, 1),
            (h0, h10_0, 10),
            (h0, h0_10, 10),
            (h0, h5_5, 10),
            (h1_2, h4_2, 3),
            (h0, h2_2, 4),
            (h_neg1_neg2, h_3_1, 7),
        ]
        
        for hex1, hex2, expected_dist in test_cases:
            with self.subTest(hex1=hex1, hex2=hex2, expected_dist=expected_dist):
                self.assertEqual(hex1.distance_to(hex2), expected_dist)
                # La distance doit être symétrique
                self.assertEqual(hex2.distance_to(hex1), expected_dist, "La distance n'est pas symétrique")

class TestHexGridUtils(unittest.TestCase):
    def test_axial_to_cube(self):
        """Teste la conversion de coordonnées axiales en cubiques."""
        test_cases = {
            AxialPos(0,0): (0,0,0),
            AxialPos(1,0): (1,-1,0),
            AxialPos(0,1): (0,-1,1),
            AxialPos(-1,0): (-1,1,0),
            AxialPos(0,-1): (0,1,-1),
            AxialPos(1,1): (1,-2,1),
            AxialPos(2,-5): (2,3,-5),
            AxialPos(-3,2): (-3,1,2),
        }
        for axial, expected_cube in test_cases.items():
            with self.subTest(axial=axial, expected_cube=expected_cube):
                self.assertEqual(expected_cube[0] + expected_cube[1] + expected_cube[2], 0, f"Coordonnée cubique attendue invalide: {expected_cube}")
                self.assertEqual(axial_to_cube(axial), expected_cube)

if __name__ == '__main__':
    unittest.main()
