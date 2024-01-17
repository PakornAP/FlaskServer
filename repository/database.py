from pymongo import MongoClient

class UserDAO:
    def __init__(self, uri , port, database_name, collection_name):
        self.client = MongoClient(uri , port)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def insert_user(self, user):
        user_data = user.to_dict()
        return self.collection.insert_one(user_data)

    def find_user_by_name(self, name):
        query = {"name": name}
        result = self.collection.find_one(query)
        return User(result["name"], result["age"],result["feel"],result["filepath"],result["ismask"]) if result else None
    
    def close_connection(self):
        self.client.close()

class User:
    def __init__(self, name,age, feel,filepath,ismask):
        self.name = name if name else ""
        self.age = age if age else -1
        self.feel = feel if feel else ""
        self.filepath = filepath if filepath else ""
        self.ismask = ismask if ismask else False

    def to_dict(self):
        return {"name": self.name, "age": self.age, "feel" : self.feel, "filepath" : self.filepath, "ismask" : self.ismask}