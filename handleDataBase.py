import  pymongo 
from dotenv import load_dotenv
import os

from pymongo import database 

load_dotenv()

MONGO_SERVER_URL = os.getenv('MONGO_SERVER_URL')
MONGO_DATABASE_NAME=os.getenv('MONGO_DATABASE_NAME')
MONGO_COLLECTION_NAME = os.getenv('MONGO_COLLECTION_NAME')


class DatabaseHandle():
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_SERVER_URL)
        self.database = self.client[MONGO_DATABASE_NAME]
        self.collection = self.database[MONGO_COLLECTION_NAME]
        pass
    def getMapByName(self,name):
        name = name.lower()
        filter = {
            'name':name
        }
        result = self.collection.find(filter,{'_id':0})
        return result
    
    def getMapByRefName(self,name):
        tokens = name.split('-')
        ref_name = [token[0] for token in tokens]
        ref_name = (''.join(ref_name)).upper()
        filter={
            'ref_name':ref_name
        }
        result = self.collection.find(filter,{'_id':0})
        return result

    def getMapByTier(self,tier):
        filter = {
            'tier':int(tier)
        }
        result = self.collection(filter,{'_id':0})
        return result 
        
    def addMapData(self,map_data):
        filter = {'name':map_data['name']}
        self.collection.update_one(filter,{'$set':map_data},upsert=True)
    
    def getMapList(self):
        return self.collection.find({},{'name':1,'tier':1})