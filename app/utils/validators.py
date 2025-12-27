"""
Utilitaires de validation (ISBN, dates, etc.).
"""

import random
import string
from datetime import datetime
from app.utils.constants import DATE_FORMAT


def generate_id(prefix: str = "") -> str:
    """
    Génère un identifiant unique au format XX000.
    
    Format : XX000 où :
    - X = lettre majuscule ou minuscule (A-Z, a-z)
    - 0 = chiffre (0-9)
    
    Args:
        prefix (str): Préfixe optionnel à ajouter avant l'ID
        
    Returns:
        str: Identifiant généré au format XX000 (ou prefixXX000 si prefix fourni)
    
    Exemples:
        >>> generate_id()
        'Ab123'
        >>> generate_id("BOOK")
        'BOOKAb123'
    """
    # Génère 2 lettres aléatoires (majuscules ou minuscules)
    letters = ''.join(random.choices(string.ascii_letters, k=2))
    
    # Génère 3 chiffres aléatoires
    numbers = ''.join(random.choices(string.digits, k=3))
    
    # Combine pour former XX000
    generated_id = f"{letters}{numbers}"
    
    # Ajoute le préfixe si fourni
    if prefix:
        return f"{prefix}{generated_id}"
    
    return generated_id


def validate_isbn(isbn: str) -> bool:
    """
    Valide le format d'un ISBN.
    
    Args:
        isbn (str): L'ISBN à valider
        
    Returns:
        bool: True si l'ISBN est valide, False sinon
    """
    if not isbn or len(isbn) != 5:
        return False
    
    # Vérifie que les 2 premiers caractères sont des lettres
    if not (isbn[0].isalpha() and isbn[1].isalpha()):
        return False
    
    # Vérifie que les 3 derniers caractères sont des chiffres
    if not (isbn[2].isdigit() and isbn[3].isdigit() and isbn[4].isdigit()):
        return False
    
    return True


def format_date(date_obj: datetime) -> str:
    """
    Formate un objet datetime au format JJ/MM/AAAA.
    
    Args:
        date_obj (datetime): Objet datetime à formater
        
    Returns:
        str: Date formatée au format JJ/MM/AAAA
    """
    return date_obj.strftime(DATE_FORMAT)


def parse_date(date_str: str) -> datetime:
    """
    Parse une chaîne de date au format JJ/MM/AAAA en objet datetime.
    
    Args:
        date_str (str): Date au format JJ/MM/AAAA
        
    Returns:
        datetime: Objet datetime correspondant
        
    Raises:
        ValueError: Si le format de date est invalide
    """
    try:
        return datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        raise ValueError(f"Format de date invalide. Format attendu: {DATE_FORMAT} (ex: 27/12/2025)")


def get_current_date() -> str:
    """
    Retourne la date actuelle formatée au format JJ/MM/AAAA.
    Utilise la variable d'environnement DATE_ACTUEL si définie, sinon la date système.
    
    Returns:
        str: Date actuelle au format JJ/MM/AAAA
    """
    import os
    date_actuel = os.getenv("DATE_ACTUEL")
    if date_actuel:
        return date_actuel
    return format_date(datetime.now())
