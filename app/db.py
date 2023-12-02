import os
from pymongo import MongoClient
import certifi

# Singleton pattern implementation
class MongoSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoSingleton, cls).__new__(cls, *args, **kwargs)
            cls._instance._init_mongo()
        return cls._instance

    def _init_mongo(self):
        mongo_uri = os.getenv("MONGO_URI")
        if mongo_uri:
            ca = certifi.where()
            cluster = MongoClient(mongo_uri, tlsCAFile=ca)
            self.db = cluster["CustomerApplicationDB"]
        else:
            raise EnvironmentError("MONGO_URI environment variable is not set.")

    def get_collection(self, collection_name):
        return self.db[collection_name]
    