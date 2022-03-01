import re 
import numpy as np
from numpy import genfromtxt
import pymongo
from dotenv import load_dotenv
import os
load_dotenv()


str_database_url = os.getenv('MONGO_SERVER_URL')
str_database_name = os.getenv('MONGO_DATABASE_NAME')
str_collection_name = os.getenv('MONGO_COLLECTION_NAME')

print(str_collection_name,str_database_name)


client = pymongo.MongoClient(str_database_url)
database = client[str_database_name]
collection = database[str_collection_name]


def insertOneMap(map):
    global collection
    filter = {'name':map['name']}
    collection.update_one(filter,{'$set':map},upsert=True)

def insertMany(maps):
    for map in maps:
        insertOneMap(map)

def getMapSortName(name):
    tokens = name.upper().split('-')
    indicate = [token[0] for token in tokens]
    return ''.join(indicate)


file_path = './avaMap.csv'

file_stream = open(file_path,'r')
maps = []
header = file_stream.readline()[:-1]
counter =0
for line in file_stream:
    data = line[:-1].split(',')
    data = ['0' if element=='' else element for element in data]
    data = [int(element) if len(element)==1 else element for element in data]
    data[1] = int(data[1][1:])
    # print(data)
    ref_name=getMapSortName(data[0])
    temp_dict = {
        'map_url':'',
        'name':data[0],
        'ref_name':ref_name,
        'tier':data[1],
        'wood':data[2],
        'stone':data[3],
        'ore':data[4],
        'hide':data[5],
        'fiber':data[6],
        'green_chest':data[7],
        'blue_chest':data[8],
        'gold_chest':data[9],
        'solo_dungeon':data[10],
        'group_dungeon':data[11],
        'ava_dungeon':data[12]
    }
    maps.append(temp_dict)

insertMany(maps)
# print(maps)
file_stream.close()
