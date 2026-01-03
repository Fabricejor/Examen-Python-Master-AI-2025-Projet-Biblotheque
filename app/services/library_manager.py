"""
Service de gestion des fichiers de bibliothèque (.docs).
"""

import re
from pathlib import Path
from typing import Optional
from app.models.book import Book


class LibraryManager:
    """
    Service pour gérer les fichiers .docs dans le dossier library.
    """
    
    LIBRARY_DIR = "library"
    
    @staticmethod
    def get_library_path() -> Path:
        """
        Retourne le chemin du dossier library.
        
        Returns:
            Path: Chemin du dossier library
        """
        base_path = Path(__file__).parent.parent
        return base_path / LibraryManager.LIBRARY_DIR
    
    @staticmethod
    def sanitize_filename(text: str) -> str:
        """
        Nettoie un texte pour en faire un nom de fichier valide.
        Remplace les caractères spéciaux et espaces par des underscores.
        
        Args:
            text (str): Texte à nettoyer
            
        Returns:
            str: Texte nettoyé pour nom de fichier
        """
        # Remplace les caractères non alphanumériques (sauf espaces) par des underscores
        text = re.sub(r'[^\w\s-]', '', text)
        # Remplace les espaces multiples par un seul underscore
        text = re.sub(r'\s+', '_', text.strip())
        # Supprime les underscores multiples
        text = re.sub(r'_+', '_', text)
        return text
    
    @staticmethod
    def get_book_filename(book: Book) -> str:
        """
        Génère le nom de fichier pour un livre selon le format: titre_isbn_auteur.docs
        
        Args:
            book (Book): Le livre
            
        Returns:
            str: Nom du fichier (ex: "Le_Livre_Ab123_Jean_Dupont.docs")
        """
        titre = LibraryManager.sanitize_filename(book.titre)
        isbn = book.isbn
        auteur = LibraryManager.sanitize_filename(book.auteur)
        
        return f"{titre}_{isbn}_{auteur}.docs"
    
    @staticmethod
    def get_book_filepath(book: Book) -> Path:
        """
        Retourne le chemin complet du fichier .docs pour un livre.
        
        Args:
            book (Book): Le livre
            
        Returns:
            Path: Chemin complet du fichier
        """
        library_path = LibraryManager.get_library_path()
        filename = LibraryManager.get_book_filename(book)
        return library_path / filename
    
    @staticmethod
    def generate_lorem_ipsum() -> str:
        """
        Génère un texte lorem ipsum pour le contenu du livre.
        
        Returns:
            str: Texte lorem ipsum
        """
        return """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.

Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.

At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga."""
    
    @staticmethod
    def create_book_file(book: Book) -> bool:
        """
        Crée le fichier .docs pour un livre dans le dossier library.
        
        Args:
            book (Book): Le livre
            
        Returns:
            bool: True si la création a réussi
        """
        try:
            library_path = LibraryManager.get_library_path()
            library_path.mkdir(parents=True, exist_ok=True)
            
            filepath = LibraryManager.get_book_filepath(book)
            
            # Génère le contenu du fichier
            content = f"""╔══════════════════════════════════════════════════════════════════════════╗
║                    INFORMATIONS DU LIVRE                               ║
╚══════════════════════════════════════════════════════════════════════════╝

ISBN: {book.isbn}
Titre: {book.titre}
Auteur: {book.auteur}
Statut: {book.statut.value}
Nombre total d'exemplaires: {book.nbre_exemplaire_total}
Exemplaires disponibles: {book.exemplaire_disponible}
Nombre d'emprunts: {book.compteur_emprunt}

╔══════════════════════════════════════════════════════════════════════════╗
║                          RÉSUMÉ                                           ║
╚══════════════════════════════════════════════════════════════════════════╝

{book.resume}

╔══════════════════════════════════════════════════════════════════════════╗
║                          CONTENU COMPLET DU LIVRE                        ║
╚══════════════════════════════════════════════════════════════════════════╝

{LibraryManager.generate_lorem_ipsum()}
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de la création du fichier library: {e}")
            return False
    
    @staticmethod
    def update_book_file(book: Book) -> bool:
        """
        Met à jour le fichier .docs d'un livre.
        
        Args:
            book (Book): Le livre
            
        Returns:
            bool: True si la mise à jour a réussi
        """
        # Pour la mise à jour, on recrée simplement le fichier
        return LibraryManager.create_book_file(book)
    
    @staticmethod
    def delete_book_file(book: Book) -> bool:
        """
        Supprime le fichier .docs d'un livre.
        
        Args:
            book (Book): Le livre
            
        Returns:
            bool: True si la suppression a réussi
        """
        try:
            filepath = LibraryManager.get_book_filepath(book)
            if filepath.exists():
                filepath.unlink()
                return True
            return False
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier library: {e}")
            return False
    
    @staticmethod
    def find_book_file_by_isbn(isbn: str) -> Optional[Path]:
        """
        Trouve le fichier .docs d'un livre par son ISBN.
        
        Args:
            isbn (str): ISBN du livre
            
        Returns:
            Optional[Path]: Chemin du fichier ou None
        """
        library_path = LibraryManager.get_library_path()
        if not library_path.exists():
            return None
        
        # Cherche un fichier contenant l'ISBN dans son nom
        for file in library_path.glob(f"*_{isbn}_*.docs"):
            return file
        
        return None

