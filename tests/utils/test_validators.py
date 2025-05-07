import unittest
from src.utils.validators import OneOf, Validator # Assurez-vous que le chemin d'import est correct

# Classe de test pour utiliser le descripteur OneOf
class TestConfig:
    # Utilisation de OneOf[str] pour s'assurer que orientation ne peut être que 'flat-top' ou 'pointy-top'
    orientation = OneOf('flat-top', 'pointy-top')
    # Utilisation de OneOf[int] pour les chiffres
    digit = OneOf(0, 1, 2, 3)

    def __init__(self, orientation: str, digit: int):
        self.orientation = orientation # Cela appellera le __set__ de OneOf
        self.digit = digit

class TestOneOfValidator(unittest.TestCase):

    def test_valid_values_str(self):
        """Teste que les valeurs valides pour OneOf[str] sont acceptées."""
        config = TestConfig(orientation='flat-top', digit=0)
        self.assertEqual(config.orientation, 'flat-top')
        
        config.orientation = 'pointy-top' # Test d'une autre valeur valide
        self.assertEqual(config.orientation, 'pointy-top')

    def test_invalid_value_str(self):
        """Teste qu'une valeur invalide pour OneOf[str] lève une ValueError."""
        with self.assertRaisesRegex(ValueError, "La valeur 'angled' n'est pas l'une des options valides : {('pointy-top', 'flat-top'| 'flat-top', 'pointy-top')}"):
            TestConfig(orientation='angled', digit=0)

    def test_valid_values_int(self):
        """Teste que les valeurs valides pour OneOf[int] sont acceptées."""
        config = TestConfig(orientation='flat-top', digit=1)
        self.assertEqual(config.digit, 1)
        
        config.digit = 3 # Test d'une autre valeur valide
        self.assertEqual(config.digit, 3)

    def test_invalid_value_int(self):
        """Teste qu'une valeur invalide pour OneOf[int] lève une ValueError."""
        # Le message d'erreur pour les sets d'entiers peut avoir un ordre variable, donc on vérifie juste le début.
        with self.assertRaisesRegex(ValueError, "La valeur 5 n'est pas l'une des options valides"):
            TestConfig(orientation='flat-top', digit=5)

    def test_direct_validator_instantiation_valid(self):
        """Teste directement l'instanciation et la validation de OneOf (cas valide)."""
        validator = OneOf("a", "b", "c")
        try:
            validator.validate("b")
        except ValueError:
            self.fail("validate() a levé ValueError de manière inattendue pour une valeur valide.")

    def test_direct_validator_instantiation_invalid(self):
        """Teste directement l'instanciation et la validation de OneOf (cas invalide)."""
        validator = OneOf("a", "b", "c")
        with self.assertRaisesRegex(ValueError, "La valeur 'd' n'est pas l'une des options valides : {('a', 'b', 'c'|)" ):
             # L'ordre des éléments dans le set affiché peut varier, 
             # donc on utilise un regex plus flexible pour le message.
            validator.validate("d")


if __name__ == '__main__':
    unittest.main()
