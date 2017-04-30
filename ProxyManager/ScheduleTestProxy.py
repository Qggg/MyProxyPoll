#!/usr/bin/python3


import requests
from multiprocessing import pool
import os

from apscheduler.schedulers.background import BlockingScheduler
import sys
sys.path.append('../')
import Utils
from ProxyManager import ProxyManager

class ScheduleTestProxy(ProxyManager):
    def __init__(self):
        ProxyManager.__init__(self)

    def TestProxy(self, aProxy, timeout_s=10, verify_opt=False):
        try:
            proxyPara = {"http": aProxy,
                         # "https": aProxy,
                         }
            header1 = {"Connection": "keep-alive",
                      "Cache-Control": "max-age=0",
                      "User-Agent": Utils.UtilClass.genUserAgent().GetRandomUserAgent(),
                      "Accept": "*/*",
                      "Accept-Encoding": "gzip, deflate, sdch",
                      "Accept-Language": "zh-CN,zh;q=0.8"}
            header = {"Accept": "*/*",
                      "Referer": "http://www.kuaidaili.com/proxylist/1/",
                      "X-Requested-With": "XMLHttpRequest",
                      "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1",
                      "Connection": "Keep-Alive",
                      "Accept-Encoding": "gzip, deflate",
                      "Accept-Language": "zh-CN,en,*",
                      "Host": "www.kuaidaili.com"
                      }
            responses = requests.get("http://www.gz.gov.cn/", timeout=timeout_s, headers=header, proxies=proxyPara, verify=verify_opt)
            if responses.status_code == 200:
                #print("{ip} is avalible".format(ip=aProxy))
                return True
            return False
        except (ConnectionError, requests.HTTPError, requests.Timeout, requests.TooManyRedirects) as e:
            #print("requests.get error:{0}".format(str(e)))
            return False
        except BaseException as e:
            #print("requests.get error:{0}".format(str(e)))
            return False

    def ValidRawProxy(self):
        self.db.Change_Table(self.rawdb)
        aIp = self.db.Pop_One_Ip()
        while aIp:
            #print("testing proxy:{0} start".format(str(aIp)))
            if self.TestProxy(aIp):
                self.db.Change_Table(self.usedb)
                self.db.Ins_One_Ip(aIp)
                print("proxy:{0} avalible".format(str(aIp)))
            else:
                print("proxy:{0} wasted".format(str(aIp)))
                pass
            self.db.Change_Table(self.rawdb)
            aIp = self.db.Pop_One_Ip()

def PackAFunc():
    print("PackAFunc {0} start".format(os.getpid()))
    stp = ScheduleTestProxy()
    stp.ValidRawProxy()
    print("PackAFunc {0} end".format(os.getpid()))

def MultiProcess():
    process_num = 10
    stp = ScheduleTestProxy()
    stp.Refresh()
    p = pool.Pool(process_num)
    for i in range(process_num):
        p.apply_async(PackAFunc)
    p.close()
    p.join()


if __name__ == "__main__":
    #定时开启
    MultiProcess()
    scheduler = BlockingScheduler()
    scheduler.add_job(MultiProcess, "interval", minutes=10)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit) as e:
        scheduler.shutdown()
    except Exception as e:
        print("scheduler.start error:",e)
