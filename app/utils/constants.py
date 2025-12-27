"""
Constantes de l'application (limites d'emprunts, durées, etc.).
"""

# Limites d'emprunts par type d'utilisateur
LIMITE_EMPRUNTS_ETUDIANT = 4
LIMITE_EMPRUNTS_ENSEIGNANT = 6
LIMITE_EMPRUNTS_PERSONNEL_ADMIN = 0

# Format de date utilisé dans toute l'application
# Format: JJ/MM/AAAA (exemple: 27/12/2025)
DATE_FORMAT = "%d/%m/%Y"
DATE_FORMAT_DISPLAY = "JJ/MM/AAAA"

# Variable d'environnement pour la date actuelle (utilisée pour les tests)
# Format attendu: "JJ/MM/AAAA" (ex: "27/12/2025")
# Si non définie, utilise la date système actuelle
# Pour définir: os.environ["DATE_ACTUEL"] = "27/12/2025"
DATE_ACTUEL_ENV = "DATE_ACTUEL"

# Durée d'emprunt par défaut (en jours)
DUREE_EMPRUNT_DEFAUT = 30

# Taux de pénalité par jour de retard
TAUX_PENALITE_PAR_JOUR = 0.5
