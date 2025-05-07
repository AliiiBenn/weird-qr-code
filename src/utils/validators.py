from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# T_Val représente le type de la valeur que le validateur va manipuler.
T_Val = TypeVar('T_Val')

class Validator(Generic[T_Val], ABC):
    """Classe de base abstraite et générique pour les validateurs d'attributs."""

    def __set_name__(self, owner: type, name: str) -> None:
        """Appelé lorsque le descripteur est assigné à un attribut de classe."""
        self.private_name: str = '_' + name

    def __get__(self, obj: object | None, objtype: type | None = None) -> T_Val | 'Validator[T_Val]':
        """Récupère la valeur de l'attribut privé managé.
        
        Si accédé via la classe (obj is None), retourne le descripteur lui-même.
        Sinon, retourne la valeur de l'attribut de type T_Val.
        """
        if obj is None:
            return self
        # On s'attend à ce que getattr retourne une valeur de type T_Val
        # Mypy pourrait avoir besoin d'un cast ici si self.private_name n'est pas connu
        # pour toujours contenir T_Val, mais pour l'usage d'un descripteur c'est l'attente.
        return getattr(obj, self.private_name)

    def __set__(self, obj: object, value: T_Val) -> None:
        """Valide et assigne la nouvelle valeur (de type T_Val) à l'attribut privé managé."""
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value: T_Val) -> None:
        """Méthode abstraite pour valider la valeur (de type T_Val).
        Doit être implémentée par les sous-classes.
        """
        pass


class OneOf(Validator[T_Val]):
    """Validateur qui vérifie si une valeur fait partie d'un ensemble d'options prédéfinies."""

    def __init__(self, *options: T_Val) -> None:
        """Initialise le validateur avec les options autorisées.

        Args:
            *options: Les valeurs autorisées pour l'attribut.
        """
        self.options: set[T_Val] = set(options)

    def validate(self, value: T_Val) -> None:
        """Valide si la valeur donnée est l'une des options autorisées.

        Args:
            value: La valeur à valider.

        Raises:
            ValueError: Si la valeur n'est pas dans l'ensemble des options autorisées.
        """
        if value not in self.options:
            raise ValueError(
                f"La valeur {value!r} n'est pas l'une des options valides : {self.options!r}"
            )
