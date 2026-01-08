# Journal de Développement - Projet Bibliothèque DIT

**Projet :** Application de Gestion de Bibliothèque  
**Chef de projet :** Fabrice Jordan RAMOS  
**Date de début :** Décembre 2025  
**Objectif :** Développer une application Python complète de gestion de bibliothèque

---

## 📋 Table des matières

1. [Phase d'initialisation](#phase-dinitialisation)
2. [Structure de base du projet](#structure-de-base-du-projet)
3. [Développement de l'interface utilisateur](#développement-de-linterface-utilisateur)
4. [Développement des modèles](#développement-des-modèles)
5. [Système de dates](#système-de-dates)
6. [Documentation](#documentation)

---

## 🎬 Phase d'initialisation

### Contexte
Création d'une application Python de gestion de bibliothèque pour le DIT (Dakar Institute of Technology) dans le cadre d'un examen de Master 1 IA. L'application doit respecter les principes de la Programmation Orientée Objet (POO) et utiliser la persistance par fichiers.

### Analyse des besoins
- Gestion complète des livres, utilisateurs, emprunts et réservations
- Interface console (terminal)
- Sauvegarde automatique des données
- Journalisation des actions
- Recherche et statistiques

---

## 📂 Structure de base du projet

### Création de l'architecture

**Dossiers principaux créés :**

1. **`app/`** - Module principal de l'application
   - `__init__.py` - Initialisation du module

2. **`app/models/`** - Modèles (classes métier)
   - Structure préparée pour : Book, User, Loan, Reservation
   - `__init__.py` - Export des modèles

3. **`app/services/`** - Services (logique métier)
   - `book_service.py` - Gestion des livres
   - `user_service.py` - Gestion des utilisateurs
   - `loan_service.py` - Gestion des emprunts
   - `reservation_service.py` - Gestion des réservations
   - `search_service.py` - Recherche avancée
   - `report_service.py` - Rapports et statistiques
   - `file_manager.py` - Persistance des données
   - `logger.py` - Journalisation
   - `__init__.py` - Export des services

4. **`app/utils/`** - Utilitaires réutilisables
   - `validators.py` - Validation (ISBN, dates, etc.)
   - `constants.py` - Constantes de l'application
   - `__init__.py` - Export des utilitaires

5. **`app/files/`** - Persistance des données
   - `books/` - Fichiers de sauvegarde des livres
   - `users/` - Fichiers de sauvegarde des utilisateurs
   - `loans/` - Fichiers de sauvegarde des emprunts
   - `reservations/` - Fichiers de sauvegarde des réservations
   - `notifications/` - Fichiers de notifications
   - `register/` - Logs système
     - `system.log` - Log système global

### Fichiers de configuration

- **`.gitignore`** - Configuration Git (fichiers à ignorer)
  - `__pycache__/`
  - `*.pyc`
  - Environnements virtuels
  - Fichiers temporaires

- **`requirements.txt`** - Dépendances Python (vide, utilise uniquement les bibliothèques standard)

- **`STRUCTURE.md`** - Documentation de la structure du projet

---

## 🖥️ Développement de l'interface utilisateur

### Point d'entrée principal (`app/main.py`)

**Fonctionnalités implémentées :**

1. **Message de bienvenue (MOTD)**
   - Affichage en ASCII art avec le titre "BIBLIOTHEQUE"
   - Message de bienvenue centré avec bordures
   - Design visuel attrayant

2. **Menu principal interactif**
   - 8 options numérotées :
     1. Gestion des utilisateurs
     2. Gestion des livres
     3. Gestion des emprunts
     4. Gestion des réservations
     5. Statistiques
     6. Effectuer une recherche
     7. Crédits de l'application
     8. Quitter l'application

3. **Système de navigation**
   - Boucle principale pour maintenir l'application active
   - Validation des choix (1-8 uniquement)
   - Gestion des erreurs et interruptions (Ctrl+C)
   - Effacement de l'écran entre les menus (`clear_screen()`)
   - Messages d'attente pour les fonctionnalités à venir

4. **Fonctions de gestion**
   - Chaque option a sa fonction dédiée (structure prête pour l'implémentation)
   - `handle_user_management()` - Gestion des utilisateurs
   - `handle_book_management()` - Gestion des livres
   - `handle_loan_management()` - Gestion des emprunts
   - `handle_reservation_management()` - Gestion des réservations
   - `handle_statistics()` - Statistiques
   - `handle_search()` - Recherche
   - `display_credits()` - Affichage des crédits avec équipe de développement
   - `handle_exit()` - Sortie propre de l'application

5. **Crédits de l'application**
   - Affichage des informations du projet
   - Liste de l'équipe de développement :
     - Fabrice Jordan RAMOS (Chef de projet)
     - Souleymane DIENG SALL
     - Zakaria
     - Babacar

---

## 🏗️ Développement des modèles

### 1. Utilitaires de base (`app/utils/validators.py`)

**Fonction `generate_id(prefix)`**
- Génère un identifiant unique au format `XX000`
  - 2 lettres aléatoires (A-Z, a-z)
  - 3 chiffres aléatoires (0-9)
- Supporte un préfixe optionnel
- Réutilisable pour tous les modèles (Book, User, Loan, Reservation)
- Exemples : `Ab123`, `userAb123`, `empruntXy456`

**Fonction `validate_isbn(isbn)`**
- Valide le format d'un ISBN (XX000)
- Vérifie la structure : 2 lettres + 3 chiffres

### 2. Constantes (`app/utils/constants.py`)

**Limites d'emprunts par type d'utilisateur :**
- `LIMITE_EMPRUNTS_ETUDIANT = 4`
- `LIMITE_EMPRUNTS_ENSEIGNANT = 6`
- `LIMITE_EMPRUNTS_PERSONNEL_ADMIN = 0`

**Durées et pénalités :**
- `DUREE_EMPRUNT_DEFAUT = 30` (jours)
- `TAUX_PENALITE_PAR_JOUR = 50` (montant par jour de retard)

### 3. Modèle Book (`app/models/book.py`)

**Classe `BookStatus` (Enum)**
- `DISPONIBLE` - Le livre est disponible
- `EMPRUNTE` - Le livre est emprunté
- `RESERVE` - Le livre est réservé
- `PERDU` - Le livre est perdu
- `ENDOMmage` - Le livre est endommagé

**Classe `Book`**

*Attributs :*
- `isbn` - Identifiant unique (format XX000, généré automatiquement)
- `titre` - Titre du livre
- `auteur` - Auteur du livre
- `resume` - Résumé du livre
- `statut` - Statut actuel (BookStatus)
- `compteur_emprunt` - Nombre total d'emprunts
- `nbre_exemplaire_total` - Nombre total d'exemplaires
- `exemplaire_disponible` - Nombre d'exemplaires disponibles

*Méthodes principales :*
- `incrementer_compteur()` - Incrémente le compteur d'emprunts
- `reset_compteur()` - Réinitialise le compteur
- `est_disponible()` - Vérifie la disponibilité
- `incrementer_exemplaire_disponible()` - Incrémente lors d'un retour
- `decrementer_exemplaire_disponible()` - Décrémente lors d'un emprunt
- `to_dict()` / `from_dict()` - Sérialisation/désérialisation

*Principes POO appliqués :*
- Encapsulation complète (attributs privés)
- Propriétés avec getters/setters
- Validation dans les setters

### 4. Modèle User (`app/models/user.py`)

**Classe `UserType` (Enum)**
- `ETUDIANT` - Étudiant
- `ENSEIGNANT` - Enseignant
- `PERSONNEL_ADMIN` - Personnel administratif

**Classe `User` (abstraite)**

*Attributs :*
- `id_user` - Identifiant unique (format userXX000)
- `nom` - Nom de l'utilisateur
- `type_utilisateur` - Type (UserType)
- `nombre_emprunt_total` - Nombre total d'emprunts dans l'historique
- `list_emprunt` - Liste des emprunts en cours (format JSON)

*Méthodes principales :*
- `limite_emprunts` - Propriété abstraite (implémentée par les classes filles)
- `peut_emprunter()` - Vérifie si l'utilisateur peut emprunter
- `ajouter_emprunt()` - Ajoute un emprunt à la liste
- `retirer_emprunt()` - Retire un emprunt de la liste
- `get_emprunt()` - Récupère un emprunt par son ID
- `nombre_emprunts_en_cours()` - Retourne le nombre d'emprunts actifs
- `to_dict()` / `from_dict()` - Sérialisation/désérialisation

**Classes dérivées :**

1. **`Etudiant`** - Hérite de `User`
   - `limite_emprunts = 4`

2. **`Enseignant`** - Hérite de `User`
   - `limite_emprunts = 6`

3. **`PersonnelAdmin`** - Hérite de `User`
   - `limite_emprunts = 0` (ne peut pas emprunter)

*Principes POO appliqués :*
- Classe abstraite avec `ABC`
- Héritage (Etudiant, Enseignant, PersonnelAdmin)
- Polymorphisme avec `limite_emprunts`
- Encapsulation complète

### 5. Modèle Loan (`app/models/loan.py`)

**Classe `Loan`**

*Attributs :*
- `id_emprunt` - Identifiant unique (format empruntXX000)
- `date_emprunt` - Date de l'emprunt (format JJ/MM/AAAA)
- `date_retour_prevue` - Date de retour prévue (format JJ/MM/AAAA)
- `id_livre` - ISBN du livre emprunté
- `titre_livre` - Titre du livre (copie pour référence)
- `id_utilisateur` - ID de l'utilisateur
- `nom_utilisateur` - Nom de l'utilisateur (copie pour référence)
- `penalites` - Montant des pénalités en cas de retard

*Méthodes principales :*
- `verification_disponibilite(livre)` - Vérifie si le livre est disponible
- `emprunter(livre, utilisateur)` - Effectue l'emprunt et met à jour les objets
- `retourner(livre, utilisateur)` - Retourne le livre et le rend disponible
- `detecter_retard()` - Calcule le nombre de jours de retard (utilise DATE_ACTUEL ou date système)
- `calculer_penalites(taux_par_jour)` - Calcule les pénalités basées sur le retard
- `to_dict()` / `from_dict()` - Sérialisation/désérialisation

*Relations :*
- Référence un `Book` via `id_livre`
- Référence un `User` via `id_utilisateur`

### 6. Modèle Reservation (`app/models/reservation.py`)

**Classe `Reservation`**

*Attributs :*
- `id_reservation` - Identifiant unique (format reservationXX000)
- `date_reservation` - Date de la réservation (format JJ/MM/AAAA)
- `id_livre` - ISBN du livre réservé
- `titre_livre` - Titre du livre
- `id_utilisateur` - ID de l'utilisateur
- `nom_utilisateur` - Nom de l'utilisateur
- `date_emprunt` - Date souhaitée pour l'emprunt (format JJ/MM/AAAA)
- `date_retour_prevue` - Date de retour prévue souhaitée (format JJ/MM/AAAA)
- `position_file` - Position dans la file d'attente

*Gestion de la file d'attente :*
- Dictionnaire statique `_files_attente` organisant les réservations par ISBN
- Réservations triées par date de réservation (premier arrivé, premier servi)
- Position calculée automatiquement

*Méthodes principales :*
- `reserver(livre, utilisateur)` - Effectue la réservation et ajoute à la file
- `annuler_reservation(livre)` - Annule et retire de la file
- `get_file_attente(id_livre)` - Retourne la file pour un livre
- `get_prochaine_reservation(id_livre)` - Retourne la première réservation
- `notifier_disponibilite(livre)` - Notifie la première personne quand un livre devient disponible (écrit dans `reservation.log`)
- `to_dict()` / `from_dict()` - Sérialisation/désérialisation

*Relations :*
- Référence un `Book` via `id_livre`
- Référence un `User` via `id_utilisateur`
- Peut se transformer en `Loan` lorsque le livre devient disponible

---

## 📅 Système de dates

### Format uniforme : JJ/MM/AAAA

**Décision :** Utiliser le format JJ/MM/AAAA (exemple: 27/12/2025) dans toute l'application.

### Implémentation

**Constantes ajoutées (`app/utils/constants.py`) :**
- `DATE_FORMAT = "%d/%m/%Y"` - Format Python pour strftime/strptime
- `DATE_FORMAT_DISPLAY = "JJ/MM/AAAA"` - Format d'affichage

**Fonctions utilitaires (`app/utils/validators.py`) :**

1. **`format_date(date_obj)`**
   - Formate un objet `datetime` en chaîne JJ/MM/AAAA
   - Exemple : `datetime(2025, 12, 27)` → `"27/12/2025"`

2. **`parse_date(date_str)`**
   - Parse une chaîne JJ/MM/AAAA en objet `datetime`
   - Exemple : `"27/12/2025"` → `datetime(2025, 12, 27)`
   - Lève `ValueError` si le format est invalide

3. **`get_current_date()`**
   - Retourne la date actuelle au format JJ/MM/AAAA
   - Utilise la variable d'environnement `DATE_ACTUEL` si définie (pour les tests)
   - Sinon utilise la date système actuelle

### Mise à jour des modèles

**Loan :**
- Toutes les dates utilisent le format JJ/MM/AAAA
- `detecter_retard()` utilise `parse_date()` et `get_current_date()`

**Reservation :**
- Toutes les dates utilisent le format JJ/MM/AAAA
- Notifications dans le log utilisent le nouveau format

### Variable d'environnement DATE_ACTUEL

Pour les tests et la simulation :
```python
import os
os.environ["DATE_ACTUEL"] = "27/12/2025"  # Format JJ/MM/AAAA
```

---

## 📚 Documentation

### 1. Documentation des modèles (`app/models/model.md`)

Documentation complète expliquant :
- Description de chaque modèle (User, Book, Loan, Reservation)
- Attributs et méthodes principales
- Relations entre les modèles
- Schéma des relations
- Cycle de vie (Réservation → Emprunt)
- Contraintes et règles métier
- Principes POO appliqués
- Exemples d'utilisation

### 2. README principal (`readme.md`)

Documentation utilisateur comprenant :
- Présentation du projet
- Prérequis (Python 3.8+)
- Instructions d'installation (git clone, etc.)
- Démarrage de l'application (`python app/main.py`)
- Navigation dans l'application (menu principal, options)
- Structure du projet
- Fonctionnalités principales
- Liste des contributeurs
- Dépannage

### 3. Journal de développement (`ramos_daily.md`)

Ce fichier documente :
- Toutes les étapes de développement depuis l'initialisation
- Structure de base créée
- Développement des modèles
- Système de dates
- Fonctionnalités implémentées

---

## ✅ Récapitulatif des réalisations

### Structure du projet
- ✅ Architecture modulaire créée
- ✅ Dossiers et fichiers organisés
- ✅ Structure respectant les principes POO

### Interface utilisateur
- ✅ Menu principal avec navigation
- ✅ Message de bienvenue (MOTD)
- ✅ Gestion des erreurs et interruptions
- ✅ Structure prête pour l'implémentation des fonctionnalités

### Modèles développés
- ✅ **Book** : Modèle complet avec statuts, exemplaires multiples
- ✅ **User** : Classe abstraite avec héritage (Etudiant, Enseignant, PersonnelAdmin)
- ✅ **Loan** : Gestion complète des emprunts avec pénalités et retards
- ✅ **Reservation** : File d'attente et notifications

### Utilitaires
- ✅ Génération d'IDs uniques réutilisables
- ✅ Validation d'ISBN
- ✅ Formatage et parsing de dates (JJ/MM/AAAA)
- ✅ Constantes centralisées

### Documentation
- ✅ Documentation des modèles
- ✅ README utilisateur
- ✅ Journal de développement

---

## 🎯 Prochaines étapes

### À implémenter (structure prête)

1. **Services** (`app/services/`)
   - Implémentation de la logique métier
   - CRUD pour chaque entité
   - Recherche avancée
   - Génération de rapports

2. **Persistance des données** (`app/services/file_manager.py`)
   - Sauvegarde/chargement depuis fichiers
   - Format JSON ou TXT

3. **Journalisation** (`app/services/logger.py`)
   - Logs de toutes les actions
   - Fichiers de log organisés

4. **Fonctionnalités dans main.py**
   - Implémentation des menus de gestion
   - Intégration avec les services

---

## 📝 Notes techniques

### Principes POO respectés

1. **Encapsulation**
   - Tous les attributs sont privés (préfixe `_`)
   - Accès via propriétés (getters/setters)
   - Validation dans les setters

2. **Héritage**
   - `User` est une classe abstraite de base
   - `Etudiant`, `Enseignant`, `PersonnelAdmin` héritent de `User`

3. **Polymorphisme**
   - Méthode abstraite `limite_emprunts` implémentée différemment
   - Instances traitées uniformément via la classe de base

4. **Abstraction**
   - Classe abstraite `User` avec `ABC`
   - Méthodes abstraites définies

### Format de données

- **Dates :** JJ/MM/AAAA (exemple: 27/12/2025)
- **IDs :** Format XX000 avec préfixe optionnel
  - Book : `Ab123`
  - User : `userAb123`
  - Loan : `empruntXy456`
  - Reservation : `reservationCd789`

### Gestion des erreurs

- Validation des entrées utilisateur
- Messages d'erreur explicites
- Gestion des exceptions

---

## 🏁 Conclusion

L'architecture de base de l'application est complète et prête pour l'implémentation des services. Tous les modèles sont développés avec une approche orientée objet rigoureuse, respectant les principes d'encapsulation, d'héritage et de polymorphisme.

L'application dispose d'une structure solide et modulaire qui facilitera l'ajout des fonctionnalités de service et de persistance.

---

**Date de dernière mise à jour :** Décembre 2025  
**Statut :** Architecture de base complète, modèles développés, documentation créée

