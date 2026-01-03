"""
Service de recherche avancée dans la bibliothèque.
"""

from typing import List, Optional
from app.models.book import Book, BookStatus
from app.services.book_service import BookService


class SearchService:
    """
    Service contenant la logique métier pour la recherche avancée de livres.
    """
    
    def __init__(self, book_service: BookService):
        """
        Initialise le service de recherche.
        
        Args:
            book_service (BookService): Service de gestion des livres
        """
        self.book_service = book_service
    
    def rechercher_par_titre(self, mot_cle: str) -> List[Book]:
        """
        Recherche des livres par titre (recherche partielle, insensible à la casse).
        
        Args:
            mot_cle (str): Mot-clé à rechercher dans le titre
            
        Returns:
            List[Book]: Liste des livres correspondants
        """
        mot_cle_lower = mot_cle.lower()
        livres = self.book_service.lister_livres()
        return [livre for livre in livres if mot_cle_lower in livre.titre.lower()]
    
    def rechercher_par_auteur(self, mot_cle: str) -> List[Book]:
        """
        Recherche des livres par auteur (recherche partielle, insensible à la casse).
        
        Args:
            mot_cle (str): Mot-clé à rechercher dans le nom de l'auteur
            
        Returns:
            List[Book]: Liste des livres correspondants
        """
        mot_cle_lower = mot_cle.lower()
        livres = self.book_service.lister_livres()
        return [livre for livre in livres if mot_cle_lower in livre.auteur.lower()]
    
    def rechercher_par_isbn(self, isbn: str) -> List[Book]:
        """
        Recherche un livre par ISBN (recherche exacte ou partielle).
        
        Args:
            isbn (str): ISBN à rechercher
            
        Returns:
            List[Book]: Liste des livres correspondants (généralement un seul)
        """
        isbn_lower = isbn.lower()
        livres = self.book_service.lister_livres()
        return [livre for livre in livres if isbn_lower in livre.isbn.lower()]
    
    def rechercher_par_disponibilite(self, disponible: bool = True) -> List[Book]:
        """
        Recherche des livres par disponibilité.
        
        Args:
            disponible (bool): True pour rechercher les livres disponibles, False pour les indisponibles
            
        Returns:
            List[Book]: Liste des livres correspondants
        """
        livres = self.book_service.lister_livres()
        if disponible:
            return [livre for livre in livres if livre.exemplaire_disponible > 0]
        else:
            return [livre for livre in livres if livre.exemplaire_disponible == 0]
    
    def rechercher_par_statut(self, statut: BookStatus) -> List[Book]:
        """
        Recherche des livres par statut.
        
        Args:
            statut (BookStatus): Statut à rechercher
            
        Returns:
            List[Book]: Liste des livres correspondants
        """
        livres = self.book_service.lister_livres()
        return [livre for livre in livres if livre.statut == statut]
    
    def rechercher_par_mots_cles(self, mots_cles: str) -> List[Book]:
        """
        Recherche des livres par mots-clés (cherche dans titre, auteur et résumé).
        
        Args:
            mots_cles (str): Mots-clés à rechercher
            
        Returns:
            List[Book]: Liste des livres correspondants
        """
        mots_lower = mots_cles.lower()
        livres = self.book_service.lister_livres()
        resultats = []
        
        for livre in livres:
            # Cherche dans le titre, l'auteur et le résumé
            if (mots_lower in livre.titre.lower() or 
                mots_lower in livre.auteur.lower() or 
                mots_lower in livre.resume.lower()):
                resultats.append(livre)
        
        return resultats
    
    def rechercher_combinee(
        self,
        titre: Optional[str] = None,
        auteur: Optional[str] = None,
        isbn: Optional[str] = None,
        disponible: Optional[bool] = None,
        statut: Optional[BookStatus] = None,
        mots_cles: Optional[str] = None
    ) -> List[Book]:
        """
        Recherche combinée avec plusieurs critères.
        
        Args:
            titre (str, optional): Mot-clé pour le titre
            auteur (str, optional): Mot-clé pour l'auteur
            isbn (str, optional): ISBN à rechercher
            disponible (bool, optional): Disponibilité (True/False)
            statut (BookStatus, optional): Statut du livre
            mots_cles (str, optional): Mots-clés généraux
            
        Returns:
            List[Book]: Liste des livres correspondant à tous les critères
        """
        livres = self.book_service.lister_livres()
        resultats = livres
        
        # Filtre par titre
        if titre:
            titre_lower = titre.lower()
            resultats = [l for l in resultats if titre_lower in l.titre.lower()]
        
        # Filtre par auteur
        if auteur:
            auteur_lower = auteur.lower()
            resultats = [l for l in resultats if auteur_lower in l.auteur.lower()]
        
        # Filtre par ISBN
        if isbn:
            isbn_lower = isbn.lower()
            resultats = [l for l in resultats if isbn_lower in l.isbn.lower()]
        
        # Filtre par disponibilité
        if disponible is not None:
            if disponible:
                resultats = [l for l in resultats if l.exemplaire_disponible > 0]
            else:
                resultats = [l for l in resultats if l.exemplaire_disponible == 0]
        
        # Filtre par statut
        if statut:
            resultats = [l for l in resultats if l.statut == statut]
        
        # Filtre par mots-clés (dans titre, auteur ou résumé)
        if mots_cles:
            mots_lower = mots_cles.lower()
            resultats = [
                l for l in resultats 
                if (mots_lower in l.titre.lower() or 
                    mots_lower in l.auteur.lower() or 
                    mots_lower in l.resume.lower())
            ]
        
        return resultats
