"""
Service de gestion des utilisateurs.
"""

from typing import List, Optional
from app.models.user import User, UserType, Etudiant, Enseignant, PersonnelAdmin
from app.services.file_manager import FileManager
from app.services.logger import Logger


class UserService:
    """
    Service contenant la logique métier pour la gestion des utilisateurs.
    """
    
    DIRECTORY = "users"
    FILENAME = "user.json"  # Le fichier s'appelle user.json selon la demande
    LOG_FILENAME = "user.log"
    
    def __init__(self):
        self.users: List[User] = []
        self._load_users()
    
    def _load_users(self):
        """Charge les utilisateurs depuis le fichier JSON."""
        data = FileManager.load_data(self.DIRECTORY, self.FILENAME)
        self.users = [User.from_dict(d) for d in data]
        Logger.log_user_action("Chargement des utilisateurs", f"{len(self.users)} utilisateur(s) chargé(s)")
    
    def _save_users(self):
        """Sauvegarde les utilisateurs dans le fichier JSON."""
        data = [user.to_dict() for user in self.users]
        FileManager.save_data(self.DIRECTORY, self.FILENAME, data)
    
    def lister_utilisateurs(self) -> List[User]:
        """
        Retourne la liste de tous les utilisateurs.
        
        Returns:
            List[User]: Liste de tous les utilisateurs
        """
        Logger.log_user_action("Liste de tous les utilisateurs", f"{len(self.users)} utilisateur(s)")
        return self.users
    
    def lister_utilisateurs_par_type(self, user_type: UserType) -> List[User]:
        """
        Liste les utilisateurs par type.
        
        Args:
            user_type (UserType): Type d'utilisateur (Etudiant, Enseignant, PersonnelAdmin)
            
        Returns:
            List[User]: Liste des utilisateurs du type spécifié
        """
        users_filtered = [u for u in self.users if u.type_utilisateur == user_type]
        Logger.log_user_action(f"Liste des utilisateurs de type {user_type.value}", f"{len(users_filtered)} utilisateur(s)")
        return users_filtered
    
    def get_utilisateur_by_id(self, id_user: str) -> Optional[User]:
        """
        Récupère un utilisateur par son ID.
        
        Args:
            id_user (str): ID de l'utilisateur
            
        Returns:
            Optional[User]: L'utilisateur ou None
        """
        for user in self.users:
            if user.id_user == id_user:
                return user
        return None
        
    def ajouter_utilisateur(self, user: User):
        """
        Ajoute un utilisateur et sauvegarde.
        
        Args:
            user (User): L'utilisateur à ajouter
            
        Raises:
            ValueError: Si un utilisateur avec le même ID existe déjà
        """
        # Vérifie que l'ID n'existe pas déjà
        if self.get_utilisateur_by_id(user.id_user):
            raise ValueError(f"Un utilisateur avec l'ID {user.id_user} existe déjà.")
        
        self.users.append(user)
        self._save_users()
        Logger.log_user_action(
            "Ajout d'utilisateur",
            f"ID: {user.id_user}, Nom: {user.nom}, Type: {user.type_utilisateur.value}"
        )
        
    def mettre_a_jour_utilisateur(self, user: User):
        """
        Met à jour un utilisateur existant.
        
        Args:
            user (User): L'utilisateur à mettre à jour
        """
        # Vérifie que l'utilisateur existe et le remplace
        existing_user = self.get_utilisateur_by_id(user.id_user)
        if not existing_user:
            raise ValueError(f"Utilisateur {user.id_user} non trouvé.")
        
        # Remplace l'ancien utilisateur par le nouveau
        index = self.users.index(existing_user)
        self.users[index] = user
        
        self._save_users()
        Logger.log_user_action(
            "Mise à jour d'utilisateur",
            f"ID: {user.id_user}, Nom: {user.nom}"
        )
    
    def supprimer_utilisateur(self, id_user: str) -> bool:
        """
        Supprime un utilisateur par son ID.
        
        Args:
            id_user (str): ID de l'utilisateur à supprimer
            
        Returns:
            bool: True si l'utilisateur a été supprimé, False s'il n'existe pas
        """
        user = self.get_utilisateur_by_id(id_user)
        if not user:
            return False
        
        self.users.remove(user)
        self._save_users()
        Logger.log_user_action(
            "Suppression d'utilisateur",
            f"ID: {id_user}, Nom: {user.nom}, Type: {user.type_utilisateur.value}"
        )
        return True
    
    def consulter_utilisateur(self, id_user: str) -> Optional[User]:
        """
        Consulte un utilisateur par son ID avec affichage détaillé.
        
        Args:
            id_user (str): ID de l'utilisateur
            
        Returns:
            Optional[User]: L'utilisateur ou None
        """
        user = self.get_utilisateur_by_id(id_user)
        if user:
            Logger.log_user_action(
                "Consultation d'utilisateur",
                f"ID: {id_user}, Nom: {user.nom}"
            )
        return user
