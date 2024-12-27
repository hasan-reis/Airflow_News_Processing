from pymongo import MongoClient

class MongoSaver:
    def __init__(self, data):
        self.data = data
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["news_database"]
        self.collection = self.db["news_articles"]

    def save_to_mongo(self):
        if self.data:
            self.collection.insert_many(self.data)
            print(f"{len(self.data)} articles inserted into MongoDB.")
        else:
            print("No data to insert.")
