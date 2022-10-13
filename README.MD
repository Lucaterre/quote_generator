# Quote generator

![Python Version](https://img.shields.io/badge/Python-%3E%3D%203.8-%2313aab7) [![Quote Generator CI build](https://github.com/Lucaterre/quote_generator/actions/workflows/CI.yml/badge.svg)](https://github.com/Lucaterre/quote_generator/actions/workflows/CI.yml)

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

## Description et motivation du projet

Ce projet est issu de l'exercice proposé sur [Coding Dojo](https://codingdojo.org/) initulé [Quote of the day](https://codingdojo.org/kata/QotdCgi/), l'auteur du kata résume l'exercice ainsi :

> You are to write a web service that returns a different quote every time you visit it. As an additional requirement, if you add a query parameter like “?q=foobar” it should return a random quote that contains the string “foobar”. – MatteoVaccari

Nous présentons ici le projet Quote generator qui se propose de résoudre l'exercice par le biais de la construction d'une API comprenant un certain nombre de méthodes, notamment celle remplissant l'objectif de l'auteur ; ainsi que d'une interface web pour appeler ces mêmes méthodes pour des utilisateurs finaux.
Ces deux services sont implémentés grâce au micro-framework Flask en Python et séparés en sous-domaines (ainsi la migration de l'API vers un autre framework est possible sans avoir à revoir l'entièreté du projet).

Plutôt que d'appeler une API déjà existante qui renvoie des citations (à l'aide du module `requests` par exemple) nous avons choisi de partir d'un dataset existant a traiter avant de l'injecter dans une base données de type SQLlite. Le script de traitement du dataset est disponible [ici](./qod_app/json_quote_preprocess.py) - suppression des citations offensantes, régularisation de l'encodage, suppression des doublons etc. - et la source du dataset est disponible sur le site [Kaggle](https://www.kaggle.com/datasets/akmittal/quotes-dataset))

Pour répondre aux objectifs du projet via ce projet :
- générer une citation aléatoire ; ex : http://127.0.0.1:3000/api/random 
- générer une citation aléatoire qui contient le terme à rechercher ; ex: http://127.0.0.1:3000/api/random?q=moon

Nous avons complexifier un peu l'exercice initial par:
  - la récupération des citations depuis une base de données SQL ;
  - la rédaction de tests fonctionnels ;
  - la création d'une interface Web ;
  - la création d'une documentation pour l'API ;
  - l'ajout de méthodes plus complexes (suppression ou mise à jour des citations) ;
  - l'ajout de l'authentification pour accéder à certaines méthodes de l'API.


## Sommaire

- [Installation du projet](#installation-du-projet)
- [Lancement des services du projet](#lancement-des-services-du-projet)
- [Les services de Quote generator](#les-services-de-quote-generator)
  - [Interface Web](#interface-web)
  - [API RESTful](#api-restful)
- [Lancement des tests](#lancement-des-tests)
- [Les outils utilisés](#les-outils-utilisés)
- [Structure générale du projet](#structure-générale-du-projet)

## Installation du projet

1. Cloner le répertoire GitHub

```bash
git clone https://github.com/Lucaterre/quote_generator.git
```

2. Se rendre dans le répertoire

```bash
cd ./quote_generator
```

4. Créer un environment virtuel avec virtualenv

```bash
virtualenv --python=/usr/bin/python3.8 venv
```

5. Activer l'environment virtuel

```bash
source venv/bin/activate
```

6. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Lancement des services du projet

Pour lancer les différents services du projet utilisé la CLI fourni et choisir un mode de configuration associé tel que :

```bash
python wsgi.py --dev_mode
```

Arguments : (via `python wsgi.py --help`)

```
usage: wsgi.py [-h] [--dev_mode] [--test_mode] [--prod_mode] [--erase_recreate_db]

optional arguments:
  -h, --help           show this help message and exit
  --dev_mode           launch dev mode
  --test_mode          launch test mode
  --prod_mode          launch production mode
  --erase_recreate_db  recreate a new database [BE CAREFUL IN PRODUCTION] | always true for dev and test mode

```

## Les services de Quote generator

Une fois l'application lancée deux services sont proposés :

### Interface web

Une interface Web est fournie aux utilisateurs finaux pour pouvoir utiliser et découvrir un certain nombre de méthodes fourni par l'API REST, par exemple :

- découvrir une nouvelle citation au hasard chaque jour ;
- rechercher dans la base de données une citation suivant une requête (recherche exacte ou approximative)

Cette interface est accessible via le port 3000 par défaut (http://localhost:3000/).

### API RESTful

L'API fournie un ensemble de méthodes pour par exemple rechercher une citation ou générer une citation aléatoirement (avec ou sans un critère). 
Elle offre également la possibilité de suggérer une nouvelle citation, ou encore de supprimer ou mettre à jour une citation.

Certaines méthodes requièrent une authentification, en mode `dev` ou `test` vous pouvez utiliser les crédits suivants:

- username: test-admin
- password: test-admin

Le point d'entrée de l'API est http://localhost:3000/api/

Une documentation plus détaillée concernant les services API de Quote generator sont accessibles ici: http://127.0.0.1:3000/api/docs#/

Pour tester les différentes méthodes de l'API vous pouvez utiliser `curl` ou le client [Postman](https://www.postman.com/)

## Lancement des tests

Les tests couvrent actuellement les services proposés par l'API (d'autres tests pourront être implémentés dans le futur), pour lancer ces tests depuis la racine du projet utiliser pytest:

```bash
pytest qod_app/tests/tests_api.py 
```

## Les outils utilisés

- backend
  - Flask : micro-framework léger open-source pour le développement web en Python qui permet du prototypage rapide par exemple ;
  - extensions Flask :
    - flask_sqlalchemy : support pour simplifier l'usage de l'ORM SQLAlchemy avec Flask ; 
    - flask_msearch : support pour faire de la recherche plein-texte dans une base de données SQL ;
    - flask_misaka : interface entre le parseur markdown Misaka et Flask. Il est utilisé pour générer le HTML de la doc de l'API à partir du markdown (Il est possible d'utiliser l'extension Flasgger pour créer une documentation avec SwaggerUI et extraire les spécifications depuis les vues Flask) ;
    - flask_httpauth : interface pour simplifier l'utilisation de l'authentification HTTP avec les routes Flask ;
  - passlib : package Python pour faire du hachage de mot de passe ;
  - requests : package Python pour réaliser des requêtes HTTP ;

- frontend
  - JavaScript/HTML/CSS
  - framework Bootstrap 

- Base de données
  - SQLite: moteur de base de données relationelle accessible via SQL ; l'intégralité de la base de données est stockée dans un fichier indépendant ;

- tests:
  - pylint : vérification de la syntaxe Python en utilisant les recommendations de la PEP 8 ;
  - pytest : implémentation de tests fonctionnels ; 

## Structure générale du projet

La structure du projet est base sur la structure traditionnelle d'un projet Flask:

```
 quote_generator/
|
├── .github/ : comprend les dossiers/fichiers nécéssaires à l'automatisation de la pipeline CI Github workflow (tests avec pylint et pytest)
│    
│   
├── qod/: module principal du projet Quote generator
|    |
│    ├── data: comprend le dataset original de citations et le dataset traité pour son injection dans la base de donnée  
|    |
│    ├── db_store: contient les fichiers de base de données Sqlite utilisés en production (pour la démonstration) et en mode dev/test 
|    |
│    ├── documentation: fichiers de documentation notamment les spécifications de l'API
|    |
│    ├── models: modèles de données utilisés pour la base de données relationelle 
|    |
│    ├── routes: les différentes vues utilisées dans les services, nous utilisons les blueprints pour bien distingués les sous-services (APP -> retourne du HTML et API -> retourne du JSON/a l'exception de la documentation). Comprend égallement la vue pour la gestion des erreurs.
|    |
│    ├── statics: fichiers CSS/JavaScript pour le rendu frontend
|    |
│    ├── templates: fichiers HTML pour le rendu frontend utilisant le moteur de template Jinja  
|    |
│    ├── tests: série de tests fonctionnels pour l'API 
|    |
│    ├── config_app.py: classes et fonctions de configuration et d'initialisation de l'environnement de la base de données et de l'application
|    |
│    ├── constants.py: constantes utilisées dans le projet (ex. chemins relatifs, template de réponse etc.)
|    |
│    ├── extensions.py: initialisation des extensions Flask
|    |
│    ├── json_quote_preprocess.py: script individuel pour pré-traiter le dataset de citations disponible dans data/
|    
├── LICENSE
│   
├── README.md : documentation générale
|
├── .gitignore : fichiers ignorés lors de l'indexation par Git
|
├── requirements.txt : ensemble des dépendances nécéssaires du projet
|
└── wsgi.py  : point d'entrée des services (CLI)
```


