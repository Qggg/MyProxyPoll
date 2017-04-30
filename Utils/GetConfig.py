#!/usr/bin/python3

import configparser
import os
from Utils import UtilClass

class GetConfig:
    def __init__(self):
        self.work_path = os.path.split(os.path.realpath(__file__))[0]
        self.config_path=os.path.join( self.work_path, "ProxyConfig.ini")
        self.cf = configparser.ConfigParser()
        self.cf.read(self.config_path)

    @UtilClass.LazyProperty
    def db_type(self):
        return self.cf.get("DB", "type")

    @UtilClass.LazyProperty
    def db_name(self):
        return self.cf.get("DB", "name")

    @UtilClass.LazyProperty
    def db_host(self):
        return self.cf.get("DB", "host")

    @UtilClass.LazyProperty
    def db_port(self):
        return self.cf.get("DB", "port")

    @UtilClass.LazyProperty
    def db_proxywebsite(self):
        list_website = []
        for line1 in self.cf.options("PROXY_WEBSITE"):
            if "0" != self.cf.get("PROXY_WEBSITE", line1):
                list_website.append(line1)
        return list_website


if __name__ == "__main__":
    acf = GetConfig()
    print("db_type=",acf.db_type)
    print("db_name=", acf.db_name)
    print("db_host=", acf.db_host)
    print("db_port=", acf.db_port)
    print("db_proxywebsite=", acf.db_proxywebsite)
