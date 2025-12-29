"""
Service de gestion des livres.
"""

from typing import List, Optional
from app.models.book import Book
from app.services.file_manager import FileManager


class BookService:
    """
    Service contenant la logique métier pour la gestion des livres.
    """
    
    DIRECTORY = "books"
    FILENAME = "books.json"
    
    def __init__(self):
        self.books: List[Book] = []
        self._load_books()
    
    def _load_books(self):
        """Charge les livres depuis le fichier JSON."""
        data = FileManager.load_data(self.DIRECTORY, self.FILENAME)
        self.books = [Book.from_dict(d) for d in data]
    
    def _save_books(self):
        """Sauvegarde les livres dans le fichier JSON."""
        data = [book.to_dict() for book in self.books]
        FileManager.save_data(self.DIRECTORY, self.FILENAME, data)
    
    def lister_livres(self) -> List[Book]:
        """Retourne la liste de tous les livres."""
        return self.books
    
    def get_livre_by_isbn(self, isbn: str) -> Optional[Book]:
        """
        Récupère un livre par son ISBN.
        
        Args:
            isbn (str): ISBN du livre
            
        Returns:
            Optional[Book]: Le livre ou None
        """
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
        
    def ajouter_livre(self, livre: Book):
        """Ajoute un livre et sauvegarde."""
        self.books.append(livre)
        self._save_books()
        
    def mettre_a_jour_livre(self, livre: Book):
        """
        Met à jour un livre existant (sauvegarde l'état actuel).
        À appeler après avoir modifié un livre (ex: changement de stock).
        """
        # Comme l'objet livre est déjà dans self.books (référence), 
        # il suffit de sauvegarder.
        self._save_books()
