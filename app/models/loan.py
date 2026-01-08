"""
Modèle représentant un emprunt de livre.
"""

from datetime import datetime, timedelta
from typing import Optional
from app.utils.validators import generate_id, format_date, parse_date, get_current_date
from app.models.book import Book, BookStatus
from app.models.user import User
from app.utils.constants import DUREE_EMPRUNT_DEFAUT


class Loan:
    """
    Classe représentant un emprunt de livre.
    
    Attributs:
        id_emprunt (str): Identifiant unique de l'emprunt (format: empruntXX000)
        date_emprunt (str): Date de l'emprunt
        date_retour_prevue (str): Date de retour prévue
        id_livre (str): ISBN du livre emprunté
        titre_livre (str): Titre du livre emprunté
        id_utilisateur (str): ID de l'utilisateur qui a emprunté
        nom_utilisateur (str): Nom de l'utilisateur
        penalites (float): Montant des pénalités si retard
    """
    
    def __init__(
        self,
        id_livre: str,
        titre_livre: str,
        id_utilisateur: str,
        nom_utilisateur: str,
        date_emprunt: Optional[str] = None,
        date_retour_prevue: Optional[str] = None,
        id_emprunt: Optional[str] = None,
        penalites: float = 0.0
    ):
        """
        Initialise un nouvel emprunt.
        
        Args:
            id_livre (str): ISBN du livre emprunté
            titre_livre (str): Titre du livre
            id_utilisateur (str): ID de l'utilisateur
            nom_utilisateur (str): Nom de l'utilisateur
            date_emprunt (str, optional): Date d'emprunt. Si None, utilise la date actuelle
            date_retour_prevue (str, optional): Date de retour prévue. Si None, calcule automatiquement
            id_emprunt (str, optional): ID de l'emprunt. Si None, généré automatiquement
            penalites (float, optional): Montant des pénalités. Par défaut: 0.0
        """
        # Génère un ID unique avec préfixe "emprunt" si non fourni
        self._id_emprunt = id_emprunt if id_emprunt else generate_id("emprunt")
        
        # Utilise la date actuelle si non fournie (depuis variable d'environnement ou date système)
        if date_emprunt is None:
            self._date_emprunt = get_current_date()
        else:
            self._date_emprunt = date_emprunt
        
        # Calcule la date de retour prévue (30 jours par défaut)
        if date_retour_prevue is None:
            date_emp = parse_date(self._date_emprunt)
            date_retour = date_emp + timedelta(days=DUREE_EMPRUNT_DEFAUT)
            self._date_retour_prevue = format_date(date_retour)
        else:
            self._date_retour_prevue = date_retour_prevue
        
        self._id_livre = id_livre
        self._titre_livre = titre_livre
        self._id_utilisateur = id_utilisateur
        self._nom_utilisateur = nom_utilisateur
        self._penalites = max(0.0, penalites)  # S'assure que c'est >= 0
    
    # Propriétés (getters) avec encapsulation
    @property
    def id_emprunt(self) -> str:
        """Retourne l'ID de l'emprunt."""
        return self._id_emprunt
    
    @property
    def date_emprunt(self) -> str:
        """Retourne la date d'emprunt."""
        return self._date_emprunt
    
    @property
    def date_retour_prevue(self) -> str:
        """Retourne la date de retour prévue."""
        return self._date_retour_prevue
    
    @property
    def id_livre(self) -> str:
        """Retourne l'ISBN du livre."""
        return self._id_livre
    
    @property
    def titre_livre(self) -> str:
        """Retourne le titre du livre."""
        return self._titre_livre
    
    @property
    def id_utilisateur(self) -> str:
        """Retourne l'ID de l'utilisateur."""
        return self._id_utilisateur
    
    @property
    def nom_utilisateur(self) -> str:
        """Retourne le nom de l'utilisateur."""
        return self._nom_utilisateur
    
    @property
    def penalites(self) -> float:
        """Retourne le montant des pénalités."""
        return self._penalites
    
    def verification_disponibilite(self, livre: Book) -> bool:
        """
        Vérifie si le livre est disponible pour l'emprunt.
        
        Args:
            livre (Book): Le livre à vérifier
            
        Returns:
            bool: True si le livre est disponible, False sinon
        """
        if livre is None:
            return False
        
        # Vérifie que l'ISBN correspond
        if livre.isbn != self._id_livre:
            return False
        
        # Vérifie la disponibilité
        return livre.est_disponible() and livre.exemplaire_disponible > 0
    
    def emprunter(self, livre: Book, utilisateur: User) -> bool:
        """
        Effectue l'emprunt d'un livre et l'attribue à un utilisateur.
        
        Args:
            livre (Book): Le livre à emprunter
            utilisateur (User): L'utilisateur qui emprunte
            
        Returns:
            bool: True si l'emprunt a réussi, False sinon
            
        Raises:
            ValueError: Si le livre n'est pas disponible ou si l'utilisateur ne peut pas emprunter
        """
        # Vérifie la disponibilité
        if not self.verification_disponibilite(livre):
            raise ValueError(f"Le livre '{livre.titre}' n'est pas disponible.")
        
        # Vérifie que l'utilisateur peut emprunter
        if not utilisateur.peut_emprunter():
            raise ValueError(
                f"L'utilisateur {utilisateur.nom} a atteint sa limite d'emprunts "
                f"({utilisateur.nombre_emprunts_en_cours()}/{utilisateur.limite_emprunts})."
            )
        
        # Effectue l'emprunt
        try:
            # Décrémente les exemplaires disponibles
            livre.decrementer_exemplaire_disponible()
            
            # Incrémente le compteur d'emprunts du livre
            livre.incrementer_compteur()
            
            # Ajoute l'emprunt à la liste de l'utilisateur
            utilisateur.ajouter_emprunt(
                id_emprunt=self._id_emprunt,
                date_emprunt=self._date_emprunt,
                date_retour_prevue=self._date_retour_prevue,
                titre_du_livre=self._titre_livre
            )
            
            return True
            
        except Exception as e:
            # En cas d'erreur, restaure l'état
            if livre.exemplaire_disponible < livre.nbre_exemplaire_total:
                livre.incrementer_exemplaire_disponible()
            raise ValueError(f"Erreur lors de l'emprunt: {str(e)}")
    
    def retourner(self, livre: Book, utilisateur: User) -> bool:
        """
        Retourne un livre emprunté et le rend disponible.
        
        Args:
            livre (Book): Le livre à retourner
            utilisateur (User): L'utilisateur qui retourne le livre
            
        Returns:
            bool: True si le retour a réussi, False sinon
        """
        if livre is None or utilisateur is None:
            return False
        
        # Vérifie que l'ISBN correspond
        if livre.isbn != self._id_livre:
            return False
        
        # Retire l'emprunt de la liste de l'utilisateur
        if not utilisateur.retirer_emprunt(self._id_emprunt):
            return False
        
        # Incrémente les exemplaires disponibles
        livre.incrementer_exemplaire_disponible()
        
        # Met à jour le statut si nécessaire
        if livre.exemplaire_disponible > 0 and livre.statut == BookStatus.EMPRUNTE:
            livre.statut = BookStatus.DISPONIBLE
        
        return True
    
    def detecter_retard(self) -> int:
        """
        Détecte et calcule le nombre de jours de retard.
        
        Returns:
            int: Nombre de jours de retard (0 si pas de retard)
        """
        # Récupère la date actuelle depuis la variable d'environnement ou date système
        date_actuelle_str = get_current_date()
        date_actuelle = parse_date(date_actuelle_str)
        
        date_retour_prevue = parse_date(self._date_retour_prevue)
        
        # Calcule la différence
        difference = (date_actuelle - date_retour_prevue).days
        
        # Retourne 0 si pas de retard, sinon le nombre de jours de retard
        return max(0, difference)
    
    def calculer_penalites(self, taux_par_jour: float = 50) -> float:
        """
        Calcule les pénalités en fonction du retard.
        
        Args:
            taux_par_jour (float): Montant de la pénalité par jour de retard. Par défaut: 50
            
        Returns:
            float: Montant total des pénalités
        """
        jours_retard = self.detecter_retard()
        self._penalites = jours_retard * taux_par_jour
        return self._penalites
    
    def to_dict(self) -> dict:
        """
        Convertit l'emprunt en dictionnaire pour la sérialisation.
        
        Returns:
            dict: Dictionnaire contenant toutes les informations de l'emprunt
        """
        return {
            "id_emprunt": self._id_emprunt,
            "date_emprunt": self._date_emprunt,
            "date_retour_prevue": self._date_retour_prevue,
            "id_livre": self._id_livre,
            "titre_livre": self._titre_livre,
            "id_utilisateur": self._id_utilisateur,
            "nom_utilisateur": self._nom_utilisateur,
            "penalites": self._penalites
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Loan':
        """
        Crée un objet Loan à partir d'un dictionnaire.
        
        Args:
            data (dict): Dictionnaire contenant les données de l'emprunt
            
        Returns:
            Loan: Instance de Loan créée à partir des données
        """
        return cls(
            id_emprunt=data.get("id_emprunt"),
            date_emprunt=data.get("date_emprunt"),
            date_retour_prevue=data.get("date_retour_prevue"),
            id_livre=data.get("id_livre", ""),
            titre_livre=data.get("titre_livre", ""),
            id_utilisateur=data.get("id_utilisateur", ""),
            nom_utilisateur=data.get("nom_utilisateur", ""),
            penalites=data.get("penalites", 0.0)
        )
    
    def __str__(self) -> str:
        """Représentation string de l'emprunt."""
        retard = self.detecter_retard()
        ret_str = f"Emprunt [{self._id_emprunt}] - {self._titre_livre} par {self._nom_utilisateur}"
        if retard > 0:
            ret_str += f" - RETARD: {retard} jours"
        return ret_str
    
    def __repr__(self) -> str:
        """Représentation technique de l'emprunt."""
        return f"Loan(id_emprunt='{self._id_emprunt}', id_livre='{self._id_livre}', id_utilisateur='{self._id_utilisateur}')"
    
    def __eq__(self, other) -> bool:
        """Compare deux emprunts par leur ID."""
        if not isinstance(other, Loan):
            return False
        return self._id_emprunt == other._id_emprunt
    
    def __hash__(self) -> int:
        """Permet d'utiliser Loan comme clé de dictionnaire."""
        return hash(self._id_emprunt)
