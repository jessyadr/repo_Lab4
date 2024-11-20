#!/usr/bin/env python3

##
# @mainpage Documentation de l'API de gestion des séances
# 
# @section description_session_controller Description
# Cette API REST permet la gestion des séances associées aux modules d'un cours. Les opérations incluent :
# - Lecture des séances d'un cours.
# - Création d'une nouvelle séance.
# - Mise à jour d'une séance existante.
#
# @section notes_session_controller Notes
# - Les données des cours et des séances sont stockées dans le fichier `data.json`.
# - Les IDs des cours et des séances doivent être uniques.
#
# @section copyright_session_controller Copyright
# Copyright (c) 2024 UQAC. Tous droits réservés.
##

##
# @file session_controller.py
# @brief Gestion des endpoints REST pour les séances.
# @details Ce fichier contient les fonctions nécessaires pour manipuler les séances associées aux modules d'un cours via l'API.
#
# @section dependances_session_controller Dépendances/Modules
# - connexion : Framework pour gérer les APIs REST.
# - json : Module standard pour manipuler les fichiers JSON.
# - os : Utilisé pour vérifier l'existence du fichier de données.
#
# @section auteur_session_controller Auteur(s)
# - Jessy / Yasmine
# - Date : 20 / 11 / 2024
#
# @section todo_session_controller TODO
# - Ajouter des validations plus strictes pour les données d'entrée.
# - Implémenter un endpoint pour supprimer une séance.
# - Ajouter des tests unitaires.
##

# Importation des modules nécessaires
import connexion
import json
import os
from typing import Dict, Tuple, Union

## Constantes globales
##
# @var DATA_FILE
# Chemin vers le fichier JSON contenant les données des cours et séances.
##
DATA_FILE = "data.json"

##
# @var COURSE_NOT_FOUND
# Message renvoyé si le cours n'existe pas.
##
COURSE_NOT_FOUND = {"message": "Cours non trouvé."}

##
# @var SESSION_NOT_FOUND
# Message renvoyé si la séance n'existe pas.
##
SESSION_NOT_FOUND = {"message": "Séance non trouvée."}

##
# @var SESSION_ALREADY_EXISTS
# Message renvoyé si une séance avec cet ID existe déjà.
##
SESSION_ALREADY_EXISTS = {"message": "Une séance avec cet ID existe déjà dans le cours."}

##
# @var SESSION_CREATED_SUCCESS
# Message de succès renvoyé lors de la création d'une séance.
##
SESSION_CREATED_SUCCESS = "Séance créée avec succès."

##
# @var SESSION_UPDATED_SUCCESS
# Message de succès renvoyé lors de la mise à jour d'une séance.
##
SESSION_UPDATED_SUCCESS = "Séance mise à jour avec succès."

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
# @brief Trouver un cours par son ID.
# @details Recherche un cours dans les données en fonction de son ID.
#
# @param data dict Les données contenant la liste des cours.
# @param course_id int L'ID du cours à rechercher.
# @return dict|None Le cours correspondant à l'ID ou None.
##
def find_course_by_id(data: Dict, course_id: int) -> Union[Dict, None]:
    return next((course for course in data['cours'] if course['id'] == course_id), None)

##
# @brief Trouver une séance par son ID dans un cours donné.
# @details Recherche une séance spécifique dans les modules d'un cours.
#
# @param course dict Le cours contenant les modules et séances.
# @param session_id int L'ID de la séance à rechercher.
# @return dict|None La séance correspondante ou None.
##
def find_session_by_id(course: Dict, session_id: int) -> Union[Dict, None]:
    for module in course.get('modules', []):
        for session in module.get('seances', []):
            if session['id'] == session_id:
                return session
    return None

##
# @brief Obtenir les séances d'un cours.
# @details Retourne toutes les séances associées aux modules d'un cours spécifique.
#
# @param course_id int L'ID du cours.
# @return tuple(dict, int) Liste des séances et un code de statut HTTP.
##
def courses_course_id_sessions_get(course_id: int) -> Tuple[Dict, int]:
    data = load_data()
    course = find_course_by_id(data, course_id)

    if not course:
        return COURSE_NOT_FOUND, 404

    sessions = []
    for module in course.get('modules', []):
        sessions.extend(module.get('seances', []))
    
    return {"seances": sessions}, 200

##
# @brief Créer une nouvelle séance pour un cours.
# @details Ajoute une nouvelle séance à un cours existant. Si une séance avec le même ID existe déjà, retourne une erreur.
#
# @param course_id int L'ID du cours.
# @return tuple(dict, int) Message de succès ou d'erreur et un code de statut HTTP.
##
def courses_course_id_sessions_post(course_id: int) -> Tuple[Dict, int]:
    data = load_data()
    course = find_course_by_id(data, course_id)

    if not course:
        return COURSE_NOT_FOUND, 404

    session_data = connexion.request.get_json()

    if any(find_session_by_id(course, session_data['id']) for module in course['modules']):
        return SESSION_ALREADY_EXISTS, 400

    if not course.get('modules'):
        course['modules'] = [{"id": "module_1", "titre": "Nouveau module", "seances": []}]
    
    course['modules'][0]['seances'].append(session_data)
    save_data(data)
    return {"message": SESSION_CREATED_SUCCESS, "seance": session_data}, 201

##
# @brief Mettre à jour une séance.
# @details Modifie les données d'une séance existante. Si la séance ou le cours n'existe pas, retourne une erreur.
#
# @param course_id int L'ID du cours.
# @param session_id int L'ID de la séance à mettre à jour.
# @return tuple(dict, int) Message de succès ou d'erreur et un code de statut HTTP.
##
def courses_course_id_sessions_session_id_put(course_id: int, session_id: int) -> Tuple[Dict, int]:
    data = load_data()
    course = find_course_by_id(data, course_id)

    if not course:
        return COURSE_NOT_FOUND, 404

    session_data = connexion.request.get_json()
    session = find_session_by_id(course, session_id)

    if not session:
        return SESSION_NOT_FOUND, 404

    session.update(session_data)
    save_data(data)
    return {"message": SESSION_UPDATED_SUCCESS, "seance": session}, 200
