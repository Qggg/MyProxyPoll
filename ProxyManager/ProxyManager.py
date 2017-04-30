#!/usr/bin/python3

from Utils.GetConfig import GetConfig
from DB.DB_Itf import DB_Itf
from ProxyListReader import readproxylist

class ProxyManager:
    def __init__(self):
        self.cfg = GetConfig()
        self.db  = DB_Itf()
        self.rawdb = "raw"
        self.usedb = "use"

    def Refresh(self):
        self.db.Change_Table(self.rawdb)
        for readfunc in self.cfg.db_proxywebsite:
            for ips in getattr(readproxylist.Read_Proxy_List, readfunc)():
                print("get a raw ip:",ips)
                self.db.Ins_One_Ip(ips.strip())

    def Get_One_Ip(self):
        self.db.Change_Table(self.usedb)
        return self.db.Get_One_Ip()

    def Get_All_Ip(self):
        self.db.Change_Table(self.usedb)
        return self.db.Get_All_Ip()

    def Del_One_Ip(self, aIp):
        self.db.Change_Table(self.usedb)
        return self.db.Del_One_Ip(aIp)

    #保留，不对外提供
    def __Ins_One_Ip(self, aIp):
        return self.db.Ins_One_Ip(aIp)

    def Clear_All(self):
        return self.db.Clear_All()