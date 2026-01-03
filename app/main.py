"""
Point d'entrée principal de l'application de gestion de bibliothèque.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.utils.validators import parse_date, format_date, get_current_date


def load_environment():
    """
    Charge la date actuelle selon l'ordre de priorité :
    1. Date système de la machine (via datetime.now())
    2. Fichier .env (si date système échoue)
    3. Demande à l'utilisateur (en dernier recours)
    
    Returns:
        str: La date actuelle au format JJ/MM/AAAA
    """
    # PRIORITÉ 1 : Tente de récupérer la date depuis le système de la machine
    try:
        date_systeme = format_date(datetime.now())
        # Valide que la date est correcte
        parse_date(date_systeme)
        os.environ["DATE_ACTUEL"] = date_systeme
        print(f"✅ Date du jour récupérée depuis le système : {date_systeme}")
        return date_systeme
    except Exception as e:
        print(f"⚠️  Impossible de récupérer la date depuis le système : {e}")
        print("   Tentative de récupération depuis le fichier .env...")
    
    # PRIORITÉ 2 : Charge depuis le fichier .env
    env_path = Path(__file__).parent.parent / ".env"
    
    if env_path.exists():
        load_dotenv(env_path)
        print("📄 Fichier .env trouvé, chargement des variables d'environnement...")
        
        date_actuel = os.getenv("DATE_ACTUEL")
        
        if date_actuel:
            # Valide le format de la date
            try:
                parse_date(date_actuel)  # Vérifie que le format est correct
                os.environ["DATE_ACTUEL"] = date_actuel
                print(f"✅ Date du jour récupérée depuis le fichier .env : {date_actuel}")
                return date_actuel
            except ValueError:
                print(f"⚠️  Format de date invalide dans .env : {date_actuel}")
                print("   Format attendu : JJ/MM/AAAA (exemple: 27/12/2025)")
        else:
            print("⚠️  Variable DATE_ACTUEL non trouvée dans le fichier .env")
    else:
        print("⚠️  Fichier .env non trouvé")
    
    # PRIORITÉ 3 : Demande à l'utilisateur de saisir la date
    print("\n" + "="*80)
    print("📅 CONFIGURATION DE LA DATE ACTUELLE")
    print("="*80)
    print("\nLa variable DATE_ACTUEL est cruciale pour le bon déroulement de l'application.")
    print("Elle est utilisée pour :")
    print("  - Calculer les dates d'emprunt et de retour")
    print("  - Détecter les retards")
    print("  - Calculer les pénalités")
    print(f"\nFormat attendu : JJ/MM/AAAA (exemple: {format_date(datetime.now())})")
    
    while True:
        try:
            date_input = input("\nVeuillez saisir la date actuelle (JJ/MM/AAAA) : ").strip()
            
            if not date_input:
                print("❌ La date ne peut pas être vide.")
                continue
            
            # Valide le format
            parse_date(date_input)  # Lève ValueError si format invalide
            
            # Définit la variable d'environnement pour cette session
            os.environ["DATE_ACTUEL"] = date_input
            
            print(f"✅ Date actuelle définie : {date_input}")
            return date_input
            
        except ValueError as e:
            print(f"❌ Erreur : {e}")
            print("   Veuillez réessayer avec le format JJ/MM/AAAA (exemple: 27/12/2025)")
        except KeyboardInterrupt:

            print("\n\n⚠️  Interruption détectée. Tentative d'utilisation de la date système.")
            try:
                date_systeme = format_date(datetime.now())
                os.environ["DATE_ACTUEL"] = date_systeme
                print(f"✅ Date système utilisée : {date_systeme}")
                return date_systeme
            except Exception:
                print("❌ Impossible de récupérer la date système. L'application va utiliser une date par défaut.")
                # Date par défaut en cas d'échec total
                date_defaut = "01/01/2025"
                os.environ["DATE_ACTUEL"] = date_defaut
                print(f"⚠️  Date par défaut utilisée : {date_defaut}")
                return date_defaut


def clear_screen():
    """Efface l'écran de la console."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_welcome_message():
    """Affiche le message de bienvenue (MOTD) en grand."""
    welcome_text = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     ██████╗ ██╗██████╗ ██╗  ██╗ ██████╗ ████████╗██╗  ██╗███████╗      ║
    ║     ██╔══██╗██║██╔══██╗██║  ██║██╔═══██╗╚══██╔══╝██║  ██║██╔════╝      ║
    ║     ██████╔╝██║██████╔╝███████║██║   ██║   ██║   ███████║█████╗        ║
    ║     ██╔══██╗██║██╔══██╗██╔══██║██║   ██║   ██║   ██╔══██║██╔══╝        ║
    ║     ██████╔╝██║██████╔╝██║  ██║╚██████╔╝   ██║   ██║  ██║███████╗      ║
    ║     ╚═════╝ ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝      ║
    ║                                                                          ║
    ║                  ╔═══════════════════════════════════════╗              ║
    ║                  ║  GESTION DE BIBLIOTHÈQUE - DIT        ║              ║
    ║                  ╚═══════════════════════════════════════╝              ║
    ║                                                                          ║
    ║              Bienvenue dans l'application de gestion                   ║
    ║                    de bibliothèque de DIT                              ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(welcome_text)
    print("\n" + "="*80)
    print()


def display_menu():
    """Affiche le menu principal de l'application."""
    menu = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                         MENU PRINCIPAL                                  ║
    ╠══════════════════════════════════════════════════════════════════════════╣
    ║                                                                          ║
    ║  Que désirez-vous faire ?                                                ║
    ║                                                                          ║
    ║  1. Gestion des utilisateurs                                             ║
    ║  2. Gestion des livres                                                   ║
    ║  3. Gestion des emprunts                                                 ║
    ║  4. Gestion des réservations                                             ║
    ║  5. Statistiques                                                         ║
    ║  6. Effectuer une recherche                                              ║
    ║  7. Crédits de l'application                                             ║
    ║  8. Quitter l'application                                                ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(menu)


def get_user_choice():
    """Demande et retourne le choix de l'utilisateur."""
    while True:
        try:
            choice = input("\nVotre choix (1-8) : ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                return int(choice)
            else:
                print("❌ Erreur : Veuillez entrer un nombre entre 1 et 8.")
        except KeyboardInterrupt:
            print("\n\n⚠️  Interruption détectée. Au revoir !")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Erreur : {e}. Veuillez réessayer.")



# Importation des services
from app.services.book_service import BookService
from app.services.user_service import UserService
from app.services.loan_service import LoanService
from app.services.reservation_service import ReservationService
from app.services.search_service import SearchService
from app.services.report_service import ReportService

# Importation des modèles nécessaires
from app.models.user import User, UserType, Etudiant, Enseignant, PersonnelAdmin
from app.models.book import Book, BookStatus
from app.models.loan import Loan

# Instanciation globale des services
book_service = BookService()
user_service = UserService()
loan_service = LoanService()
reservation_service = ReservationService()
search_service = SearchService(book_service)
report_service = ReportService(book_service, user_service, loan_service, reservation_service)

def display_user_menu():
    """Affiche le menu de gestion des utilisateurs."""
    menu = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                    GESTION DES UTILISATEURS                              ║
    ╠══════════════════════════════════════════════════════════════════════════╣
    ║                                                                          ║
    ║  Que désirez-vous faire ?                                                ║
    ║                                                                          ║
    ║  1. Ajouter un utilisateur                                               ║
    ║  2. Lister tous les utilisateurs                                         ║
    ║  3. Consulter un utilisateur (par ID)                                    ║
    ║  4. Lister les utilisateurs par type                                     ║
    ║  5. Modifier un utilisateur                                              ║
    ║  6. Supprimer un utilisateur                                             ║
    ║  7. Retour au menu principal                                             ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(menu)


def get_user_menu_choice():
    """Demande et retourne le choix de l'utilisateur pour le menu utilisateurs."""
    while True:
        try:
            choice = input("\nVotre choix (1-7) : ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                return int(choice)
            else:
                print("❌ Erreur : Veuillez entrer un nombre entre 1 et 7.")
        except KeyboardInterrupt:
            return 7


def ajouter_utilisateur_menu(user_service):
    """Menu pour ajouter un utilisateur."""
    clear_screen()
    print("\n" + "="*80)
    print("➕ AJOUT D'UN UTILISATEUR")
    print("="*80)
    
    print("\nTypes d'utilisateurs disponibles :")
    print("  1. Étudiant (limite d'emprunts: 4)")
    print("  2. Enseignant (limite d'emprunts: 6)")
    print("  3. Personnel administratif (limite d'emprunts: 0 - ne peut pas emprunter)")
    
    while True:
        try:
            type_choice = input("\nChoisissez le type d'utilisateur (1-3) : ").strip()
            if type_choice == '1':
                user_type = UserType.ETUDIANT
                user_class = Etudiant
                break
            elif type_choice == '2':
                user_type = UserType.ENSEIGNANT
                user_class = Enseignant
                break
            elif type_choice == '3':
                user_type = UserType.PERSONNEL_ADMIN
                user_class = PersonnelAdmin
                break
            else:
                print("❌ Erreur : Veuillez choisir 1, 2 ou 3.")
        except KeyboardInterrupt:
            return
    
    nom = input("\nNom de l'utilisateur : ").strip()
    if not nom:
        print("❌ Le nom ne peut pas être vide.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    try:
        new_user = user_class(nom=nom)
        user_service.ajouter_utilisateur(new_user)
        print(f"\n✅ Utilisateur ajouté avec succès !")
        print(f"   ID: {new_user.id_user}")
        print(f"   Nom: {new_user.nom}")
        print(f"   Type: {new_user.type_utilisateur.value}")
        print(f"   Limite d'emprunts: {new_user.limite_emprunts}")
    except ValueError as e:
        print(f"\n❌ Erreur : {e}")
    except Exception as e:
        print(f"\n❌ Une erreur est survenue : {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")


def lister_tous_utilisateurs(user_service):
    """Affiche la liste de tous les utilisateurs."""
    clear_screen()
    print("\n" + "="*80)
    print("📋 LISTE DE TOUS LES UTILISATEURS")
    print("="*80)
    
    users = user_service.lister_utilisateurs()
    
    if not users:
        print("\n📭 Aucun utilisateur enregistré.")
    else:
        print(f"\nTotal : {len(users)} utilisateur(s)\n")
        print("-" * 80)
        
        for i, user in enumerate(users, 1):
            print(f"\n{i}. [{user.id_user}] {user.nom}")
            print(f"   Type : {user.type_utilisateur.value}")
            print(f"   Emprunts en cours : {user.nombre_emprunts_en_cours()}/{user.limite_emprunts}")
            print(f"   Total emprunts : {user.nombre_emprunt_total}")
            if i < len(users):
                print("-" * 80)
    
    input("\n\nAppuyez sur Entrée pour continuer...")


def consulter_utilisateur_menu(user_service):
    """Menu pour consulter un utilisateur par ID."""
    clear_screen()
    print("\n" + "="*80)
    print("🔍 CONSULTATION D'UN UTILISATEUR")
    print("="*80)
    
    id_user = input("\nID de l'utilisateur à consulter : ").strip()
    
    if not id_user:
        print("❌ L'ID ne peut pas être vide.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    user = user_service.consulter_utilisateur(id_user)
    
    if not user:
        print(f"\n❌ Aucun utilisateur trouvé avec l'ID : {id_user}")
    else:
        print("\n" + "="*80)
        print("📄 INFORMATIONS DE L'UTILISATEUR")
        print("="*80)
        print(f"\nID : {user.id_user}")
        print(f"Nom : {user.nom}")
        print(f"Type : {user.type_utilisateur.value}")
        print(f"Limite d'emprunts : {user.limite_emprunts}")
        print(f"Emprunts en cours : {user.nombre_emprunts_en_cours()}/{user.limite_emprunts}")
        print(f"Nombre total d'emprunts : {user.nombre_emprunt_total}")
        
        # Historique des emprunts en cours
        list_emprunt = user.list_emprunt
        if list_emprunt:
            print("\n" + "-"*80)
            print("📚 EMPRUNTS EN COURS :")
            print("-"*80)
            for emprunt in list_emprunt:
                print(f"\n  ID Emprunt : {emprunt.get('id_emprunt', 'N/A')}")
                print(f"  Titre du livre : {emprunt.get('titre_du_livre', 'N/A')}")
                print(f"  Date d'emprunt : {emprunt.get('date_emprunt', 'N/A')}")
                print(f"  Date de retour prévue : {emprunt.get('date_retour_prevue', 'N/A')}")
        else:
            print("\n📭 Aucun emprunt en cours.")
    
    input("\n\nAppuyez sur Entrée pour continuer...")


def lister_utilisateurs_par_type_menu(user_service):
    """Menu pour lister les utilisateurs par type."""
    clear_screen()
    print("\n" + "="*80)
    print("📋 LISTE DES UTILISATEURS PAR TYPE")
    print("="*80)
    
    print("\nTypes d'utilisateurs disponibles :")
    print("  1. Étudiant")
    print("  2. Enseignant")
    print("  3. Personnel administratif")
    
    while True:
        try:
            type_choice = input("\nChoisissez le type (1-3) : ").strip()
            if type_choice == '1':
                user_type = UserType.ETUDIANT
                break
            elif type_choice == '2':
                user_type = UserType.ENSEIGNANT
                break
            elif type_choice == '3':
                user_type = UserType.PERSONNEL_ADMIN
                break
            else:
                print("❌ Erreur : Veuillez choisir 1, 2 ou 3.")
        except KeyboardInterrupt:
            return
    
    users = user_service.lister_utilisateurs_par_type(user_type)
    
    clear_screen()
    print("\n" + "="*80)
    print(f"📋 LISTE DES {user_type.value.upper()}S")
    print("="*80)
    
    if not users:
        print(f"\n📭 Aucun {user_type.value.lower()} enregistré.")
    else:
        print(f"\nTotal : {len(users)} {user_type.value.lower()}(s)\n")
        print("-" * 80)
        
        for i, user in enumerate(users, 1):
            print(f"\n{i}. [{user.id_user}] {user.nom}")
            print(f"   Emprunts en cours : {user.nombre_emprunts_en_cours()}/{user.limite_emprunts}")
            print(f"   Total emprunts : {user.nombre_emprunt_total}")
            if i < len(users):
                print("-" * 80)
    
    input("\n\nAppuyez sur Entrée pour continuer...")


def modifier_utilisateur_menu(user_service):
    """Menu pour modifier un utilisateur."""
    clear_screen()
    print("\n" + "="*80)
    print("✏️  MODIFICATION D'UN UTILISATEUR")
    print("="*80)
    
    id_user = input("\nID de l'utilisateur à modifier : ").strip()
    
    if not id_user:
        print("❌ L'ID ne peut pas être vide.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    user = user_service.get_utilisateur_by_id(id_user)
    
    if not user:
        print(f"\n❌ Aucun utilisateur trouvé avec l'ID : {id_user}")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    print(f"\nUtilisateur actuel : [{user.id_user}] {user.nom} ({user.type_utilisateur.value})")
    
    nouveau_nom = input("\nNouveau nom (laissez vide pour ne pas modifier) : ").strip()
    
    if nouveau_nom:
        try:
            user.nom = nouveau_nom
            user_service.mettre_a_jour_utilisateur(user)
            print(f"\n✅ Utilisateur modifié avec succès !")
            print(f"   Nouveau nom : {user.nom}")
        except ValueError as e:
            print(f"\n❌ Erreur : {e}")
        except Exception as e:
            print(f"\n❌ Une erreur est survenue : {e}")
    else:
        print("\nℹ️  Aucune modification effectuée.")
    
    input("\nAppuyez sur Entrée pour continuer...")


def supprimer_utilisateur_menu(user_service):
    """Menu pour supprimer un utilisateur."""
    clear_screen()
    print("\n" + "="*80)
    print("🗑️  SUPPRESSION D'UN UTILISATEUR")
    print("="*80)
    
    id_user = input("\nID de l'utilisateur à supprimer : ").strip()
    
    if not id_user:
        print("❌ L'ID ne peut pas être vide.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    user = user_service.get_utilisateur_by_id(id_user)
    
    if not user:
        print(f"\n❌ Aucun utilisateur trouvé avec l'ID : {id_user}")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    print(f"\n⚠️  ATTENTION : Vous êtes sur le point de supprimer :")
    print(f"   ID : {user.id_user}")
    print(f"   Nom : {user.nom}")
    print(f"   Type : {user.type_utilisateur.value}")
    print(f"   Emprunts en cours : {user.nombre_emprunts_en_cours()}")
    
    if user.nombre_emprunts_en_cours() > 0:
        print("\n⚠️  Cet utilisateur a des emprunts en cours. La suppression est déconseillée.")
    
    confirmation = input("\nConfirmez la suppression (OUI pour confirmer) : ").strip()
    
    if confirmation.upper() == "OUI":
        if user_service.supprimer_utilisateur(id_user):
            print(f"\n✅ Utilisateur supprimé avec succès !")
        else:
            print(f"\n❌ Erreur lors de la suppression.")
    else:
        print("\nℹ️  Suppression annulée.")
    
    input("\nAppuyez sur Entrée pour continuer...")


def handle_user_management():
    """Gère le menu de gestion des utilisateurs."""
    while True:
        clear_screen()
        display_user_menu()
        
        choice = get_user_menu_choice()
        
        if choice == 1:
            ajouter_utilisateur_menu(user_service)
        elif choice == 2:
            lister_tous_utilisateurs(user_service)
        elif choice == 3:
            consulter_utilisateur_menu(user_service)
        elif choice == 4:
            lister_utilisateurs_par_type_menu(user_service)
        elif choice == 5:
            modifier_utilisateur_menu(user_service)
        elif choice == 6:
            supprimer_utilisateur_menu(user_service)
        elif choice == 7:
            break


def display_book_menu():
    """Affiche le menu de gestion des livres."""
    menu = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                      GESTION DES LIVRES                                  ║
    ╠══════════════════════════════════════════════════════════════════════════╣
    ║                                                                          ║
    ║  Que désirez-vous faire ?                                                ║
    ║                                                                          ║
    ║  1. Ajouter un livre                                                     ║
    ║  2. Lister tous les livres                                               ║
    ║  3. Consulter un livre (par ISBN)                                        ║
    ║  4. Modifier un livre                                                    ║
    ║  5. Supprimer un livre                                                   ║
    ║  6. Retour au menu principal                                             ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(menu)


def get_book_menu_choice():
    """Demande et retourne le choix de l'utilisateur pour le menu livres."""
    while True:
        try:
            choice = input("\nVotre choix (1-6) : ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return int(choice)
            else:
                print("❌ Erreur : Veuillez entrer un nombre entre 1 et 6.")
        except KeyboardInterrupt:
            return 6


def ajouter_livre_menu(book_service):
    """Menu pour ajouter un livre."""
    clear_screen()
    print("\n" + "="*80)
    print("➕ AJOUT D'UN LIVRE")
    print("="*80)
    
    try:
        titre = input("\nTitre du livre : ").strip()
        if not titre:
            print("❌ Le titre ne peut pas être vide.")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        auteur = input("Auteur du livre : ").strip()
        if not auteur:
            print("❌ L'auteur ne peut pas être vide.")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        resume = input("Résumé du livre : ").strip()
        if not resume:
            print("❌ Le résumé ne peut pas être vide.")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        # Nombre d'exemplaires
        while True:
            try:
                nbre_exemplaire = input("Nombre d'exemplaires (défaut: 1) : ").strip()
                if not nbre_exemplaire:
                    nbre_exemplaire = 1
                    break
                nbre_exemplaire = int(nbre_exemplaire)
                if nbre_exemplaire < 1:
                    print("❌ Le nombre d'exemplaires doit être au moins 1.")
                    continue
                break
            except ValueError:
                print("❌ Veuillez entrer un nombre valide.")
        
        # Création du livre
        new_book = Book(
            titre=titre,
            auteur=auteur,
            resume=resume,
            nbre_exemplaire_total=nbre_exemplaire
        )
        
        book_service.ajouter_livre(new_book)
        
        print(f"\n✅ Livre ajouté avec succès !")
        print(f"   ISBN: {new_book.isbn}")
        print(f"   Titre: {new_book.titre}")
        print(f"   Auteur: {new_book.auteur}")
        print(f"   Exemplaires: {new_book.exemplaire_disponible}/{new_book.nbre_exemplaire_total} disponibles")
        print(f"   Fichier créé dans library/: {new_book.titre}_{new_book.isbn}_{new_book.auteur}.docs")
        
    except ValueError as e:
        print(f"\n❌ Erreur : {e}")
    except Exception as e:
        print(f"\n❌ Une erreur est survenue : {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")


def lister_tous_livres(book_service):
    """Affiche la liste de tous les livres avec détails des exemplaires."""
    clear_screen()
    print("\n" + "="*80)
    print("📋 LISTE DE TOUS LES LIVRES")
    print("="*80)
    
    books = book_service.lister_livres()
    
    if not books:
        print("\n📭 Aucun livre enregistré.")
    else:
        print(f"\nTotal : {len(books)} livre(s)\n")
        print("-" * 80)
        
        for i, book in enumerate(books, 1):
            exemplaires_empruntes = book.nbre_exemplaire_total - book.exemplaire_disponible
            statut_global = book.statut.value
            
            print(f"\n{i}. [{book.isbn}] {book.titre}")
            print(f"   Auteur : {book.auteur}")
            print(f"   Statut global : {statut_global}")
            print(f"   Exemplaires : {book.exemplaire_disponible} disponible(s) / {book.nbre_exemplaire_total} total")
            if exemplaires_empruntes > 0:
                print(f"   Exemplaires empruntés : {exemplaires_empruntes}")
            print(f"   Nombre d'emprunts : {book.compteur_emprunt}")
            if i < len(books):
                print("-" * 80)
    
    input("\n\nAppuyez sur Entrée pour continuer...")


def consulter_livre_menu(book_service):
    """Menu pour consulter un livre par ISBN."""
    clear_screen()
    print("\n" + "="*80)
    print("🔍 CONSULTATION D'UN LIVRE")
    print("="*80)
    
    isbn = input("\nISBN du livre à consulter : ").strip()
    
    if not isbn:
        print("❌ L'ISBN ne peut pas être vide.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    book = book_service.consulter_livre(isbn)
    
    if not book:
        print(f"\n❌ Aucun livre trouvé avec l'ISBN : {isbn}")
    else:
        exemplaires_empruntes = book.nbre_exemplaire_total - book.exemplaire_disponible
        
        print("\n" + "="*80)
        print("📄 INFORMATIONS DU LIVRE")
        print("="*80)
        print(f"\nISBN : {book.isbn}")
        print(f"Titre : {book.titre}")
        print(f"Auteur : {book.auteur}")
        print(f"Statut global : {book.statut.value}")
        print(f"\nExemplaires :")
        print(f"  - Total : {book.nbre_exemplaire_total}")
        print(f"  - Disponibles : {book.exemplaire_disponible}")
        print(f"  - Empruntés : {exemplaires_empruntes}")
        print(f"\nNombre total d'emprunts : {book.compteur_emprunt}")
        print(f"\nRésumé :")
        print(f"  {book.resume}")
    
    input("\n\nAppuyez sur Entrée pour continuer...")


def modifier_livre_menu(book_service):
    """Menu pour modifier un livre."""
    clear_screen()
    print("\n" + "="*80)
    print("✏️  MODIFICATION D'UN LIVRE")
    print("="*80)
    
    isbn = input("\nISBN du livre à modifier : ").strip()
    
    if not isbn:
        print("❌ L'ISBN ne peut pas être vide.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    book = book_service.get_livre_by_isbn(isbn)
    
    if not book:
        print(f"\n❌ Aucun livre trouvé avec l'ISBN : {isbn}")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    print(f"\nLivre actuel : [{book.isbn}] {book.titre} par {book.auteur}")
    print(f"Exemplaires : {book.exemplaire_disponible}/{book.nbre_exemplaire_total}")
    
    try:
        # Modification du titre
        nouveau_titre = input("\nNouveau titre (laissez vide pour ne pas modifier) : ").strip()
        if nouveau_titre:
            book.titre = nouveau_titre
        
        # Modification de l'auteur
        nouveau_auteur = input("Nouveau auteur (laissez vide pour ne pas modifier) : ").strip()
        if nouveau_auteur:
            book.auteur = nouveau_auteur
        
        # Modification du résumé
        nouveau_resume = input("Nouveau résumé (laissez vide pour ne pas modifier) : ").strip()
        if nouveau_resume:
            book.resume = nouveau_resume
        
        # Modification du nombre d'exemplaires
        nouveau_nbre = input(f"Nouveau nombre d'exemplaires (actuel: {book.nbre_exemplaire_total}, laissez vide pour ne pas modifier) : ").strip()
        if nouveau_nbre:
            try:
                book.nbre_exemplaire_total = int(nouveau_nbre)
            except ValueError:
                print("⚠️  Nombre invalide, le nombre d'exemplaires n'a pas été modifié.")
        
        # Modification du statut
        print("\nStatuts disponibles :")
        for status in BookStatus:
            print(f"  - {status.value}")
        nouveau_statut = input(f"Nouveau statut (actuel: {book.statut.value}, laissez vide pour ne pas modifier) : ").strip()
        if nouveau_statut:
            try:
                book.statut = nouveau_statut
            except ValueError:
                print("⚠️  Statut invalide, le statut n'a pas été modifié.")
        
        # Sauvegarde
        book_service.mettre_a_jour_livre(book)
        print(f"\n✅ Livre modifié avec succès !")
        print(f"   ISBN: {book.isbn}")
        print(f"   Titre: {book.titre}")
        print(f"   Auteur: {book.auteur}")
        print(f"   Exemplaires: {book.exemplaire_disponible}/{book.nbre_exemplaire_total}")
        
    except ValueError as e:
        print(f"\n❌ Erreur : {e}")
    except Exception as e:
        print(f"\n❌ Une erreur est survenue : {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")


def supprimer_livre_menu(book_service):
    """Menu pour supprimer un livre."""
    clear_screen()
    print("\n" + "="*80)
    print("🗑️  SUPPRESSION D'UN LIVRE")
    print("="*80)
    
    isbn = input("\nISBN du livre à supprimer : ").strip()
    
    if not isbn:
        print("❌ L'ISBN ne peut pas être vide.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    book = book_service.get_livre_by_isbn(isbn)
    
    if not book:
        print(f"\n❌ Aucun livre trouvé avec l'ISBN : {isbn}")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    print(f"\n⚠️  ATTENTION : Vous êtes sur le point de supprimer :")
    print(f"   ISBN : {book.isbn}")
    print(f"   Titre : {book.titre}")
    print(f"   Auteur : {book.auteur}")
    print(f"   Exemplaires : {book.exemplaire_disponible}/{book.nbre_exemplaire_total}")
    print(f"   Nombre d'emprunts : {book.compteur_emprunt}")
    
    if book.exemplaire_disponible < book.nbre_exemplaire_total:
        print(f"\n⚠️  Ce livre a des exemplaires empruntés. La suppression est déconseillée.")
    
    confirmation = input("\nConfirmez la suppression (OUI pour confirmer) : ").strip()
    
    if confirmation.upper() == "OUI":
        if book_service.supprimer_livre(isbn):
            print(f"\n✅ Livre supprimé avec succès !")
            print(f"   Le fichier dans library/ a également été supprimé.")
        else:
            print(f"\n❌ Erreur lors de la suppression.")
    else:
        print("\nℹ️  Suppression annulée.")
    
    input("\nAppuyez sur Entrée pour continuer...")


def handle_book_management():
    """Gère le menu de gestion des livres."""
    while True:
        clear_screen()
        display_book_menu()
        
        choice = get_book_menu_choice()
        
        if choice == 1:
            ajouter_livre_menu(book_service)
        elif choice == 2:
            lister_tous_livres(book_service)
        elif choice == 3:
            consulter_livre_menu(book_service)
        elif choice == 4:
            modifier_livre_menu(book_service)
        elif choice == 5:
            supprimer_livre_menu(book_service)
        elif choice == 6:
            break


# ============================================================================
# FONCTIONS UTILITAIRES POUR LA GESTION DES EMPRUNTS
# ============================================================================

def search_books_by_keyword(books: List[Book], keyword: str) -> List[Book]:
    """Recherche des livres par mot-clé dans le titre."""
    keyword_lower = keyword.lower()
    return [b for b in books if keyword_lower in b.titre.lower()]


def search_users_by_name(users: List[User], keyword: str) -> List[User]:
    """Recherche des utilisateurs par mot-clé dans le nom."""
    keyword_lower = keyword.lower()
    return [u for u in users if keyword_lower in u.nom.lower()]


def display_numbered_books(books: List[Book], title: str = ""):
    """Affiche une liste numérotée de livres."""
    if not books:
        print("\n📭 Aucun livre trouvé.")
        return None
    
    if title:
        print(f"\n{title}")
    print("-" * 80)
    
    for i, book in enumerate(books, 1):
        print(f"{i}. [{book.isbn}] {book.titre} - {book.auteur} "
              f"(Disponibles: {book.exemplaire_disponible}/{book.nbre_exemplaire_total})")
    
    return books


def display_numbered_users(users: List[User], title: str = ""):
    """Affiche une liste numérotée d'utilisateurs groupés par type."""
    if not users:
        print("\n📭 Aucun utilisateur trouvé.")
        return None
    
    if title:
        print(f"\n{title}")
    print("-" * 80)
    
    # Groupe par type
    etudiants = [u for u in users if u.type_utilisateur.value == "Etudiant"]
    enseignants = [u for u in users if u.type_utilisateur.value == "Enseignant"]
    
    counter = 1
    
    if etudiants:
        print("\n📚 ÉTUDIANTS :")
        for user in etudiants:
            print(f"{counter}. [{user.id_user}] {user.nom} "
                  f"(Emprunts: {user.nombre_emprunts_en_cours()}/{user.limite_emprunts})")
            counter += 1
    
    if enseignants:
        print("\n👨‍🏫 ENSEIGNANTS :")
        for user in enseignants:
            print(f"{counter}. [{user.id_user}] {user.nom} "
                  f"(Emprunts: {user.nombre_emprunts_en_cours()}/{user.limite_emprunts})")
            counter += 1
    
    return users


def select_from_list(items: List, item_type: str = "élément", allow_search: bool = True) -> Optional:
    """Permet de sélectionner un élément dans une liste numérotée."""
    if not items:
        return None
    
    while True:
        try:
            if allow_search:
                choice = input(f"\nChoisissez un {item_type} (numéro) ou 'r' pour rechercher : ").strip()
            else:
                choice = input(f"\nChoisissez un {item_type} (numéro) : ").strip()
            
            if allow_search and choice.lower() == 'r':
                return None  # Signal pour faire une recherche
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(items):
                return items[choice_num - 1]
            else:
                print(f"❌ Veuillez choisir un nombre entre 1 et {len(items)}.")
        except ValueError:
            if allow_search:
                print("❌ Veuillez entrer un nombre valide ou 'r' pour rechercher.")
            else:
                print("❌ Veuillez entrer un nombre valide.")
        except KeyboardInterrupt:
            return None


# ============================================================================
# MENU PRINCIPAL DE GESTION DES EMPRUNTS
# ============================================================================

def display_loan_menu():
    """Affiche le menu de gestion des emprunts."""
    menu = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                      GESTION DES EMPRUNTS                                ║
    ╠══════════════════════════════════════════════════════════════════════════╣
    ║                                                                          ║
    ║  Que désirez-vous faire ?                                                ║
    ║                                                                          ║
    ║  1. Emprunter un livre                                                   ║
    ║  2. Retourner un livre                                                   ║
    ║  3. Vérification automatique de disponibilité                            ║
    ║  4. Gestion des dates d'emprunt et de retour prévue                      ║
    ║  5. Détection des retards                                                ║
    ║  6. Renouvellement d'emprunt                                             ║
    ║  7. Retour au menu principal                                             ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(menu)


def get_loan_menu_choice():
    """Demande et retourne le choix de l'utilisateur pour le menu emprunts."""
    while True:
        try:
            choice = input("\nVotre choix (1-7) : ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                return int(choice)
            else:
                print("❌ Erreur : Veuillez entrer un nombre entre 1 et 7.")
        except KeyboardInterrupt:
            return 7


def handle_loan_management():
    """Gère le menu de gestion des emprunts."""
    while True:
        clear_screen()
        display_loan_menu()
        
        choice = get_loan_menu_choice()
        
        if choice == 1:
            menu_emprunter_livre()
        elif choice == 2:
            menu_retourner_livre()
        elif choice == 3:
            menu_verification_disponibilite()
        elif choice == 4:
            menu_gestion_dates_emprunts()
        elif choice == 5:
            menu_detection_retards()
        elif choice == 6:
            menu_renouveler_emprunt()
        elif choice == 7:
            break


# ============================================================================
# MENU 1 : EMPRUNTER UN LIVRE
# ============================================================================

def menu_emprunter_livre():
    """Menu pour emprunter un livre avec recherche et sélection."""
    clear_screen()
    print("\n" + "="*80)
    print("➕ EMPRUNTER UN LIVRE")
    print("="*80)
    
    # Étape 1 : Demander le nombre d'exemplaires
    print("\n📚 Nombre d'exemplaires à emprunter")
    print("-" * 80)
    
    while True:
        try:
            nbre_exemplaires = input("Combien d'exemplaires voulez-vous emprunter ? (1-6) : ").strip()
            if not nbre_exemplaires:
                nbre_exemplaires = 1
                break
            nbre_exemplaires = int(nbre_exemplaires)
            if 1 <= nbre_exemplaires <= 6:
                break
            else:
                print("❌ Le nombre d'exemplaires doit être entre 1 et 6 (limite max pour enseignants).")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide.")
        except KeyboardInterrupt:
            return
    
    # Étape 2 : Sélectionner un livre
    livres_disponibles = loan_service.lister_livres_disponibles(book_service)
    
    if not livres_disponibles:
        print("\n❌ Aucun livre disponible pour l'emprunt.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    # Filtrer les livres ayant assez d'exemplaires
    livres_suffisants = [b for b in livres_disponibles if b.exemplaire_disponible >= nbre_exemplaires]
    
    if not livres_suffisants:
        print(f"\n❌ Aucun livre n'a {nbre_exemplaires} exemplaire(s) disponible(s).")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    livre_selectionne = None
    
    while livre_selectionne is None:
        clear_screen()
        print("\n" + "="*80)
        print("📚 SÉLECTION DU LIVRE")
        print("="*80)
        
        display_numbered_books(livres_suffisants, "Livres disponibles (avec assez d'exemplaires) :")
        
        livre_selectionne = select_from_list(livres_suffisants, "livre", allow_search=True)
        
        if livre_selectionne is None:
            # Recherche par mot-clé
            keyword = input("\nEntrez un mot-clé pour rechercher dans les titres : ").strip()
            if keyword:
                livres_filtres = search_books_by_keyword(livres_suffisants, keyword)
                if livres_filtres:
                    display_numbered_books(livres_filtres, f"Résultats de recherche pour '{keyword}' :")
                    livre_selectionne = select_from_list(livres_filtres, "livre", allow_search=False)
                else:
                    print(f"\n❌ Aucun livre trouvé avec le mot-clé '{keyword}'.")
                    input("\nAppuyez sur Entrée pour continuer...")
            else:
                livre_selectionne = None  # Continue la boucle
    
    if not livre_selectionne:
        return
    
    # Étape 3 : Sélectionner un utilisateur
    utilisateurs_emprunteurs = loan_service.lister_utilisateurs_emprunteurs(user_service)
    
    if not utilisateurs_emprunteurs:
        print("\n❌ Aucun utilisateur pouvant emprunter (Étudiant ou Enseignant).")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    utilisateur_selectionne = None
    
    while utilisateur_selectionne is None:
        clear_screen()
        print("\n" + "="*80)
        print("👤 SÉLECTION DE L'UTILISATEUR")
        print("="*80)
        
        display_numbered_users(utilisateurs_emprunteurs, "Utilisateurs pouvant emprunter :")
        
        utilisateur_selectionne = select_from_list(utilisateurs_emprunteurs, "utilisateur", allow_search=True)
        
        if utilisateur_selectionne is None:
            # Recherche par nom
            keyword = input("\nEntrez un mot-clé pour rechercher dans les noms : ").strip()
            if keyword:
                users_filtres = search_users_by_name(utilisateurs_emprunteurs, keyword)
                if users_filtres:
                    display_numbered_users(users_filtres, f"Résultats de recherche pour '{keyword}' :")
                    utilisateur_selectionne = select_from_list(users_filtres, "utilisateur", allow_search=False)
                else:
                    print(f"\n❌ Aucun utilisateur trouvé avec le mot-clé '{keyword}'.")
                    input("\nAppuyez sur Entrée pour continuer...")
            else:
                utilisateur_selectionne = None  # Continue la boucle
    
    if not utilisateur_selectionne:
        return
    
    # Vérification de la disponibilité avant emprunt
    if not menu_verification_disponibilite_silencieuse(livre_selectionne, utilisateur_selectionne, nbre_exemplaires):
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    # Étape 4 : Effectuer l'emprunt
    try:
        emprunts_crees = loan_service.emprunter_livre(
            livre_selectionne, 
            utilisateur_selectionne, 
            book_service,
            user_service,
            nbre_exemplaires
        )
        
        clear_screen()
        print("\n" + "="*80)
        print("✅ EMPRUNT RÉUSSI")
        print("="*80)
        print(f"\nLivre : {livre_selectionne.titre}")
        print(f"ISBN : {livre_selectionne.isbn}")
        print(f"Utilisateur : {utilisateur_selectionne.nom} ({utilisateur_selectionne.id_user})")
        print(f"Nombre d'exemplaires empruntés : {nbre_exemplaires}")
        print(f"\nID(s) d'emprunt : {', '.join([e.id_emprunt for e in emprunts_crees])}")
        print(f"Date d'emprunt : {emprunts_crees[0].date_emprunt}")
        print(f"Date de retour prévue : {emprunts_crees[0].date_retour_prevue}")
        
    except ValueError as e:
        print(f"\n❌ Erreur lors de l'emprunt : {e}")
    except Exception as e:
        print(f"\n❌ Une erreur est survenue : {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU 2 : RETOURNER UN LIVRE
# ============================================================================

def menu_retourner_livre():
    """Menu pour retourner un livre emprunté."""
    clear_screen()
    print("\n" + "="*80)
    print("↩️  RETOURNER UN LIVRE")
    print("="*80)
    
    # Étape 1 : Sélectionner un utilisateur
    utilisateurs_emprunteurs = loan_service.lister_utilisateurs_emprunteurs(user_service)
    
    if not utilisateurs_emprunteurs:
        print("\n❌ Aucun utilisateur pouvant emprunter.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    utilisateur_selectionne = None
    
    while utilisateur_selectionne is None:
        clear_screen()
        print("\n" + "="*80)
        print("👤 SÉLECTION DE L'UTILISATEUR")
        print("="*80)
        
        display_numbered_users(utilisateurs_emprunteurs, "Utilisateurs :")
        
        utilisateur_selectionne = select_from_list(utilisateurs_emprunteurs, "utilisateur", allow_search=True)
        
        if utilisateur_selectionne is None:
            keyword = input("\nEntrez un mot-clé pour rechercher dans les noms : ").strip()
            if keyword:
                users_filtres = search_users_by_name(utilisateurs_emprunteurs, keyword)
                if users_filtres:
                    display_numbered_users(users_filtres, f"Résultats de recherche pour '{keyword}' :")
                    utilisateur_selectionne = select_from_list(users_filtres, "utilisateur", allow_search=False)
                else:
                    print(f"\n❌ Aucun utilisateur trouvé avec le mot-clé '{keyword}'.")
                    input("\nAppuyez sur Entrée pour continuer...")
    
    if not utilisateur_selectionne:
        return
    
    # Étape 2 : Afficher les emprunts en cours de l'utilisateur
    emprunts_utilisateur = loan_service.lister_emprunts_utilisateur(utilisateur_selectionne.id_user)
    
    if not emprunts_utilisateur:
        print(f"\n📭 {utilisateur_selectionne.nom} n'a aucun emprunt en cours.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    # Étape 3 : Sélectionner les emprunts à retourner
    clear_screen()
    print("\n" + "="*80)
    print(f"📚 EMPRUNTS EN COURS - {utilisateur_selectionne.nom}")
    print("="*80)
    print("-" * 80)
    
    for i, loan in enumerate(emprunts_utilisateur, 1):
        livre = book_service.get_livre_by_isbn(loan.id_livre)
        jours_retard = loan.detecter_retard()
        statut_retard = ""
        if jours_retard > 0:
            statut_retard = f" ⚠️ RETARD DE {jours_retard} JOUR(S)"
        elif jours_retard == -1:
            statut_retard = " ⚠️ ÉCHÉANCE DEMAIN"
        
        print(f"\n{i}. ID: {loan.id_emprunt}")
        print(f"   Livre: {loan.titre_livre} (ISBN: {loan.id_livre})")
        print(f"   Date emprunt: {loan.date_emprunt}")
        print(f"   Date retour prévue: {loan.date_retour_prevue}{statut_retard}")
        if i < len(emprunts_utilisateur):
            print("-" * 80)
    
    while True:
        try:
            choice = input(f"\nChoisissez l'emprunt à retourner (1-{len(emprunts_utilisateur)}) ou 'tous' pour tous : ").strip()
            
            if choice.lower() == 'tous':
                # Retourner tous les emprunts
                emprunts_a_retourner = emprunts_utilisateur
                break
            else:
                choice_num = int(choice)
                if 1 <= choice_num <= len(emprunts_utilisateur):
                    emprunts_a_retourner = [emprunts_utilisateur[choice_num - 1]]
                    break
                else:
                    print(f"❌ Veuillez choisir un nombre entre 1 et {len(emprunts_utilisateur)}.")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide ou 'tous'.")
        except KeyboardInterrupt:
            return
    
    # Étape 4 : Effectuer les retours
    retours_reussis = 0
    
    for loan in emprunts_a_retourner:
        livre = book_service.get_livre_by_isbn(loan.id_livre)
        if not livre:
            print(f"\n❌ Livre {loan.id_livre} non trouvé pour l'emprunt {loan.id_emprunt}.")
            continue
        
        try:
            if loan_service.retourner_livre(loan.id_emprunt, livre, utilisateur_selectionne, book_service, user_service):
                retours_reussis += 1
                
                # Vérification des réservations
                from app.services.reservation_service import ReservationService
                reservation_service = ReservationService()
                if reservation_service.traiter_retour_livre(livre):
                    print(f"ℹ️  Notification envoyée pour '{livre.titre}' (réservation en attente).")
        except ValueError as e:
            print(f"\n❌ Erreur lors du retour de {loan.id_emprunt} : {e}")
    
    clear_screen()
    print("\n" + "="*80)
    print("✅ RETOUR(S) EFFECTUÉ(S)")
    print("="*80)
    print(f"\n{retours_reussis} emprunt(s) retourné(s) sur {len(emprunts_a_retourner)}.")
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU 3 : VÉRIFICATION AUTOMATIQUE DE DISPONIBILITÉ
# ============================================================================

def menu_verification_disponibilite():
    """Menu de vérification automatique de disponibilité."""
    clear_screen()
    print("\n" + "="*80)
    print("🔍 VÉRIFICATION AUTOMATIQUE DE DISPONIBILITÉ")
    print("="*80)
    
    livres_disponibles = loan_service.lister_livres_disponibles(book_service)
    
    if not livres_disponibles:
        print("\n📭 Aucun livre disponible actuellement.")
    else:
        print(f"\n✅ {len(livres_disponibles)} livre(s) disponible(s) :")
        print("-" * 80)
        
        for i, book in enumerate(livres_disponibles, 1):
            print(f"\n{i}. [{book.isbn}] {book.titre}")
            print(f"   Auteur: {book.auteur}")
            print(f"   Exemplaires disponibles: {book.exemplaire_disponible}/{book.nbre_exemplaire_total}")
            if i < len(livres_disponibles):
                print("-" * 80)
    
    input("\nAppuyez sur Entrée pour continuer...")


def menu_verification_disponibilite_silencieuse(livre: Book, utilisateur: User, nbre_exemplaires: int) -> bool:
    """Vérification silencieuse de disponibilité (sans affichage)."""
    # Vérifie que le livre a assez d'exemplaires
    if livre.exemplaire_disponible < nbre_exemplaires:
        print(f"\n❌ Le livre '{livre.titre}' n'a que {livre.exemplaire_disponible} exemplaire(s) disponible(s).")
        return False
    
    # Vérifie que l'utilisateur peut emprunter
    emprunts_possibles = utilisateur.limite_emprunts - utilisateur.nombre_emprunts_en_cours()
    if nbre_exemplaires > emprunts_possibles:
        print(f"\n❌ L'utilisateur ne peut emprunter que {emprunts_possibles} exemplaire(s) supplémentaire(s).")
        return False
    
    return True


# ============================================================================
# MENU 4 : GESTION DES DATES D'EMPRUNT ET DE RETOUR PRÉVUE
# ============================================================================

def menu_gestion_dates_emprunts():
    """Menu de gestion des dates d'emprunt et de retour prévue."""
    clear_screen()
    print("\n" + "="*80)
    print("📅 GESTION DES DATES D'EMPRUNT ET DE RETOUR PRÉVUE")
    print("="*80)
    
    emprunts = loan_service.lister_emprunts_en_cours()
    
    if not emprunts:
        print("\n📭 Aucun emprunt en cours.")
    else:
        print(f"\nTotal : {len(emprunts)} emprunt(s) en cours\n")
        print("-" * 80)
        
        for i, loan in enumerate(emprunts, 1):
            utilisateur = user_service.get_utilisateur_by_id(loan.id_utilisateur)
            jours_retard = loan.detecter_retard()
            statut = "✅ À jour"
            if jours_retard > 0:
                statut = f"⚠️ RETARD DE {jours_retard} JOUR(S)"
            elif jours_retard == -1:
                statut = "⚠️ ÉCHÉANCE DEMAIN"
            
            print(f"\n{i}. ID Emprunt: {loan.id_emprunt}")
            print(f"   Utilisateur: {utilisateur.nom if utilisateur else loan.nom_utilisateur} ({loan.id_utilisateur})")
            print(f"   Livre: {loan.titre_livre} (ISBN: {loan.id_livre})")
            print(f"   Date emprunt: {loan.date_emprunt}")
            print(f"   Date retour prévue: {loan.date_retour_prevue}")
            print(f"   Statut: {statut}")
            if i < len(emprunts):
                print("-" * 80)
        
        print("\n" + "="*80)
        print("Options disponibles :")
        print("  1. Emprunter un livre")
        print("  2. Retourner un livre")
        print("  3. Retour au menu emprunts")
        
        choice = input("\nVotre choix : ").strip()
        
        if choice == '1':
            menu_emprunter_livre()
        elif choice == '2':
            menu_retourner_livre()
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU 5 : DÉTECTION DES RETARDS
# ============================================================================

def menu_detection_retards():
    """Menu de détection des retards."""
    clear_screen()
    print("\n" + "="*80)
    print("⚠️  DÉTECTION DES RETARDS")
    print("="*80)
    
    emprunts_1_jour, emprunts_retard = loan_service.detecter_retards()
    
    if not emprunts_1_jour and not emprunts_retard:
        print("\n✅ Aucun emprunt en retard ou proche de l'échéance.")
    else:
        if emprunts_1_jour:
            print(f"\n⚠️  {len(emprunts_1_jour)} EMPRUNT(S) À 1 JOUR DE L'ÉCHÉANCE :")
            print("-" * 80)
            
            for i, loan in enumerate(emprunts_1_jour, 1):
                utilisateur = user_service.get_utilisateur_by_id(loan.id_utilisateur)
                print(f"\n{i}. ID: {loan.id_emprunt}")
                print(f"   Utilisateur: {utilisateur.nom if utilisateur else loan.nom_utilisateur} ({loan.id_utilisateur})")
                print(f"   Livre: {loan.titre_livre} (ISBN: {loan.id_livre})")
                print(f"   Date retour prévue: {loan.date_retour_prevue}")
                print(f"   ⚠️  ÉCHÉANCE DEMAIN")
                if i < len(emprunts_1_jour):
                    print("-" * 80)
        
        if emprunts_retard:
            print(f"\n🚨 {len(emprunts_retard)} EMPRUNT(S) EN RETARD :")
            print("-" * 80)
            
            for i, loan in enumerate(emprunts_retard, 1):
                utilisateur = user_service.get_utilisateur_by_id(loan.id_utilisateur)
                jours_retard = loan.detecter_retard()
                penalites = loan.calculer_penalites()
                
                print(f"\n{i}. ID: {loan.id_emprunt}")
                print(f"   Utilisateur: {utilisateur.nom if utilisateur else loan.nom_utilisateur} ({loan.id_utilisateur})")
                print(f"   Livre: {loan.titre_livre} (ISBN: {loan.id_livre})")
                print(f"   Date retour prévue: {loan.date_retour_prevue}")
                print(f"   🚨 RETARD DE {jours_retard} JOUR(S)")
                print(f"   Pénalités: {penalites:.2f} FCFA")
                if i < len(emprunts_retard):
                    print("-" * 80)
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU 6 : RENOUVELLEMENT D'EMPRUNT
# ============================================================================

def menu_renouveler_emprunt():
    """Menu de renouvellement d'emprunt."""
    clear_screen()
    print("\n" + "="*80)
    print("🔄 RENOUVELLEMENT D'EMPRUNT")
    print("="*80)
    
    # Sélectionner un utilisateur
    utilisateurs_emprunteurs = loan_service.lister_utilisateurs_emprunteurs(user_service)
    
    if not utilisateurs_emprunteurs:
        print("\n❌ Aucun utilisateur pouvant emprunter.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    utilisateur_selectionne = None
    
    while utilisateur_selectionne is None:
        clear_screen()
        print("\n" + "="*80)
        print("👤 SÉLECTION DE L'UTILISATEUR")
        print("="*80)
        
        display_numbered_users(utilisateurs_emprunteurs, "Utilisateurs :")
        
        utilisateur_selectionne = select_from_list(utilisateurs_emprunteurs, "utilisateur", allow_search=True)
        
        if utilisateur_selectionne is None:
            keyword = input("\nEntrez un mot-clé pour rechercher dans les noms : ").strip()
            if keyword:
                users_filtres = search_users_by_name(utilisateurs_emprunteurs, keyword)
                if users_filtres:
                    display_numbered_users(users_filtres, f"Résultats de recherche pour '{keyword}' :")
                    utilisateur_selectionne = select_from_list(users_filtres, "utilisateur", allow_search=False)
                else:
                    print(f"\n❌ Aucun utilisateur trouvé avec le mot-clé '{keyword}'.")
                    input("\nAppuyez sur Entrée pour continuer...")
    
    if not utilisateur_selectionne:
        return
    
    # Afficher les emprunts de l'utilisateur
    emprunts_utilisateur = loan_service.lister_emprunts_utilisateur(utilisateur_selectionne.id_user)
    
    if not emprunts_utilisateur:
        print(f"\n📭 {utilisateur_selectionne.nom} n'a aucun emprunt en cours.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    clear_screen()
    print("\n" + "="*80)
    print(f"📚 EMPRUNTS EN COURS - {utilisateur_selectionne.nom}")
    print("="*80)
    print("-" * 80)
    
    for i, loan in enumerate(emprunts_utilisateur, 1):
        print(f"\n{i}. ID: {loan.id_emprunt}")
        print(f"   Livre: {loan.titre_livre} (ISBN: {loan.id_livre})")
        print(f"   Date retour prévue: {loan.date_retour_prevue}")
        if i < len(emprunts_utilisateur):
            print("-" * 80)
    
    while True:
        try:
            choice = input(f"\nChoisissez l'emprunt à renouveler (1-{len(emprunts_utilisateur)}) : ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(emprunts_utilisateur):
                loan_a_renouveler = emprunts_utilisateur[choice_num - 1]
                break
            else:
                print(f"❌ Veuillez choisir un nombre entre 1 et {len(emprunts_utilisateur)}.")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide.")
        except KeyboardInterrupt:
            return
    
    # Effectuer le renouvellement
    try:
        if loan_service.renouveler_emprunt(loan_a_renouveler.id_emprunt, user_service):
            print(f"\n✅ Emprunt {loan_a_renouveler.id_emprunt} renouvelé avec succès !")
            print(f"   Nouvelle date de retour prévue : {loan_a_renouveler.date_retour_prevue}")
        else:
            print(f"\n❌ Erreur lors du renouvellement.")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU PRINCIPAL DE GESTION DES RÉSERVATIONS
# ============================================================================

def display_reservation_menu():
    """Affiche le menu de gestion des réservations."""
    menu = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                      GESTION DES RÉSERVATIONS                             ║
    ╠══════════════════════════════════════════════════════════════════════════╣
    ║                                                                          ║
    ║  Que désirez-vous faire ?                                                ║
    ║                                                                          ║
    ║  1. Réserver un livre indisponible                                       ║
    ║  2. Gestion d'une file d'attente des réservations                         ║
    ║  3. Annuler une réservation                                               ║
    ║  4. Vérifier les notifications de disponibilité                           ║
    ║  5. Transformer une réservation en emprunt                                ║
    ║  6. Retour au menu principal                                              ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(menu)


def get_reservation_menu_choice():
    """Demande et retourne le choix de l'utilisateur pour le menu réservations."""
    while True:
        try:
            choice = input("\nVotre choix (1-6) : ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return int(choice)
            else:
                print("❌ Erreur : Veuillez entrer un nombre entre 1 et 6.")
        except KeyboardInterrupt:
            return 6


def handle_reservation_management():
    """Gère le menu de gestion des réservations."""
    while True:
        clear_screen()
        display_reservation_menu()
        
        choice = get_reservation_menu_choice()
        
        if choice == 1:
            menu_reserver_livre_indisponible()
        elif choice == 2:
            menu_gestion_file_attente()
        elif choice == 3:
            menu_annuler_reservation()
        elif choice == 4:
            menu_verifier_notifications()
        elif choice == 5:
            menu_transformer_reservation_en_emprunt()
        elif choice == 6:
            break


# ============================================================================
# MENU 1 : RÉSERVER UN LIVRE INDISPONIBLE
# ============================================================================

def menu_reserver_livre_indisponible():
    """Menu pour réserver un livre indisponible avec liste déroulante et recherche."""
    clear_screen()
    print("\n" + "="*80)
    print("📚 RÉSERVER UN LIVRE INDISPONIBLE")
    print("="*80)
    
    # Étape 1 : Sélectionner un livre indisponible
    livres_indisponibles = reservation_service.lister_livres_indisponibles(book_service)
    
    if not livres_indisponibles:
        print("\n✅ Tous les livres sont disponibles. Aucune réservation nécessaire.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    livre_selectionne = None
    
    while livre_selectionne is None:
        clear_screen()
        print("\n" + "="*80)
        print("📚 SÉLECTION DU LIVRE INDISPONIBLE")
        print("="*80)
        
        display_numbered_books(livres_indisponibles, "Livres indisponibles :")
        
        livre_selectionne = select_from_list(livres_indisponibles, "livre", allow_search=True)
        
        if livre_selectionne is None:
            # Recherche par mot-clé
            keyword = input("\nEntrez un mot-clé pour rechercher dans les titres : ").strip()
            if keyword:
                livres_filtres = search_books_by_keyword(livres_indisponibles, keyword)
                if livres_filtres:
                    display_numbered_books(livres_filtres, f"Résultats de recherche pour '{keyword}' :")
                    livre_selectionne = select_from_list(livres_filtres, "livre", allow_search=False)
                else:
                    print(f"\n❌ Aucun livre trouvé avec le mot-clé '{keyword}'.")
                    input("\nAppuyez sur Entrée pour continuer...")
            else:
                livre_selectionne = None  # Continue la boucle
    
    if not livre_selectionne:
        return
    
    # Étape 2 : Sélectionner un utilisateur
    utilisateurs_emprunteurs = loan_service.lister_utilisateurs_emprunteurs(user_service)
    
    if not utilisateurs_emprunteurs:
        print("\n❌ Aucun utilisateur pouvant emprunter (Étudiant ou Enseignant).")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    utilisateur_selectionne = None
    
    while utilisateur_selectionne is None:
        clear_screen()
        print("\n" + "="*80)
        print("👤 SÉLECTION DE L'UTILISATEUR")
        print("="*80)
        
        display_numbered_users(utilisateurs_emprunteurs, "Utilisateurs pouvant réserver :")
        
        utilisateur_selectionne = select_from_list(utilisateurs_emprunteurs, "utilisateur", allow_search=True)
        
        if utilisateur_selectionne is None:
            # Recherche par nom
            keyword = input("\nEntrez un mot-clé pour rechercher dans les noms : ").strip()
            if keyword:
                users_filtres = search_users_by_name(utilisateurs_emprunteurs, keyword)
                if users_filtres:
                    display_numbered_users(users_filtres, f"Résultats de recherche pour '{keyword}' :")
                    utilisateur_selectionne = select_from_list(users_filtres, "utilisateur", allow_search=False)
                else:
                    print(f"\n❌ Aucun utilisateur trouvé avec le mot-clé '{keyword}'.")
                    input("\nAppuyez sur Entrée pour continuer...")
            else:
                utilisateur_selectionne = None  # Continue la boucle
    
    if not utilisateur_selectionne:
        return
    
    # Étape 3 : Demander la date d'emprunt souhaitée avec validation
    clear_screen()
    print("\n" + "="*80)
    print("📅 DATE D'EMPRUNT SOUHAITÉE")
    print("="*80)
    
    # Affiche les informations pour aider l'utilisateur
    date_actuelle = get_current_date()
    print(f"\nDate actuelle : {date_actuelle}")
    
    # Récupère les emprunts en cours pour ce livre
    emprunts_livre = loan_service.lister_emprunts_livre(livre_selectionne.isbn)
    if emprunts_livre:
        print(f"\n⚠️  Emprunts en cours pour ce livre :")
        for emp in emprunts_livre:
            print(f"   - Retour prévu le : {emp.date_retour_prevue}")
    
    # Récupère la file d'attente actuelle
    file_attente = reservation_service.lister_reservations_pour_livre(livre_selectionne.isbn)
    position_estimee = len(file_attente) + 1
    print(f"\n📋 Position estimée dans la file d'attente : {position_estimee}")
    
    # Calcule la date minimale recommandée
    from datetime import timedelta
    date_min = parse_date(date_actuelle)
    if emprunts_livre:
        # Prend la date de retour la plus tardive
        dates_retour = [parse_date(emp.date_retour_prevue) for emp in emprunts_livre]
        date_retour_max = max(dates_retour)
        if date_retour_max > date_min:
            date_min = date_retour_max
    
    # Ajuste selon la position dans la file (plus on est loin, plus on repousse)
        # Chaque position ajoute 3 semaines (durée d'emprunt)
        jours_ajout = (position_estimee - 1) * 21
        date_min = date_min + timedelta(days=jours_ajout)
    
    date_min_str = format_date(date_min)
    print(f"📅 Date minimale recommandée : {date_min_str} (selon position dans file)")
    
    date_emprunt = None
    while date_emprunt is None:
        try:
            date_input = input(f"\nEntrez la date d'emprunt souhaitée (JJ/MM/AAAA) [min: {date_min_str}] : ").strip()
            
            if not date_input:
                print("❌ La date ne peut pas être vide.")
                continue
            
            # Parse la date
            date_emprunt_parsed = parse_date(date_input)
            date_actuelle_parsed = parse_date(date_actuelle)
            
            # Vérifie que la date est >= date actuelle
            if date_emprunt_parsed < date_actuelle_parsed:
                print(f"❌ La date doit être supérieure ou égale à la date actuelle ({date_actuelle}).")
                continue
            
            # Vérifie que la date est >= date de retour prévue la plus tardive
            if emprunts_livre:
                dates_retour = [parse_date(emp.date_retour_prevue) for emp in emprunts_livre]
                date_retour_max = max(dates_retour)
                if date_emprunt_parsed < date_retour_max:
                    print(f"❌ La date doit être supérieure ou égale à la date de retour prévue la plus tardive ({format_date(date_retour_max)}).")
                    continue
            
            # Vérifie que la date est >= date minimale recommandée
            if date_emprunt_parsed < date_min:
                print(f"⚠️  Attention : La date est antérieure à la date minimale recommandée ({date_min_str}).")
                confirm = input("Voulez-vous continuer quand même ? (o/n) : ").strip().lower()
                if confirm != 'o':
                    continue
            
            date_emprunt = date_input
            break
            
        except ValueError as e:
            print(f"❌ Format de date invalide : {e}")
            print("   Format attendu : JJ/MM/AAAA (exemple: 27/12/2025)")
        except KeyboardInterrupt:
            return
    
    # Calcule la date de retour prévue (3 semaines après)
    date_emprunt_parsed = parse_date(date_emprunt)
    date_retour_prevue = format_date(date_emprunt_parsed + timedelta(days=21))
    
    print(f"\n📅 Date de retour prévue calculée : {date_retour_prevue} (3 semaines après l'emprunt)")
    
    # Étape 4 : Effectuer la réservation
    try:
        reservation = reservation_service.reserver_livre(
            livre_selectionne,
            utilisateur_selectionne,
            date_emprunt=date_emprunt,
            date_retour_prevue=date_retour_prevue
        )
        
        # Met à jour le livre
        book_service.mettre_a_jour_livre(livre_selectionne)
        
        clear_screen()
        print("\n" + "="*80)
        print("✅ RÉSERVATION RÉUSSIE")
        print("="*80)
        print(f"\nLivre : {livre_selectionne.titre}")
        print(f"ISBN : {livre_selectionne.isbn}")
        print(f"Utilisateur : {utilisateur_selectionne.nom} ({utilisateur_selectionne.id_user})")
        print(f"Date d'emprunt souhaitée : {date_emprunt}")
        print(f"Date de retour prévue : {date_retour_prevue}")
        print(f"Position dans la file d'attente : {reservation.position_file}")
        
    except ValueError as e:
        print(f"\n❌ Erreur lors de la réservation : {e}")
    except Exception as e:
        print(f"\n❌ Une erreur est survenue : {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU 2 : GESTION D'UNE FILE D'ATTENTE DES RÉSERVATIONS
# ============================================================================

def menu_gestion_file_attente():
    """Menu pour afficher la file d'attente des réservations pour un livre."""
    clear_screen()
    print("\n" + "="*80)
    print("📋 GESTION D'UNE FILE D'ATTENTE DES RÉSERVATIONS")
    print("="*80)
    
    # Sélectionner un livre
    livres = book_service.lister_livres()
    
    if not livres:
        print("\n📭 Aucun livre dans la bibliothèque.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    livre_selectionne = None
    
    while livre_selectionne is None:
        clear_screen()
        print("\n" + "="*80)
        print("📚 SÉLECTION DU LIVRE")
        print("="*80)
        
        display_numbered_books(livres, "Livres :")
        
        livre_selectionne = select_from_list(livres, "livre", allow_search=True)
        
        if livre_selectionne is None:
            keyword = input("\nEntrez un mot-clé pour rechercher dans les titres : ").strip()
            if keyword:
                livres_filtres = search_books_by_keyword(livres, keyword)
                if livres_filtres:
                    display_numbered_books(livres_filtres, f"Résultats de recherche pour '{keyword}' :")
                    livre_selectionne = select_from_list(livres_filtres, "livre", allow_search=False)
                else:
                    print(f"\n❌ Aucun livre trouvé avec le mot-clé '{keyword}'.")
                    input("\nAppuyez sur Entrée pour continuer...")
    
    if not livre_selectionne:
        return
    
    # Affiche la file d'attente sous format tableau
    file_attente = reservation_service.lister_reservations_pour_livre(livre_selectionne.isbn)
    
    clear_screen()
    print("\n" + "="*80)
    print(f"📋 FILE D'ATTENTE - {livre_selectionne.titre} (ISBN: {livre_selectionne.isbn})")
    print("="*80)
    
    if not file_attente:
        print("\n📭 Aucune réservation en attente pour ce livre.")
    else:
        print(f"\nTotal : {len(file_attente)} réservation(s) en attente\n")
        print("=" * 120)
        print(f"{'Position':<10} {'ID Réservation':<20} {'Utilisateur':<30} {'Date Réservation':<18} {'Date Emprunt':<18} {'Date Retour':<18}")
        print("=" * 120)
        
        for res in file_attente:
            print(f"{res.position_file:<10} {res.id_reservation:<20} {res.nom_utilisateur:<30} {res.date_reservation:<18} {res.date_emprunt:<18} {res.date_retour_prevue:<18}")
        
        print("=" * 120)
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU 3 : ANNULER UNE RÉSERVATION
# ============================================================================

def menu_annuler_reservation():
    """Menu pour annuler une réservation."""
    clear_screen()
    print("\n" + "="*80)
    print("❌ ANNULER UNE RÉSERVATION")
    print("="*80)
    
    reservations = reservation_service.lister_reservations()
    
    if not reservations:
        print("\n📭 Aucune réservation en cours.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    # Affiche les réservations
    print("\nRéservations en cours :")
    print("-" * 80)
    
    for i, res in enumerate(reservations, 1):
        print(f"\n{i}. ID: {res.id_reservation}")
        print(f"   Livre: {res.titre_livre} (ISBN: {res.id_livre})")
        print(f"   Utilisateur: {res.nom_utilisateur} ({res.id_utilisateur})")
        print(f"   Position: {res.position_file}")
        print(f"   Date emprunt: {res.date_emprunt}")
        if i < len(reservations):
            print("-" * 80)
    
    while True:
        try:
            choice = input(f"\nChoisissez la réservation à annuler (1-{len(reservations)}) : ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(reservations):
                reservation_a_annuler = reservations[choice_num - 1]
                break
            else:
                print(f"❌ Veuillez choisir un nombre entre 1 et {len(reservations)}.")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide.")
        except KeyboardInterrupt:
            return
    
    livre = book_service.get_livre_by_isbn(reservation_a_annuler.id_livre)
    if not livre:
        print("❌ Livre associé non trouvé.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    try:
        if reservation_service.annuler_reservation(reservation_a_annuler.id_reservation, livre):
            book_service.mettre_a_jour_livre(livre)
            print(f"\n✅ Réservation {reservation_a_annuler.id_reservation} annulée avec succès.")
        else:
            print("\n❌ Erreur lors de l'annulation.")
    except ValueError as e:
        print(f"\n❌ Erreur : {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU 4 : VÉRIFIER LES NOTIFICATIONS DE DISPONIBILITÉ
# ============================================================================

def menu_verifier_notifications():
    """Menu pour vérifier les notifications de disponibilité."""
    clear_screen()
    print("\n" + "="*80)
    print("🔔 VÉRIFICATION DES NOTIFICATIONS DE DISPONIBILITÉ")
    print("="*80)
    
    # Vérifie et notifie les disponibilités
    notifications = reservation_service.verifier_et_notifier_disponibilites(book_service)
    
    if notifications > 0:
        print(f"\n✅ {notifications} notification(s) envoyée(s).")
        print("   Consultez le fichier reservation.log pour les détails.")
    else:
        print("\n📭 Aucune nouvelle notification.")
    
    # Affiche les dernières notifications du fichier log
    log_path = Path(__file__).parent.parent / "files" / "reservations" / "reservation.log"
    if log_path.exists():
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Affiche les 5 dernières notifications
                notification_lines = [l for l in lines if 'NOTIFICATION:' in l]
                if notification_lines:
                    print("\n📋 Dernières notifications :")
                    print("-" * 80)
                    for line in notification_lines[-5:]:
                        print(line.strip())
        except Exception as e:
            print(f"\n⚠️  Erreur lors de la lecture du log : {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU 5 : TRANSFORMER UNE RÉSERVATION EN EMPRUNT
# ============================================================================

def menu_transformer_reservation_en_emprunt():
    """Menu pour transformer une réservation en emprunt."""
    clear_screen()
    print("\n" + "="*80)
    print("🔄 TRANSFORMER UNE RÉSERVATION EN EMPRUNT")
    print("="*80)
    
    # Récupère les réservations pour des livres disponibles
    reservations = reservation_service.lister_reservations()
    reservations_transformables = []
    
    for res in reservations:
        livre = book_service.get_livre_by_isbn(res.id_livre)
        if livre and livre.est_disponible() and res.position_file == 1:
            reservations_transformables.append(res)
    
    if not reservations_transformables:
        print("\n📭 Aucune réservation transformable (livre disponible et position 1).")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    # Affiche les réservations transformables
    print("\nRéservations transformables (livre disponible, position 1) :")
    print("-" * 80)
    
    for i, res in enumerate(reservations_transformables, 1):
        livre = book_service.get_livre_by_isbn(res.id_livre)
        print(f"\n{i}. ID: {res.id_reservation}")
        print(f"   Livre: {res.titre_livre} (ISBN: {res.id_livre}) - Disponible: {livre.exemplaire_disponible} exemplaire(s)")
        print(f"   Utilisateur: {res.nom_utilisateur} ({res.id_utilisateur})")
        print(f"   Date emprunt: {res.date_emprunt}")
        print(f"   Date retour: {res.date_retour_prevue}")
        if i < len(reservations_transformables):
            print("-" * 80)
    
    while True:
        try:
            choice = input(f"\nChoisissez la réservation à transformer (1-{len(reservations_transformables)}) : ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(reservations_transformables):
                reservation_a_transformer = reservations_transformables[choice_num - 1]
                break
            else:
                print(f"❌ Veuillez choisir un nombre entre 1 et {len(reservations_transformables)}.")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide.")
        except KeyboardInterrupt:
            return
    
    try:
        if reservation_service.transformer_reservation_en_emprunt(
            reservation_a_transformer.id_reservation,
            loan_service,
            book_service,
            user_service
        ):
            print(f"\n✅ Réservation {reservation_a_transformer.id_reservation} transformée en emprunt avec succès.")
        else:
            print("\n❌ Erreur lors de la transformation.")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU PRINCIPAL DE STATISTIQUES
# ============================================================================

def display_statistics_menu():
    """Affiche le menu de statistiques."""
    menu = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                         STATISTIQUES                                     ║
    ╠══════════════════════════════════════════════════════════════════════════╣
    ║                                                                          ║
    ║  Que désirez-vous consulter ?                                            ║
    ║                                                                          ║
    ║  1. Statistiques générales (vue d'ensemble)                              ║
    ║  2. Statistiques sur les livres                                          ║
    ║  3. Statistiques sur les emprunts                                        ║
    ║  4. Top 5 des livres les plus empruntés                                  ║
    ║  5. Top 5 des utilisateurs les plus actifs                               ║
    ║  6. Livres jamais empruntés                                              ║
    ║  7. Sauvegarder toutes les statistiques                                  ║
    ║  8. Retour au menu principal                                             ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(menu)


def get_statistics_menu_choice():
    """Demande et retourne le choix de l'utilisateur pour le menu statistiques."""
    while True:
        try:
            choice = input("\nVotre choix (1-8) : ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                return int(choice)
            else:
                print("❌ Erreur : Veuillez entrer un nombre entre 1 et 8.")
        except KeyboardInterrupt:
            return 8


def handle_statistics():
    """Gère le menu de statistiques."""
    while True:
        clear_screen()
        display_statistics_menu()
        
        choice = get_statistics_menu_choice()
        
        if choice == 1:
            menu_statistiques_generales()
        elif choice == 2:
            menu_statistiques_livres()
        elif choice == 3:
            menu_statistiques_emprunts()
        elif choice == 4:
            menu_top_5_livres()
        elif choice == 5:
            menu_top_5_utilisateurs()
        elif choice == 6:
            menu_livres_jamais_empruntes()
        elif choice == 7:
            menu_sauvegarder_statistiques()
        elif choice == 8:
            break


# ============================================================================
# MENU 1 : STATISTIQUES GÉNÉRALES
# ============================================================================

def menu_statistiques_generales():
    """Affiche les statistiques générales de l'application."""
    clear_screen()
    print("\n" + "="*80)
    print("📊 STATISTIQUES GÉNÉRALES")
    print("="*80)
    
    stats_livres = report_service.get_statistiques_livres()
    stats_utilisateurs = report_service.get_statistiques_utilisateurs()
    stats_emprunts = report_service.get_statistiques_emprunts()
    stats_reservations = report_service.get_statistiques_reservations()
    metriques = report_service.get_metriques_generales()
    
    print("\n📚 LIVRES :")
    print("-" * 80)
    print(f"  Total de livres : {stats_livres['total_livres']}")
    print(f"  Total d'exemplaires : {stats_livres['total_exemplaires']}")
    print(f"  Livres disponibles : {stats_livres['livres_disponibles']}")
    print(f"  Exemplaires disponibles : {stats_livres['exemplaires_disponibles']}")
    
    print("\n👥 UTILISATEURS :")
    print("-" * 80)
    print(f"  Total d'utilisateurs : {stats_utilisateurs['total_utilisateurs']}")
    print(f"    - Étudiants : {stats_utilisateurs['par_type']['etudiants']}")
    print(f"    - Enseignants : {stats_utilisateurs['par_type']['enseignants']}")
    print(f"    - Personnel admin : {stats_utilisateurs['par_type']['personnel_admin']}")
    print(f"  Utilisateurs actifs : {stats_utilisateurs['utilisateurs_actifs']}")
    
    print("\n📖 EMPRUNTS :")
    print("-" * 80)
    print(f"  Emprunts en cours : {stats_emprunts['total_emprunts_actuels']}")
    print(f"  Total emprunts (historique) : {stats_emprunts['total_emprunts_historique']}")
    print(f"  Emprunts en retard : {stats_emprunts['emprunts_en_retard']}")
    
    print("\n🔖 RÉSERVATIONS :")
    print("-" * 80)
    print(f"  Total de réservations : {stats_reservations['total_reservations']}")
    print(f"  Livres avec réservations : {stats_reservations['livres_avec_reservations']}")
    
    print("\n📈 MÉTRIQUES :")
    print("-" * 80)
    print(f"  Taux de disponibilité : {metriques['taux_disponibilite']}%")
    print(f"  Taux d'utilisation : {metriques['taux_utilisation']}%")
    print(f"  Moyenne emprunts/livre : {metriques['moyenne_emprunts_par_livre']}")
    print(f"  Moyenne emprunts/utilisateur : {metriques['moyenne_emprunts_par_utilisateur']}")
    print(f"  Ratio livres/utilisateurs : {metriques['ratio_livres_utilisateurs']}")
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU 2 : STATISTIQUES SUR LES LIVRES
# ============================================================================

def menu_statistiques_livres():
    """Affiche les statistiques détaillées sur les livres."""
    clear_screen()
    print("\n" + "="*80)
    print("📚 STATISTIQUES SUR LES LIVRES")
    print("="*80)
    
    stats = report_service.get_statistiques_livres()
    
    print(f"\n📊 RÉSUMÉ :")
    print("-" * 80)
    print(f"  Nombre total de livres : {stats['total_livres']}")
    print(f"  Nombre total d'exemplaires : {stats['total_exemplaires']}")
    print(f"  Livres disponibles : {stats['livres_disponibles']}")
    print(f"  Exemplaires disponibles : {stats['exemplaires_disponibles']}")
    
    print(f"\n📋 RÉPARTITION PAR STATUT :")
    print("-" * 80)
    print(f"  Livres empruntés : {stats['par_statut']['empruntes']}")
    print(f"  Livres réservés : {stats['par_statut']['reserves']}")
    print(f"  Livres perdus : {stats['par_statut']['perdus']}")
    print(f"  Livres endommagés : {stats['par_statut']['endommagés']}")
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU 3 : STATISTIQUES SUR LES EMPRUNTS
# ============================================================================

def menu_statistiques_emprunts():
    """Affiche les statistiques sur les emprunts."""
    clear_screen()
    print("\n" + "="*80)
    print("📖 STATISTIQUES SUR LES EMPRUNTS")
    print("="*80)
    
    stats = report_service.get_statistiques_emprunts()
    
    print(f"\n📊 RÉSUMÉ :")
    print("-" * 80)
    print(f"  Nombre total d'emprunts en cours : {stats['total_emprunts_actuels']}")
    print(f"  Nombre total d'emprunts (historique) : {stats['total_emprunts_historique']}")
    print(f"  Emprunts en retard : {stats['emprunts_en_retard']}")
    
    if stats['total_emprunts_actuels'] > 0:
        taux_retard = (stats['emprunts_en_retard'] / stats['total_emprunts_actuels']) * 100
        print(f"  Taux de retard : {round(taux_retard, 2)}%")
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU 4 : TOP 5 DES LIVRES LES PLUS EMPRUNTÉS
# ============================================================================

def menu_top_5_livres():
    """Affiche le top 5 des livres les plus empruntés."""
    clear_screen()
    print("\n" + "="*80)
    print("🏆 TOP 5 DES LIVRES LES PLUS EMPRUNTÉS")
    print("="*80)
    
    top_5 = report_service.get_top_5_livres_plus_empruntes()
    
    if not top_5:
        print("\n📭 Aucun livre emprunté pour le moment.")
    else:
        print("\n" + "-" * 120)
        print(f"{'Rang':<6} {'ISBN':<12} {'Titre':<40} {'Auteur':<25} {'Emprunts':<10} {'Disponibles':<12}")
        print("-" * 120)
        
        for i, livre in enumerate(top_5, 1):
            print(f"{i:<6} {livre['isbn']:<12} {livre['titre'][:38]:<40} {livre['auteur'][:23]:<25} {livre['nombre_emprunts']:<10} {livre['exemplaires_disponibles']}")
        
        print("-" * 120)
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU 5 : TOP 5 DES UTILISATEURS LES PLUS ACTIFS
# ============================================================================

def menu_top_5_utilisateurs():
    """Affiche le top 5 des utilisateurs les plus actifs."""
    clear_screen()
    print("\n" + "="*80)
    print("🏆 TOP 5 DES UTILISATEURS LES PLUS ACTIFS")
    print("="*80)
    
    top_5 = report_service.get_top_5_utilisateurs_plus_actifs()
    
    if not top_5:
        print("\n📭 Aucun utilisateur actif pour le moment.")
    else:
        print("\n" + "-" * 100)
        print(f"{'Rang':<6} {'ID':<15} {'Nom':<30} {'Type':<15} {'Emprunts Total':<15} {'En cours':<10}")
        print("-" * 100)
        
        for i, user in enumerate(top_5, 1):
            print(f"{i:<6} {user['id_user']:<15} {user['nom'][:28]:<30} {user['type']:<15} {user['nombre_emprunts_total']:<15} {user['emprunts_en_cours']:<10}")
        
        print("-" * 100)
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU 6 : LIVRES JAMAIS EMPRUNTÉS
# ============================================================================

def menu_livres_jamais_empruntes():
    """Affiche la liste des livres jamais empruntés."""
    clear_screen()
    print("\n" + "="*80)
    print("📚 LIVRES JAMAIS EMPRUNTÉS")
    print("="*80)
    
    livres = report_service.get_livres_jamais_empruntes()
    
    if not livres:
        print("\n✅ Tous les livres ont été empruntés au moins une fois.")
    else:
        print(f"\n📭 {len(livres)} livre(s) jamais emprunté(s) :")
        print("-" * 120)
        print(f"{'ISBN':<12} {'Titre':<40} {'Auteur':<25} {'Statut':<15} {'Disponibles':<12}")
        print("-" * 120)
        
        for livre in livres:
            print(f"{livre['isbn']:<12} {livre['titre'][:38]:<40} {livre['auteur'][:23]:<25} {livre['statut']:<15} {livre['exemplaires_disponibles']}/{livre['exemplaires_totaux']:<11}")
        
        print("-" * 120)
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU 7 : SAUVEGARDER LES STATISTIQUES
# ============================================================================

def menu_sauvegarder_statistiques():
    """Sauvegarde toutes les statistiques dans stats.json."""
    clear_screen()
    print("\n" + "="*80)
    print("💾 SAUVEGARDE DES STATISTIQUES")
    print("="*80)
    
    if report_service.sauvegarder_statistiques():
        print("\n✅ Statistiques sauvegardées avec succès dans app/statistiques/stats.json")
        print("\nLes statistiques incluent :")
        print("  - Statistiques sur les livres")
        print("  - Statistiques sur les utilisateurs")
        print("  - Statistiques sur les emprunts")
        print("  - Statistiques sur les réservations")
        print("  - Top 5 des livres les plus empruntés")
        print("  - Top 5 des utilisateurs les plus actifs")
        print("  - Liste des livres jamais empruntés")
        print("  - Métriques générales")
    else:
        print("\n❌ Erreur lors de la sauvegarde des statistiques.")
    
    input("\nAppuyez sur Entrée pour continuer...")


# ============================================================================
# MENU PRINCIPAL DE RECHERCHE AVANCÉE
# ============================================================================

def display_search_menu():
    """Affiche le menu de recherche avancée."""
    menu = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                      RECHERCHE AVANCÉE                                   ║
    ╠══════════════════════════════════════════════════════════════════════════╣
    ║                                                                          ║
    ║  Que désirez-vous rechercher ?                                           ║
    ║                                                                          ║
    ║  1. Recherche par titre                                                  ║
    ║  2. Recherche par auteur                                                 ║
    ║  3. Recherche par ISBN                                                   ║
    ║  4. Recherche par disponibilité                                          ║
    ║  5. Recherche par statut                                                 ║
    ║  6. Recherche par mots-clés (titre, auteur, résumé)                      ║
    ║  7. Recherche combinée (plusieurs critères)                              ║
    ║  8. Retour au menu principal                                             ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(menu)


def get_search_menu_choice():
    """Demande et retourne le choix de l'utilisateur pour le menu recherche."""
    while True:
        try:
            choice = input("\nVotre choix (1-8) : ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                return int(choice)
            else:
                print("❌ Erreur : Veuillez entrer un nombre entre 1 et 8.")
        except KeyboardInterrupt:
            return 8


def afficher_resultats_recherche(resultats: List[Book], titre_recherche: str):
    """Affiche les résultats de recherche de manière formatée."""
    clear_screen()
    print("\n" + "="*80)
    print(f"🔍 {titre_recherche}")
    print("="*80)
    
    if not resultats:
        print("\n📭 Aucun livre trouvé.")
    else:
        print(f"\n✅ {len(resultats)} livre(s) trouvé(s)\n")
        print("-" * 120)
        print(f"{'ISBN':<12} {'Titre':<40} {'Auteur':<25} {'Statut':<15} {'Disponibles':<12}")
        print("-" * 120)
        
        for livre in resultats:
            print(f"{livre.isbn:<12} {livre.titre[:38]:<40} {livre.auteur[:23]:<25} {livre.statut.value:<15} {livre.exemplaire_disponible}/{livre.nbre_exemplaire_total:<11}")
        
        print("-" * 120)
        
        # Option pour voir les détails
        if len(resultats) == 1:
            print("\n💡 Un seul résultat trouvé. Souhaitez-vous voir les détails ?")
            choix = input("Voir les détails ? (o/n) : ").strip().lower()
            if choix == 'o':
                livre = resultats[0]
                print("\n" + "="*80)
                print(f"DÉTAILS DU LIVRE - {livre.titre}")
                print("="*80)
                print(f"\nISBN : {livre.isbn}")
                print(f"Titre : {livre.titre}")
                print(f"Auteur : {livre.auteur}")
                print(f"Statut : {livre.statut.value}")
                print(f"Exemplaires disponibles : {livre.exemplaire_disponible}/{livre.nbre_exemplaire_total}")
                print(f"Nombre d'emprunts : {livre.compteur_emprunt}")
                print(f"\nRésumé :\n{livre.resume}")
                print("="*80)
    
    input("\nAppuyez sur Entrée pour continuer...")


def handle_search():
    """Gère le menu de recherche avancée."""
    while True:
        clear_screen()
        display_search_menu()
        
        choice = get_search_menu_choice()
        
        if choice == 1:
            menu_recherche_par_titre()
        elif choice == 2:
            menu_recherche_par_auteur()
        elif choice == 3:
            menu_recherche_par_isbn()
        elif choice == 4:
            menu_recherche_par_disponibilite()
        elif choice == 5:
            menu_recherche_par_statut()
        elif choice == 6:
            menu_recherche_par_mots_cles()
        elif choice == 7:
            menu_recherche_combinee()
        elif choice == 8:
            break


# ============================================================================
# MENU 1 : RECHERCHE PAR TITRE
# ============================================================================

def menu_recherche_par_titre():
    """Menu de recherche par titre."""
    clear_screen()
    print("\n" + "="*80)
    print("🔍 RECHERCHE PAR TITRE")
    print("="*80)
    
    mot_cle = input("\nEntrez un mot-clé à rechercher dans les titres : ").strip()
    
    if not mot_cle:
        print("\n❌ Le mot-clé ne peut pas être vide.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    resultats = search_service.rechercher_par_titre(mot_cle)
    afficher_resultats_recherche(resultats, f"RECHERCHE PAR TITRE - '{mot_cle}'")


# ============================================================================
# MENU 2 : RECHERCHE PAR AUTEUR
# ============================================================================

def menu_recherche_par_auteur():
    """Menu de recherche par auteur."""
    clear_screen()
    print("\n" + "="*80)
    print("🔍 RECHERCHE PAR AUTEUR")
    print("="*80)
    
    mot_cle = input("\nEntrez un mot-clé à rechercher dans les noms d'auteurs : ").strip()
    
    if not mot_cle:
        print("\n❌ Le mot-clé ne peut pas être vide.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    resultats = search_service.rechercher_par_auteur(mot_cle)
    afficher_resultats_recherche(resultats, f"RECHERCHE PAR AUTEUR - '{mot_cle}'")


# ============================================================================
# MENU 3 : RECHERCHE PAR ISBN
# ============================================================================

def menu_recherche_par_isbn():
    """Menu de recherche par ISBN."""
    clear_screen()
    print("\n" + "="*80)
    print("🔍 RECHERCHE PAR ISBN")
    print("="*80)
    
    isbn = input("\nEntrez l'ISBN (recherche partielle acceptée) : ").strip()
    
    if not isbn:
        print("\n❌ L'ISBN ne peut pas être vide.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    resultats = search_service.rechercher_par_isbn(isbn)
    afficher_resultats_recherche(resultats, f"RECHERCHE PAR ISBN - '{isbn}'")


# ============================================================================
# MENU 4 : RECHERCHE PAR DISPONIBILITÉ
# ============================================================================

def menu_recherche_par_disponibilite():
    """Menu de recherche par disponibilité."""
    clear_screen()
    print("\n" + "="*80)
    print("🔍 RECHERCHE PAR DISPONIBILITÉ")
    print("="*80)
    
    print("\nQue recherchez-vous ?")
    print("1. Livres disponibles (au moins 1 exemplaire)")
    print("2. Livres indisponibles (aucun exemplaire disponible)")
    
    while True:
        try:
            choix = input("\nVotre choix (1-2) : ").strip()
            if choix == '1':
                disponible = True
                break
            elif choix == '2':
                disponible = False
                break
            else:
                print("❌ Veuillez choisir 1 ou 2.")
        except KeyboardInterrupt:
            return
    
    resultats = search_service.rechercher_par_disponibilite(disponible)
    titre = "RECHERCHE PAR DISPONIBILITÉ - Livres disponibles" if disponible else "RECHERCHE PAR DISPONIBILITÉ - Livres indisponibles"
    afficher_resultats_recherche(resultats, titre)


# ============================================================================
# MENU 5 : RECHERCHE PAR STATUT
# ============================================================================

def menu_recherche_par_statut():
    """Menu de recherche par statut."""
    clear_screen()
    print("\n" + "="*80)
    print("🔍 RECHERCHE PAR STATUT")
    print("="*80)
    
    print("\nStatuts disponibles :")
    print("1. Disponible")
    print("2. Emprunté")
    print("3. Réservé")
    print("4. Perdu")
    print("5. Endommagé")
    
    statuts_map = {
        '1': BookStatus.DISPONIBLE,
        '2': BookStatus.EMPRUNTE,
        '3': BookStatus.RESERVE,
        '4': BookStatus.PERDU,
        '5': BookStatus.ENDOMMAGE
    }
    
    while True:
        try:
            choix = input("\nVotre choix (1-5) : ").strip()
            if choix in statuts_map:
                statut = statuts_map[choix]
                break
            else:
                print("❌ Veuillez choisir un nombre entre 1 et 5.")
        except KeyboardInterrupt:
            return
    
    resultats = search_service.rechercher_par_statut(statut)
    afficher_resultats_recherche(resultats, f"RECHERCHE PAR STATUT - {statut.value}")


# ============================================================================
# MENU 6 : RECHERCHE PAR MOTS-CLÉS
# ============================================================================

def menu_recherche_par_mots_cles():
    """Menu de recherche par mots-clés."""
    clear_screen()
    print("\n" + "="*80)
    print("🔍 RECHERCHE PAR MOTS-CLÉS")
    print("="*80)
    print("\nLa recherche s'effectue dans : titre, auteur et résumé")
    
    mots_cles = input("\nEntrez les mots-clés à rechercher : ").strip()
    
    if not mots_cles:
        print("\n❌ Les mots-clés ne peuvent pas être vides.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    resultats = search_service.rechercher_par_mots_cles(mots_cles)
    afficher_resultats_recherche(resultats, f"RECHERCHE PAR MOTS-CLÉS - '{mots_cles}'")


# ============================================================================
# MENU 7 : RECHERCHE COMBINÉE
# ============================================================================

def menu_recherche_combinee():
    """Menu de recherche combinée avec plusieurs critères."""
    clear_screen()
    print("\n" + "="*80)
    print("🔍 RECHERCHE COMBINÉE")
    print("="*80)
    print("\nVous pouvez combiner plusieurs critères de recherche.")
    print("Laissez vide les critères que vous ne souhaitez pas utiliser.\n")
    
    titre = input("Titre (mot-clé) : ").strip() or None
    auteur = input("Auteur (mot-clé) : ").strip() or None
    isbn = input("ISBN : ").strip() or None
    
    disponible = None
    choix_dispo = input("Disponibilité (1=Disponible, 2=Indisponible, Enter=Les deux) : ").strip()
    if choix_dispo == '1':
        disponible = True
    elif choix_dispo == '2':
        disponible = False
    
    statut = None
    print("\nStatut (1=Disponible, 2=Emprunté, 3=Réservé, 4=Perdu, 5=Endommagé, Enter=Ignorer) : ", end="")
    choix_statut = input().strip()
    statuts_map = {
        '1': BookStatus.DISPONIBLE,
        '2': BookStatus.EMPRUNTE,
        '3': BookStatus.RESERVE,
        '4': BookStatus.PERDU,
        '5': BookStatus.ENDOMMAGE
    }
    if choix_statut in statuts_map:
        statut = statuts_map[choix_statut]
    
    mots_cles = input("Mots-clés généraux (titre, auteur, résumé) : ").strip() or None
    
    # Vérifie qu'au moins un critère est fourni
    if not any([titre, auteur, isbn, disponible is not None, statut, mots_cles]):
        print("\n❌ Veuillez fournir au moins un critère de recherche.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    resultats = search_service.rechercher_combinee(
        titre=titre,
        auteur=auteur,
        isbn=isbn,
        disponible=disponible,
        statut=statut,
        mots_cles=mots_cles
    )
    
    afficher_resultats_recherche(resultats, "RECHERCHE COMBINÉE")


def display_credits():
    """Affiche les crédits de l'application."""
    clear_screen()
    credits = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                         CRÉDITS DE L'APPLICATION                         ║
    ╠══════════════════════════════════════════════════════════════════════════╣
    ║                                                                          ║
    ║  Application de Gestion de Bibliothèque                                  ║
    ║  Dakar Institute of Technology (DIT)                                     ║
    ║                                                                          ║
    ║  Master 1 Intelligence Artificielle                                      ║
    ║  Examen Pratique de Python                                               ║
    ║                                                                          ║
    ║  Développé avec Python                                                    ║
    ║  Programmation Orientée Objet (POO)                                       ║
    ║                                                                          ║
    ║  ──────────────────────────────────────────────────────────────────────  ║
    ║                         ÉQUIPE DE DÉVELOPPEMENT                          ║
    ║  ──────────────────────────────────────────────────────────────────────  ║
    ║                                                                          ║
    ║  👤 Fabrice Jordan RAMOS                                                 ║
    ║     Chef de Projet                                                       ║
    ║                                                                          ║
    ║  👤 Souleymane DIENG SALL                                                 ║
    ║                                                                          ║
    ║  👤 Zakaria                                                              ║
    ║                                                                          ║
    ║  👤 Babacar                                                              ║
    ║                                                                          ║
    ║  © 2025 - DIT                                                             ║
    ║                                                                          ║
    ║  ╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(credits)
    input("\nAppuyez sur Entrée pour retourner au menu principal...")


def handle_exit():
    """Gère la sortie de l'application."""
    clear_screen()
    print("\n" + "="*80)
    print("👋 AU REVOIR !")
    print("="*80)
    print("\nMerci d'avoir utilisé l'application de gestion de bibliothèque DIT.")
    print("À bientôt !\n")
    sys.exit(0)


def main():
    """Fonction principale de l'application."""
    # Charge la configuration d'environnement au démarrage
    clear_screen()
    print("\n" + "="*80)
    print("🚀 DÉMARRAGE DE L'APPLICATION")
    print("="*80)
    print()
    
    # Charge DATE_ACTUEL depuis .env ou demande à l'utilisateur
    load_environment()
    
    # Vérifie et notifie les disponibilités au démarrage
    print("\n🔔 Vérification des notifications de disponibilité...")
    notifications = reservation_service.verifier_et_notifier_disponibilites(book_service)
    if notifications > 0:
        print(f"✅ {notifications} notification(s) envoyée(s).")
    else:
        print("📭 Aucune nouvelle notification.")
    
    print("\n" + "="*80)
    input("\nAppuyez sur Entrée pour continuer...")
    
    # Boucle principale de l'application
    while True:
        try:
            clear_screen()
            display_welcome_message()
            display_menu()
            
            choice = get_user_choice()
            
            # Traitement du choix de l'utilisateur
            if choice == 1:
                handle_user_management()
            elif choice == 2:
                handle_book_management()
            elif choice == 3:
                handle_loan_management()
            elif choice == 4:
                handle_reservation_management()
            elif choice == 5:
                handle_statistics()
            elif choice == 6:
                handle_search()
            elif choice == 7:
                display_credits()
            elif choice == 8:
                handle_exit()
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Interruption détectée. Au revoir !")
            sys.exit(0)
        except Exception as e:
            # print(f"\n❌ Une erreur est survenue : {e}")
            # En production, on peut vouloir logger l'erreur plutôt que l'afficher crûment
            import traceback
            traceback.print_exc()
            input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()

