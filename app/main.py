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


def handle_user_management():
    """Gère le menu de gestion des utilisateurs."""
    clear_screen()
    print("\n" + "="*80)
    print("📚 GESTION DES UTILISATEURS")
    print("="*80)
    print("\n⚠️  Fonctionnalité en cours de développement...")
    input("\nAppuyez sur Entrée pour retourner au menu principal...")


def handle_book_management():
    """Gère le menu de gestion des livres."""
    clear_screen()
    print("\n" + "="*80)
    print("📖 GESTION DES LIVRES")
    print("="*80)
    print("\n⚠️  Fonctionnalité en cours de développement...")
    input("\nAppuyez sur Entrée pour retourner au menu principal...")


def handle_loan_management():
    """Gère le menu de gestion des emprunts."""
    clear_screen()
    print("\n" + "="*80)
    print("📋 GESTION DES EMPRUNTS")
    print("="*80)
    print("\n⚠️  Fonctionnalité en cours de développement...")
    input("\nAppuyez sur Entrée pour retourner au menu principal...")


def handle_reservation_management():
    """Gère le menu de gestion des réservations."""
    clear_screen()
    print("\n" + "="*80)
    print("🔖 GESTION DES RÉSERVATIONS")
    print("="*80)
    print("\n⚠️  Fonctionnalité en cours de développement...")
    input("\nAppuyez sur Entrée pour retourner au menu principal...")


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
    ╚══════════════════════════════════════════════════════════════════════════╝
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
            print(f"\n❌ Une erreur est survenue : {e}")
            input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()
