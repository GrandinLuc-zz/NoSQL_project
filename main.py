from MySQLScript import *
from RedisScript import *
from MongoDBScript import *
import urllib.request
import json
import mysql.connector
from pymongo import MongoClient
import redis
# MySQL
mydbSQL = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mdp",
)
mycursor = mydbSQL.cursor(buffered=True)
file =open('database.txt','r')
for line in file:
    mycursor.execute(line)

#MongoDB
myclient = MongoClient(port=27017)
mydbNOSQL=myclient['local']
mycol = mydbNOSQL["dossier"]

#redis
r = redis.Redis(host='localhost', port=6379, db=0)

# We use the next.json-generator.com API to serve as our primary data source
data = json.load(urllib.request.urlopen('https://next.json-generator.com/api/json/get/VkGhn8OXc'))

dossier_nom, dossier_element=lire('jeuDeDonnees_1.log')

# insertion dans mysql
insertion_multiple_fichier(dossier_nom,mydbSQL)
insertion_multiple_element(dossier_element, mydbSQL)
#insertion dans MongoDB
mgo_multiple_insertion(info_total_dict(mydbSQL),mycol)
#insertion dans redis
insertion_redis(info_total_dict(mydbSQL),r)

# Partie 1 mongodb

# • Récupérer le cycle de vie parcouru (la liste des status d’un objet donné)
# • Compter le nombre d’objets par status 
print(Count_path(Object_statue(mycol)))
# • Compter le nombre d’objets par status sur la dernière heure
print(Count_path(Object_statue(mycol,get_date(10))))
# • Compter le nombre d’objets respectant l’intégrité du graphe du cycle de vie

#Partie 2
# • Pour un objet de nature fichier, compter le nombre d’objets dans ce fcihier
object_name='File-24'
print(nombre_objet_Mongo(object_name,mycol))
# • Reprendre l’ensemble des cas d’utilisation de la partie 1 et ajouter de la traçabilité (sous 
# forme de métadonnées) avec l’objet parent
print(Mongo_Meta(object_name,mycol))

# Partie 1 redis

# • Récupérer le cycle de vie parcouru (la liste des status d’un objet donné)
print(Redis_path(object_name,r,get_date(1000)))
# • Compter le nombre d’objets par status 
print(count_redis(Redis_Object(r,get_date(1000)),r))
# • Compter le nombre d’objets par status sur la dernière heure
print(count_redis(Redis_Object(r,get_date(10000)),r))
# • Compter le nombre d’objets respectant l’intégrité du graphe du cycle de vie

#Partie 2
# • Pour un objet de nature fichier, compter le nombre d’objets dans ce fcihier
print(nb_objet_Redis(object_name,r))
# • Reprendre l’ensemble des cas d’utilisation de la partie 1 et ajouter de la traçabilité (sous 
# forme de métadonnées) avec l’objet parent
print(Redis_Meta(object_name,r))

mydbSQL.close()
mycol.drop()
myclient.close()
#DROP all key redis
r.flushall()
r.close()