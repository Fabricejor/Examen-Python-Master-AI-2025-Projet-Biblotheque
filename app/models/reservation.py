"""
Modèle représentant une réservation de livre.
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict
from pathlib import Path
from app.utils.validators import generate_id, format_date, parse_date, get_current_date
from app.models.book import Book, BookStatus
from app.models.user import User
from app.utils.constants import DUREE_EMPRUNT_DEFAUT


class Reservation:
    """
    Classe représentant une réservation de livre.
    
    La file d'attente est gérée automatiquement : les réservations sont organisées
    par livre (ISBN) et ordonnées par date de réservation.
    
    Attributs:
        id_reservation (str): Identifiant unique de la réservation (format: reservationXX000)
        date_reservation (str): Date de la réservation
        id_livre (str): ISBN du livre réservé
        titre_livre (str): Titre du livre réservé
        id_utilisateur (str): ID de l'utilisateur qui a réservé
        nom_utilisateur (str): Nom de l'utilisateur
        date_emprunt (str): Date souhaitée pour l'emprunt
        date_retour_prevue (str): Date de retour prévue pour l'emprunt
        position_file (int): Position dans la file d'attente pour ce livre
    """
    
    # Dictionnaire pour stocker les files d'attente par livre (ISBN -> liste de réservations)
    _files_attente: Dict[str, List['Reservation']] = {}
    
    # Chemin du fichier de log des réservations
    LOG_FILE_PATH = Path(__file__).parent.parent / "files" / "reservations" / "reservation.log"
    
    def __init__(
        self,
        id_livre: str,
        titre_livre: str,
        id_utilisateur: str,
        nom_utilisateur: str,
        date_emprunt: Optional[str] = None,
        date_retour_prevue: Optional[str] = None,
        id_reservation: Optional[str] = None,
        date_reservation: Optional[str] = None,
        position_file: Optional[int] = None
    ):
        """
        Initialise une nouvelle réservation.
        
        Args:
            id_livre (str): ISBN du livre à réserver
            titre_livre (str): Titre du livre
            id_utilisateur (str): ID de l'utilisateur
            nom_utilisateur (str): Nom de l'utilisateur
            date_emprunt (str, optional): Date souhaitée pour l'emprunt. Si None, calculée automatiquement
            date_retour_prevue (str, optional): Date de retour prévue. Si None, calculée automatiquement
            id_reservation (str, optional): ID de la réservation. Si None, généré automatiquement
            date_reservation (str, optional): Date de réservation. Si None, utilise la date actuelle
            position_file (int, optional): Position dans la file. Si None, calculée automatiquement
        """
        # Génère un ID unique avec préfixe "reservation" si non fourni
        self._id_reservation = id_reservation if id_reservation else generate_id("reservation")
        
        # Utilise la date actuelle si non fournie
        if date_reservation is None:
            self._date_reservation = get_current_date()
        else:
            self._date_reservation = date_reservation
        
        self._id_livre = id_livre
        self._titre_livre = titre_livre
        self._id_utilisateur = id_utilisateur
        self._nom_utilisateur = nom_utilisateur
        
        # Calcule les dates d'emprunt si non fournies
        if date_emprunt is None:
            # Par défaut, la date d'emprunt est la date actuelle
            self._date_emprunt = self._date_reservation
        else:
            self._date_emprunt = date_emprunt
        
        if date_retour_prevue is None:
            # Calcule la date de retour prévue (30 jours après la date d'emprunt)
            date_emp = parse_date(self._date_emprunt)
            date_retour = date_emp + timedelta(days=DUREE_EMPRUNT_DEFAUT)
            self._date_retour_prevue = format_date(date_retour)
        else:
            self._date_retour_prevue = date_retour_prevue
        
        # Position dans la file (sera calculée lors de l'ajout à la file)
        self._position_file = position_file if position_file is not None else 0
    
    # Propriétés (getters) avec encapsulation
    @property
    def id_reservation(self) -> str:
        """Retourne l'ID de la réservation."""
        return self._id_reservation
    
    @property
    def date_reservation(self) -> str:
        """Retourne la date de réservation."""
        return self._date_reservation
    
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
    def date_emprunt(self) -> str:
        """Retourne la date d'emprunt souhaitée."""
        return self._date_emprunt
    
    @property
    def date_retour_prevue(self) -> str:
        """Retourne la date de retour prévue."""
        return self._date_retour_prevue
    
    @property
    def position_file(self) -> int:
        """Retourne la position dans la file d'attente."""
        return self._position_file
    
    @position_file.setter
    def position_file(self, value: int):
        """Modifie la position dans la file d'attente."""
        self._position_file = max(0, value)
    
    @classmethod
    def get_file_attente(cls, id_livre: str) -> List['Reservation']:
        """
        Retourne la file d'attente pour un livre donné.
        
        Args:
            id_livre (str): ISBN du livre
            
        Returns:
            List[Reservation]: Liste des réservations pour ce livre, triée par date
        """
        return cls._files_attente.get(id_livre, []).copy()
    
    @classmethod
    def ajouter_a_file(cls, reservation: 'Reservation'):
        """
        Ajoute une réservation à la file d'attente du livre correspondant.
        
        Args:
            reservation (Reservation): La réservation à ajouter
        """
        id_livre = reservation._id_livre
        
        # Initialise la file si elle n'existe pas
        if id_livre not in cls._files_attente:
            cls._files_attente[id_livre] = []
        
        # Vérifie que la réservation n'est pas déjà dans la file
        if reservation not in cls._files_attente[id_livre]:
            cls._files_attente[id_livre].append(reservation)
            # Trie par date de réservation (plus ancienne en premier)
            cls._files_attente[id_livre].sort(key=lambda r: r._date_reservation)
            # Met à jour les positions
            cls._mettre_a_jour_positions(id_livre)
    
    @classmethod
    def retirer_de_file(cls, reservation: 'Reservation') -> bool:
        """
        Retire une réservation de la file d'attente.
        
        Args:
            reservation (Reservation): La réservation à retirer
            
        Returns:
            bool: True si la réservation a été retirée, False sinon
        """
        id_livre = reservation._id_livre
        
        if id_livre in cls._files_attente and reservation in cls._files_attente[id_livre]:
            cls._files_attente[id_livre].remove(reservation)
            cls._mettre_a_jour_positions(id_livre)
            return True
        return False
    
    @classmethod
    def _mettre_a_jour_positions(cls, id_livre: str):
        """
        Met à jour les positions dans la file d'attente pour un livre donné.
        
        Args:
            id_livre (str): ISBN du livre
        """
        if id_livre in cls._files_attente:
            for index, reservation in enumerate(cls._files_attente[id_livre], start=1):
                reservation._position_file = index
    
    @classmethod
    def get_prochaine_reservation(cls, id_livre: str) -> Optional['Reservation']:
        """
        Retourne la prochaine réservation dans la file d'attente pour un livre.
        
        Args:
            id_livre (str): ISBN du livre
            
        Returns:
            Reservation ou None: La prochaine réservation (position 1) ou None si la file est vide
        """
        file_attente = cls.get_file_attente(id_livre)
        return file_attente[0] if file_attente else None
    
    def reserver(self, livre: Book, utilisateur: User) -> bool:
        """
        Effectue la réservation d'un livre et l'associe à un utilisateur.
        Ajoute la réservation à la file d'attente.
        
        Args:
            livre (Book): Le livre à réserver
            utilisateur (User): L'utilisateur qui fait la réservation
            
        Returns:
            bool: True si la réservation a réussi, False sinon
            
        Raises:
            ValueError: Si le livre est déjà disponible ou si l'utilisateur a déjà réservé ce livre
        """
        # Vérifie que l'ISBN correspond
        if livre.isbn != self._id_livre:
            raise ValueError("L'ISBN du livre ne correspond pas à la réservation.")
        
        # Vérifie que l'ID utilisateur correspond
        if utilisateur.id_user != self._id_utilisateur:
            raise ValueError("L'ID utilisateur ne correspond pas à la réservation.")
        
        # Si le livre est disponible, on ne peut pas le réserver
        if livre.est_disponible():
            raise ValueError(f"Le livre '{livre.titre}' est disponible. Veuillez l'emprunter directement.")
        
        # Vérifie si l'utilisateur n'a pas déjà une réservation pour ce livre
        file_attente = self.get_file_attente(self._id_livre)
        for reservation in file_attente:
            if reservation._id_utilisateur == self._id_utilisateur:
                raise ValueError(f"L'utilisateur {utilisateur.nom} a déjà une réservation pour ce livre.")
        
        # Ajoute à la file d'attente
        self.ajouter_a_file(self)
        
        # Met à jour le statut du livre s'il n'est pas déjà réservé
        if livre.statut != BookStatus.RESERVE:
            livre.statut = BookStatus.RESERVE
        
        return True
    
    def annuler_reservation(self, livre: Book) -> bool:
        """
        Annule une réservation et la retire de la file d'attente.
        
        Args:
            livre (Book): Le livre concerné
            
        Returns:
            bool: True si l'annulation a réussi, False sinon
        """
        # Retire de la file d'attente
        if self.retirer_de_file(self):
            # Si la file est vide, remet le livre en statut approprié
            file_attente = self.get_file_attente(self._id_livre)
            if not file_attente:
                if livre.exemplaire_disponible > 0:
                    livre.statut = BookStatus.DISPONIBLE
                elif livre.exemplaire_disponible == 0:
                    livre.statut = BookStatus.EMPRUNTE
            return True
        return False
    
    @classmethod
    def notifier_disponibilite(cls, livre: Book) -> bool:
        """
        Notifie la première personne dans la file d'attente lorsqu'un livre devient disponible.
        Écrit la notification dans le fichier reservation.log.
        
        Args:
            livre (Book): Le livre qui est devenu disponible
            
        Returns:
            bool: True si une notification a été envoyée, False sinon
        """
        # Récupère la prochaine réservation
        prochaine_reservation = cls.get_prochaine_reservation(livre.isbn)
        
        if not prochaine_reservation:
            return False
        
        # Crée le message de notification
        message = (
            f"[{format_date(datetime.now())} {datetime.now().strftime('%H:%M:%S')}] "
            f"NOTIFICATION: Le livre '{livre.titre}' (ISBN: {livre.isbn}) est maintenant disponible.\n"
            f"Réservation ID: {prochaine_reservation._id_reservation}\n"
            f"Utilisateur: {prochaine_reservation._nom_utilisateur} (ID: {prochaine_reservation._id_utilisateur})\n"
            f"Position dans la file: {prochaine_reservation._position_file}\n"
            f"Date de réservation: {prochaine_reservation._date_reservation}\n"
            f"{'='*80}\n\n"
        )
        
        # Écrit dans le fichier de log
        try:
            # Crée le dossier s'il n'existe pas
            cls.LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
            
            # Écrit le message dans le fichier
            with open(cls.LOG_FILE_PATH, 'a', encoding='utf-8') as f:
                f.write(message)
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'écriture de la notification: {e}")
            return False
    
    def to_dict(self) -> dict:
        """
        Convertit la réservation en dictionnaire pour la sérialisation.
        
        Returns:
            dict: Dictionnaire contenant toutes les informations de la réservation
        """
        return {
            "id_reservation": self._id_reservation,
            "date_reservation": self._date_reservation,
            "id_livre": self._id_livre,
            "titre_livre": self._titre_livre,
            "id_utilisateur": self._id_utilisateur,
            "nom_utilisateur": self._nom_utilisateur,
            "date_emprunt": self._date_emprunt,
            "date_retour_prevue": self._date_retour_prevue,
            "position_file": self._position_file
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Reservation':
        """
        Crée un objet Reservation à partir d'un dictionnaire.
        
        Args:
            data (dict): Dictionnaire contenant les données de la réservation
            
        Returns:
            Reservation: Instance de Reservation créée à partir des données
        """
        reservation = cls(
            id_reservation=data.get("id_reservation"),
            date_reservation=data.get("date_reservation"),
            id_livre=data.get("id_livre", ""),
            titre_livre=data.get("titre_livre", ""),
            id_utilisateur=data.get("id_utilisateur", ""),
            nom_utilisateur=data.get("nom_utilisateur", ""),
            date_emprunt=data.get("date_emprunt"),
            date_retour_prevue=data.get("date_retour_prevue"),
            position_file=data.get("position_file")
        )
        
        # Ajoute à la file d'attente si nécessaire
        if reservation._position_file > 0:
            cls.ajouter_a_file(reservation)
        
        return reservation
    
    def __str__(self) -> str:
        """Représentation string de la réservation."""
        return (
            f"Réservation [{self._id_reservation}] - {self._titre_livre} "
            f"par {self._nom_utilisateur} - Position: {self._position_file}"
        )
    
    def __repr__(self) -> str:
        """Représentation technique de la réservation."""
        return (
            f"Reservation(id_reservation='{self._id_reservation}', "
            f"id_livre='{self._id_livre}', id_utilisateur='{self._id_utilisateur}')"
        )
    
    def __eq__(self, other) -> bool:
        """Compare deux réservations par leur ID."""
        if not isinstance(other, Reservation):
            return False
        return self._id_reservation == other._id_reservation
    
    def __hash__(self) -> int:
        """Permet d'utiliser Reservation comme clé de dictionnaire."""
        return hash(self._id_reservation)
