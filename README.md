# NoSQL_project
#### Créer une solution d’ingestion et d’analyse de donnés de cycle de vie

-  Base relationnelle MySQL
- base NoSQL MongoDB
- base NoSQL Redis

To change the data to get the right date format use the following script: node changeDate.js

## Installation

1) MySQL :
> Système de gestion de bases de données.
[follow instruction here](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/) 

Créer dans `C:\Users\#nom>` un fichier `Integ` et y placer les fichiers pour les installations suivantes :

2) MongoDB :
>  Système de gestion de base de données NoSQL orientée documents.
[follow instruction here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)

1) Redis
> Système de stockage de données en mémoire de type NoSQL, enregistrement en clef : valeur.
[follow instruction here](https://redis.io/download) 


## Start
Instaler les logiciels
Dans une première console , pour lancer le server MongoDB faire :
```sh
cd c:\Integ
cd .\mongodb-win32-x86_64-windows-4.4.3\
bin\mongod --dbpath data
```
Dans une seconde console , pour lancer le server Redis faire :
```sh
cd c:\Integ
cd .\redis\64bit\
.\redis-server.exe
```
lancer `main.py`
- Donner son mot de passe MySQL
- Le numéro du fichier à étudier
