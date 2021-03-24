import redis #!pip install redis

r = redis.Redis(host='localhost', port=6379, db=0)
#print(r)

def Unique(Liste):
    Liste_uniq=[]
    for x in Liste:
        if x not in Liste_uniq:
            Liste_uniq.append(x)
    return Liste_uniq

def insertion_redis(dic,r):
    Liste_fichier=[]
    for i in dic:
        info = {'valeur':i['valeur'],'date':i['date'],'path':i['path'],'object_name':i['object_name']}
        key=i['id_element']
        r.hmset(key,info)
        r.set(i['object_name'],i['valeur']+1)
        Liste_fichier.append(i['object_name'])
    Liste_fichier=Unique(Liste_fichier)
    r.set('MaListe',",".join(Liste_fichier))
    return None

def get_redis(id, key,r):
    return r.hmget(id,key)[0].decode('utf-8')

def initialisation(r):
    r.set('TO_BE_PURGED',0)
    r.set('PURGED',0)
    r.set('RECEIVED',0)
    r.set('VERIFIED',0)
    r.set('PROCESSED',0)
    r.set('CONSUMED',0)
    r.set('REJECTED',0)
    r.set('REMEDIED',0)
    return None

def show(r):
    print('TO_BE_PURGED : ',r.get('TO_BE_PURGED').decode())
    print('PURGED : ',r.get('PURGED').decode())
    print('RECEIVED : ',r.get('RECEIVED').decode())
    print('VERIFIED : ',r.get('VERIFIED').decode())
    print('PROCESSED : ',r.get('PROCESSED').decode())
    print('CONSUMED : ',r.get('CONSUMED').decode())
    print('REJECTED : ',r.get('REJECTED').decode())
    print('REMEDIED : ',r.get('REMEDIED').decode())
    return None

#Récupérer le cycle de vie parcouru (la liste des status d’un objet donné)
def Redis_path(object_name,r,date=None):
    Nb_path=int(r.get(object_name).decode()) #compteur
    paths=[]
    for i in range(Nb_path):
        info=r.hmget(object_name+'_'+str(i),'path','date')
        if date is None:
            path=info[0].decode()
            paths+=path[1:-1].split(',')
        else:
            file_date=info[1].decode()
            if file_date >= date:
                path=info[0].decode()
                paths+=path[1:-1].split(',')
    return paths

# Compter le nombre d’objets par status 
def Redis_Object(r,date=None):
    date=date
    Paths=[]
    Liste_file = r.get('MaListe').decode().split(',')
    for file in Liste_file:
        Paths+=Unique((Redis_path(file,r,date)))
    return Paths

def count_redis(paths,r):
    initialisation(r)
    for path in paths:
        r.incr(path.replace(' ',''))
    show(r)
    return None

#Pour un objet de nature fichier, compter le nombre d’objets dans ce fcihier
def nb_objet_Redis(object_name,r):
    Compteur= int(r.get(object_name).decode())
    return Compteur

#Reprendre l’ensemble des cas d’utilisation de la partie 1 et ajouter de la traçabilité (sous 
#forme de métadonnées) avec l’objet parent
def Redis_Meta(object_name,r):
    Compteur = nb_objet_Redis(object_name,r)
    Metadonnee=object_name+' : '
    for i in range(Compteur):
        info=r.hmget(object_name+'_'+str(i),'path','date')
        path=info[0].decode()
        date=info[1].decode()
        Metadonnee+=date+' '+path+' ==> \n'
    return Metadonnee

datazz = [{'id_element': 'A1_0',
  'valeur': 0,
  'date': '2021-03-10 00:00:00',
  'path': 'VERIFIED,VALIDATE',
  'object_name': 'A1'},
 {'id_element': 'A2_0',
  'valeur': 0,
  'date': '2021-03-10 00:00:00',
  'path': 'VERIFIED,VALIDATE',
  'object_name': 'A2'},
 {'id_element': 'A3_0',
  'valeur': 0,
  'date': '2021-03-10 00:00:00',
  'path': 'VERIFIED,VALIDATE',
  'object_name': 'A3'},
 {'id_element': 'A2_1',
  'valeur': 1,
  'date': '10-03-2021 11:14:47',
  'path': 'RETURN,DETRUIT,JETER',
  'object_name': 'A2'},
 {'id_element': 'A2_2',
  'valeur': 2,
  'date': '10-03-2021 11:35:56',
  'path': 'NULL',
  'object_name': 'A2'}]

#insertion_redis(datazz,r)

#print(r.hgetall("A2_1"))
#print(get_redis("A2_1",'valeur',r))

#print(r.hmget('A1_0','valeur','date','path','object_name'))