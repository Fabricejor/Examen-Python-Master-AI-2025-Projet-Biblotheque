"""
Service de gestion des réservations.
"""

from typing import List, Optional
from app.models.reservation import Reservation
from app.models.book import Book
from app.models.user import User
from app.services.file_manager import FileManager


class ReservationService:
    """
    Service contenant la logique métier pour la gestion des réservations.
    """
    
    DIRECTORY = "reservations"
    FILENAME = "reservations.json"
    
    def __init__(self):
        self.reservations: List[Reservation] = []
        self._load_reservations()
    
    def _load_reservations(self):
        """Charge les réservations depuis le fichier JSON."""
        data = FileManager.load_data(self.DIRECTORY, self.FILENAME)
        self.reservations = [Reservation.from_dict(d) for d in data]
        
        # Reconstruit les files d'attente en mémoire
        # Note: Reservation.from_dict appelle déjà ajouter_a_file si position_file > 0
        pass
    
    def _save_reservations(self):
        """Sauvegarde les réservations dans le fichier JSON."""
        data = [r.to_dict() for r in self.reservations]
        FileManager.save_data(self.DIRECTORY, self.FILENAME, data)
    
    def lister_reservations(self) -> List[Reservation]:
        """Retourne la liste de toutes les réservations."""
        return self.reservations
    
    def lister_reservations_pour_livre(self, isbn: str) -> List[Reservation]:
        """Retourne la file d'attente pour un livre."""
        # On utilise la méthode de classe du modèle qui gère le tri
        return Reservation.get_file_attente(isbn)
        
    def reserver_livre(self, livre: Book, utilisateur: User) -> Reservation:
        """
        Effectue une réservation de livre.
        
        Args:
            livre (Book): Le livre à réserver
            utilisateur (User): L'utilisateur qui réserve
            
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
            nom_utilisateur=utilisateur.nom
        )
        
        # Tente d'effectuer la réservation
        if reservation.reserver(livre, utilisateur):
            self.reservations.append(reservation)
            self._save_reservations()
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
            return True
            
        return False

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
