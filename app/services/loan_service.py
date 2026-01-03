"""
Service de gestion des emprunts.
"""

from typing import List, Optional
from app.models.loan import Loan
from app.models.book import Book, BookStatus
from app.models.user import User, UserType
from app.services.file_manager import FileManager
from app.services.logger import Logger
from app.services.book_service import BookService
from app.services.user_service import UserService
from app.utils.validators import parse_date, format_date


class LoanService:
    """
    Service contenant la logique métier pour la gestion des emprunts.
    """
    
    DIRECTORY = "loans"
    FILENAME = "loan.json"  # Selon la demande : loan.json
    LOG_FILENAME = "loans.log"
    
    def __init__(self):
        self.loans: List[Loan] = []
        self._load_loans()
    
    def _load_loans(self):
        """Charge les emprunts depuis le fichier JSON."""
        data = FileManager.load_data(self.DIRECTORY, self.FILENAME)
        self.loans = [Loan.from_dict(d) for d in data]
        Logger.log_loan_action("Chargement des emprunts", f"{len(self.loans)} emprunt(s) chargé(s)")
    
    def _save_loans(self):
        """Sauvegarde les emprunts dans le fichier JSON."""
        data = [loan.to_dict() for loan in self.loans]
        FileManager.save_data(self.DIRECTORY, self.FILENAME, data)
    
    def lister_emprunts(self) -> List[Loan]:
        """
        Retourne la liste de tous les emprunts.
        
        Returns:
            List[Loan]: Liste de tous les emprunts
        """
        Logger.log_loan_action("Liste de tous les emprunts", f"{len(self.loans)} emprunt(s)")
        return self.loans
    
    def lister_emprunts_en_cours(self) -> List[Loan]:
        """
        Retourne la liste de tous les emprunts en cours (non retournés).
        
        Returns:
            List[Loan]: Liste des emprunts en cours
        """
        return self.loans  # Tous les emprunts dans la liste sont en cours
    
    def lister_livres_disponibles(self, book_service: BookService) -> List[Book]:
        """
        Retourne la liste des livres ayant au moins 1 exemplaire disponible.
        
        Args:
            book_service (BookService): Service de gestion des livres
            
        Returns:
            List[Book]: Liste des livres disponibles
        """
        return [book for book in book_service.lister_livres() if book.exemplaire_disponible > 0]
    
    def lister_utilisateurs_emprunteurs(self, user_service: UserService) -> List[User]:
        """
        Retourne la liste des utilisateurs pouvant emprunter (Étudiant et Enseignant).
        
        Args:
            user_service (UserService): Service de gestion des utilisateurs
            
        Returns:
            List[User]: Liste des utilisateurs pouvant emprunter
        """
        all_users = user_service.lister_utilisateurs()
        return [u for u in all_users if u.type_utilisateur in [UserType.ETUDIANT, UserType.ENSEIGNANT]]
    
    def lister_emprunts_utilisateur(self, id_utilisateur: str) -> List[Loan]:
        """
        Retourne la liste des emprunts d'un utilisateur spécifique.
        
        Args:
            id_utilisateur (str): ID de l'utilisateur
            
        Returns:
            List[Loan]: Liste des emprunts de l'utilisateur
        """
        return [loan for loan in self.loans if loan.id_utilisateur == id_utilisateur]
    
    def lister_emprunts_livre(self, isbn: str) -> List[Loan]:
        """
        Retourne la liste des emprunts pour un livre spécifique.
        
        Args:
            isbn (str): ISBN du livre
            
        Returns:
            List[Loan]: Liste des emprunts du livre
        """
        return [loan for loan in self.loans if loan.id_livre == isbn]
    
    def emprunter_livre(
        self, 
        livre: Book, 
        utilisateur: User, 
        book_service: BookService,
        user_service: UserService,
        nbre_exemplaires: int = 1
    ) -> List[Loan]:
        """
        Effectue un emprunt de livre (peut emprunter plusieurs exemplaires).
        
        Args:
            livre (Book): Le livre à emprunter
            utilisateur (User): L'utilisateur qui emprunte
            book_service (BookService): Service de gestion des livres
            user_service (UserService): Service de gestion des utilisateurs
            nbre_exemplaires (int): Nombre d'exemplaires à emprunter (défaut: 1)
            
        Returns:
            List[Loan]: Liste des objets Loan créés
            
        Raises:
            ValueError: Si l'emprunt est impossible (livre indisponible, limite atteinte, etc.)
        """
        if nbre_exemplaires < 1:
            raise ValueError("Le nombre d'exemplaires doit être au moins 1.")
        
        # Vérifie que l'utilisateur peut emprunter autant d'exemplaires
        emprunts_possibles = utilisateur.limite_emprunts - utilisateur.nombre_emprunts_en_cours()
        if nbre_exemplaires > emprunts_possibles:
            raise ValueError(
                f"L'utilisateur ne peut emprunter que {emprunts_possibles} exemplaire(s) supplémentaire(s). "
                f"Limite: {utilisateur.limite_emprunts}, Emprunts en cours: {utilisateur.nombre_emprunts_en_cours()}"
            )
        
        # Vérifie que le livre a assez d'exemplaires disponibles
        if livre.exemplaire_disponible < nbre_exemplaires:
            raise ValueError(
                f"Le livre '{livre.titre}' n'a que {livre.exemplaire_disponible} exemplaire(s) disponible(s), "
                f"mais {nbre_exemplaires} exemplaire(s) sont demandés."
            )
        
        emprunts_crees = []
        
        # Crée un emprunt pour chaque exemplaire
        for i in range(nbre_exemplaires):
            emprunt = Loan(
                id_livre=livre.isbn,
                titre_livre=livre.titre,
                id_utilisateur=utilisateur.id_user,
                nom_utilisateur=utilisateur.nom
            )
            
            # Effectue l'emprunt (vérifie dispo et limites)
            if emprunt.emprunter(livre, utilisateur):
                self.loans.append(emprunt)
                emprunts_crees.append(emprunt)
            else:
                # En cas d'échec, annule les emprunts déjà créés
                for emp in emprunts_crees:
                    if emp in self.loans:
                        self.loans.remove(emp)
                raise ValueError(f"L'emprunt de l'exemplaire {i+1} a échoué.")
        
        # Sauvegarde et met à jour les services
        self._save_loans()
        book_service.mettre_a_jour_livre(livre)
        user_service.mettre_a_jour_utilisateur(utilisateur)
        
        # Logging
        Logger.log_loan_action(
            "Emprunt de livre",
            f"ISBN: {livre.isbn}, Titre: {livre.titre}, Utilisateur: {utilisateur.nom} ({utilisateur.id_user}), "
            f"Exemplaires: {nbre_exemplaires}, ID(s): {', '.join([e.id_emprunt for e in emprunts_crees])}"
        )
        
        return emprunts_crees
    
    def retourner_livre(
        self, 
        id_emprunt: str, 
        livre: Book, 
        utilisateur: User,
        book_service: BookService,
        user_service: UserService
    ) -> bool:
        """
        Retourne un livre emprunté.
        
        Args:
            id_emprunt (str): ID de l'emprunt à clore
            livre (Book): Livre concerné (pour mise à jour stock)
            utilisateur (User): Utilisateur concerné (pour mise à jour liste emprunts)
            book_service (BookService): Service de gestion des livres
            user_service (UserService): Service de gestion des utilisateurs
            
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
            # Supprime de la liste des emprunts actifs
            self.loans.remove(loan_to_remove)
            self._save_loans()
            
            # Met à jour les services
            book_service.mettre_a_jour_livre(livre)
            user_service.mettre_a_jour_utilisateur(utilisateur)
            
            # Logging
            Logger.log_loan_action(
                "Retour de livre",
                f"ID: {id_emprunt}, ISBN: {livre.isbn}, Titre: {livre.titre}, "
                f"Utilisateur: {utilisateur.nom} ({utilisateur.id_user})"
            )
            
            return True
            
        return False
    
    def renouveler_emprunt(self, id_emprunt: str, user_service: UserService) -> bool:
        """
        Renouvelle un emprunt en ajoutant 1 jour à la date de retour prévue.
        
        Args:
            id_emprunt (str): ID de l'emprunt à renouveler
            user_service (UserService): Service de gestion des utilisateurs
            
        Returns:
            bool: True si le renouvellement a réussi
        """
        emprunt = self.get_emprunt_by_id(id_emprunt)
        if not emprunt:
            return False
        
        # Ajoute 1 jour à la date de retour prévue
        from datetime import timedelta
        date_retour = parse_date(emprunt.date_retour_prevue)
        nouvelle_date = date_retour + timedelta(days=1)
        emprunt._date_retour_prevue = format_date(nouvelle_date)
        
        # Met à jour dans la liste de l'utilisateur
        utilisateur = user_service.get_utilisateur_by_id(emprunt.id_utilisateur)
        if utilisateur:
            emprunt_user = utilisateur.get_emprunt(id_emprunt)
            if emprunt_user:
                emprunt_user["date_retour_prevue"] = emprunt.date_retour_prevue
                user_service.mettre_a_jour_utilisateur(utilisateur)
        
        self._save_loans()
        
        Logger.log_loan_action(
            "Renouvellement d'emprunt",
            f"ID: {id_emprunt}, Nouvelle date retour: {emprunt.date_retour_prevue}"
        )
        
        return True
    
    def detecter_retards(self) -> tuple[List[Loan], List[Loan]]:
        """
        Détecte les emprunts en retard ou proches de l'échéance.
        
        Returns:
            tuple: (emprunts_1_jour_avant, emprunts_en_retard)
        """
        emprunts_1_jour_avant = []
        emprunts_en_retard = []
        
        for loan in self.loans:
            jours_retard = loan.detecter_retard()
            if jours_retard > 0:
                emprunts_en_retard.append(loan)
            elif jours_retard == -1:  # 1 jour avant l'échéance
                emprunts_1_jour_avant.append(loan)
        
        return emprunts_1_jour_avant, emprunts_en_retard

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
