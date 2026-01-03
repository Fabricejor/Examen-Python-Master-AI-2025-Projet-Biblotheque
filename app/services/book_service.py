"""
Service de gestion des livres.
"""

from typing import List, Optional
from app.models.book import Book, BookStatus
from app.services.file_manager import FileManager
from app.services.logger import Logger
from app.services.library_manager import LibraryManager


class BookService:
    """
    Service contenant la logique métier pour la gestion des livres.
    """
    
    DIRECTORY = "books"
    FILENAME = "book.json"  # Selon la demande : book.json
    LOG_FILENAME = "book.log"
    
    def __init__(self):
        self.books: List[Book] = []
        self._load_books()
    
    def _load_books(self):
        """Charge les livres depuis le fichier JSON."""
        data = FileManager.load_data(self.DIRECTORY, self.FILENAME)
        self.books = [Book.from_dict(d) for d in data]
        Logger.log_book_action("Chargement des livres", f"{len(self.books)} livre(s) chargé(s)")
    
    def _save_books(self):
        """Sauvegarde les livres dans le fichier JSON."""
        data = [book.to_dict() for book in self.books]
        FileManager.save_data(self.DIRECTORY, self.FILENAME, data)
    
    def lister_livres(self) -> List[Book]:
        """
        Retourne la liste de tous les livres.
        
        Returns:
            List[Book]: Liste de tous les livres
        """
        Logger.log_book_action("Liste de tous les livres", f"{len(self.books)} livre(s)")
        return self.books
    
    def consulter_livre(self, isbn: str) -> Optional[Book]:
        """
        Consulte un livre par son ISBN avec affichage détaillé.
        
        Args:
            isbn (str): ISBN du livre
            
        Returns:
            Optional[Book]: Le livre ou None
        """
        book = self.get_livre_by_isbn(isbn)
        if book:
            Logger.log_book_action("Consultation de livre", f"ISBN: {isbn}, Titre: {book.titre}")
        return book
    
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
        """
        Ajoute un livre et sauvegarde.
        
        Args:
            livre (Book): Le livre à ajouter
            
        Raises:
            ValueError: Si un livre avec le même ISBN existe déjà
        """
        # Vérifie que l'ISBN n'existe pas déjà
        if self.get_livre_by_isbn(livre.isbn):
            raise ValueError(f"Un livre avec l'ISBN {livre.isbn} existe déjà.")
        
        self.books.append(livre)
        self._save_books()
        
        # Crée le fichier .docs dans library
        LibraryManager.create_book_file(livre)
        
        Logger.log_book_action(
            "Ajout de livre",
            f"ISBN: {livre.isbn}, Titre: {livre.titre}, Auteur: {livre.auteur}, Exemplaires: {livre.nbre_exemplaire_total}"
        )
        
    def mettre_a_jour_livre(self, livre: Book):
        """
        Met à jour un livre existant.
        
        Args:
            livre (Book): Le livre à mettre à jour
        """
        # Vérifie que le livre existe
        existing_book = self.get_livre_by_isbn(livre.isbn)
        if not existing_book:
            raise ValueError(f"Livre {livre.isbn} non trouvé.")
        
        # Remplace l'ancien livre par le nouveau
        index = self.books.index(existing_book)
        self.books[index] = livre
        
        self._save_books()
        
        # Met à jour le fichier .docs dans library
        LibraryManager.update_book_file(livre)
        
        Logger.log_book_action(
            "Mise à jour de livre",
            f"ISBN: {livre.isbn}, Titre: {livre.titre}"
        )
    
    def supprimer_livre(self, isbn: str) -> bool:
        """
        Supprime un livre par son ISBN.
        
        Args:
            isbn (str): ISBN du livre à supprimer
            
        Returns:
            bool: True si le livre a été supprimé, False s'il n'existe pas
        """
        book = self.get_livre_by_isbn(isbn)
        if not book:
            return False
        
        self.books.remove(book)
        self._save_books()
        
        # Supprime le fichier .docs dans library
        LibraryManager.delete_book_file(book)
        
        Logger.log_book_action(
            "Suppression de livre",
            f"ISBN: {isbn}, Titre: {book.titre}, Auteur: {book.auteur}"
        )
        return True
