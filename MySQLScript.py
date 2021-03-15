import mysql.connector
from datetime import datetime

mydbSQL = mysql.connector.connect(
  host="localhost",
  user="root",
  password="iD8DBQBeFL3pjHGNO1By4fURAt2yAKCFs5XrQlaTBqE1f536MgL2fxNiCQCgkPM+",
    database="dossier"
)

#print(mydbSQL)

mycursor = mydbSQL.cursor(buffered=True)

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

now = datetime.now()
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

def insertion_simple(val):
    sql = 'INSERT INTO `dossier`.`element` (id_element,valeur,date,path,object_name) VALUES (%s,%s,%s,%s,%s)'
    mycursor.execute(sql, val)
    mydbSQL.commit()
    #print(mycursor.rowcount, "was inserted.")
    return None

def get_date():
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    return dt_string

def info(object_name):
    info=[]
    val=[]
    sql=("SELECT * FROM element Where object_name = %s ORDER BY valeur")
    val.append(object_name)
    mycursor.execute(sql,val)
    myresult = mycursor.fetchall()
    for x in myresult:
        info.append([x[0],x[1],x[2],x[3],x[4]])
    return info

def info_total_list():
    info=[]
    sql=("SELECT * FROM element ORDER BY valeur")
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        info.append([x[0],x[1],x[2],x[3],x[4]])
    return info

def info_total_dict():
    info=[]
    sql=("SELECT * FROM element ORDER BY valeur")
    mycursor.execute(sql)
    value = mycursor.fetchall()
    for myresult in value:
        dic={'id_element':myresult[0],'valeur':myresult[1],'date':myresult[2],'path':myresult[3],'object_name':myresult[4]}
        info.append(dic)
    return info

def info_last(object_name):
    val=[]
    sql=("SELECT * FROM element Where object_name = %s ORDER BY valeur DESC")
    val.append(object_name)
    mycursor.execute(sql,val)
    myresult = mycursor.fetchone()
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

P=info('A2')

#print(P)

def Insertion_path(object_name):
    I=info_last(object_name)
    valeur=I['valeur']+1
    id_element=object_name+'_'+str(valeur)
    date= get_date()
    path=new_path()
    val=[id_element,valeur,date,path,object_name]
    insertion_simple(val)
    return None


#Insertion_path('A2')
#info('A2')
#info_total_list()
#info_total_dict()


mydbSQL.close()