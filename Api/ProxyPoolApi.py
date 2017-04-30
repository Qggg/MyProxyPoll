#!/usr/bin/python3

from flask import Flask,jsonify,request
from ProxyManager.ProxyManager import ProxyManager

app = Flask(__name__)

api_list={'get': 'get an usable proxy',
          'refresh':'refresh the proxy',
          'getall': 'show all avalible proxy',
          'delete?proxy=111.111.111.111:8888':'delete an proxy'}

apm = ProxyManager()

@app.route('/')
def root_path():
    return jsonify(api_list)

@app.route('/get/')
def get_path():
    return apm.Get_One_Ip()

@app.route('/getall/')
def getall_path():
    return jsonify(apm.Get_All_Ip())

@app.route('/refresh/')
def refresh_path():
    apm.Refresh()
    return "Refresh OK"

@app.route('/delete/',methods=["GET"])
def delete_path():
    aproxy = request.values.get("proxy")
    apm.Del_One_Ip(aproxy)
    return "Delete OK"


if __name__=='__main__':
    app.run(host='0.0.0.0',port=4999)
