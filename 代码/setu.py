#! -coding:utf8 -*-
import threading,sys
import requests
import time
import datetime
import random
import re
import os
import json
from collections import OrderedDict

html_list = []
host='https://api.pixivic.com/ranks?'
headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/80.0.3987.163 Safari/537.36",
            "Referer": "https://www.pixiv.net/tags/good/artworks?s_mode=s_tag"} # 注意,他的referfer在pixiv,这东西搞了我好久
updata_host = 'http://127.0.0.1:8080/uploadImage'

class MulThreadDownload(threading.Thread):
    def __init__(self,url,startpos,endpos,f):
        super(MulThreadDownload,self).__init__()
        self.url = url
        self.startpos = startpos
        self.endpos = endpos
        self.fd = f

    def download(self):
        print("start thread:%s at %s" % (self.getName(), time.time()))
        headerp = {"Range":"bytes=%s-%s"%(self.startpos,self.endpos),"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) ""Chrome/80.0.3987.163 Safari/537.36","Referer": "https://www.pixiv.net/tags/good/artworks?s_mode=s_tag"}
        res = requests.get(self.url,headers=headerp)
        # res.text 是将get获取的byte类型数据自动编码，是str类型， res.content是原始的byte类型数据
        # 所以下面是直接write(res.content)
        self.fd.seek(self.startpos)
        self.fd.write(res.content)
        print("stop thread:%s at %s" % (self.getName(), time.time()))
        # f.close()

    def run(self):
        self.download()

def post(host,files,data):#post请求
    post_respose = requests.post(url=host,data=data,files=files)
    post_rest = post_respose.text
    print(post_rest)
    return post_rest

def suiji_updimage(session,type):
    suiji_setu()
    image_data={
        "img": open('./updata_suiji.jpg', "rb")
    }
    data = {
        'sessionKey':session,
        'type':type
    }
    print(image_data)
    json_imag_rest = json.loads(post(host = updata_host,files=image_data,data=data))
    ID = json_imag_rest['imageId']
    print(ID)
    return ID

def search_updimage(session,type,person):
    search(word=person)
    image_data={
        "img": open("./updata_sous.jpg", "rb")
    }
    data = {
        'sessionKey':session,
        'type':type
    }
    print(image_data)
    json_imag_rest = json.loads(post(host = updata_host,files=image_data,data=data))
    url = json_imag_rest['imageId']
    print(url)
    return url

def getday(): 
    today=datetime.date.today() 
    oneday=datetime.timedelta(random.randint(1,4)) 
    yesterday=today-oneday
    print(yesterday)
    return yesterday

def suiji_setu():
    try:
        post_host = host + 'page='+str(random.randint(1,4))+'&date=' + str(getday()) + '&mode=day&pageSize=30'
        print(post_host)
        html = requests.get(post_host).text
        all_url = re.findall('"original":"(https://i.pximg.net/img-original/img/..../../../../../../[0-9]*?_p0.*?g)"', html)
        if len(all_url) != 0:
            setu_url = all_url[random.randint(0,len(all_url)-1)]
            print('图片链接为：'+setu_url)
            url = setu_url
            #获取文件的大小和文件名
            filename = url.split('/')[-1]
            filesize = int(requests.head(url,headers=headers).headers['Content-Length'])
            print("%s filesize:%s"%(filename,filesize))

    #线程数
            threadnum = 2
    #信号量，同时只允许3个线程运行
            threading.BoundedSemaphore(threadnum)
    # 默认6线程现在，也可以通过传参的方式设置线程数
            step = filesize // threadnum
            mtd_list = []
            start = 0
            end = -1

    # 请空并生成文件
            tempf = open('./updata_suiji.jpg','w')
            tempf.close()
        # rb+ ，二进制打开，可任意位置读写
            with open('./updata_suiji.jpg','rb+') as  f:
                fileno = f.fileno()
        # 如果文件大小为11字节，那就是获取文件0-10的位置的数据。如果end = 10，说明数据已经获取完了。
                while end < filesize -1:
                    start = end +1
                    end = start + step -1
                    if end > filesize:
                        end = filesize
            # print("start:%s, end:%s"%(start,end))
            # 复制文件句柄
                    dup = os.dup(fileno)
            # print(dup)
            # 打开文件
                    fd = os.fdopen(dup,'rb+',-1)
            # print(fd)
                    t = MulThreadDownload(url,start,end,fd)
                    t.start()
                    mtd_list.append(t)
                for i in  mtd_list:
                    i.join()
        else:
            save_html()
    except:
        print("未知错误正在重试")
        time.sleep(5)
        suiji_setu()

def search(word):
    try:
        host = 'https://api.pixivic.com/illustrations?illustType=illust&searchType=original&maxSanityLevel=6&page='+str(1)+'&keyword='+word+'&pageSize=30'
        html = requests.get(host).text
        all_url = re.findall('"original":"(https://i.pximg.net/img-original/img/..../../../../../../[0-9]*?_p0.*?g)"', html)
        if len(all_url) != 0:
            setu_url = all_url[random.randint(0,len(all_url)-1)]
            url = setu_url
        #获取文件的大小和文件名
            filename = url.split('/')[-1]
            filesize = int(requests.head(url,headers=headers).headers['Content-Length'])
            print("%s filesize:%s"%(filename,filesize))

    #线程数
            threadnum = 2
    #信号量，同时只允许3个线程运行
            threading.BoundedSemaphore(threadnum)
    # 默认6线程现在，也可以通过传参的方式设置线程数
            step = filesize // threadnum
            mtd_list = []
            start = 0
            end = -1

    # 请空并生成文件
            tempf = open('./updata_sous.jpg','w')
            tempf.close()
        # rb+ ，二进制打开，可任意位置读写
            with open('./updata_sous.jpg','rb+') as  f:
                fileno = f.fileno()
        # 如果文件大小为11字节，那就是获取文件0-10的位置的数据。如果end = 10，说明数据已经获取完了。
                while end < filesize -1:
                    start = end +1
                    end = start + step -1
                    if end > filesize:
                        end = filesize
            # print("start:%s, end:%s"%(start,end))
            # 复制文件句柄
                    dup = os.dup(fileno)
            # print(dup)
            # 打开文件
                    fd = os.fdopen(dup,'rb+',-1)
            # print(fd)
                    t = MulThreadDownload(url,start,end,fd)
                    t.start()
                    mtd_list.append(t)
                for i in  mtd_list:
                    i.join()
        else:          
            response = requests.get(url='https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1596978581&di=8ad7b62011b9d53a90ab8410c73b70fb&src=http://dpic.tiankong.com/gx/07/QJ8574616543.jpg', headers=headers)
            with open('./updata_sous.jpg','wb') as f:
                f.write(response.content)
                f.close()
    except:
        print("未知错误正在重试")
        search(word=word)