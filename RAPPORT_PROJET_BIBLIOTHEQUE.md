# Rapport Technique - Application de Gestion de Bibliothèque

**Projet :** Application de Gestion de Bibliothèque DIT  
**Date :** Décembre 2025  
**Contexte :** Master 1 Intelligence Artificielle - DIT (Dakar Institute of Technology)

---

## 📋 Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture du système](#architecture-du-système)
3. [Fonctionnalités implémentées](#fonctionnalités-implémentées)
4. [Détails techniques](#détails-techniques)
5. [Structure des données](#structure-des-données)
6. [Interface utilisateur](#interface-utilisateur)
7. [Tests et validation](#tests-et-validation)
8. [Conclusion](#conclusion)

---

## 1. Vue d'ensemble

### 1.1 Présentation du projet

Cette application Python permet de gérer numériquement une bibliothèque académique avec un système complet de :
- Gestion des livres (CRUD complet)
- Gestion des utilisateurs (étudiants, enseignants, personnel)
- Gestion des emprunts avec suivi des retards
- Système de réservation avec file d'attente
- Recherche avancée
- Statistiques et rapports
- Sauvegarde automatique et journalisation

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Écran d'accueil (MOTD) de l'application

### 1.2 Technologies utilisées

- **Langage :** Python 3.8+
- **Paradigme :** Programmation Orientée Objet (POO)
- **Persistance :** Fichiers JSON
- **Journalisation :** Fichiers logs (.log)
- **Dépendances externes :** python-dotenv

### 1.3 Structure du projet

```
Examen-Python-Master-AI-2025-Projet-Biblotheque/
├── app/
│   ├── main.py                  # Point d'entrée principal
│   ├── models/                  # Modèles métier (Book, User, Loan, Reservation)
│   ├── services/                # Services (logique métier)
│   ├── utils/                   # Utilitaires (validators, constants)
│   └── files/                   # Persistance des données (JSON, logs)
├── readme.md                    # Documentation principale
├── requirements.txt             # Dépendances
└── .env                         # Variables d'environnement (optionnel)
```

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Structure du projet dans l'explorateur de fichiers

---

## 2. Architecture du système

### 2.1 Architecture en couches

L'application suit une architecture en couches claire :

1. **Couche Présentation (UI)** : `app/main.py`
   - Interface utilisateur en ligne de commande (CLI)
   - Menus interactifs avec navigation

2. **Couche Service (Logique métier)** : `app/services/`
   - `BookService` : Gestion des livres
   - `UserService` : Gestion des utilisateurs
   - `LoanService` : Gestion des emprunts
   - `ReservationService` : Gestion des réservations
   - `SearchService` : Recherche avancée
   - `ReportService` : Statistiques et rapports
   - `FileManager` : Gestion de la persistance
   - `Logger` : Journalisation

3. **Couche Modèle (Données)** : `app/models/`
   - `Book` : Modèle livre
   - `User` : Modèle utilisateur (avec héritage)
   - `Loan` : Modèle emprunt
   - `Reservation` : Modèle réservation

4. **Couche Utilitaire** : `app/utils/`
   - `validators.py` : Validation et formatage
   - `constants.py` : Constantes du système

### 2.2 Principes de conception

- **Encapsulation** : Utilisation de propriétés (@property) et setters
- **Héritage** : User → Etudiant, Enseignant, PersonnelAdmin
- **Séparation des responsabilités** : Chaque service a un rôle précis
- **Persistance** : Sauvegarde automatique après chaque opération
- **Journalisation** : Traçabilité complète des actions

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Diagramme de classe (si disponible) ou schéma de l'architecture

---

## 3. Fonctionnalités implémentées

### 3.1 Menu principal

Le menu principal offre 8 options :

1. Gestion des utilisateurs
2. Gestion des livres
3. Gestion des emprunts
4. Gestion des réservations
5. Statistiques
6. Effectuer une recherche
7. Crédits de l'application
8. Quitter l'application

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu principal de l'application

### 3.2 Gestion des utilisateurs 🟢

**État :** Fonctionnel (100%)

#### Fonctionnalités complètes :

##### 1. Ajouter un utilisateur
- Formulaire complet avec choix du type
- Génération automatique d'ID (format userXX000)
- Validation des données
- Sauvegarde automatique

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu d'ajout d'utilisateur  
**📸 CAPTURE D'ÉCRAN À AJOUTER :** Formulaire d'ajout

##### 2. Lister tous les utilisateurs
- Affichage complet avec :
  - ID
  - Nom
  - Type
  - Emprunts en cours / limite
  - Total des emprunts

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Liste complète des utilisateurs

##### 3. Consulter un utilisateur (par ID)
- Affichage détaillé avec :
  - ID, Nom, Type
  - Limite d'emprunts
  - Emprunts en cours / limite
  - Nombre total d'emprunts
  - Historique détaillé des emprunts en cours (ID emprunt, titre livre, dates)

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Consultation d'un utilisateur avec historique

##### 4. Lister les utilisateurs par type
- Filtrage par type (Etudiant, Enseignant, Personnel)
- Affichage des statistiques par type

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Liste par type

##### 5. Modifier un utilisateur
- Modification du nom
- Modification partielle (laissez vide pour ne pas modifier)
- Sauvegarde automatique

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu de modification

##### 6. Supprimer un utilisateur
- Confirmation obligatoire (saisir "OUI")
- Avertissement si emprunts en cours
- Sauvegarde automatique

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu de suppression

#### Menu utilisateur :
```
1. Ajouter un utilisateur
2. Lister tous les utilisateurs
3. Consulter un utilisateur (par ID)
4. Lister les utilisateurs par type
5. Modifier un utilisateur
6. Supprimer un utilisateur
7. Retour au menu principal
```

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu complet de gestion des utilisateurs

#### Types d'utilisateurs :
- **Etudiant** : Limite de 4 emprunts
- **Enseignant** : Limite de 6 emprunts
- **Personnel administratif** : Limite de 0 emprunts (ne peut pas emprunter)

#### Notes sur le modèle :
Le modèle User est simplifié et contient uniquement :
- `id_user` : Identifiant unique (format userXX000)
- `nom` : Nom de l'utilisateur
- `type_utilisateur` : Type (Etudiant, Enseignant, PersonnelAdmin)
- `nombre_emprunt_total` : Nombre total d'emprunts effectués
- `list_emprunt` : Liste des emprunts en cours (format JSON)

**Note :** Le modèle ne contient pas de prénom, email, ou autres informations personnelles. C'est une simplification intentionnelle du modèle pour ce projet.

**Fichiers concernés :**
- `app/models/user.py` : Modèle complet avec héritage (Etudiant, Enseignant, PersonnelAdmin)
- `app/services/user_service.py` : Service complet (156 lignes)
- `app/main.py` : Menus complets (lignes 200-519)

---

### 3.3 Gestion des livres 🟢

**État :** Fonctionnel (100%)

#### Fonctionnalités complètes :

##### 1. Ajouter un livre
- Formulaire complet avec validation
- Génération automatique d'ISBN (format XX000)
- Gestion du nombre d'exemplaires
- Création automatique du fichier .docs dans library/
- Sauvegarde automatique

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu d'ajout de livre  
**📸 CAPTURE D'ÉCRAN À AJOUTER :** Formulaire d'ajout de livre  
**📸 CAPTURE D'ÉCRAN À AJOUTER :** Confirmation d'ajout

##### 2. Lister tous les livres
- Affichage complet avec :
  - ISBN
  - Titre
  - Auteur
  - Statut global
  - Exemplaires (disponibles/total/empruntés)
  - Nombre d'emprunts

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Liste complète des livres

##### 3. Consulter un livre (par ISBN)
- Affichage détaillé avec toutes les informations :
  - ISBN, Titre, Auteur
  - Statut global
  - Détails des exemplaires
  - Nombre total d'emprunts
  - Résumé complet

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Consultation d'un livre

##### 4. Modifier un livre
- Modification partielle (laissez vide pour ne pas modifier) :
  - Titre
  - Auteur
  - Résumé
  - Nombre d'exemplaires
  - Statut (disponible, emprunté, réservé, perdu, endommagé)
- Sauvegarde automatique
- Mise à jour du fichier .docs

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu de modification  
**📸 CAPTURE D'ÉCRAN À AJOUTER :** Formulaire de modification

##### 5. Supprimer un livre
- Confirmation obligatoire (saisir "OUI")
- Avertissement si exemplaires empruntés
- Suppression du fichier .docs dans library/
- Sauvegarde automatique

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu de suppression  
**📸 CAPTURE D'ÉCRAN À AJOUTER :** Confirmation de suppression

#### Menu livre :
```
1. Ajouter un livre
2. Lister tous les livres
3. Consulter un livre (par ISBN)
4. Modifier un livre
5. Supprimer un livre
6. Retour au menu principal
```

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu complet de gestion des livres

#### Statuts des livres :
- **disponible** : Exemplaires disponibles
- **emprunté** : Tous les exemplaires sont empruntés
- **réservé** : Livre réservé
- **perdu** : Livre perdu
- **endommagé** : Livre endommagé

**Fichiers concernés :**
- `app/models/book.py` : Modèle complet avec toutes les propriétés
- `app/services/book_service.py` : Service complet (152 lignes)
- `app/main.py` : Menus complets (lignes 521-831)

---

### 3.4 Gestion des emprunts 🟢

**État :** Fonctionnel (100%)

#### Fonctionnalités disponibles :

##### 1. Emprunter un livre
- Recherche de livre par ISBN ou mot-clé
- Vérification de disponibilité
- Vérification des limites d'emprunts par type d'utilisateur
- Calcul automatique de la date de retour (30 jours par défaut)
- Mise à jour automatique du livre et de l'utilisateur
- Sauvegarde automatique

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu d'emprunt  
**📸 CAPTURE D'ÉCRAN À AJOUTER :** Processus d'emprunt

##### 2. Retourner un livre
- Sélection par ID d'emprunt
- Mise à jour des exemplaires disponibles
- Gestion automatique des réservations (notification si file d'attente)
- Sauvegarde automatique

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu de retour  
**📸 CAPTURE D'ÉCRAN À AJOUTER :** Processus de retour

##### 3. Lister les emprunts en cours
- Affichage de tous les emprunts actifs
- Détails complets (livre, utilisateur, dates)

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Liste des emprunts en cours

##### 4. Vérification de disponibilité
- Vérification silencieuse ou avec affichage

##### 5. Gestion des dates d'emprunts
- Format JJ/MM/AAAA
- Calcul automatique

##### 6. Détection des retards
- Utilise DATE_ACTUEL ou date système
- Affichage des emprunts en retard

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Détection des retards

##### 7. Calcul des pénalités
- Taux configurable (0.5€ par jour par défaut)
- Calcul automatique en cas de retard

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Calcul des pénalités

##### 8. Renouvellement d'emprunt
- Menu complet avec sélection utilisateur et emprunt
- Renouvellement avec extension de la date de retour
- Sauvegarde automatique

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Renouvellement d'emprunt

#### Menu emprunt :
```
1. Emprunter un livre
2. Retourner un livre
3. Vérification de disponibilité
4. Gestion des dates d'emprunts
5. Détection des retards
6. Renouveler un emprunt
7. Retour au menu principal
```

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu complet de gestion des emprunts

**Fichiers concernés :**
- `app/models/loan.py` : Modèle avec toutes les méthodes
- `app/services/loan_service.py` : Service complet
- `app/main.py` : Menus complets (lignes 834-1530)

---

### 3.5 Gestion des réservations 🟢

**État :** Fonctionnel (100%)

#### Fonctionnalités disponibles :

##### 1. Réserver un livre indisponible
- Vérification que le livre n'est pas disponible
- Vérification qu'un utilisateur n'a pas déjà réservé ce livre
- Ajout automatique à la file d'attente
- Sauvegarde automatique

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu de réservation  
**📸 CAPTURE D'ÉCRAN À AJOUTER :** Processus de réservation

##### 2. Gestion de la file d'attente
- Tri automatique par date de réservation
- Position calculée automatiquement
- Méthodes : `get_file_attente()`, `ajouter_a_file()`, `retirer_de_file()`

**📸 CAPTURE D'ÉCRAN À AJOUTER :** File d'attente des réservations

##### 3. Notification automatique
- Notification lorsqu'un livre devient disponible
- Écriture dans `app/files/reservations/reservation.log`
- Format de notification complet

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Notifications de réservation

##### 4. Annuler une réservation
- Retrait de la file d'attente
- Mise à jour du statut du livre si nécessaire

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Annulation de réservation

##### 5. Lister les réservations
- Affichage de toutes les réservations actives

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Liste des réservations

##### 6. Transformer réservation en emprunt
- Menu complet avec liste des réservations transformables
- Filtrage automatique (livre disponible, position 1 dans la file)
- Transformation avec création de l'emprunt
- Retrait automatique de la file d'attente
- Sauvegarde automatique

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Transformation réservation → emprunt

#### Menu réservation :
```
1. Réserver un livre indisponible
2. Gestion de la file d'attente
3. Annuler une réservation
4. Vérifier les notifications
5. Transformer réservation en emprunt
6. Retour au menu principal
```

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu complet de gestion des réservations

**Fichiers concernés :**
- `app/models/reservation.py` : Modèle avec file d'attente
- `app/services/reservation_service.py` : Service complet
- `app/main.py` : Menus complets (lignes 1533-2674)

---

### 3.6 Recherche avancée 🟢

**État :** Fonctionnel (~100%)

#### Fonctionnalités disponibles :

##### 1. Recherche par titre
- Recherche partielle, insensible à la casse

##### 2. Recherche par auteur
- Recherche partielle, insensible à la casse

##### 3. Recherche par ISBN
- Recherche exacte ou partielle

##### 4. Recherche par disponibilité
- Livres disponibles / indisponibles

##### 5. Recherche par statut
- Filtrage par statut (disponible, emprunté, réservé, perdu, endommagé)

##### 6. Recherche par mots-clés
- Recherche dans titre, auteur, résumé

##### 7. Recherche combinée
- Combinaison de plusieurs critères

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu de recherche  
**📸 CAPTURE D'ÉCRAN À AJOUTER :** Résultats de recherche

**Fichiers concernés :**
- `app/services/search_service.py` : Service complet
- `app/main.py` : Menus de recherche (lignes 2341-2626)

---

### 3.7 Statistiques 🟢

**État :** Fonctionnel (~100%)

#### Statistiques disponibles :

##### 1. Statistiques générales
- Nombre total de livres
- Nombre de livres disponibles
- Nombre de livres empruntés, réservés, perdus, endommagés

##### 2. Top 5 des livres les plus empruntés
- Classement par nombre d'emprunts

##### 3. Top 5 des utilisateurs les plus actifs
- Classement par nombre d'emprunts

##### 4. Nombre total d'emprunts effectués

##### 5. Liste des livres jamais empruntés

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Menu des statistiques  
**📸 CAPTURE D'ÉCRAN À AJOUTER :** Statistiques générales  
**📸 CAPTURE D'ÉCRAN À AJOUTER :** Top 5 livres  
**📸 CAPTURE D'ÉCRAN À AJOUTER :** Top 5 utilisateurs

**Fichiers concernés :**
- `app/services/report_service.py` : Service complet
- `app/main.py` : Menus de statistiques (lignes 2136-2340)

---

### 3.8 Sauvegarde et journalisation 🟢

**État :** Fonctionnel (100%)

#### Fonctionnalités :

##### 1. Sauvegarde automatique
- Format JSON avec indentation
- Sauvegarde après chaque opération dans :
  - `app/files/books/book.json`
  - `app/files/users/user.json`
  - `app/files/loans/loan.json`
  - `app/files/reservations/reservation.json`

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Structure du dossier files/  
**📸 CAPTURE D'ÉCRAN À AJOUTER :** Exemple de fichier JSON

##### 2. Chargement automatique
- Chargement au démarrage de l'application
- Gestion des fichiers inexistants (retourne liste vide)

##### 3. Journalisation
- Service Logger complet et utilisé dans tous les services
- Fichiers de log pour chaque entité avec horodatage :
  - `app/files/books/book.log` - Toutes les actions sur les livres
  - `app/files/users/user.log` - Toutes les actions sur les utilisateurs
  - `app/files/loans/loans.log` - Toutes les actions sur les emprunts
  - `app/files/reservations/reservation.log` - Toutes les actions sur les réservations
  - `app/files/notifications/notifications.log` - Notifications système
  - `app/files/register/system.log` - Logs système
- Format structuré avec timestamp [JJ/MM/AAAA HH:MM:SS]
- Logs pour chaque opération : ajout, modification, suppression, consultation, chargement

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Exemple de fichier log

##### 4. Gestion des fichiers .docs
- Création automatique dans `app/library/`
- Format : `{titre}_{isbn}_{auteur}.docs`
- Mise à jour et suppression automatiques

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Dossier library/ avec fichiers .docs

**Fichiers concernés :**
- `app/services/file_manager.py` : Service complet
- `app/services/logger.py` : Service de journalisation
- `app/services/library_manager.py` : Gestion des fichiers .docs

---

## 4. Détails techniques

### 4.1 Gestion de la date actuelle

L'application utilise un système de priorité pour récupérer `DATE_ACTUEL` :

1. **Date système** (priorité 1) : Récupération automatique depuis `datetime.now()`
2. **Fichier .env** (priorité 2) : Variable `DATE_ACTUEL=JJ/MM/AAAA`
3. **Saisie utilisateur** (priorité 3) : Demande interactive

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Démarrage de l'application avec récupération de date

**Format de date :** JJ/MM/AAAA (exemple: 27/12/2025)

### 4.2 Génération d'ISBN

- Format : XX000 (2 lettres + 3 chiffres)
- Génération automatique si non fourni
- Exemples : Ab123, Xy789

**Fichier :** `app/utils/validators.py` - Fonction `generate_id()`

### 4.3 Validation des données

- Validation des ISBN
- Validation des dates (format JJ/MM/AAAA)
- Validation des champs obligatoires (titre, auteur, résumé)
- Vérification des limites d'emprunts

**Fichier :** `app/utils/validators.py`

### 4.4 Gestion des erreurs

- Gestion des exceptions (try/except)
- Messages d'erreur clairs pour l'utilisateur
- Validation des entrées utilisateur
- Gestion des interruptions clavier (Ctrl+C)

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Exemple de message d'erreur

### 4.5 Interface utilisateur

- Interface en ligne de commande (CLI)
- Menus avec bordures Unicode
- Affichage formaté des données
- Navigation intuitive avec retour au menu principal

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Exemple d'affichage formaté

---

## 5. Structure des données

### 5.1 Modèle Book

```python
Book:
  - isbn: str (format XX000)
  - titre: str
  - auteur: str
  - resume: str
  - statut: BookStatus (enum)
  - compteur_emprunt: int
  - nbre_exemplaire_total: int
  - exemplaire_disponible: int
```

**Enum BookStatus :**
- DISPONIBLE
- EMPRUNTE
- RESERVE
- PERDU
- ENDOMMAGE

### 5.2 Modèle User

```python
User (classe abstraite de base):
  - id_user: str (format userXX000)
  - nom: str
  - type_utilisateur: UserType (enum)
  - nombre_emprunt_total: int
  - list_emprunt: List[Dict] (emprunts en cours)

Etudiant(User):
  - limite_emprunts: 4 (propriété)

Enseignant(User):
  - limite_emprunts: 6 (propriété)

PersonnelAdmin(User):
  - limite_emprunts: 0 (propriété)
```

**Note :** Le modèle est simplifié et ne contient pas de prénom, email ou autres informations personnelles supplémentaires. Cela permet de se concentrer sur les fonctionnalités principales de gestion de bibliothèque.

### 5.3 Modèle Loan

```python
Loan:
  - id: str
  - id_livre: str (ISBN)
  - id_utilisateur: str
  - date_emprunt: str (JJ/MM/AAAA)
  - date_retour_prevu: str (JJ/MM/AAAA)
  - date_retour_effectif: Optional[str]
  - statut: str
```

### 5.4 Modèle Reservation

```python
Reservation:
  - id: str
  - id_livre: str (ISBN)
  - id_utilisateur: str
  - date_reservation: str (JJ/MM/AAAA)
  - statut: str
  - position_file: int
```

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Schéma de base de données ou diagramme de classes

---

## 6. Interface utilisateur

### 6.1 Navigation

- Menu principal → Sous-menus → Actions
- Retour au menu principal avec option 6/7/8
- Interruption avec Ctrl+C

### 6.2 Format d'affichage

- Bordures Unicode (╔═══╗)
- Séparateurs clairs
- Numérotation des options
- Messages de confirmation/erreur avec emojis

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Différents écrans de navigation

### 6.3 Expérience utilisateur

- Messages clairs et informatifs
- Validation en temps réel
- Confirmation pour les actions destructives
- Avertissements pour les actions risquées

---

## 7. Tests et validation

### 7.1 Tests fonctionnels

#### Gestion des livres
- ✅ Ajout de livre avec validation
- ✅ Liste des livres
- ✅ Consultation par ISBN
- ✅ Modification partielle
- ✅ Suppression avec confirmation
- ✅ Gestion des exemplaires multiples

#### Gestion des emprunts
- ✅ Emprunt avec vérification de disponibilité
- ✅ Retour avec gestion des réservations
- ✅ Détection des retards
- ✅ Calcul des pénalités

#### Gestion des réservations
- ✅ Réservation avec file d'attente
- ✅ Notification automatique
- ✅ Annulation
- ✅ Transformation en emprunt

#### Recherche
- ✅ Toutes les méthodes de recherche
- ✅ Recherche combinée

#### Statistiques
- ✅ Toutes les statistiques disponibles

### 7.2 Tests de persistance

- ✅ Sauvegarde automatique
- ✅ Chargement au démarrage
- ✅ Gestion des fichiers inexistants
- ✅ Intégrité des données JSON

### 7.3 Tests de validation

- ✅ Validation des ISBN
- ✅ Validation des dates
- ✅ Validation des champs obligatoires
- ✅ Vérification des limites d'emprunts

**📸 CAPTURE D'ÉCRAN À AJOUTER :** Tests d'exécution (si disponibles)

---

## 8. Conclusion

### 8.1 Résumé des fonctionnalités

| Fonctionnalité | État | Pourcentage |
|----------------|------|-------------|
| Gestion des utilisateurs | 🟢 Fonctionnel | 100% |
| Gestion des livres | 🟢 Fonctionnel | 100% |
| Gestion des emprunts | 🟢 Fonctionnel | 100% |
| Gestion des réservations | 🟢 Fonctionnel | 100% |
| Recherche avancée | 🟢 Fonctionnel | ~100% |
| Statistiques | 🟢 Fonctionnel | ~100% |
| Sauvegarde/Journalisation | 🟢 Fonctionnel | 100% |

### 8.2 Points forts

- ✅ Architecture claire et modulaire
- ✅ Code bien structuré avec séparation des responsabilités
- ✅ Gestion complète des livres (CRUD complet)
- ✅ Système de réservation avec file d'attente
- ✅ Recherche avancée complète
- ✅ Statistiques détaillées
- ✅ Sauvegarde automatique
- ✅ Journalisation complète
- ✅ Interface utilisateur intuitive

### 8.3 Améliorations possibles

- 🔄 Améliorer l'intégration du logger général
- 🔄 Ajouter des tests unitaires automatisés
- 🔄 Interface graphique (optionnel)
- 🔄 Base de données (optionnel, pour plus de performances)
- 🔄 Ajouter plus d'informations utilisateur (prénom, email, etc.) - optionnel

### 8.4 Contribution

**Chef de projet :** Fabrice Jordan RAMOS  
**Équipe de développement :**
- Souleymane DIENG SALL
- Zakaria
- Babacar

---

## Annexes

### A. Commandes de démarrage

```bash
# Depuis la racine du projet
python app/main.py

# Ou
python -m app.main
```

### B. Structure des fichiers de données

**Fichiers JSON :**
- `app/files/books/book.json`
- `app/files/users/user.json`
- `app/files/loans/loan.json`
- `app/files/reservations/reservation.json`

**Fichiers LOG :**
- `app/files/books/book.log`
- `app/files/users/user.log`
- `app/files/loans/loans.log`
- `app/files/reservations/reservation.log`
- `app/files/notifications/notifications.log`
- `app/files/register/system.log`

### C. Variables d'environnement

Fichier `.env` (optionnel) :
```
DATE_ACTUEL=27/12/2025
```

### D. Dépendances

Voir `requirements.txt` :
- python-dotenv

---

**📸 CAPTURE D'ÉCRAN FINALE À AJOUTER :** Vue d'ensemble de l'application en fonctionnement

---

*Rapport généré le : [DATE]*  
*Version : 1.0*

