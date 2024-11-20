#!/usr/bin/env python3

##
# @mainpage Documentation de l'API de gestion des cours
# 
# @section description_cours_controller Description
# Cette API REST permet la gestion des cours via des opérations CRUD (Créer, Lire, Mettre à jour, Supprimer).
# Les données sont stockées dans un fichier JSON local, et l'API est implémentée avec le framework Connexion.
#
# @section notes_cours_controller Notes
# - Assurez-vous que le fichier `data.json` est présent dans le répertoire racine.
# - Les IDs des cours doivent être uniques.
#
# @section copyright_cours_controller Copyright
# Copyright (c) 2024 UQAC. Tous droits réservés.
##

##
# @file cours_controller.py
# @brief Gestion des endpoints REST pour les cours.
# @details Ce fichier contient les fonctions nécessaires pour manipuler les données des cours via l'API.
#
# @section dependances_cours_controller Dépendances/Modules
# - connexion : Framework pour gérer les APIs REST.
# - json : Module standard pour manipuler les fichiers JSON.
# - os : Utilisé pour vérifier l'existence du fichier de données.
#
# @section auteur_cours_controller Auteur(s)
# - Jessy / Yasmine
# - Date : 20 / 11 / 2024
#
# @section todo_cours_controller TODO
# - Ajouter une validation des données d'entrée.
# - Implémenter des tests unitaires pour chaque endpoint.
##

import connexion
import json
import os
from typing import Dict, Tuple, Union

## Constantes globales
##
# @var DATA_FILE
# Chemin vers le fichier JSON contenant les données des cours.
##
DATA_FILE = "data.json"

##
# @var COURSE_NOT_FOUND
# Message renvoyé si le cours n'existe pas.
##
COURSE_NOT_FOUND = {"message": "Cours non trouvé."}

##
# @var COURSE_ALREADY_EXISTS
# Message renvoyé si un cours avec le même ID existe déjà.
##
COURSE_ALREADY_EXISTS = {"message": "Un cours avec cet ID existe déjà."}

## Fonctions principales

##
# @brief Charger les données depuis le fichier JSON.
# @details Si le fichier JSON est absent ou corrompu, retourne une structure de données par défaut.
# 
# @return dict Les données chargées ou un dictionnaire par défaut.
##
def load_data() -> Dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"cours": []}
    return {"cours": []}

##
# @brief Sauvegarder les données dans le fichier JSON.
# @details Écrit les données JSON dans le fichier `data.json`.
#
# @param data dict Les données à sauvegarder.
##
def save_data(data: Dict) -> None:
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

##
# @brief Obtenir la liste des cours.
# @details Retourne tous les cours stockés dans le fichier JSON.
# 
# @return tuple(dict, int) Liste des cours et code HTTP 200.
##
def courses_get() -> Tuple[Dict, int]:
    data = load_data()
    return {"cours": data["cours"]}, 200

##
# @brief Créer un nouveau cours.
# @details Ajoute un cours à la base de données si l'ID est unique.
#
# @return tuple(dict, int) Message de succès ou d'erreur, et code HTTP.
##
def courses_post() -> Tuple[Dict, int]:
    course_data = connexion.request.get_json()
    data = load_data()
    
    if any(course['id'] == course_data.get('id') for course in data['cours']):
        return COURSE_ALREADY_EXISTS, 400

    data['cours'].append(course_data)
    save_data(data)
    return {"message": "Cours créé avec succès.", "cours": course_data}, 201

##
# @brief Obtenir les détails d'un cours spécifique.
# @details Recherche un cours par son ID et retourne ses détails s'il existe.
#
# @param course_id int L'ID du cours recherché.
# @return tuple(dict, int) Détails du cours ou message d'erreur.
##
def courses_course_id_get(course_id: int) -> Tuple[Dict, int]:
    data = load_data()
    course = next((c for c in data['cours'] if c['id'] == course_id), None)
    if not course:
        return COURSE_NOT_FOUND, 404
    return course, 200

##
# @brief Mettre à jour un cours.
# @details Modifie les données d'un cours existant par son ID.
#
# @param course_id int L'ID du cours à mettre à jour.
# @return tuple(dict, int) Message de succès ou d'erreur.
##
def courses_course_id_put(course_id: int) -> Tuple[Dict, int]:
    course_data = connexion.request.get_json()
    data = load_data()
    course = next((c for c in data['cours'] if c['id'] == course_id), None)
    
    if not course:
        return COURSE_NOT_FOUND, 404

    course.update(course_data)
    save_data(data)
    return {"message": "Cours mis à jour avec succès.", "cours": course}, 200

##
# @brief Supprimer un cours.
# @details Supprime un cours par son ID si celui-ci existe.
#
# @param course_id int L'ID du cours à supprimer.
# @return tuple(dict, int) Message de succès ou d'erreur.
##
def courses_course_id_delete(course_id: int) -> Tuple[Dict, int]:
    data = load_data()
    course = next((c for c in data['cours'] if c['id'] == course_id), None)
    
    if not course:
        return COURSE_NOT_FOUND, 404
    
    data['cours'].remove(course)
    save_data(data)
    return {"message": "Cours supprimé avec succès."}, 200
