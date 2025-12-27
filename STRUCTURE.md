# Structure du Projet - Application de Gestion de Bibliothèque

## Vue d'ensemble

Cette structure respecte les exigences du projet d'examen Python M1 IA DIT et suit les principes de la programmation orientée objet.

## Organisation des dossiers

```
Examen-Python-Master-AI-2025-Projet-Biblotheque/
│
├── app/                          # Module principal de l'application
│   ├── __init__.py              # Initialisation du module app
│   ├── main.py                  # Point d'entrée principal
│   │
│   ├── models/                  # Modèles (classes métier)
│   │   ├── __init__.py
│   │   ├── book.py             # Modèle Livre
│   │   ├── user.py             # Modèle Utilisateur (base + héritage)
│   │   ├── loan.py             # Modèle Emprunt
│   │   └── reservation.py      # Modèle Réservation
│   │
│   ├── services/                # Services (logique métier)
│   │   ├── __init__.py
│   │   ├── book_service.py     # Gestion des livres
│   │   ├── user_service.py     # Gestion des utilisateurs
│   │   ├── loan_service.py     # Gestion des emprunts
│   │   ├── reservation_service.py  # Gestion des réservations
│   │   ├── search_service.py   # Recherche avancée
│   │   ├── report_service.py   # Rapports et statistiques
│   │   ├── file_manager.py     # Persistance des données
│   │   └── logger.py           # Journalisation
│   │
│   ├── utils/                   # Utilitaires
│   │   ├── __init__.py
│   │   ├── validators.py       # Validation (ISBN, dates, etc.)
│   │   └── constants.py        # Constantes (limites, durées, etc.)
│   │
│   └── files/                   # Persistance des données
│       ├── books/              # Fichiers de sauvegarde des livres
│       ├── users/              # Fichiers de sauvegarde des utilisateurs
│       ├── loans/              # Fichiers de sauvegarde des emprunts
│       ├── reservations/       # Fichiers de sauvegarde des réservations
│       ├── notifications/      # Fichiers de notifications
│       ├── register/           # Logs système
│       │   └── system.log
│       └── users/              # Logs utilisateurs
│           └── user.log
│
├── requirements.txt            # Dépendances Python
├── .gitignore                 # Fichiers à ignorer par Git
├── readme.md                  # Documentation principale
└── STRUCTURE.md              # Ce fichier (documentation de la structure)

```

## Description des composants

### Models (app/models/)
Contient les classes métier représentant les entités du système :
- **Book** : Représente un livre avec ISBN, titre, auteur, statut, etc.
- **User** : Classe de base pour les utilisateurs avec héritage (Étudiant, Enseignant, Personnel)
- **Loan** : Représente un emprunt avec dates, statut, pénalités
- **Reservation** : Représente une réservation avec file d'attente

### Services (app/services/)
Contient la logique métier et les opérations sur les modèles :
- **book_service.py** : CRUD des livres, gestion des exemplaires
- **user_service.py** : Gestion des utilisateurs, génération d'ID unique
- **loan_service.py** : Emprunt, retour, renouvellement, détection retards
- **reservation_service.py** : Réservations, file d'attente, notifications
- **search_service.py** : Recherche par titre, auteur, ISBN, catégorie, etc.
- **report_service.py** : Statistiques, top 5, rapports
- **file_manager.py** : Sauvegarde/chargement depuis fichiers
- **logger.py** : Journalisation de toutes les actions

### Utils (app/utils/)
Utilitaires réutilisables :
- **validators.py** : Validation ISBN, dates, formats
- **constants.py** : Limites d'emprunts par type d'utilisateur, durées, etc.

### Files (app/files/)
Stockage persistant des données :
- **books/** : Fichiers JSON/TXT des livres
- **users/** : Fichiers JSON/TXT des utilisateurs
- **loans/** : Fichiers JSON/TXT des emprunts
- **reservations/** : Fichiers JSON/TXT des réservations
- **notifications/** : Fichiers de notifications pour réservations
- **register/system.log** : Log système global
- **users/user.log** : Log des actions utilisateurs

## Principes de conception

1. **Séparation des responsabilités** : Modèles, Services, Utils
2. **POO** : Encapsulation, héritage, polymorphisme
3. **Persistance** : Fichiers pour toutes les données
4. **Journalisation** : Toutes les actions sont loggées
5. **Modularité** : Chaque service gère un domaine spécifique

## Prochaines étapes

1. Implémenter les modèles avec leurs attributs et méthodes
2. Développer les services avec la logique métier
3. Créer l'interface utilisateur (CLI ou autre)
4. Implémenter la persistance dans file_manager.py
5. Ajouter la journalisation dans logger.py
6. Tester toutes les fonctionnalités

