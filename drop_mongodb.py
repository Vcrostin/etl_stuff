from pymongo import MongoClient

from common import MONGO_URL, DataBases, DATABASE
import logging

def drop_mongodb():
    with MongoClient(MONGO_URL) as connection:
        db = connection[DATABASE]
        for collection_name in DataBases:
            collection = db[collection_name.value]
            collection.drop()
            logging.info(f"Dropping {collection_name}")
