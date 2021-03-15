import redis

r = redis.Redis(host='localhost', port=6379, db=0)
#print(r)

def insertion_redis(data_dict):
    for i in data_dict:
        info = {'valeur':i['valeur'],'date':i['date'],'path':i['path'],'object_name':i['object_name']}
        key = i['id_element']
        
        r.hmset(key,info)    
    return None

def get_redis(id, key):
    return r.hmget(id,key)[0].decode('utf-8')

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

insertion_redis(datazz)

#print(r.hgetall("A2_1"))
print(get_redis("A2_1",'valeur'))

#print(r.hmget('A1_0','valeur','date','path','object_name'))
