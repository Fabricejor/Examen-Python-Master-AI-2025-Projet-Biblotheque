# Documentation des Modèles - Application de Gestion de Bibliothèque

## Vue d'ensemble

Cette application utilise une architecture orientée objet avec 4 modèles principaux : **User**, **Book**, **Loan** et **Reservation**. Chaque modèle représente une entité métier et entretient des relations avec les autres modèles.

---

## 1. Modèle User (Utilisateur)

### Description
Le modèle `User` représente un utilisateur de la bibliothèque. C'est une classe abstraite qui sert de base pour trois types d'utilisateurs spécifiques.

### Attributs principaux
- `id_user` : Identifiant unique (format: `userXX000`)
- `nom` : Nom de l'utilisateur
- `type_utilisateur` : Type d'utilisateur (Étudiant, Enseignant, Personnel_admin)
- `nombre_emprunt_total` : Nombre total d'emprunts effectués dans l'historique
- `list_emprunt` : Liste des emprunts actuellement en cours (format JSON)

### Classes dérivées (Héritage)
Le modèle `User` utilise le polymorphisme avec trois classes filles :

1. **Etudiant** : Limite de 4 emprunts simultanés
2. **Enseignant** : Limite de 6 emprunts simultanés
3. **PersonnelAdmin** : Limite de 0 emprunt (ne peut pas emprunter)

### Relations
- **User ↔ Loan** : Un utilisateur peut avoir plusieurs emprunts (1-N)
- **User ↔ Reservation** : Un utilisateur peut avoir plusieurs réservations (1-N)

---

## 2. Modèle Book (Livre)

### Description
Le modèle `Book` représente un livre de la bibliothèque avec ses caractéristiques et son état.

### Attributs principaux
- `isbn` : Identifiant unique du livre (format: `XX000`)
- `titre` : Titre du livre
- `auteur` : Auteur du livre
- `resume` : Résumé du livre
- `statut` : Statut actuel (disponible, emprunté, réservé, perdu, endommagé)
- `compteur_emprunt` : Nombre total de fois que le livre a été emprunté
- `nbre_exemplaire_total` : Nombre total d'exemplaires du livre
- `exemplaire_disponible` : Nombre d'exemplaires actuellement disponibles

### Statuts possibles (BookStatus)
- `DISPONIBLE` : Le livre est disponible pour l'emprunt
- `EMPRUNTE` : Le livre est actuellement emprunté
- `RESERVE` : Le livre est réservé (en attente)
- `PERDU` : Le livre a été perdu
- `ENDOMmage` : Le livre est endommagé

### Relations
- **Book ↔ Loan** : Un livre peut être emprunté plusieurs fois (1-N)
- **Book ↔ Reservation** : Un livre peut avoir plusieurs réservations en file d'attente (1-N)

---

## 3. Modèle Loan (Emprunt)

### Description
Le modèle `Loan` représente un emprunt de livre par un utilisateur. Il fait le lien entre un `User` et un `Book`.

### Attributs principaux
- `id_emprunt` : Identifiant unique (format: `empruntXX000`)
- `date_emprunt` : Date de l'emprunt (format: JJ/MM/AAAA)
- `date_retour_prevue` : Date de retour prévue (format: JJ/MM/AAAA)
- `id_livre` : ISBN du livre emprunté
- `titre_livre` : Titre du livre (copie pour référence)
- `id_utilisateur` : ID de l'utilisateur qui a emprunté
- `nom_utilisateur` : Nom de l'utilisateur (copie pour référence)
- `penalites` : Montant des pénalités en cas de retard

### Méthodes principales
- `verification_disponibilite(livre)` : Vérifie si un livre est disponible
- `emprunter(livre, utilisateur)` : Effectue l'emprunt et met à jour les objets associés
- `retourner(livre, utilisateur)` : Retourne le livre et le rend disponible
- `detecter_retard()` : Calcule le nombre de jours de retard
- `calculer_penalites()` : Calcule les pénalités basées sur le retard

### Relations
- **Loan ↔ User** : Un emprunt appartient à un utilisateur (N-1)
  - `id_utilisateur` référence `User.id_user`
- **Loan ↔ Book** : Un emprunt concerne un livre (N-1)
  - `id_livre` référence `Book.isbn`

### Conditions de création
Pour qu'un `Loan` puisse être créé :
1. Le livre doit être disponible (`Book.est_disponible()` retourne `True`)
2. Le livre doit avoir des exemplaires disponibles (`exemplaire_disponible > 0`)
3. L'utilisateur doit pouvoir emprunter (`User.peut_emprunter()` retourne `True`)
4. L'utilisateur ne doit pas avoir atteint sa limite d'emprunts

---

## 4. Modèle Reservation (Réservation)

### Description
Le modèle `Reservation` représente une réservation de livre par un utilisateur lorsque le livre n'est pas disponible. Les réservations sont organisées en file d'attente par livre.

### Attributs principaux
- `id_reservation` : Identifiant unique (format: `reservationXX000`)
- `date_reservation` : Date de la réservation (format: JJ/MM/AAAA)
- `id_livre` : ISBN du livre réservé
- `titre_livre` : Titre du livre (copie pour référence)
- `id_utilisateur` : ID de l'utilisateur qui a réservé
- `nom_utilisateur` : Nom de l'utilisateur (copie pour référence)
- `date_emprunt` : Date souhaitée pour l'emprunt (format: JJ/MM/AAAA)
- `date_retour_prevue` : Date de retour prévue souhaitée (format: JJ/MM/AAAA)
- `position_file` : Position dans la file d'attente pour ce livre (1 = premier)

### File d'attente
- Les réservations sont organisées par livre (ISBN) dans un dictionnaire statique `_files_attente`
- Les réservations sont triées par date de réservation (la plus ancienne en premier)
- La position dans la file est calculée automatiquement

### Méthodes principales
- `reserver(livre, utilisateur)` : Effectue la réservation et ajoute à la file d'attente
- `annuler_reservation(livre)` : Annule la réservation et la retire de la file
- `notifier_disponibilite(livre)` : Notifie la première personne dans la file lorsqu'un livre devient disponible (écrit dans `reservation.log`)

### Relations
- **Reservation ↔ User** : Une réservation appartient à un utilisateur (N-1)
  - `id_utilisateur` référence `User.id_user`
- **Reservation ↔ Book** : Une réservation concerne un livre (N-1)
  - `id_livre` référence `Book.isbn`

### Conditions de création
Pour qu'une `Reservation` puisse être créée :
1. Le livre ne doit **PAS** être disponible (`Book.est_disponible()` retourne `False`)
2. L'utilisateur ne doit pas avoir déjà une réservation pour ce livre
3. L'utilisateur doit pouvoir emprunter (vérifie la limite d'emprunts)

---

## Relations entre les modèles

### Schéma des relations

```
┌─────────┐         ┌─────────┐
│  User   │         │  Book   │
│         │         │         │
│ id_user │◄──┐     │ isbn    │◄──┐
│ nom     │   │     │ titre   │   │
│ type    │   │     │ statut  │   │
└─────────┘   │     └─────────┘   │
              │                    │
              │                    │
      ┌───────┘                    └───────┐
      │                                    │
      │                                    │
┌─────┴──────┐                    ┌───────┴──────┐
│   Loan     │                    │ Reservation  │
│            │                    │              │
│ id_emprunt │                    │ id_reservation│
│ id_user    │                    │ id_user      │
│ id_livre   │                    │ id_livre     │
│ date_emp   │                    │ date_reserv  │
│ date_retour│                    │ position_file│
└────────────┘                    └──────────────┘
```

### Relations détaillées

1. **User ↔ Loan (1-N)**
   - Un utilisateur peut avoir plusieurs emprunts
   - Un emprunt appartient à un seul utilisateur
   - Relation via `Loan.id_utilisateur = User.id_user`
   - Les emprunts actifs sont stockés dans `User.list_emprunt`

2. **Book ↔ Loan (1-N)**
   - Un livre peut être emprunté plusieurs fois (historique)
   - Un emprunt concerne un seul livre
   - Relation via `Loan.id_livre = Book.isbn`
   - Le compteur d'emprunts est incrémenté dans `Book.compteur_emprunt`

3. **User ↔ Reservation (1-N)**
   - Un utilisateur peut avoir plusieurs réservations
   - Une réservation appartient à un seul utilisateur
   - Relation via `Reservation.id_utilisateur = User.id_user`

4. **Book ↔ Reservation (1-N)**
   - Un livre peut avoir plusieurs réservations (file d'attente)
   - Une réservation concerne un seul livre
   - Relation via `Reservation.id_livre = Book.isbn`
   - Les réservations sont organisées en file d'attente par livre

---

## Cycle de vie : Réservation → Emprunt

### Transformation d'une réservation en emprunt

Une `Reservation` peut devenir un `Loan` lorsque :

1. **Le livre devient disponible** : `Book.exemplaire_disponible > 0` et `Book.statut = DISPONIBLE`

2. **La première personne dans la file est notifiée** :
   - `Reservation.notifier_disponibilite(livre)` est appelée
   - La notification est écrite dans `reservation.log`
   - L'utilisateur en position 1 peut maintenant créer un `Loan`

3. **Création de l'emprunt** :
   - Un nouveau `Loan` est créé avec les informations de la réservation
   - `Loan.date_emprunt` peut utiliser `Reservation.date_emprunt`
   - `Loan.date_retour_prevue` peut utiliser `Reservation.date_retour_prevue`
   - La réservation est retirée de la file d'attente

### Exemple de workflow

```
1. Livre indisponible → Utilisateur crée une Reservation
   Reservation: id_user, id_livre, position_file=1

2. Livre retourné → Book.exemplaire_disponible = 1
   → Reservation.notifier_disponibilite(livre) appelée
   → Notification écrite dans reservation.log

3. Utilisateur crée un Loan depuis sa réservation
   → Loan créé avec Reservation.date_emprunt et Reservation.date_retour_prevue
   → Reservation retirée de la file d'attente
   → Book.exemplaire_disponible décrémenté
   → Book.statut = EMPRUNTE (si exemplaire_disponible = 0)
```

---

## Contraintes et règles métier

### Contraintes sur les emprunts
- Un utilisateur ne peut pas dépasser sa limite d'emprunts (Étudiant: 4, Enseignant: 6, Personnel: 0)
- Un livre doit avoir au moins un exemplaire disponible pour être emprunté
- Un livre avec `exemplaire_disponible = 0` ne peut pas être emprunté

### Contraintes sur les réservations
- Un utilisateur ne peut pas réserver un livre disponible (il doit l'emprunter directement)
- Un utilisateur ne peut avoir qu'une seule réservation par livre
- Les réservations sont organisées en file d'attente (premier arrivé, premier servi)

### Gestion des exemplaires multiples
- `Book.nbre_exemplaire_total` : Nombre total d'exemplaires
- `Book.exemplaire_disponible` : Nombre d'exemplaires disponibles
- Lors d'un emprunt : `exemplaire_disponible` est décrémenté
- Lors d'un retour : `exemplaire_disponible` est incrémenté
- Le livre est disponible si `exemplaire_disponible > 0`

### Gestion des dates
- Format de date uniforme : **JJ/MM/AAAA** (exemple: 27/12/2025)
- Toutes les dates utilisent ce format dans toute l'application
- Les dates sont gérées via les fonctions utilitaires dans `app.utils.validators`

---

## Principes POO appliqués

### Encapsulation
- Tous les attributs sont privés (préfixe `_`)
- Accès via des propriétés (getters/setters)
- Validation dans les setters

### Héritage
- `User` est une classe abstraite de base
- `Etudiant`, `Enseignant`, `PersonnelAdmin` héritent de `User`
- Utilisation du polymorphisme avec la méthode abstraite `limite_emprunts`

### Polymorphisme
- Chaque type d'utilisateur implémente différemment `limite_emprunts`
- Les instances peuvent être traitées de manière uniforme via la classe de base `User`

### Abstraction
- `User` est une classe abstraite (`ABC`)
- Méthode abstraite `limite_emprunts` qui doit être implémentée par les classes filles

---

## Exemple d'utilisation

```python
from app.models import Book, Etudiant, Loan, Reservation
from app.models.book import BookStatus

# 1. Créer un livre
livre = Book(
    titre="Python Avancé",
    auteur="John Doe",
    resume="Guide Python",
    nbre_exemplaire_total=2
)

# 2. Créer un utilisateur (étudiant)
etudiant = Etudiant(nom="Jean Dupont")
print(etudiant.limite_emprunts)  # 4

# 3. Emprunter un livre
emprunt = Loan(
    id_livre=livre.isbn,
    titre_livre=livre.titre,
    id_utilisateur=etudiant.id_user,
    nom_utilisateur=etudiant.nom
)

if emprunt.verification_disponibilite(livre):
    emprunt.emprunter(livre, etudiant)
    print(f"Emprunt créé: {emprunt.id_emprunt}")

# 4. Si le livre n'est pas disponible, créer une réservation
if not livre.est_disponible():
    reservation = Reservation(
        id_livre=livre.isbn,
        titre_livre=livre.titre,
        id_utilisateur=etudiant.id_user,
        nom_utilisateur=etudiant.nom
    )
    reservation.reserver(livre, etudiant)
    print(f"Réservation créée, position: {reservation.position_file}")
```

---

## Conclusion

Les modèles `User`, `Book`, `Loan` et `Reservation` forment un système cohérent qui permet de gérer efficacement une bibliothèque avec :
- Gestion des utilisateurs avec différents types et limites
- Gestion des livres avec exemplaires multiples
- Emprunts avec suivi des dates et pénalités
- Réservations avec file d'attente et notifications

Tous les modèles respectent les principes de la POO (encapsulation, héritage, polymorphisme) et sont conçus pour être maintenables et évolutifs.
