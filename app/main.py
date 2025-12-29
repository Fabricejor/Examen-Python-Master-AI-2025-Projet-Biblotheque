"""
Point d'entrée principal de l'application de gestion de bibliothèque.
"""

import os
import sys


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

# Instanciation globale des services
book_service = BookService()
user_service = UserService()
loan_service = LoanService()
reservation_service = ReservationService()

def handle_user_management():
    """Gère le menu de gestion des utilisateurs."""
    clear_screen()
    print("\n" + "="*80)
    print("📚 GESTION DES UTILISATEURS")
    print("="*80)
    
    users = user_service.lister_utilisateurs()
    if not users:
        print("\nAucun utilisateur enregistré.")
    else:
        print(f"\nListe des utilisateurs ({len(users)}) :")
        for u in users:
            print(f" - [{u.id_user}] {u.nom} ({u.type_utilisateur.value})")
            
    print("\n(Note: Fonctionnalité d'ajout complète à implémenter dans UserService)")
    input("\nAppuyez sur Entrée pour retourner au menu principal...")


def handle_book_management():
    """Gère le menu de gestion des livres."""
    clear_screen()
    print("\n" + "="*80)
    print("📖 GESTION DES LIVRES")
    print("="*80)
    
    livres = book_service.lister_livres()
    if not livres:
        print("\nAucun livre enregistré.")
    else:
        print(f"\nListe des livres ({len(livres)}) :")
        for b in livres:
            dispo = f"{b.exemplaire_disponible}/{b.nbre_exemplaire_total}"
            print(f" - [{b.isbn}] {b.titre} (Stock: {dispo}) - {b.statut.value}")
            
    print("\n(Note: Fonctionnalité d'ajout complète à implémenter dans BookService)")
    input("\nAppuyez sur Entrée pour retourner au menu principal...")


def handle_loan_management():
    """Gère le menu de gestion des emprunts."""
    while True:
        clear_screen()
        print("\n" + "="*80)
        print("📋 GESTION DES EMPRUNTS")
        print("="*80)
        print("1. Emprunter un livre")
        print("2. Retourner un livre")
        print("3. Lister les emprunts en cours")
        print("4. Retour au menu principal")
        
        choice = input("\nVotre choix : ").strip()
        
        if choice == '1':
            _menu_emprunter()
        elif choice == '2':
            _menu_retourner()
        elif choice == '3':
            _menu_lister_emprunts()
        elif choice == '4':
            break

def _menu_emprunter():
    print("\n--- NOUVEL EMPRUNT ---")
    user_id = input("ID Utilisateur (ex: ETU101) : ").strip()
    user = user_service.get_utilisateur_by_id(user_id)
    
    if not user:
        print("❌ Utilisateur non trouvé.")
        input("Entrée pour continuer...")
        return
        
    book_id = input("ISBN Livre (ex: LPP001) : ").strip()
    book = book_service.get_livre_by_isbn(book_id)
    
    if not book:
        print("❌ Livre non trouvé.")
        input("Entrée pour continuer...")
        return
        
    try:
        loan_service.emprunter_livre(book, user)
        # Il faut sauvegarder les états modifiés du livre et de l'utilisateur
        book_service.mettre_a_jour_livre(book)
        user_service.mettre_a_jour_utilisateur(user)
        print(f"✅ Emprunt réussi ! {user.nom} a emprunté '{book.titre}'.")
    except ValueError as e:
        print(f"❌ Erreur : {e}")
        
    input("\nEntrée pour continuer...")

def _menu_retourner():
    print("\n--- RETOUR DE LIVRE ---")
    loan_id = input("ID Emprunt (ex: empruntXX000) : ").strip()
    loan = loan_service.get_emprunt_by_id(loan_id)
    
    if not loan:
        print("❌ Emprunt non trouvé.")
        input("Entrée pour continuer...")
        return
        
    # On doit retrouver les objets liés pour mettre à jour
    book = book_service.get_livre_by_isbn(loan.id_livre)
    user = user_service.get_utilisateur_by_id(loan.id_utilisateur)
    
    if not book or not user:
        print("❌ Erreur de cohérence des données (livre ou utilisateur introuvable).")
        return
        
    try:
        if loan_service.retourner_livre(loan_id, book, user):
            print(f"✅ Livre '{book.titre}' retourné avec succès.")
            
            # Vérification des réservations
            if reservation_service.traiter_retour_livre(book):
                print("ℹ️  Une notification de disponibilité a été envoyée pour ce livre.")
            
            # Sauvegarde des états
            book_service.mettre_a_jour_livre(book)
            user_service.mettre_a_jour_utilisateur(user)
        else:
            print("❌ Erreur lors du retour.")
    except ValueError as e:
        print(f"❌ Erreur : {e}")
        
    input("\nEntrée pour continuer...")

def _menu_lister_emprunts():
    print("\n--- LISTE DES EMPRUNTS ---")
    loans = loan_service.lister_emprunts()
    if not loans:
        print("Aucun emprunt en cours.")
    else:
        for loan in loans:
            print(f" - {loan}")
    input("\nEntrée pour continuer...")


def handle_reservation_management():
    """Gère le menu de gestion des réservations."""
    while True:
        clear_screen()
        print("\n" + "="*80)
        print("🔖 GESTION DES RÉSERVATIONS")
        print("="*80)
        print("1. Réserver un livre")
        print("2. Annuler une réservation")
        print("3. Lister les réservations")
        print("4. Retour au menu principal")
        
        choice = input("\nVotre choix : ").strip()
        
        if choice == '1':
            _menu_reserver()
        elif choice == '2':
            _menu_annuler_reservation()
        elif choice == '3':
            _menu_lister_reservations()
        elif choice == '4':
            break

def _menu_reserver():
    print("\n--- NOUVELLE RÉSERVATION ---")
    user_id = input("ID Utilisateur : ").strip()
    user = user_service.get_utilisateur_by_id(user_id)
    
    if not user:
        print("❌ Utilisateur non trouvé.")
        input("Entrée pour continuer...")
        return
        
    book_id = input("ISBN Livre : ").strip()
    book = book_service.get_livre_by_isbn(book_id)
    
    if not book:
        print("❌ Livre non trouvé.")
        input("Entrée pour continuer...")
        return
        
    try:
        res = reservation_service.reserver_livre(book, user)
        # Mettre à jour le livre (statut peut changer)
        book_service.mettre_a_jour_livre(book)
        print(f"✅ Réservation réussie ! Position : {res.position_file}")
    except ValueError as e:
        print(f"❌ Erreur : {e}")
        
    input("\nEntrée pour continuer...")

def _menu_annuler_reservation():
    print("\n--- ANNULATION RÉSERVATION ---")
    res_id = input("ID Réservation : ").strip()
    
    # Pour annuler, on a besoin de l'objet livre car la méthode demande 'livre'
    # C'est une petite limitation de l'architecture actuelle, on va chercher la résa d'abord
    res_found = None
    for r in reservation_service.lister_reservations():
        if r.id_reservation == res_id:
            res_found = r
            break
            
    if not res_found:
        print("❌ Réservation non trouvée.")
        input("Entrée pour continuer...")
        return

    book = book_service.get_livre_by_isbn(res_found.id_livre)
    if not book:
         print("❌ Livre associé non trouvé.")
         return

    try:
        if reservation_service.annuler_reservation(res_id, book):
            book_service.mettre_a_jour_livre(book)
            print("✅ Réservation annulée.")
        else:
            print("❌ Erreur lors de l'annulation.")
    except ValueError as e:
        print(f"❌ Erreur : {e}")
        
    input("\nEntrée pour continuer...")

def _menu_lister_reservations():
    print("\n--- LISTE DES RÉSERVATIONS ---")
    reservations = reservation_service.lister_reservations()
    if not reservations:
        print("Aucune réservation en cours.")
    else:
        for res in reservations:
            print(f" - {res}")
    input("\nEntrée pour continuer...")


def handle_statistics():
    """Affiche les statistiques de la bibliothèque."""
    clear_screen()
    print("\n" + "="*80)
    print("📊 STATISTIQUES")
    print("="*80)
    print("\n⚠️  Fonctionnalité en cours de développement...")
    input("\nAppuyez sur Entrée pour retourner au menu principal...")


def handle_search():
    """Gère la recherche dans la bibliothèque."""
    clear_screen()
    print("\n" + "="*80)
    print("🔍 RECHERCHE")
    print("="*80)
    print("\n⚠️  Fonctionnalité en cours de développement...")
    input("\nAppuyez sur Entrée pour retourner au menu principal...")


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

