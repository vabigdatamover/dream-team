import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['datalake_db']
cities_city = db['city']

with open('json_file.json') as f:
    file_data = json.load(f)

# use collection_currency.insert(file_data) if pymongo version < 3.0
cities_city.insert_one(file_data)
client.close()

