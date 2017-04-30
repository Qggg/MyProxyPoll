#!/usr/bin/python3



import sys
import os
sys.path.append("../")

from Utils.GetConfig import GetConfig
from Utils.UtilClass import Singleton


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class DB_Itf(metaclass=Singleton):
#class DB_Itf:
    def __init__(self):
        self.cfg = GetConfig()
        self.__loadDB()

    def __loadDB(self):
        db_Module=None
        if self.cfg.db_type.upper() == "MONGODB":
            db_Module = "MongoDB_Itf"
        elif self.cfg.db_type.upper() == "REDIS":
            db_Module = "Redis_Itf"
        elif self.cfg.db_type.upper() == "SSDB":
            db_Module = "Ssdb_Itf"
        else:
            print("Invalid DB type",self.cfg.db_type)
            exit()
        #这个是核心语句，实现动态加载的！！！
        self.db = getattr(__import__(db_Module),db_Module)(self.cfg.db_host, self.cfg.db_port, self.cfg.db_name)
        #self.db = getattr(__import__("MongoDB_Itf"), "MongoDB_Itf")(host=self.cfg.db_host, port=self.cfg.db_port, name=self.cfg.db_name)

    def Change_Table(self, TableName):
        return self.db.Change_Table(TableName)

    def Get_One_Ip(self):
        return self.db.Get_One_Ip()

    def Pop_One_Ip(self):
        return self.db.Pop_One_Ip()

    def Get_All_Ip(self):
        return self.db.Get_All_Ip()

    def Del_One_Ip(self, aIp):
        return self.db.Del_One_Ip(aIp)

    def Ins_One_Ip(self, aIp):
        return self.db.Ins_One_Ip(aIp)

    def Clear_All(self):
        return self.db.Clear_All()

if __name__ == "__main__":
    db = DB_Itf()
    aIp = "10.10.10.11:1234"
    db.Ins_One_Ip(aIp)
    print(db.Get_All_Ip())