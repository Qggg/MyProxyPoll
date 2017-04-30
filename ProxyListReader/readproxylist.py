#!/usr/bin/python3
#-*- coding=utf-8 -*-
import sys

sys.path.append('../')

from Utils import UtilClass,UtilFunc
import requests
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib

class Read_Proxy_List:

    def __init__(self):
        pass

    @staticmethod
    def read_cookie(url, titlecontain, timeout_s=30):
        driver = webdriver.PhantomJS()
        driver.get(url)
        retlist = []
        #WebDriverWait(driver, 超时时长, 调用频率, 忽略异常).until(可执行方法, 超时时返回的信息)
        try:
            WebDriverWait(driver, timeout_s, 0.5).until(EC.title_contains(titlecontain))
        except Exception as e:
            print("WebDriverWait get a error:",e)
            return None
        retlist = driver.get_cookies().copy()
        #print("title:",driver.title)
        #print("cookies:",driver.get_cookies())
        #print(driver.page_source)
        driver.quit()
        return retlist

    @staticmethod
    @UtilFunc.PackException("read_kuaidaili")
    def read_kuaidaili(max_page= 10, timeout_s=30):
        """
        读取快代理网站的IP列表。
        header是分析出的，不能改变
        :param max_page: 抓取多少页的数据
        :param timeout_s: 超时时间
        :return:
        """
        header1 = {"Host": "www.kuaidaili.com",
                    "Connection": "keep-alive",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
                    "Referer": "http://www.kuaidaili.com/proxylist/1/",
                    "Accept-Encoding": "gzip, deflate, sdch",
                    "Accept-Language": "zh-CN,zh;q=0.8",
                    #"Cookie": "channelid=0; sid=1491188703700887; _ydclearance=bd42b90e23106343cf6a66fd-d531-4d12-8b25-e85d83fa97e8-1491299530"
                  }
        header = {"Accept": "*/*",
                    "Referer": "http://www.kuaidaili.com/proxylist/1/",
                    "X-Requested-With": "XMLHttpRequest",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,en,*",
                    "Host": "www.kuaidaili.com"
                  }

        url_list = ("http://www.kuaidaili.com/proxylist/{pageno}".format(pageno = page) for page in range(1, max_page+1, 1) )

        cookie_dict = {}
        #先去查个cookie
        cookie_list = Read_Proxy_List.read_cookie("http://www.kuaidaili.com/proxylist/1/", "快代理")
        #转为map
        for cookie in cookie_list:
            if ('name' in cookie) and ('value' in cookie):
                cookie_dict[cookie['name']] = cookie['value']

        #print("cookie_dict=",cookie_dict)
        for url in url_list:
            #print("url=", url)
            htmlresponse = requests.get(url, headers=header, cookies=cookie_dict,timeout=timeout_s)
            #htmlresponse = requests.get(url, headers=header, timeout=timeout_s)
            iplistn = re.findall(r'IP">(.*?)</(.*?)PORT">(.*?)<', htmlresponse.text, re.S)  ##表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！
            for amatch in iplistn:
                #print(amatch[0]+":"+amatch[2])
                yield (amatch[0]+":"+amatch[2])




    @staticmethod
    @UtilFunc.PackException("read_66ip")
    def read_66ip(max_page = 10, timeout_s=30):
        """
        读取快代理网站的IP列表。
        header是分析出的，不能改变
        :param max_page: 抓取多少页的数据
        :param timeout_s: 超时时间
        :return:
        """
        header = {"Connection": "keep-alive",
                  "Cache-Control": "max-age=0",
                  "User-Agent": UtilClass.genUserAgent().GetRandomUserAgent(),
                  "Accept": "*/*",
                  "Accept-Encoding": "gzip, deflate, sdch",
                  "Accept-Language": "zh-CN,zh;q=0.8"}

        url_list = ("http://www.66ip.cn/{pageno}.html".format(pageno = page) for page in range(1, max_page+1, 1) )

        for url in url_list:
            htmlresponse = requests.get(url, headers=header, timeout=timeout_s)
            #print(htmlresponse.text)
            iplistn = re.findall(r'<tr><td>(.*?)</td><td>(.*?)</td>', htmlresponse.text, re.S)  ##表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！
            if len(iplistn)>0:
                del iplistn[0]
            for amatch in iplistn:
                #print(amatch[0]+":"+amatch[1])
                if len(amatch) == 3:
                    yield (amatch[0]+":"+amatch[2])
                elif len(amatch) == 2:
                    yield (amatch[0] + ":" + amatch[1])
                else:
                    print("read_66ip return a invalid ip:{0}".format(str(amatch)))


    @staticmethod
    @UtilFunc.PackException("youdaili")
    def read_youdaili(max_page = 10, timeout_s=30, expiredtime=48*60*60):
        header = {"Connection": "keep-alive",
                  "Cache-Control": "max-age=0",
                  "User-Agent": UtilClass.genUserAgent().GetRandomUserAgent(),
                  "Accept": "*/*",
                  "Accept-Encoding": "gzip, deflate, sdch",
                  "Accept-Language": "zh-CN,zh;q=0.8"}

        url_main = "http://www.youdaili.net/Daili/http/"
        htmlresponse = requests.get(url_main, headers=header, timeout=timeout_s)
        #print(htmlresponse.text)
        iplistn = re.findall(r'<li><p><a href="(.*?)" target(.*?)</a></p><span>(.*?)</span', htmlresponse.text, re.S)  ##表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！
        #在0，1，2中。1是垃圾，0是支链接，2是当前时间。
        #比较2和当前，如果当前时间差超过1天就不用爬取。
        #print("iplistn=",iplistn)

        for amatch in iplistn:
            #如果不全，那么略过
            if len(amatch) < 3:
                continue
            # 如果超时，那么略过
            inttime = time.mktime(time.strptime(amatch[2], '%Y-%m-%d %H:%M:%S'))
            if time.time()-inttime > expiredtime:
                continue
            #爬取子页面
            htmlresponse = requests.get(amatch[0], headers=header, timeout=timeout_s)
            #print(htmlresponse.text)
            iplistn = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', htmlresponse.text)
            #去重
            iplistn = list(set(iplistn))
            for aip in iplistn:
                yield aip

    @staticmethod
    @UtilFunc.PackException("read_xicidaili")
    def read_xicidaili(max_page = 10, timeout_s=30):
        """
        读取快代理网站的IP列表。
        header是分析出的，不能改变
        :param max_page: 抓取多少页的数据
        :param timeout_s: 超时时间
        :return:
        """
        header = {"Connection": "keep-alive",
                  "Cache-Control": "max-age=0",
                  "User-Agent": UtilClass.genUserAgent().GetRandomUserAgent(),
                  "Accept": "*/*",
                  "Accept-Encoding": "gzip, deflate, sdch",
                  "Accept-Language": "zh-CN,zh;q=0.8"}

        url_list = ("http://www.xicidaili.com/nn/{pageno}".format(pageno = page) for page in range(1, max_page+1, 1) )

        for url in url_list:
            htmlresponse = requests.get(url, headers=header, timeout=timeout_s)
            asoup = BeautifulSoup(htmlresponse.text, "lxml")
            tag_list = asoup.find_all("tr",class_="odd")
            for a_tr_tag in tag_list:
                td_tag_list = a_tr_tag.find_all("td")
                if len(td_tag_list) > 4:
                    #print("{0}:{1}".format(td_tag_list[1].get_text().strip(),td_tag_list[2].get_text().strip()))
                    yield ("{0}:{1}".format(td_tag_list[1].get_text().strip(), td_tag_list[2].get_text().strip()))


    @staticmethod
    #@UtilFunc.PackException("read_goubanjia")
    def read_goubanjia(max_page = 1, timeout_s=30):
        """
        这个网站出了古怪的防爬方式，暂时搞不定。
        header是分析出的，不能改变
        :param max_page: 抓取多少页的数据
        :param timeout_s: 超时时间
        :return:
        """
        header = {"Connection": "keep-alive",
                  "Cache-Control": "max-age=0",
                  "User-Agent": UtilClass.genUserAgent().GetRandomUserAgent(),
                  "Accept": "*/*",
                  "Accept-Encoding": "gzip, deflate, sdch",
                  "Accept-Language": "zh-CN,zh;q=0.8"}

        url_list = ("http://www.goubanjia.com/free/gngn/index{pageno}.shtml".format(pageno = page) for page in range(1, max_page+1, 1) )

        for url in url_list:
            htmlresponse = requests.get(url, headers=header, timeout=timeout_s)
            asoup = BeautifulSoup(htmlresponse.text, "lxml")
            #a_driver = webdriver.PhantomJS()
            #a_driver.get("http://www.goubanjia.com/free/gngn/index1.shtml")
            #asoup = BeautifulSoup(a_driver.page_source, "lxml")
            tag_list = asoup.find_all("td", class_="ip")
            print(tag_list)

            for a_tr_tag in tag_list:
                aIP = ""
                for child in a_tr_tag.children:
                    #print("child=", str(child), type(child))
                    if type(child) == type(a_tr_tag):
                        attrdict = dict(child.attrs)
                        if "style" in attrdict.keys() and attrdict["style"]=="display: none;":
                            pass
                        elif "class" in attrdict.keys() and "port" in attrdict["class"]:
                            aIP = aIP + ":" + child.get_text()
                        else:
                            if hasattr(child, "get_text"):
                                aIP += child.get_text()


                if UtilFunc.IsStringProxy(aIP):
                    print("1IP=", aIP)
                else:
                    print("2IP =", aIP)
                    print("Tag=", a_tr_tag)

    @staticmethod
    @UtilFunc.PackException("ip3366")
    def read_ip3366(max_page = 10, timeout_s=30, expiredtime=48*60*60):

        header = {"Connection": "keep-alive",
                  "Cache-Control": "max-age=0",
                  "User-Agent": UtilClass.genUserAgent().GetRandomUserAgent(),
                  "Accept": "*/*",
                  "Accept-Encoding": "gzip, deflate, sdch",
                  "Accept-Language": "zh-CN,zh;q=0.8"}

        url_main = "http://www.ip3366.net/?"
        pagelist = [{"stype":1,"page":pageno} for pageno in range(1, max_page)]
        urllist = [url_main + urllib.parse.urlencode(apage)  for apage in pagelist]

        for url in urllist:
            htmlresponse = requests.get(url, headers=header, timeout=timeout_s)
            asoup = BeautifulSoup(htmlresponse.text, "lxml")
            abody = asoup.find("tbody")
            if abody == None:
                yield None

            trlist = abody.find_all("tr")
            for atr in trlist:
                tdlist = atr.find_all("td")
                inttime = time.mktime(time.strptime(tdlist[7].get_text(), '%Y/%m/%d %H:%M:%S'))
                if time.time()-inttime>expiredtime:
                    continue
                aproxy = tdlist[0].get_text() + ":" + tdlist[1].get_text()
                yield aproxy


if __name__ == "__main__":


    #Read_Proxy_List().read_kuaidaili()
    #Read_Proxy_List().read_66ip()
    #Read_Proxy_List().read_youdaili()
    #Read_Proxy_List().read_xicidaili()
    #Read_Proxy_List().read_goubanjia()
    #Read_Proxy_List().read_ip3366()

    # print("read_kuaidaili")
    # for x in Read_Proxy_List().read_kuaidaili():
    #    print("xx=",x)
    #
    # print("read_66ip")
    # for x in Read_Proxy_List().read_66ip():
    #    print("xx=",x)
    #
    # print("read_youdaili")
    # for x in Read_Proxy_List().read_youdaili():
    #    print("xx=",x)
    #
    # print("read_xicidaili")
    # for x in Read_Proxy_List().read_xicidaili():
    #    print("xx=",x)

    print("read_ip3366")
    for x in Read_Proxy_List().read_ip3366():
       print("xx=",x)
