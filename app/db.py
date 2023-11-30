import os
from pymongo import MongoClient

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
            cluster = MongoClient(mongo_uri)
            self.db = cluster["CustomerApplicationDB"]
        else:
            raise EnvironmentError("MONGO_URI environment variable is not set.")

    @property
    def customers_collection(self):
        return self.db["customers"]

    @property
    def applications_collection(self):
        return self.db["applications"]

    @property
    def animals_collection(self):
        return self.db["animals"]

# Usage
mongo_instance = MongoSingleton()
customers_collection = mongo_instance.customers_collection
customers_collection.create_index("email", unique=True)

applications_collection = mongo_instance.applications_collection
animals_collection = mongo_instance.animals_collection

# Now you can use `customers_collection.insert_one()` to insert a customer.
