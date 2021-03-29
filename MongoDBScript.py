from pymongo import MongoClient
from random import randint
import json


#Step 1: Connect to MongoDB - Note: Change connection string as needed
myclient = MongoClient(port=27017)
mydbNOSQL=myclient['local']
mycol = mydbNOSQL["dossier"]
print(mydbNOSQL.list_collection_names())


#multiple insertion
#x = mycol.insert_many(info_total_dict(mydbSQL))
#print(x.inserted_ids)
#
#for x in mycol.find():
#    print(x)
#
#mycol.drop()

#multiple insertion
def mgo_multiple_insertion(info_dict,mycol):
    x = mycol.insert_many(info_dict)
    return x

def Unique(Liste):
    Liste_uniq=[]
    for x in Liste:
        if x not in Liste_uniq:
            Liste_uniq.append(x)
    return Liste_uniq

#Récupérer le cycle de vie parcouru (la liste des status d’un objet donné)
object_name='File-24'
def Liste_statue(object_name,mycol):
    d=[]
    Liste_path=[]
    for x in mycol.find({'object_name': object_name},{'_id':0,'path':1}).sort('valeur'):
        d.append(x['path'])
    for i in d:
        Liste_path+=i[1:-1].split(',')
    return Liste_path

def Object_statue(mycol, date=None):
    Liste_File=[]
    Liste_File_uniq=[]
    Liste_path=[]
    Liste_path_uniq=[]
    #CHERCHER LES FICHIERS ET METTRE EN UNIQUE LES FICHIERS
    if date is None:
        for x in mycol.find({},{'_id':0,'object_name':1}):
            Liste_File.append(x['object_name'])
    if date:
        for x in mycol.find({'date':{'$gt':date}},{'_id':0,'object_name':1}):
            Liste_File.append(x['object_name'])
    Liste_File_uniq=Unique( Liste_File)
    #CHERCHER LES PATHS ET METTRE EN UNIQUE LES PATHS POUR CHAQUE FICHIER
    for x in Liste_File_uniq:
        Liste_path.append(Liste_statue(x,mycol))
    for x in Liste_path:
        Liste_path_uniq+=(Unique(x))
    return Liste_path_uniq

#Compter le nombre d’objets par status 
def Count_path(Liste):
    Compteur=[]
    Liste_Unique=Unique(Liste)
    for path in Liste_Unique:
        Compteur.append(Liste.count(path))
    return dict(zip(Liste_Unique,Compteur))

#Pour un objet de nature fichier, compter le nombre d’objets dans ce fcihier
def nombre_objet_Mongo(object_name,mycol):
    nb_objet = mycol.find({'object_name': object_name}).count()
    return nb_objet

#traçabilité 
def Mongo_Meta(object_name,mycol):
    Metadonnee=object_name+" : "
    for x in mycol.find({'object_name': object_name},{'_id':0,'date':1,'path':1}).sort('valeur'):
        Metadonnee+=x['date']+' '+x['path']+' ===> \n'
    return Metadonnee

def MAJ_Mongo(info_dict,mycol):
    mycol.drop()
    x = mycol.insert_many(info_dict)
    return x

mycol.drop()
myclient.close()