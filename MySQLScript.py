import mysql.connector
import datetime
from getpass import getpass
mydbSQL = mysql.connector.connect(
  host="localhost",
  user="root",
  password=getpass('mysql password : ')
)

#print(mydbSQL)

mycursor = mydbSQL.cursor(buffered=True)
# creation de la table
file =open('database.txt','r')
for line in file:
    mycursor.execute(line)

### Insertion multiple dans nom_fichier
sql = 'INSERT INTO `dossier`.`nom_fichier` (object_name) VALUES (%s)'
#val=['A2']
val = [['A1'],['A2'],['A3'],['A4'],['A5']]
mycursor.executemany(sql, val)
#mycursor.execute(sql, val)
mydbSQL.commit()
#print(mycursor.rowcount, "was inserted.")

### Insertion multiple dans element
sql = 'INSERT INTO `dossier`.`element` (id_element,valeur,date,path,object_name) VALUES (%s,%s,%s,%s,%s)'
val = [['A1_0',0,'2021-03-10 00:00:00','VERIFIED,VALIDATE','A1'],['A2_0',0,'2021-03-10 00:00:00','VERIFIED,VALIDATE','A2'],['A3_0',0,'2021-03-10 00:00:00','VERIFIED,VALIDATE','A3']]
mycursor.executemany(sql, val)
#mycursor.execute(sql, val)
mydbSQL.commit()
#print(mycursor.rowcount, "was inserted.")

now = datetime.datetime.now()
dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
#print("Today's date: ",dt_string)
#print(type(dt_string))

mycursor.execute("SELECT* FROM nom_fichier NATURAL JOIN element")
myresult = mycursor.fetchall()
#for x in myresult:
#  print(x)

mycursor.execute("SELECT* FROM nom_fichier NATURAL JOIN element ORDER BY object_name DESC")
myresult = mycursor.fetchall()
#for x in myresult:
#  print(x)

sql=("SELECT * FROM element Where object_name = %s")
val=['A2']
mycursor.execute(sql,val)
myresult = mycursor.fetchall()
#for x in myresult:
#  print(x)

#############################################################
def reformat_date(date_str):
    date=datetime.datetime.strptime(date_str,"%Y-%m-%dT%H:%M:%S.%f")
    new_date=date.strftime("%d-%m-%Y %H:%M:%S")
    return new_date

def lire(file_path):
    #PARAMETERS
    dossier_nom=[]
    dossier_element=[]
    dossier=[]
    
    #COMPTEUR
    Compteur=[]
    Liste_Nom=[]
    
    #Récupération
    file= open(file_path,"r")
    for line in file:
        dossier.append(eval(line))
    file.close()
        
        
    for i in dossier:
        
        if(i['object-name'] in Liste_Nom):
            Compteur[Liste_Nom.index(i['object-name'])] +=1
        else:
            dossier_nom.append([i['object-name']])
            Liste_Nom.append(i['object-name'])
            Compteur.append(0)
        dossier_element.append([i['object-name']+'_'+str(Compteur[Liste_Nom.index(i['object-name'])]),Compteur[Liste_Nom.index(i['object-name'])],reformat_date(i['occurredOn']),i['path'],i['object-name']])
    return dossier_nom, dossier_element

### Insertion multiple dans nom_fichier
def insertion_multiple_fichier(val,db):
    sql = 'INSERT INTO `dossier`.`nom_fichier` (object_name) VALUES (%s)'
    #val=['A2']
    #val = dossier_nom
    cursor = db.cursor(buffered=True)
    cursor.executemany(sql, val)
    #mycursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "was inserted.")
    return None

### Insertion multiple dans element
def insertion_multiple_element(val, db):
    sql = 'INSERT INTO `dossier`.`element` (id_element,valeur,date,path,object_name) VALUES (%s,%s,%s,%s,%s)'
    #val = dossier_element
    cursor = db.cursor(buffered=True)
    cursor.executemany(sql, val)
    #mycursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "was inserted.")
    return None

# INSERTION D'UN NOUVEAU ELEMENT
def insertion_simple(val,db):
    sql = 'INSERT INTO `dossier`.`element` (id_element,valeur,date,path,object_name) VALUES (%s,%s,%s,%s,%s)'
    cursor = db.cursor(buffered=True)
    cursor.execute(sql, val)
    db.commit()
    #print(mycursor.rowcount, "was inserted.")
    return None

#AVOIR LA DATE
def get_date(heureDelta=0):
    now = datetime.datetime.now() - datetime.timedelta(hours=heureDelta)
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    return dt_string

#PRENDRE LES INFOS D'UN FICHIER ET RETOURNER UNE LISTE
def info(object_name,db):
    info=[]
    val=[]
    sql=("SELECT * FROM element Where object_name = %s ORDER BY valeur")
    cursor = db.cursor(buffered=True)
    val.append(object_name)
    cursor.execute(sql,val)
    myresult = cursor.fetchall()
    for x in myresult:
        info.append([x[0],x[1],x[2],x[3],x[4]])
    return info

#PRENDRE TOUS ET RETOURNER UNE LISTE
def info_total_list(db):
    info=[]
    sql=("SELECT * FROM element ORDER BY valeur")
    cursor = db.cursor(buffered=True)
    cursor.execute(sql)
    myresult = cursor.fetchall()
    for x in myresult:
        info.append([x[0],x[1],x[2],x[3],x[4]])
    return info

#PRENDRE TOUS ET RETOURNER UNE LISTE DE DICTIONNAIRE
def info_total_dict(db):
    info=[]
    sql=("SELECT * FROM element ORDER BY valeur")
    cursor = db.cursor(buffered=True)
    cursor.execute(sql)
    value = cursor.fetchall()
    for myresult in value:
        dic={'id_element':myresult[0],'valeur':myresult[1],'date':myresult[2],'path':myresult[3],'object_name':myresult[4]}
        info.append(dic)
    return info

#PRENDRE LE DERNIER UPDATE D'UN FICHIER
def info_last(object_name,db):
    val=[]
    sql=("SELECT * FROM element Where object_name = %s ORDER BY valeur DESC")
    val.append(object_name)
    cursor = db.cursor(buffered=True)
    cursor.execute(sql,val)
    myresult = cursor.fetchone()
    info={'id_element':myresult[0],'valeur':myresult[1],'date':myresult[2],'path':myresult[3],'object_name':myresult[4]}
    return info

def new_path():
    path=''
    p='donner le nouveau chemin pour aujoud\'hui 1 à 1 : '
    enc=' Encore 0(non) 1(oui) ? : '
    verify= 1
    while verify ==1:
        ch=input(p)
        path+=ch+','
        verify=eval(input(enc))
    return path[:-1]

def Insertion_path(object_name,db):
    I=info_last(object_name,db)
    valeur=I['valeur']+1
    id_element=object_name+'_'+str(valeur)
    date= get_date()
    path=new_path()
    val=[id_element,valeur,date,path,object_name]
    insertion_simple(val,db)
    return None

# Polling
def Polling(file_path,db):
    #CURSEUR
    Liste_Nom=[]
    Compteur=[]
    cursor = db.cursor(buffered=True)
    cursor.execute("SELECT object_name,max(valeur) from element group by object_name")
    myresult=cursor.fetchall()
    for x in myresult:
        Liste_Nom.append(x[0])
        Compteur.append(x[1])
    print(Compteur)
    #PARAMETERS
    dossier_nom=[]
    dossier_element=[]
    dossier=[]
    
    #Récupération
    file= open(file_path,"r")
    for line in file:
        dossier.append(eval(line))
    file.close()
        
        
    for i in dossier:
        
        if(i['object-name'] in Liste_Nom):
            Compteur[Liste_Nom.index(i['object-name'])] +=1
        else:
            dossier_nom.append([i['object-name']])
            Liste_Nom.append(i['object-name'])
            Compteur.append(0)
        dossier_element.append([i['object-name']+'_'+str(Compteur[Liste_Nom.index(i['object-name'])]),Compteur[Liste_Nom.index(i['object-name'])],reformat_date(i['occurredOn']),i['path'],i['object-name']])
        
    # insertion du polling
    sql = 'INSERT INTO `dossier`.`nom_fichier` (object_name) VALUES (%s)'
    val = dossier_nom
    cursor.executemany(sql, val)
    db.commit()
    
    sql = 'INSERT INTO `dossier`.`element` (id_element,valeur,date,path,object_name) VALUES (%s,%s,%s,%s,%s)'
    val = dossier_element
    cursor.executemany(sql, val)
    db.commit()


mydbSQL.close()