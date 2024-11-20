#!/usr/bin/env python3

##
# @mainpage Documentation de l'application API de gestion de contenu de cours
# 
# @section description_main Description
# Ce projet implémente une API REST basée sur Swagger pour gérer le contenu des cours.
# Il utilise le framework Connexion pour exposer des endpoints REST. Ce fichier principal configure 
# et lance le serveur de l'API.
#
# @section notes_main Notes
# - Le serveur écoute par défaut sur le port 8080.
# - Assurez-vous que le fichier `swagger.yaml` est correctement configuré.
#
# @section copyright_main Copyright
# Copyright (c) 2024 UQAC. Tous droits réservés.
##

##
# @file __main__.py
# @brief Point d'entrée principal de l'application API de gestion de contenu de cours.
# @details Ce fichier configure et démarre une application REST basée sur Swagger, permettant la gestion de contenu de cours.
#
# @section dependances_main Dépendances/Modules
# - connexion : Framework pour créer des APIs REST.
# - swagger_server.encoder : Fournit un encodeur JSON personnalisé pour gérer les données.
#
# @section auteur_main Auteur(s)
# - Jessy / Yasmine
# - Date : 20 / 11 / 2024
#
# @section todo_main TODO
# - Ajouter des validations supplémentaires.
# - Implémenter des tests unitaires pour les endpoints.
##

# Importation des modules nécessaires
import connexion  # @note Framework pour créer des APIs RESTful à partir de spécifications Swagger
from swagger_server import encoder  # @note Codeur JSON personnalisé pour gérer les réponses API

##
# @brief Lance l'application de gestion de contenu de cours.
# @details Configure et démarre une application Connexion pour exposer l'API décrite dans swagger.yaml.
#
# @note Le serveur écoute sur le port 8080 par défaut.
##
def main():
    # Initialisation de l'application Connexion
    app = connexion.App(__name__, specification_dir='./swagger/')
    
    # Définir l'encodeur JSON personnalisé
    app.app.json_encoder = encoder.JSONEncoder
    
    # Ajouter les spécifications Swagger
    app.add_api('swagger.yaml', arguments={'title': 'API de Gestion de Contenu de Cours'})
    
    # Démarrer le serveur
    app.run(port=8080)


##
# @brief Point d'entrée principal du script.
# @details Vérifie si le fichier est exécuté directement et appelle la fonction main.
#
# @note Cette vérification empêche l'exécution automatique du script lorsqu'il est importé comme module.
##
if __name__ == '__main__':
    main()
