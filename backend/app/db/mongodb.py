from pymongo import MongoClient
import os

def get_mongo_client():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    return client

def get_db():
    client = get_mongo_client()
    db = client['content_gen_ai']
    return db

def init_mongo_db():
    db = get_db()
    db.create_collection('users', validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['username', 'hashed_password'],
            'properties': {
                'username': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                },
                'hashed_password': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                }
            }
        }
    })
    db.create_collection('tokens', validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['user_id', 'token'],
            'properties': {
                'user_id': {
                    'bsonType': 'objectId',
                    'description': 'must be an objectId and is required'
                },
                'token': {
                    'bsonType': 'string',
                    'description': 'must be a string and is required'
                }
            }
        }
    })
