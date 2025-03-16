from pymongo import MongoClient

from common import MONGO_URL, DataBases, DATABASE

def check_connection():
    with MongoClient(MONGO_URL) as connection:
        # check connection
        result = connection.admin.command('ping')
        print(result)
