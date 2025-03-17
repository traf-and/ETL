import re
import json

from pymongo import MongoClient

def create_collections(db_name, collection_name):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db_name]

    db.create_collection(collection_name)

def get_max_id(collection_name:str,
               attribute:str,
               db_name:str='ETL',
               mongocon:str='mongodb://localhost:27017/'
               )-> int: 

    client = MongoClient(mongocon)
    db = client[db_name]
    collection = db[collection_name]
    
    result = list(collection.find())
    if result:
        ids = []
        for row in result:
            col = row[f'{attribute}']
            col = int(re.search(r'\d+', col).group())+1
            ids.append(col)
        return max(ids)#int(result.group())+1
    else:
        return 1

def insert_data_to_mongodb(data, db_name):
    # Подключение к MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    
    # Вставка данных в соответствующие коллекции
    for collection_name, documents in data.items():
        collection = db[collection_name]
        if isinstance(documents, list):
            collection.insert_many(documents)
        else:
            collection.insert_one(documents)


def list_collections(db_name:str='ETL'):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    return db.list_collection_names()

def get_mongo_data(collection_name:str,
                   attribute:str,
                   attribute_val:int,
                   db_name:str='ETL',
                   mongocon:str='mongodb://localhost:27017/'):
    client = MongoClient(mongocon)
    db = client[db_name]
    collection = db[collection_name]
    
    data = list(collection.find())

    if data:
        out = []
        for row in data:
            col = row[f'{attribute}']
            col = int(re.search(r'\d+', col).group())
            if col>attribute_val:
                out.append(row)
        return out

    return None