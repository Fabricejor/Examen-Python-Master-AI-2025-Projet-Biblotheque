"""
Modèle représentant un livre de la bibliothèque.
"""

from enum import Enum
from typing import Optional
from app.utils.validators import generate_id #pour generer les id de type {prefix}XX000


class BookStatus(Enum):
    """Énumération des statuts possibles d'un livre."""
    DISPONIBLE = "disponible"
    EMPRUNTE = "emprunté"
    RESERVE = "réservé"
    PERDU = "perdu"
    ENDOMMAGE = "endommagé"


class Book:
    """
    Classe représentant un livre de la bibliothèque.
    
    Attributs:
        isbn (str): Identifiant unique du livre (format XX000)
        titre (str): Titre du livre
        auteur (str): Auteur du livre
        resume (str): Résumé du livre
        statut (BookStatus): Statut actuel du livre
        compteur_emprunt (int): Nombre de fois que le livre a été emprunté
    """
    
    def __init__(
        self,
        titre: str,
        auteur: str,
        resume: str,
        isbn: Optional[str] = None,
        statut: BookStatus = BookStatus.DISPONIBLE,
        compteur_emprunt: int = 0,
        nbre_exemplaire_total: int = 1,
        exemplaire_disponible: Optional[int] = None
    ):
        """
        Initialise un nouveau livre.
        
        Args:
            titre (str): Titre du livre
            auteur (str): Auteur du livre
            resume (str): Résumé du livre
            isbn (str, optional): ISBN du livre. Si non fourni, généré automatiquement
            statut (BookStatus, optional): Statut initial du livre. Par défaut: DISPONIBLE
            compteur_emprunt (int, optional): Nombre d'emprunts. Par défaut: 0
            nbre_exemplaire_total (int, optional): Nombre total d'exemplaires. Par défaut: 1
            exemplaire_disponible (int, optional): Nombre d'exemplaires disponibles. Si None, égal à nbre_exemplaire_total
        """
        # Génère un ISBN unique si non fourni
        self._isbn = isbn if isbn else generate_id()
        self._titre = titre
        self._auteur = auteur
        self._resume = resume
        self._statut = statut if isinstance(statut, BookStatus) else BookStatus(statut)
        self._compteur_emprunt = max(0, compteur_emprunt)  # S'assure que c'est >= 0
        self._nbre_exemplaire_total = max(1, nbre_exemplaire_total)  # Au moins 1 exemplaire
        self._exemplaire_disponible = exemplaire_disponible if exemplaire_disponible is not None else self._nbre_exemplaire_total
        # S'assure que exemplaire_disponible ne dépasse pas le total
        self._exemplaire_disponible = min(self._exemplaire_disponible, self._nbre_exemplaire_total)
    
    # Propriétés (getters) avec encapsulation
    @property
    def isbn(self) -> str:
        """Retourne l'ISBN du livre."""
        return self._isbn
    
    @property
    def titre(self) -> str:
        """Retourne le titre du livre."""
        return self._titre
    
    @property
    def auteur(self) -> str:
        """Retourne l'auteur du livre."""
        return self._auteur
    
    @property
    def resume(self) -> str:
        """Retourne le résumé du livre."""
        return self._resume
    
    @property
    def statut(self) -> BookStatus:
        """Retourne le statut du livre."""
        return self._statut
    
    @property
    def compteur_emprunt(self) -> int:
        """Retourne le nombre d'emprunts du livre."""
        return self._compteur_emprunt
    
    @property
    def nbre_exemplaire_total(self) -> int:
        """Retourne le nombre total d'exemplaires du livre."""
        return self._nbre_exemplaire_total
    
    @property
    def exemplaire_disponible(self) -> int:
        """Retourne le nombre d'exemplaires disponibles du livre."""
        return self._exemplaire_disponible
    
    # Setters avec validation
    @titre.setter
    def titre(self, value: str):
        """Modifie le titre du livre."""
        if not value or not value.strip():
            raise ValueError("Le titre ne peut pas être vide.")
        self._titre = value.strip()
    
    @auteur.setter
    def auteur(self, value: str):
        """Modifie l'auteur du livre."""
        if not value or not value.strip():
            raise ValueError("L'auteur ne peut pas être vide.")
        self._auteur = value.strip()
    
    @resume.setter
    def resume(self, value: str):
        """Modifie le résumé du livre."""
        if not value or not value.strip():
            raise ValueError("Le résumé ne peut pas être vide.")
        self._resume = value.strip()
    
    @statut.setter
    def statut(self, value):
        """Modifie le statut du livre."""
        if isinstance(value, str):
            try:
                self._statut = BookStatus(value.lower())
            except ValueError:
                raise ValueError(f"Statut invalide: {value}. Statuts valides: {[s.value for s in BookStatus]}")
        elif isinstance(value, BookStatus):
            self._statut = value
        else:
            raise TypeError("Le statut doit être de type BookStatus ou une chaîne de caractères.")
    
    def incrementer_compteur(self):
        """Incrémente le compteur d'emprunts."""
        self._compteur_emprunt += 1
    
    def reset_compteur(self):
        """Réinitialise le compteur d'emprunts à 0."""
        self._compteur_emprunt = 0
    
    def est_disponible(self) -> bool:
        """Vérifie si le livre est disponible."""
        return self._statut == BookStatus.DISPONIBLE and self._exemplaire_disponible > 0
    
    @nbre_exemplaire_total.setter
    def nbre_exemplaire_total(self, value: int):
        """Modifie le nombre total d'exemplaires."""
        if value < 1:
            raise ValueError("Le nombre d'exemplaires doit être au moins 1.")
        old_total = self._nbre_exemplaire_total
        self._nbre_exemplaire_total = value
        # Ajuste les exemplaires disponibles si nécessaire
        if self._exemplaire_disponible > value:
            self._exemplaire_disponible = value
        elif old_total > 0:
            # Ajuste proportionnellement les exemplaires disponibles
            ratio = self._exemplaire_disponible / old_total
            self._exemplaire_disponible = int(value * ratio)
    
    def incrementer_exemplaire_disponible(self):
        """Incrémente le nombre d'exemplaires disponibles (retour d'un livre)."""
        if self._exemplaire_disponible < self._nbre_exemplaire_total:
            self._exemplaire_disponible += 1
    
    def decrementer_exemplaire_disponible(self):
        """Décrémente le nombre d'exemplaires disponibles (emprunt d'un livre)."""
        if self._exemplaire_disponible > 0:
            self._exemplaire_disponible -= 1
            # Met à jour le statut si plus d'exemplaires disponibles
            if self._exemplaire_disponible == 0:
                self._statut = BookStatus.EMPRUNTE
    
    def est_emprunte(self) -> bool:
        """Vérifie si le livre est emprunté."""
        return self._statut == BookStatus.EMPRUNTE
    
    def est_reserve(self) -> bool:
        """Vérifie si le livre est réservé."""
        return self._statut == BookStatus.RESERVE
    
    def to_dict(self) -> dict:
        """
        Convertit le livre en dictionnaire pour la sérialisation.
        
        Returns:
            dict: Dictionnaire contenant toutes les informations du livre
        """
        return {
            "isbn": self._isbn,
            "titre": self._titre,
            "auteur": self._auteur,
            "resume": self._resume,
            "statut": self._statut.value,
            "compteur_emprunt": self._compteur_emprunt
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """
        Crée un objet Book à partir d'un dictionnaire.
        
        Args:
            data (dict): Dictionnaire contenant les données du livre
            
        Returns:
            Book: Instance de Book créée à partir des données
        """
        return cls(
            isbn=data.get("isbn"),
            titre=data.get("titre", ""),
            auteur=data.get("auteur", ""),
            resume=data.get("resume", ""),
            statut=BookStatus(data.get("statut", "disponible")),
            compteur_emprunt=data.get("compteur_emprunt", 0),
            nbre_exemplaire_total=data.get("nbre_exemplaire_total", 1),
            exemplaire_disponible=data.get("exemplaire_disponible")
        )
    
    def __str__(self) -> str:
        """Représentation string du livre."""
        return f"Livre [{self._isbn}] - {self._titre} par {self._auteur} - Statut: {self._statut.value}"
    
    def __repr__(self) -> str:
        """Représentation technique du livre."""
        return f"Book(isbn='{self._isbn}', titre='{self._titre}', auteur='{self._auteur}', statut={self._statut})"
    
    def __eq__(self, other) -> bool:
        """Compare deux livres par leur ISBN."""
        if not isinstance(other, Book):
            return False
        return self._isbn == other._isbn
    
    def __hash__(self) -> int:
        """Permet d'utiliser Book comme clé de dictionnaire."""
        return hash(self._isbn)
