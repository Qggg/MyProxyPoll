from pymongo import MongoClient
import random

class MongoDB_Itf:
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name
        self.client = MongoClient("mongodb://{host}:{port}".format(host=host,port=port))
        self.db = self.client.proxy

    def Change_Table(self, TableName):
        self.name = TableName
        return self.name

    def Get_One_Ip(self):
        allip = self.Get_All_Ip()
        return random.choice(allip) if allip else None

    def Pop_One_Ip(self):
        aIp = self.Get_One_Ip()
        if aIp:
            self.Del_One_Ip(aIp)
        return aIp

    def Get_All_Ip(self):
        return [p["proxy"] for p in self.db[self.name].find() ]

    def Del_One_Ip(self, aIp):
        return self.db[self.name].delete_one({"proxy":aIp})

    def Ins_One_Ip(self, aIp):
        if self.db[self.name].find_one({"proxy":aIp}):
            return None
        else:
            return self.db[self.name].insert_one({"proxy":aIp})

    def Clear_All(self):
        return self.db[self.name].remove()


