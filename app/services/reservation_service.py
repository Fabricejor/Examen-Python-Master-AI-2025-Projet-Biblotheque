"""
Service de gestion des réservations.
"""

from typing import List, Optional
from app.models.reservation import Reservation
from app.models.loan import Loan
from app.models.book import Book
from app.models.user import User, UserType
from app.services.file_manager import FileManager
from app.services.logger import Logger
from app.services.book_service import BookService
from app.services.user_service import UserService
from app.services.loan_service import LoanService
from app.utils.validators import parse_date, get_current_date


class ReservationService:
    """
    Service contenant la logique métier pour la gestion des réservations.
    """
    
    DIRECTORY = "reservations"
    FILENAME = "reservation.json"  # Selon la demande : reservation.json
    LOG_FILENAME = "reservation.log"
    
    def __init__(self):
        self.reservations: List[Reservation] = []
        self._load_reservations()
    
    def _load_reservations(self):
        """Charge les réservations depuis le fichier JSON."""
        data = FileManager.load_data(self.DIRECTORY, self.FILENAME)
        self.reservations = [Reservation.from_dict(d) for d in data]
        
        # Reconstruit les files d'attente en mémoire
        for reservation in self.reservations:
            Reservation.ajouter_a_file(reservation)
        
        Logger.log_reservation_action("Chargement des réservations", f"{len(self.reservations)} réservation(s) chargée(s)")
    
    def _save_reservations(self):
        """Sauvegarde les réservations dans le fichier JSON."""
        data = [r.to_dict() for r in self.reservations]
        FileManager.save_data(self.DIRECTORY, self.FILENAME, data)
    
    def lister_reservations(self) -> List[Reservation]:
        """
        Retourne la liste de toutes les réservations.
        
        Returns:
            List[Reservation]: Liste de toutes les réservations
        """
        Logger.log_reservation_action("Liste de toutes les réservations", f"{len(self.reservations)} réservation(s)")
        return self.reservations
    
    def lister_livres_indisponibles(self, book_service: BookService) -> List[Book]:
        """
        Retourne la liste des livres indisponibles (exemplaire_disponible = 0).
        
        Args:
            book_service (BookService): Service de gestion des livres
            
        Returns:
            List[Book]: Liste des livres indisponibles
        """
        return [book for book in book_service.lister_livres() if book.exemplaire_disponible == 0]
    
    def lister_reservations_pour_livre(self, isbn: str) -> List[Reservation]:
        """Retourne la file d'attente pour un livre."""
        # On utilise la méthode de classe du modèle qui gère le tri
        return Reservation.get_file_attente(isbn)
        
    def reserver_livre(
        self, 
        livre: Book, 
        utilisateur: User,
        date_emprunt: Optional[str] = None,
        date_retour_prevue: Optional[str] = None
    ) -> Reservation:
        """
        Effectue une réservation de livre.
        
        Args:
            livre (Book): Le livre à réserver
            utilisateur (User): L'utilisateur qui réserve
            date_emprunt (str, optional): Date souhaitée pour l'emprunt (format JJ/MM/AAAA)
            date_retour_prevue (str, optional): Date de retour prévue (format JJ/MM/AAAA)
            
        Returns:
            Reservation: L'objet Reservation créé
            
        Raises:
            ValueError: Si la réservation est impossible
        """
        # Crée un nouvel objet réservation
        reservation = Reservation(
            id_livre=livre.isbn,
            titre_livre=livre.titre,
            id_utilisateur=utilisateur.id_user,
            nom_utilisateur=utilisateur.nom,
            date_emprunt=date_emprunt,
            date_retour_prevue=date_retour_prevue
        )
        
        # Tente d'effectuer la réservation
        if reservation.reserver(livre, utilisateur):
            self.reservations.append(reservation)
            self._save_reservations()
            
            Logger.log_reservation_action(
                "Réservation de livre",
                f"ID: {reservation.id_reservation}, ISBN: {livre.isbn}, Titre: {livre.titre}, "
                f"Utilisateur: {utilisateur.nom} ({utilisateur.id_user}), Position: {reservation.position_file}"
            )
            
            return reservation
            
        raise ValueError("La réservation a échoué.")
    
    def annuler_reservation(self, id_reservation: str, livre: Book) -> bool:
        """
        Annule une réservation.
        
        Args:
            id_reservation (str): ID de la réservation à annuler
            livre (Book): Livre concerné (pour mise à jour statut/file)
            
        Returns:
            bool: True si l'annulation a réussi
        """
        reservation_to_remove = None
        for res in self.reservations:
            if res.id_reservation == id_reservation:
                reservation_to_remove = res
                break
        
        if not reservation_to_remove:
            raise ValueError(f"Réservation {id_reservation} non trouvée.")
            
        if reservation_to_remove.annuler_reservation(livre):
            self.reservations.remove(reservation_to_remove)
            self._save_reservations()
            
            Logger.log_reservation_action(
                "Annulation de réservation",
                f"ID: {id_reservation}, ISBN: {livre.isbn}, Titre: {livre.titre}"
            )
            
            return True
            
        return False
    
    def transformer_reservation_en_emprunt(
        self,
        id_reservation: str,
        loan_service: LoanService,
        book_service: BookService,
        user_service: UserService
    ) -> bool:
        """
        Transforme une réservation en emprunt lorsque le livre devient disponible.
        
        Args:
            id_reservation (str): ID de la réservation à transformer
            loan_service (LoanService): Service de gestion des emprunts
            book_service (BookService): Service de gestion des livres
            user_service (UserService): Service de gestion des utilisateurs
            
        Returns:
            bool: True si la transformation a réussi
        """
        reservation = None
        for res in self.reservations:
            if res.id_reservation == id_reservation:
                reservation = res
                break
        
        if not reservation:
            return False
        
        livre = book_service.get_livre_by_isbn(reservation.id_livre)
        utilisateur = user_service.get_utilisateur_by_id(reservation.id_utilisateur)
        
        if not livre or not utilisateur:
            return False
        
        # Vérifie que le livre est disponible
        if not livre.est_disponible():
            return False
        
        # Crée l'emprunt avec les dates de la réservation
        try:
            emprunt = Loan(
                id_livre=livre.isbn,
                titre_livre=livre.titre,
                id_utilisateur=utilisateur.id_user,
                nom_utilisateur=utilisateur.nom,
                date_emprunt=reservation.date_emprunt,
                date_retour_prevue=reservation.date_retour_prevue
            )
            
            if emprunt.emprunter(livre, utilisateur):
                loan_service.loans.append(emprunt)
                loan_service._save_loans()
                book_service.mettre_a_jour_livre(livre)
                user_service.mettre_a_jour_utilisateur(utilisateur)
                
                # Annule la réservation
                reservation.annuler_reservation(livre)
                self.reservations.remove(reservation)
                self._save_reservations()
                
                Logger.log_reservation_action(
                    "Transformation réservation en emprunt",
                    f"ID Réservation: {id_reservation}, ID Emprunt: {emprunt.id_emprunt}"
                )
                
                return True
        except Exception:
            return False
        
        return False
    
    def verifier_et_notifier_disponibilites(
        self,
        book_service: BookService
    ) -> int:
        """
        Vérifie tous les livres devenus disponibles et notifie les réservations.
        
        Args:
            book_service (BookService): Service de gestion des livres
            
        Returns:
            int: Nombre de notifications envoyées
        """
        notifications = 0
        livres = book_service.lister_livres()
        
        for livre in livres:
            if livre.est_disponible():
                if Reservation.notifier_disponibilite(livre):
                    notifications += 1
        
        return notifications

    def traiter_retour_livre(self, livre: Book) -> bool:
        """
        Vérifie si un livre retourné a des réservations en attente et notifie le premier utilisateur.
        
        Args:
            livre (Book): Le livre qui vient d'être retourné
            
        Returns:
            bool: True si une notification a été envoyée
        """
        # Vérifie s'il y a des réservations pour ce livre
        file_attente = Reservation.get_file_attente(livre.isbn)
        
        if file_attente:
            # Notifie le premier de la liste
            if Reservation.notifier_disponibilite(livre):
                return True
                
        return False
