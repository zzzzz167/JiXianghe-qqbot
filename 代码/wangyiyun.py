#--*-- coding:utf-8 --*--
import requests
import json
import time

host = 'https://cdn.ipayy.net/wangyy/api.php'

def post(data):#post请求
    post_respose = requests.post(url=host,json=data)
    post_rest = post_respose.text
    #print(post_rest)
    return post_rest

def reping():
    json_reping = {
        'format':'json'
    }
    rest_all=json.loads(post(json_reping))
    rest =rest_all['content']
    print(rest)
    return rest
