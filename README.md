Étudiantes:
- Jessy Andrianandraina
- Yasmine Kagone

Documentation de l'API de Gestion de Contenu de Cours

Introduction à Doxygen

Doxygen est un outil de génération de documentation automatisée à partir de commentaires structurés dans le code source. Il est principalement utilisé pour les projets logiciels écrits en C++, C, Python, et bien d'autres langages. Doxygen lit les commentaires spécialement formatés dans les fichiers source et produit une documentation HTML, LaTeX ou PDF. Cet outil permet de maintenir une documentation à jour en alignement direct avec le code, ce qui est essentiel pour la collaboration et la maintenance à long terme.

 Aperçu du Projet

Ce projet implémente une API REST pour la gestion de cours et des séances associées. Il repose sur le framework Connexion pour exposer des endpoints REST basés sur des spécifications Swagger. Les principales fonctionnalités incluent :

- La gestion des cours avec des opérations (Créer, Lire, Mettre à jour, Supprimer).
- La gestion des séances associées aux cours, également à travers des opérations .

Explication des commentaires

Les principaux types de commentaires qu'on a utilisé sont :

- @mainpage : pour fournir une vue d'ensemble de l'application et des fonctionnalités principales. C'est la page d'accueil de la documentation générée.
- @file : pour documenter les fichiers source individuels en indiquant leur rôle et leur contenu principal.
- @section : pour structurer la documentation en sections distinctes (ex. : description, notes, dépendances, TODO).
- @brief: pour Fournir une description concise des fonctions, classes ou constantes.
- @details : pour ajouter des informations détaillées pour expliquer des éléments complexes ou le fonctionnement d'une méthode.
- @param et @return : pour décrire les paramètres des fonctions et leur valeur de retour.


Conclusion

L'utilisation de Doxygen offre une solution plus robuste et cohérentepour documenter un projet logiciel. Contrairement à la documentation traditionnelle, elle facilite l'accès et la navigation, tout en garantissant que la documentation reste alignée avec le code source. Ce qui fait que c'est un outil indispensable pour les projets modernes, surtout ceux qui nécessitent une collaboration entre plusieurs développeurs. La documentation générée améliore également la qualité et la compréhension du projet, ce qui est crucial pour le développement logiciel à long terme.
