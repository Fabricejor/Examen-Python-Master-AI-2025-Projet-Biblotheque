"""
Service de génération de rapports et statistiques.
"""

from typing import List, Dict, Tuple
from datetime import datetime
from pathlib import Path
import json
from app.models.book import Book, BookStatus
from app.models.user import User, UserType
from app.models.loan import Loan
from app.models.reservation import Reservation
from app.services.book_service import BookService
from app.services.user_service import UserService
from app.services.loan_service import LoanService
from app.services.reservation_service import ReservationService
from app.utils.validators import format_date, get_current_date


class ReportService:
    """
    Service contenant la logique métier pour la génération de statistiques et rapports.
    """
    
    STATS_DIRECTORY = "statistiques"
    STATS_FILENAME = "stats.json"
    
    def __init__(
        self,
        book_service: BookService,
        user_service: UserService,
        loan_service: LoanService,
        reservation_service: ReservationService
    ):
        """
        Initialise le service de statistiques.
        
        Args:
            book_service (BookService): Service de gestion des livres
            user_service (UserService): Service de gestion des utilisateurs
            loan_service (LoanService): Service de gestion des emprunts
            reservation_service (ReservationService): Service de gestion des réservations
        """
        self.book_service = book_service
        self.user_service = user_service
        self.loan_service = loan_service
        self.reservation_service = reservation_service
    
    def generer_statistiques_completes(self) -> Dict:
        """
        Génère toutes les statistiques de l'application.
        
        Returns:
            Dict: Dictionnaire contenant toutes les statistiques
        """
        stats = {
            "date_generation": get_current_date(),
            "heure_generation": datetime.now().strftime("%H:%M:%S"),
            "livres": self.get_statistiques_livres(),
            "utilisateurs": self.get_statistiques_utilisateurs(),
            "emprunts": self.get_statistiques_emprunts(),
            "reservations": self.get_statistiques_reservations(),
            "top_livres": self.get_top_5_livres_plus_empruntes(),
            "top_utilisateurs": self.get_top_5_utilisateurs_plus_actifs(),
            "livres_jamais_empruntes": self.get_livres_jamais_empruntes(),
            "metriques_generales": self.get_metriques_generales()
        }
        
        return stats
    
    def get_statistiques_livres(self) -> Dict:
        """
        Récupère les statistiques sur les livres.
        
        Returns:
            Dict: Statistiques sur les livres
        """
        livres = self.book_service.lister_livres()
        total_livres = len(livres)
        
        # Compte par statut
        livres_disponibles = sum(1 for livre in livres if livre.exemplaire_disponible > 0)
        livres_empruntes = sum(1 for livre in livres if livre.statut == BookStatus.EMPRUNTE)
        livres_reserves = sum(1 for livre in livres if livre.statut == BookStatus.RESERVE)
        livres_perdus = sum(1 for livre in livres if livre.statut == BookStatus.PERDU)
        livres_endommages = sum(1 for livre in livres if livre.statut == BookStatus.ENDOMMAGE)
        
        # Total d'exemplaires
        total_exemplaires = sum(livre.nbre_exemplaire_total for livre in livres)
        total_exemplaires_disponibles = sum(livre.exemplaire_disponible for livre in livres)
        
        return {
            "total_livres": total_livres,
            "total_exemplaires": total_exemplaires,
            "livres_disponibles": livres_disponibles,
            "exemplaires_disponibles": total_exemplaires_disponibles,
            "par_statut": {
                "empruntes": livres_empruntes,
                "reserves": livres_reserves,
                "perdus": livres_perdus,
                "endommagés": livres_endommages
            }
        }
    
    def get_statistiques_utilisateurs(self) -> Dict:
        """
        Récupère les statistiques sur les utilisateurs.
        
        Returns:
            Dict: Statistiques sur les utilisateurs
        """
        utilisateurs = self.user_service.lister_utilisateurs()
        total_utilisateurs = len(utilisateurs)
        
        # Compte par type
        etudiants = sum(1 for u in utilisateurs if u.type_utilisateur == UserType.ETUDIANT)
        enseignants = sum(1 for u in utilisateurs if u.type_utilisateur == UserType.ENSEIGNANT)
        personnel_admin = sum(1 for u in utilisateurs if u.type_utilisateur == UserType.PERSONNEL_ADMIN)
        
        # Utilisateurs actifs (ayant au moins un emprunt en cours)
        utilisateurs_actifs = sum(1 for u in utilisateurs if u.nombre_emprunts_en_cours() > 0)
        
        return {
            "total_utilisateurs": total_utilisateurs,
            "par_type": {
                "etudiants": etudiants,
                "enseignants": enseignants,
                "personnel_admin": personnel_admin
            },
            "utilisateurs_actifs": utilisateurs_actifs
        }
    
    def get_statistiques_emprunts(self) -> Dict:
        """
        Récupère les statistiques sur les emprunts.
        
        Returns:
            Dict: Statistiques sur les emprunts
        """
        emprunts = self.loan_service.lister_emprunts()
        total_emprunts = len(emprunts)
        
        # Emprunts avec retards
        emprunts_en_retard = sum(1 for loan in emprunts if loan.detecter_retard() > 0)
        
        # Total d'emprunts dans l'historique (depuis les utilisateurs)
        utilisateurs = self.user_service.lister_utilisateurs()
        total_emprunts_historique = sum(u.nombre_emprunt_total for u in utilisateurs)
        
        return {
            "total_emprunts_actuels": total_emprunts,
            "total_emprunts_historique": total_emprunts_historique,
            "emprunts_en_retard": emprunts_en_retard
        }
    
    def get_statistiques_reservations(self) -> Dict:
        """
        Récupère les statistiques sur les réservations.
        
        Returns:
            Dict: Statistiques sur les réservations
        """
        reservations = self.reservation_service.lister_reservations()
        total_reservations = len(reservations)
        
        # Réservations par livre (files d'attente)
        livres_avec_reservations = {}
        for res in reservations:
            isbn = res.id_livre
            if isbn not in livres_avec_reservations:
                file_attente = self.reservation_service.lister_reservations_pour_livre(isbn)
                livres_avec_reservations[isbn] = len(file_attente)
        
        return {
            "total_reservations": total_reservations,
            "livres_avec_reservations": len(livres_avec_reservations)
        }
    
    def get_top_5_livres_plus_empruntes(self) -> List[Dict]:
        """
        Récupère le top 5 des livres les plus empruntés.
        
        Returns:
            List[Dict]: Liste des 5 livres les plus empruntés avec leurs statistiques
        """
        livres = self.book_service.lister_livres()
        
        # Trie par compteur d'emprunts décroissant
        livres_tries = sorted(livres, key=lambda l: l.compteur_emprunt, reverse=True)
        
        top_5 = livres_tries[:5]
        
        return [
            {
                "isbn": livre.isbn,
                "titre": livre.titre,
                "auteur": livre.auteur,
                "nombre_emprunts": livre.compteur_emprunt,
                "exemplaires_disponibles": livre.exemplaire_disponible,
                "statut": livre.statut.value
            }
            for livre in top_5
        ]
    
    def get_top_5_utilisateurs_plus_actifs(self) -> List[Dict]:
        """
        Récupère le top 5 des utilisateurs les plus actifs.
        
        Returns:
            List[Dict]: Liste des 5 utilisateurs les plus actifs avec leurs statistiques
        """
        utilisateurs = self.user_service.lister_utilisateurs()
        
        # Trie par nombre d'emprunts total décroissant
        utilisateurs_tries = sorted(utilisateurs, key=lambda u: u.nombre_emprunt_total, reverse=True)
        
        top_5 = utilisateurs_tries[:5]
        
        return [
            {
                "id_user": user.id_user,
                "nom": user.nom,
                "type": user.type_utilisateur.value,
                "nombre_emprunts_total": user.nombre_emprunt_total,
                "emprunts_en_cours": user.nombre_emprunts_en_cours()
            }
            for user in top_5
        ]
    
    def get_livres_jamais_empruntes(self) -> List[Dict]:
        """
        Récupère la liste des livres jamais empruntés.
        
        Returns:
            List[Dict]: Liste des livres jamais empruntés
        """
        livres = self.book_service.lister_livres()
        livres_jamais_empruntes = [livre for livre in livres if livre.compteur_emprunt == 0]
        
        return [
            {
                "isbn": livre.isbn,
                "titre": livre.titre,
                "auteur": livre.auteur,
                "statut": livre.statut.value,
                "exemplaires_disponibles": livre.exemplaire_disponible,
                "exemplaires_totaux": livre.nbre_exemplaire_total
            }
            for livre in livres_jamais_empruntes
        ]
    
    def get_metriques_generales(self) -> Dict:
        """
        Récupère les métriques générales de l'application.
        
        Returns:
            Dict: Métriques générales
        """
        livres = self.book_service.lister_livres()
        utilisateurs = self.user_service.lister_utilisateurs()
        emprunts = self.loan_service.lister_emprunts()
        reservations = self.reservation_service.lister_reservations()
        
        # Taux de disponibilité
        total_exemplaires = sum(l.nbre_exemplaire_total for l in livres)
        exemplaires_disponibles = sum(l.exemplaire_disponible for l in livres)
        taux_disponibilite = (exemplaires_disponibles / total_exemplaires * 100) if total_exemplaires > 0 else 0
        
        # Taux d'utilisation (nombre d'emprunts / nombre d'utilisateurs pouvant emprunter)
        utilisateurs_emprunteurs = [u for u in utilisateurs if u.type_utilisateur in [UserType.ETUDIANT, UserType.ENSEIGNANT]]
        taux_utilisation = (len(emprunts) / len(utilisateurs_emprunteurs) * 100) if utilisateurs_emprunteurs else 0
        
        # Moyenne d'emprunts par livre
        moyenne_emprunts_livre = sum(l.compteur_emprunt for l in livres) / len(livres) if livres else 0
        
        # Moyenne d'emprunts par utilisateur
        moyenne_emprunts_utilisateur = sum(u.nombre_emprunt_total for u in utilisateurs) / len(utilisateurs) if utilisateurs else 0
        
        return {
            "taux_disponibilite": round(taux_disponibilite, 2),
            "taux_utilisation": round(taux_utilisation, 2),
            "moyenne_emprunts_par_livre": round(moyenne_emprunts_livre, 2),
            "moyenne_emprunts_par_utilisateur": round(moyenne_emprunts_utilisateur, 2),
            "ratio_livres_utilisateurs": round(len(livres) / len(utilisateurs), 2) if utilisateurs else 0
        }
    
    def sauvegarder_statistiques(self) -> bool:
        """
        Génère et sauvegarde toutes les statistiques dans stats.json.
        
        Returns:
            bool: True si la sauvegarde a réussi
        """
        try:
            stats = self.generer_statistiques_completes()
            
            # Sauvegarde directement dans le dossier statistiques
            base_path = Path(__file__).parent.parent / self.STATS_DIRECTORY
            base_path.mkdir(parents=True, exist_ok=True)
            
            file_path = base_path / self.STATS_FILENAME
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des statistiques : {e}")
            return False
