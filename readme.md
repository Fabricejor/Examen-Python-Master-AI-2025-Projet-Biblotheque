# Application de Gestion de Bibliothèque - DIT

Application Python de gestion de bibliothèque développée pour le Dakar Institute of Technology (DIT), Master 1 Intelligence Artificielle.

## 📋 Table des matières

- [Présentation](#présentation)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Démarrage de l'application](#démarrage-de-lapplication)
- [Navigation dans l'application](#navigation-dans-lapplication)
- [Structure du projet](#structure-du-projet)
- [Fonctionnalités principales](#fonctionnalités-principales)
- [Contributeurs](#contributeurs)

---

## 🎯 Présentation

Cette application permet de gérer numériquement une bibliothèque académique avec :
- Gestion des livres (ajout, modification, suppression, recherche)
- Gestion des utilisateurs (étudiants, enseignants, personnel administratif)
- Gestion des emprunts (avec suivi des retards et pénalités)
- Système de réservation avec file d'attente
- Recherche avancée
- Rapports et statistiques
- Sauvegarde automatique des données

---

## 📦 Prérequis

### Version Python
- **Python 3.8 ou supérieur** est requis

Pour vérifier votre version de Python :
```bash
python --version
# ou
python3 --version
```

### Bibliothèques Python
Cette application utilise uniquement les bibliothèques standard de Python. Aucune installation de dépendances externes n'est nécessaire.

Bibliothèques utilisées :
- `datetime` (standard)
- `enum` (standard)
- `pathlib` (standard)
- `os` (standard)
- `typing` (standard)
- `abc` (standard)

---

## 🚀 Installation

### 1. Cloner le projet

Si le projet est dans un dépôt Git, clonez-le :

```bash
git clone <URL_DU_REPOSITORY>
cd Examen-Python-Master-AI-2025-Projet-Biblotheque
```

Si vous avez déjà le projet localement, naviguez vers le dossier :

```bash
cd Examen-Python-Master-AI-2025-Projet-Biblotheque
```

### 2. Vérifier la structure

Assurez-vous que la structure du projet est correcte :

```
Examen-Python-Master-AI-2025-Projet-Biblotheque/
├── app/
│   ├── main.py
│   ├── models/
│   ├── services/
│   ├── utils/
│   └── files/
├── readme.md
└── requirements.txt
```

### 3. (Optionnel) Créer un environnement virtuel

Bien que non obligatoire, il est recommandé d'utiliser un environnement virtuel :

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

---

## ▶️ Démarrage de l'application

### Méthode 1 : Exécution directe depuis la racine

Depuis la racine du projet, exécutez :

```bash
python app/main.py
```

ou

```bash
python -m app.main
```

### Méthode 2 : Exécution depuis le dossier app

```bash
cd app
python main.py
```

### Windows PowerShell

```powershell
python app\main.py
```

### Linux/Mac

```bash
python3 app/main.py
```

---

## 🧭 Navigation dans l'application

### Écran d'accueil

Au démarrage, vous verrez un message de bienvenue (MOTD) avec le titre de l'application :

```
╔══════════════════════════════════════════════════════════════════════════╗
║                        BIBLIOTHEQUE                                      ║
║                  GESTION DE BIBLIOTHÈQUE - DIT                           ║
║                                                                          ║
║              Bienvenue dans l'application de gestion                   ║
║                    de bibliothèque de DIT                              ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### Menu principal

Le menu principal affiche les options suivantes :

```
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

Votre choix (1-8) : 
```

### Navigation

1. **Saisissez le numéro** correspondant à votre choix (1-8)
2. **Appuyez sur Entrée**
3. L'écran se mettra à jour pour afficher le menu ou la fonctionnalité sélectionnée
4. Suivez les instructions à l'écran
5. Pour retourner au menu principal, appuyez sur Entrée quand demandé

### Raccourcis clavier

- **Ctrl+C** : Interrompt l'application (quitte directement)
- **Entrée** : Valide une saisie ou retourne au menu

---

## 📁 Structure du projet

```
Examen-Python-Master-AI-2025-Projet-Biblotheque/
│
├── app/                          # Module principal
│   ├── __init__.py              # Initialisation du module
│   ├── main.py                  # Point d'entrée principal ⭐
│   │
│   ├── models/                  # Modèles (classes métier)
│   │   ├── __init__.py
│   │   ├── book.py             # Modèle Livre
│   │   ├── user.py             # Modèle Utilisateur
│   │   ├── loan.py             # Modèle Emprunt
│   │   ├── reservation.py      # Modèle Réservation
│   │   └── model.md            # Documentation des modèles
│   │
│   ├── services/                # Services (logique métier)
│   │   ├── __init__.py
│   │   ├── book_service.py
│   │   ├── user_service.py
│   │   ├── loan_service.py
│   │   ├── reservation_service.py
│   │   ├── search_service.py
│   │   ├── report_service.py
│   │   ├── file_manager.py
│   │   └── logger.py
│   │
│   ├── utils/                   # Utilitaires
│   │   ├── __init__.py
│   │   ├── validators.py       # Validation et formatage
│   │   └── constants.py        # Constantes
│   │
│   └── files/                   # Persistance des données
│       ├── books/              # Fichiers des livres
│       ├── users/              # Fichiers des utilisateurs
│       ├── loans/              # Fichiers des emprunts
│       ├── reservations/       # Fichiers des réservations
│       ├── notifications/      # Notifications
│       └── register/           # Logs système
│
├── readme.md                   # Ce fichier
├── STRUCTURE.md                # Documentation de la structure
├── requirements.txt            # Dépendances (vide pour l'instant)
└── .gitignore                  # Fichiers ignorés par Git
```

---

## ⚙️ Fonctionnalités principales

### 1. Gestion des utilisateurs
- Ajouter des utilisateurs (Étudiant, Enseignant, Personnel administratif)
- Lister tous les utilisateurs
- Gestion automatique des limites d'emprunts selon le type
- Historique complet des emprunts par utilisateur

### 2. Gestion des livres
- Ajouter, modifier et supprimer des livres
- Lister tous les livres
- Gestion des exemplaires multiples
- Gestion du statut (disponible, emprunté, réservé, perdu, endommagé)
- Compteur du nombre d'emprunts par livre

### 3. Gestion des emprunts
- Emprunter un livre disponible
- Retourner un livre emprunté
- Vérification automatique de la disponibilité
- Gestion des dates d'emprunt et de retour prévue
- Détection des retards
- Renouvellement d'emprunt
- Calcul des pénalités en cas de retard

### 4. Gestion des réservations
- Réserver un livre indisponible
- Gestion d'une file d'attente des réservations
- Notification automatique lorsqu'un livre devient disponible
- Transformation d'une réservation en emprunt

### 5. Recherche avancée
- Recherche par titre, auteur, catégorie
- Recherche par ISBN et année de publication
- Recherche par disponibilité
- Recherche par mots-clés

### 6. Statistiques
- Nombre total de livres et de livres disponibles
- Nombre de livres empruntés, réservés, perdus ou endommagés
- Top 5 des livres les plus empruntés
- Top 5 des utilisateurs les plus actifs
- Nombre total d'emprunts effectués
- Liste des livres jamais empruntés

### 7. Sauvegarde et journalisation
- Sauvegarde automatique après chaque opération
- Fichiers de log pour toutes les actions
- Persistance des données dans des fichiers JSON/TXT

---

## 👥 Contributeurs

**Chef de projet :** Fabrice Jordan RAMOS

**Équipe de développement :**
- Souleymane DIENG SALL
- Zakaria
- Babacar

---

## 📝 Notes importantes

### Format de date
Toutes les dates dans l'application utilisent le format **JJ/MM/AAAA** (exemple: 27/12/2025).

### Variables d'environnement
Pour les tests, vous pouvez définir la variable d'environnement `DATE_ACTUEL` :
```bash
# Windows PowerShell
$env:DATE_ACTUEL = "27/12/2025"

# Windows CMD
set DATE_ACTUEL=27/12/2025

# Linux/Mac
export DATE_ACTUEL="27/12/2025"
```

### Fichiers de données
Les données sont stockées dans le dossier `app/files/`. Les fichiers sont créés automatiquement lors de la première utilisation.

---

## 🆘 Dépannage

### L'application ne démarre pas

**Erreur : "ModuleNotFoundError"**
- Vérifiez que vous êtes dans le bon répertoire
- Utilisez `python -m app.main` depuis la racine du projet

**Erreur : "Python not found"**
- Installez Python 3.8 ou supérieur
- Vérifiez que Python est dans votre PATH

### Problèmes d'affichage dans le terminal

- Assurez-vous que votre terminal supporte les caractères Unicode (pour les bordures)
- Sur Windows, utilisez PowerShell ou Windows Terminal

---

## 📄 Licence

Ce projet est développé dans le cadre d'un examen académique pour le DIT (Dakar Institute of Technology).

---

## 📧 Contact

Pour toute question ou problème, contactez l'équipe de développement.

---

**Bonne utilisation de l'application ! 📚**
