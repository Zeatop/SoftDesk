# SoftDesk API

API RESTful pour la gestion de projets techniques, développée avec Django et Django REST Framework.

## Description

SoftDesk API fournit une interface pour gérer des projets de développement logiciel, des problèmes (issues) et des commentaires associés. L'API gère l'authentification des utilisateurs et les autorisations basées sur les rôles.

## Fonctionnalités

- Authentification des utilisateurs
- Gestion des projets (création, modification, suppression)
- Système de contributeurs pour les projets
- Suivi des problèmes (issues) avec priorité et statut
- Système de commentaires sur les issues
- Contrôle d'accès basé sur les rôles (propriétaire, contributeur)

## Structure du projet

- **Users** : Application gérant les utilisateurs personnalisés
- **Project** : Application principale gérant les projets, issues et commentaires

## Modèles

- **CustomUser** : Utilisateur personnalisé avec champs additionnels
- **Project** : Projets de développement (Backend/Frontend, iOS/Android)
- **Contributor** : Relation entre utilisateurs et projets avec rôles
- **Issue** : Problèmes associés à un projet avec priorité et statut
- **Comment** : Commentaires associés à une issue

## Endpoints API

- `/api/createuser/` : Création d'utilisateur
- `/api/login/` : Authentification
- `/projects/` : CRUD pour les projets
- `/projects/{id}/join/` : Rejoindre un projet en tant que contributeur
- `/issues/` : CRUD pour les issues
- `/comments/` : CRUD pour les commentaires

## Installation

1. Cloner le dépôt
2. Créer un environnement virtuel : `python -m venv env`
3. Activer l'environnement virtuel : `source env/bin/activate` (Linux/Mac) ou `env\Scripts\activate` (Windows)
4. Installer les dépendances : `pip install -r requirements.txt`
5. Effectuer les migrations : `python manage.py migrate`
6. Lancer le serveur : `python manage.py runserver`

## Utilisation

Toutes les requêtes (sauf création d'utilisateur et login) nécessitent une authentification avec un token JWT dans l'en-tête d'autorisation.
