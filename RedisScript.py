import redis

r = redis.Redis(host='localhost', port=6379, db=0)
#print(r)

def insertion_redis(Liste):
    for i in Liste:
        info = {'valeur':i['valeur'],'date':i['date'],'path':i['path'],'object_name':i['object_name']}
        key=i['id_element']
        
        r.hmset(key,info)
        return None
    
#insertion_redis(info_total_dict())
#
#print(r.hmget('A1_0','valeur','date','path','object_name'))
