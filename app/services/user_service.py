"""
Service de gestion des utilisateurs.
"""

from typing import List, Optional
from app.models.user import User
from app.services.file_manager import FileManager


class UserService:
    """
    Service contenant la logique métier pour la gestion des utilisateurs.
    """
    
    DIRECTORY = "users"
    FILENAME = "users.json"
    
    def __init__(self):
        self.users: List[User] = []
        self._load_users()
    
    def _load_users(self):
        """Charge les utilisateurs depuis le fichier JSON."""
        data = FileManager.load_data(self.DIRECTORY, self.FILENAME)
        self.users = [User.from_dict(d) for d in data]
    
    def _save_users(self):
        """Sauvegarde les utilisateurs dans le fichier JSON."""
        data = [user.to_dict() for user in self.users]
        FileManager.save_data(self.DIRECTORY, self.FILENAME, data)
    
    def lister_utilisateurs(self) -> List[User]:
        """Retourne la liste de tous les utilisateurs."""
        return self.users
    
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
        """Ajoute un utilisateur et sauvegarde."""
        self.users.append(user)
        self._save_users()
        
    def mettre_a_jour_utilisateur(self, user: User):
        """
        Met à jour un utilisateur existant.
        """
        self._save_users()
