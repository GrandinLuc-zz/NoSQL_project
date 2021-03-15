from .MySQLScript import *
from .RedisScript import *
from .MongoDBScript import *
import urllib.request
import json

# We use the next.json-generator.com API to serve as our primary data source
data = json.load(urllib.request.urlopen('https://next.json-generator.com/api/json/get/VkGhn8OXc'))

# MySQL
mydbSQL = mysql.connector.connect(
  host="localhost",
  user="root",
  password="iD8DBQBeFL3pjHGNO1By4fURAt2yAKCFs5XrQlaTBqE1f536MgL2fxNiCQCgkPM+",
  database="dossier"
)


for e in data:
    val=[e['id_element'], e['valeur'], e['date'], e['path'], e['object_name']]
    insertion_simple(val,mydbSQL)


# Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# MongoDB
myclient = MongoClient(port=27017)



insertion_redis(info_total_dict())