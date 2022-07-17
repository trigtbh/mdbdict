import pymongo
from typing import *

class MDict(dict):
    def __init__(self, uri: str, *args, **kwargs):
        super(MDict, self).__init__(*args, **kwargs)
        
        self.client: pymongo.MongoClient = pymongo.MongoClient(uri)

        for database in self.client.list_databases():
            try:
                self[database["name"]] = Database(self.client[database["name"]])
            except Exception as e:
                #raise e
                pass

    def __setitem__(self, key, value):

        super(MDict, self).__setitem__(key, value)

class Database(dict):
    def __init__(self, database: pymongo.database.Database, *args, **kwargs):
        super(Database, self).__init__(*args, **kwargs)
        self.collection: pymongo.database.Database = database
        
        for collection in self.collection.list_collections():
            self[collection["name"]] = Collection(self.collection[collection["name"]])

    def __getitem__(self, key):
        if key in self:
            return super(Database, self).__getitem__(key)
        else:
            self[key] = Collection(self.collection[key])
            return super(Database, self).__getitem__(key)

class Collection(list):
    def __init__(self, collection: pymongo.collection.Collection, *args, **kwargs):
        self.collection: pymongo.collection.Collection = collection
        super(Collection, self).__init__([Post(post, self) for post in collection.find({})], *args, **kwargs)
        

    def __delitem__(self, index):
        item = self[index]
        query = {"_id": item["_id"]}
        self.collection.delete_one(query)
        super(Collection, self).__delitem__(index)

    def append(self, item):
        self.collection.insert_one(item)
        super(Collection, self).append(item)

class Post(dict):
    def __init__(self, p: dict, parent_collection: Collection, *args, **kwargs):
        super(Post, self).__init__(p, *args, **kwargs)
        self.post: dict = p
        self.parent: Collection = parent_collection

        for key, value in self.post.items():
            if isinstance(value, list):
                self[key] = AutoList(self, key, value)
            elif isinstance(value, dict):
                self[key] = AutoDict(self, key, value)

    def __setitem__(self, k: Any, v: Any):
        query = {"$set": {k: v}}
        self.parent.collection.update_one({"_id": self["_id"]}, query)
        super(Post, self).__setitem__(k, v)

    def __delitem__(self, k: Any):
        query = {"$unset": {k: 1}}
        self.parent.collection.update_one({"_id": self["_id"]}, query)
        super(Post, self).__delitem__(k)

class AutoList(list):
    def __init__(
        self,
        post: Post,
        basekey: Any,
        items: List[Any],
        *args,
        **kwargs
    ):
        super(AutoList, self).__init__(items, *args, **kwargs)
        self.post: Post = post
        self.basekey: Any = basekey
        self.items = items

        for i in range(len(self)):
            if isinstance(self[i], list):
                self[i] = AutoList(self.post, self.basekey, self[i])
            elif isinstance(self[i], dict):
                self[i] = AutoDict(self.post, self.basekey, self[i])

    def __delitem__(self, index):
        super(AutoList, self).__delitem__(index)
        self.post[self.basekey] = self.post[self.basekey]

    def append(self, item):
        super(AutoList, self).append(item)
        self.post[self.basekey] = self.post[self.basekey]

    def __setitem__(self, index, item):
        super(AutoList, self).__setitem__(index, item)
        self.post[self.basekey] = self.post[self.basekey]


class AutoDict(dict):
    def __init__(
        self,
        post: Post,
        basekey: Any,
        items: Dict[Any, Any],
        *args,
        **kwargs
    ):
        super(AutoDict, self).__init__(items, *args, **kwargs)
        self.post: Post = post
        self.basekey: Any = basekey
        self.items = items

        for k, v in self.items.items():
            if isinstance(v, list):
                self[k] = AutoList(self.post, self.basekey, v)
            elif isinstance(v, dict):
                self[k] = AutoDict(self.post, self.basekey, v)


    def __delitem__(self, index):
        super(AutoDict, self).__delitem__(index)
        self.post[self.basekey] = self.post[self.basekey]

    def __setitem__(self, index, item):
        super(AutoDict, self).__setitem__(index, item)
        self.post[self.basekey] = self.post[self.basekey]