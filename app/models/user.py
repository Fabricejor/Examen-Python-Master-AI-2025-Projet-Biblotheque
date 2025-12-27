"""
Modèle représentant un utilisateur de la bibliothèque.
Types d'utilisateurs : Étudiant, Enseignant, Personnel administratif
"""

from enum import Enum
from typing import List, Dict, Optional
from datetime import datetime
from abc import ABC, abstractmethod
from app.utils.validators import generate_id
from app.utils.constants import (
    LIMITE_EMPRUNTS_ETUDIANT,
    LIMITE_EMPRUNTS_ENSEIGNANT,
    LIMITE_EMPRUNTS_PERSONNEL_ADMIN
)


class UserType(Enum):
    """Énumération des types d'utilisateurs."""
    ETUDIANT = "Etudiant"
    ENSEIGNANT = "Enseignant"
    PERSONNEL_ADMIN = "Personnel_admin"


class User(ABC):
    """
    Classe abstraite de base représentant un utilisateur de la bibliothèque.
    
    Attributs:
        id_user (str): Identifiant unique de l'utilisateur (format: userXX000)
        type_utilisateur (UserType): Type d'utilisateur
        nombre_emprunt_total (int): Nombre total d'emprunts effectués
        list_emprunt (List[Dict]): Liste des emprunts en cours (format JSON)
    """
    
    def __init__(
        self,
        type_utilisateur: UserType,
        nom: str,
        id_user: Optional[str] = None,
        nombre_emprunt_total: int = 0,
        list_emprunt: Optional[List[Dict]] = None
    ):
        """
        Initialise un nouvel utilisateur.
        
        Args:
            type_utilisateur (UserType): Type d'utilisateur
            nom (str): Nom de l'utilisateur
            id_user (str, optional): ID de l'utilisateur. Si non fourni, généré automatiquement
            nombre_emprunt_total (int, optional): Nombre total d'emprunts. Par défaut: 0
            list_emprunt (List[Dict], optional): Liste des emprunts. Par défaut: liste vide
        """
        # Génère un ID unique avec préfixe "user" si non fourni
        self._id_user = id_user if id_user else generate_id("user")
        self._nom = nom.strip() if nom else ""
        self._type_utilisateur = type_utilisateur if isinstance(type_utilisateur, UserType) else UserType(type_utilisateur)
        self._nombre_emprunt_total = max(0, nombre_emprunt_total)
        self._list_emprunt = list_emprunt if list_emprunt is not None else []
    
    # Propriétés (getters) avec encapsulation
    @property
    def id_user(self) -> str:
        """Retourne l'ID de l'utilisateur."""
        return self._id_user
    
    @property
    def nom(self) -> str:
        """Retourne le nom de l'utilisateur."""
        return self._nom
    
    @property
    def type_utilisateur(self) -> UserType:
        """Retourne le type d'utilisateur."""
        return self._type_utilisateur
    
    @property
    def nombre_emprunt_total(self) -> int:
        """Retourne le nombre total d'emprunts."""
        return self._nombre_emprunt_total
    
    @property
    def list_emprunt(self) -> List[Dict]:
        """Retourne la liste des emprunts en cours."""
        return self._list_emprunt.copy()  # Retourne une copie pour éviter les modifications externes
    
    @nom.setter
    def nom(self, value: str):
        """Modifie le nom de l'utilisateur."""
        if not value or not value.strip():
            raise ValueError("Le nom ne peut pas être vide.")
        self._nom = value.strip()
    
    @property
    @abstractmethod
    def limite_emprunts(self) -> int:
        """Retourne la limite d'emprunts pour ce type d'utilisateur."""
        pass
    
    def nombre_emprunts_en_cours(self) -> int:
        """Retourne le nombre d'emprunts actuellement en cours."""
        return len(self._list_emprunt)
    
    def peut_emprunter(self) -> bool:
        """
        Vérifie si l'utilisateur peut effectuer un nouvel emprunt.
        
        Returns:
            bool: True si l'utilisateur peut emprunter, False sinon
        """
        return self.nombre_emprunts_en_cours() < self.limite_emprunts
    
    def ajouter_emprunt(
        self,
        id_emprunt: str,
        date_emprunt: str,
        date_retour_prevue: str,
        titre_du_livre: str
    ):
        """
        Ajoute un emprunt à la liste des emprunts en cours.
        
        Args:
            id_emprunt (str): Identifiant de l'emprunt
            date_emprunt (str): Date d'emprunt (format string)
            date_retour_prevue (str): Date de retour prévue (format string)
            titre_du_livre (str): Titre du livre emprunté
            
        Raises:
            ValueError: Si l'utilisateur a atteint sa limite d'emprunts
        """
        if not self.peut_emprunter():
            raise ValueError(
                f"Limite d'emprunts atteinte. "
                f"Limite: {self.limite_emprunts}, "
                f"Emprunts en cours: {self.nombre_emprunts_en_cours()}"
            )
        
        emprunt = {
            "id_emprunt": id_emprunt,
            "date_emprunt": date_emprunt,
            "date_retour_prevue": date_retour_prevue,
            "titre_du_livre": titre_du_livre
        }
        
        self._list_emprunt.append(emprunt)
        self._nombre_emprunt_total += 1
    
    def retirer_emprunt(self, id_emprunt: str) -> bool:
        """
        Retire un emprunt de la liste des emprunts en cours.
        
        Args:
            id_emprunt (str): Identifiant de l'emprunt à retirer
            
        Returns:
            bool: True si l'emprunt a été retiré, False s'il n'existe pas
        """
        for i, emprunt in enumerate(self._list_emprunt):
            if emprunt.get("id_emprunt") == id_emprunt:
                self._list_emprunt.pop(i)
                return True
        return False
    
    def get_emprunt(self, id_emprunt: str) -> Optional[Dict]:
        """
        Récupère un emprunt par son ID.
        
        Args:
            id_emprunt (str): Identifiant de l'emprunt
            
        Returns:
            Dict ou None: L'emprunt trouvé ou None
        """
        for emprunt in self._list_emprunt:
            if emprunt.get("id_emprunt") == id_emprunt:
                return emprunt.copy()
        return None
    
    def to_dict(self) -> dict:
        """
        Convertit l'utilisateur en dictionnaire pour la sérialisation.
        
        Returns:
            dict: Dictionnaire contenant toutes les informations de l'utilisateur
        """
        return {
            "id_user": self._id_user,
            "nom": self._nom,
            "type_utilisateur": self._type_utilisateur.value,
            "nombre_emprunt_total": self._nombre_emprunt_total,
            "list_emprunt": self._list_emprunt.copy()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """
        Crée un objet User à partir d'un dictionnaire.
        
        Args:
            data (dict): Dictionnaire contenant les données de l'utilisateur
            
        Returns:
            User: Instance de User créée à partir des données
        """
        type_user = UserType(data.get("type_utilisateur", "Etudiant"))
        
        # Crée l'instance appropriée selon le type
        if type_user == UserType.ETUDIANT:
            return Etudiant(
                nom=data.get("nom", ""),
                id_user=data.get("id_user"),
                nombre_emprunt_total=data.get("nombre_emprunt_total", 0),
                list_emprunt=data.get("list_emprunt", [])
            )
        elif type_user == UserType.ENSEIGNANT:
            return Enseignant(
                nom=data.get("nom", ""),
                id_user=data.get("id_user"),
                nombre_emprunt_total=data.get("nombre_emprunt_total", 0),
                list_emprunt=data.get("list_emprunt", [])
            )
        elif type_user == UserType.PERSONNEL_ADMIN:
            return PersonnelAdmin(
                nom=data.get("nom", ""),
                id_user=data.get("id_user"),
                nombre_emprunt_total=data.get("nombre_emprunt_total", 0),
                list_emprunt=data.get("list_emprunt", [])
            )
        else:
            raise ValueError(f"Type d'utilisateur inconnu: {type_user}")
    
    def __str__(self) -> str:
        """Représentation string de l'utilisateur."""
        return f"Utilisateur [{self._id_user}] - {self._nom} - {self._type_utilisateur.value} - Emprunts: {self.nombre_emprunts_en_cours()}/{self.limite_emprunts}"
    
    def __repr__(self) -> str:
        """Représentation technique de l'utilisateur."""
        return f"{self.__class__.__name__}(id_user='{self._id_user}', type_utilisateur={self._type_utilisateur})"
    
    def __eq__(self, other) -> bool:
        """Compare deux utilisateurs par leur ID."""
        if not isinstance(other, User):
            return False
        return self._id_user == other._id_user
    
    def __hash__(self) -> int:
        """Permet d'utiliser User comme clé de dictionnaire."""
        return hash(self._id_user)


class Etudiant(User):
    """
    Classe représentant un étudiant.
    Limite d'emprunts : 4
    """
    
    def __init__(
        self,
        nom: str,
        id_user: Optional[str] = None,
        nombre_emprunt_total: int = 0,
        list_emprunt: Optional[List[Dict]] = None
    ):
        """Initialise un étudiant."""
        super().__init__(
            type_utilisateur=UserType.ETUDIANT,
            nom=nom,
            id_user=id_user,
            nombre_emprunt_total=nombre_emprunt_total,
            list_emprunt=list_emprunt
        )
    
    @property
    def limite_emprunts(self) -> int:
        """Retourne la limite d'emprunts pour un étudiant (4)."""
        return LIMITE_EMPRUNTS_ETUDIANT


class Enseignant(User):
    """
    Classe représentant un enseignant.
    Limite d'emprunts : 6
    """
    
    def __init__(
        self,
        nom: str,
        id_user: Optional[str] = None,
        nombre_emprunt_total: int = 0,
        list_emprunt: Optional[List[Dict]] = None
    ):
        """Initialise un enseignant."""
        super().__init__(
            type_utilisateur=UserType.ENSEIGNANT,
            nom=nom,
            id_user=id_user,
            nombre_emprunt_total=nombre_emprunt_total,
            list_emprunt=list_emprunt
        )
    
    @property
    def limite_emprunts(self) -> int:
        """Retourne la limite d'emprunts pour un enseignant (6)."""
        return LIMITE_EMPRUNTS_ENSEIGNANT


class PersonnelAdmin(User):
    """
    Classe représentant un personnel administratif.
    Limite d'emprunts : 0 (ne peut pas emprunter)
    """
    
    def __init__(
        self,
        nom: str,
        id_user: Optional[str] = None,
        nombre_emprunt_total: int = 0,
        list_emprunt: Optional[List[Dict]] = None
    ):
        """Initialise un personnel administratif."""
        super().__init__(
            type_utilisateur=UserType.PERSONNEL_ADMIN,
            nom=nom,
            id_user=id_user,
            nombre_emprunt_total=nombre_emprunt_total,
            list_emprunt=list_emprunt
        )
    
    @property
    def limite_emprunts(self) -> int:
        """Retourne la limite d'emprunts pour un personnel admin (0)."""
        return LIMITE_EMPRUNTS_PERSONNEL_ADMIN
