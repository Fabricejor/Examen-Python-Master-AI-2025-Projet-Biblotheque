"""
Service de journalisation (logging) des actions de l'application.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """
    Service de journalisation pour enregistrer les actions dans des fichiers de log.
    """
    
    @staticmethod
    def get_log_path(directory: str, log_filename: str) -> Path:
        """
        Retourne le chemin absolu d'un fichier de log.
        
        Args:
            directory (str): Nom du sous-dossier (ex: 'users', 'books')
            log_filename (str): Nom du fichier de log (ex: 'user.log')
            
        Returns:
            Path: Chemin complet du fichier de log
        """
        base_path = Path(__file__).parent.parent / "files"
        return base_path / directory / log_filename
    
    @staticmethod
    def log_action(
        directory: str,
        log_filename: str,
        action: str,
        details: Optional[str] = None
    ) -> bool:
        """
        Enregistre une action dans un fichier de log.
        
        Args:
            directory (str): Nom du sous-dossier (ex: 'users')
            log_filename (str): Nom du fichier de log (ex: 'user.log')
            action (str): Description de l'action effectuée
            details (str, optional): Détails supplémentaires
            
        Returns:
            bool: True si l'écriture a réussi, False sinon
        """
        try:
            log_path = Logger.get_log_path(directory, log_filename)
            
            # Crée le dossier s'il n'existe pas
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Formate le message de log
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            message = f"[{timestamp}] {action}"
            
            if details:
                message += f" - {details}"
            
            message += "\n"
            
            # Écrit dans le fichier (mode append)
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(message)
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'écriture du log: {e}")
            return False
    
    @staticmethod
    def log_user_action(action: str, details: Optional[str] = None) -> bool:
        """
        Enregistre une action utilisateur dans user.log.
        
        Args:
            action (str): Description de l'action (ex: "Ajout d'utilisateur")
            details (str, optional): Détails supplémentaires (ex: "ID: userAb123, Nom: Jean Dupont")
            
        Returns:
            bool: True si l'écriture a réussi
        """
        return Logger.log_action("users", "user.log", action, details)
    
    @staticmethod
    def log_book_action(action: str, details: Optional[str] = None) -> bool:
        """
        Enregistre une action livre dans book.log.
        
        Args:
            action (str): Description de l'action (ex: "Ajout de livre")
            details (str, optional): Détails supplémentaires (ex: "ISBN: Ab123, Titre: Le Livre")
            
        Returns:
            bool: True si l'écriture a réussi
        """
        return Logger.log_action("books", "book.log", action, details)
    
    @staticmethod
    def log_loan_action(action: str, details: Optional[str] = None) -> bool:
        """
        Enregistre une action emprunt dans loans.log.
        
        Args:
            action (str): Description de l'action (ex: "Emprunt de livre")
            details (str, optional): Détails supplémentaires (ex: "ID: empruntAb123, ISBN: dw863")
            
        Returns:
            bool: True si l'écriture a réussi
        """
        return Logger.log_action("loans", "loans.log", action, details)
    
    @staticmethod
    def log_reservation_action(action: str, details: Optional[str] = None) -> bool:
        """
        Enregistre une action réservation dans reservation.log.
        
        Args:
            action (str): Description de l'action (ex: "Réservation de livre")
            details (str, optional): Détails supplémentaires (ex: "ID: reservationAb123, ISBN: dw863")
            
        Returns:
            bool: True si l'écriture a réussi
        """
        return Logger.log_action("reservations", "reservation.log", action, details)
