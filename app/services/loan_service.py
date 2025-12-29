"""
Service de gestion des emprunts.
"""

from typing import List, Optional
from app.models.loan import Loan
from app.models.book import Book
from app.models.user import User
from app.services.file_manager import FileManager


class LoanService:
    """
    Service contenant la logique métier pour la gestion des emprunts.
    """
    
    DIRECTORY = "loans"
    FILENAME = "loans.json"
    
    def __init__(self):
        self.loans: List[Loan] = []
        self._load_loans()
    
    def _load_loans(self):
        """Charge les emprunts depuis le fichier JSON."""
        data = FileManager.load_data(self.DIRECTORY, self.FILENAME)
        self.loans = [Loan.from_dict(d) for d in data]
    
    def _save_loans(self):
        """Sauvegarde les emprunts dans le fichier JSON."""
        data = [loan.to_dict() for loan in self.loans]
        FileManager.save_data(self.DIRECTORY, self.FILENAME, data)
    
    def lister_emprunts(self) -> List[Loan]:
        """Retourne la liste de tous les emprunts."""
        return self.loans
    
    def lister_emprunts_utilisateur(self, id_utilisateur: str) -> List[Loan]:
        """
        Retourne la liste des emprunts d'un utilisateur spécifique.
        
        Args:
            id_utilisateur (str): ID de l'utilisateur
            
        Returns:
            List[Loan]: Liste des emprunts de l'utilisateur
        """
        return [loan for loan in self.loans if loan.id_utilisateur == id_utilisateur]
    
    def emprunter_livre(self, livre: Book, utilisateur: User) -> Loan:
        """
        Effectue un emprunt de livre.
        
        Args:
            livre (Book): Le livre à emprunter
            utilisateur (User): L'utilisateur qui emprunte
            
        Returns:
            Loan: L'objet Loan créé si l'emprunt a réussi
            
        Raises:
            ValueError: Si l'emprunt est impossible (livre indisponible, limite atteinte, etc.)
        """
        # Crée un nouvel objet emprunt
        emprunt = Loan(
            id_livre=livre.isbn,
            titre_livre=livre.titre,
            id_utilisateur=utilisateur.id_user,
            nom_utilisateur=utilisateur.nom
        )
        
        # Tente d'effectuer l'emprunt (vérifie dispo et limites)
        # Note: Cela met à jour les objets livre et utilisateur en mémoire
        if emprunt.emprunter(livre, utilisateur):
            self.loans.append(emprunt)
            self._save_loans()
            return emprunt
            
        raise ValueError("L'emprunt a échoué pour une raison inconnue.")
    
    def retourner_livre(self, id_emprunt: str, livre: Book, utilisateur: User) -> bool:
        """
        Retourne un livre emprunté.
        
        Args:
            id_emprunt (str): ID de l'emprunt à clore
            livre (Book): Livre concerné (pour mise à jour stock)
            utilisateur (User): Utilisateur concerné (pour mise à jour liste emprunts)
            
        Returns:
            bool: True si le retour a réussi
            
        Raises:
            ValueError: Si l'emprunt n'est pas trouvé
        """
        # Trouve l'emprunt dans la liste locale
        loan_to_remove = None
        for loan in self.loans:
            if loan.id_emprunt == id_emprunt:
                loan_to_remove = loan
                break
        
        if not loan_to_remove:
            raise ValueError(f"Emprunt {id_emprunt} non trouvé.")
        
        # Effectue le retour (logique métier)
        if loan_to_remove.retourner(livre, utilisateur):
            # Supprime de la liste des emprunts actifs (historique à gérer si besoin, ici on supprime)
            # Pour un historique complet, on pourrait déplacer vers un fichier "history_loans.json"
            # Mais pour l'instant, on retire simplement de la liste active
            self.loans.remove(loan_to_remove)
            self._save_loans()
            return True
            
        return False

    def get_emprunt_by_id(self, id_emprunt: str) -> Optional[Loan]:
        """
        Récupère un emprunt par son ID.
        
        Args:
            id_emprunt (str): ID de l'emprunt
            
        Returns:
            Optional[Loan]: L'emprunt ou None
        """
        for loan in self.loans:
            if loan.id_emprunt == id_emprunt:
                return loan
        return None
