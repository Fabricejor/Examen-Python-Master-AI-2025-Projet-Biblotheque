"""
Service de gestion de la persistance des données (sauvegarde/chargement).
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Union


class FileManager:
    """
    Classe utilitaire pour la gestion des fichiers JSON.
    """
    
    @staticmethod
    def get_file_path(directory: str, filename: str) -> Path:
        """
        Retourne le chemin absolu d'un fichier dans le dossier 'app/files'.
        
        Args:
            directory (str): Nom du sous-dossier (ex: 'books', 'users')
            filename (str): Nom du fichier (ex: 'books.json')
            
        Returns:
            Path: Chemin complet du fichier
        """
        # Remonte de 2 niveaux depuis services/ (app/services -> app) puis descend dans files/
        base_path = Path(__file__).parent.parent / "files"
        return base_path / directory / filename

    @staticmethod
    def ensure_directory_exists(file_path: Path):
        """
        S'assure que le dossier parent du fichier existe.
        
        Args:
            file_path (Path): Chemin du fichier
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def save_data(directory: str, filename: str, data: List[Dict[str, Any]]) -> bool:
        """
        Sauvegarde une liste de dictionnaires dans un fichier JSON.
        
        Args:
            directory (str): Nom du sous-dossier
            filename (str): Nom du fichier
            data (List[Dict]): Données à sauvegarder
            
        Returns:
            bool: True si la sauvegarde a réussi, False sinon
        """
        try:
            file_path = FileManager.get_file_path(directory, filename)
            FileManager.ensure_directory_exists(file_path)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde dans {filename}: {e}")
            return False

    @staticmethod
    def load_data(directory: str, filename: str) -> List[Dict[str, Any]]:
        """
        Charge une liste de dictionnaires depuis un fichier JSON.
        
        Args:
            directory (str): Nom du sous-dossier
            filename (str): Nom du fichier
            
        Returns:
            List[Dict]: Données chargées (liste vide si fichier inexistant ou erreur)
        """
        try:
            file_path = FileManager.get_file_path(directory, filename)
            
            if not file_path.exists():
                return []
                
            with open(file_path, 'r', encoding='utf-8') as f:
                # Vérifie si le fichier est vide
                content = f.read()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            print(f"Erreur: Le fichier {filename} contient un JSON invalide.")
            return []
        except Exception as e:
            print(f"Erreur lors du chargement de {filename}: {e}")
            return []
