import datetime
import json
import os
import random
import sys
import threading
import time
from os import system

import joblib
import requests
from websocket import create_connection

import mirai_def
import setu
import wangyiyun
import health
import ziyuan
import duihua
#import ziyuan

bot_qq = 机器人QQ
master_group = [管理群群号]
host = 'http://127.0.0.1:8080'
ws_host = 'ws://127.0.0.1:8080/all?sessionKey='
auth_host = host + '/auth'
session_host = host + '/verify'
friend_host = host + '/sendFriendMessage'
recall_host = host + '/recall'
group_host = host + '/sendGroupMessage'
image_host = host + '/sendImageMessage'
updata_host = host + '/uploadImage'
json_authKey={'authKey':'20ailliom'}
sleep = 0
xianceng = 0
cd_lengq = datetime.datetime(2020,8,15,0,0,0)
sosuobieming = ["搜索涩图","涩图搜索","色图搜索","搜索色图"]
suijibieming = ["来一份涩图","来一份色图"]
wyybm = ['网易云热评','网抑云热评']
moren_list = ["找我有什么事情嘛？学~长~(✿◡‿◡)","学长好啊，有什么事情尽管说呀"]
setlujing = 'F:\\技术\\项目\\姬缃核\\taootao\\group\\'
recall_time = 40
ziyuanlujing ='F:\\技术\\项目\\姬缃核\\taootao\\resource\\resfile\\'
evey = 'F:\\技术\\项目\\姬缃核\\taootao\\resource\\'

class ziyuan_group(threading.Thread):
    def __init__(self, threadID, name,lisr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.lisr = lisr
    def run(self):
        print ("Starting " + self.name)
        ziyuan.zhu(msg=self.lisr,session=session,get_msg=get_msg)
        print("stop" + self.name)

def download_img(img_url, name,lujing):
    print (img_url)
    #header = {"Authorization": "Bearer " + api_token} # 设置http header，视情况加需要的条目，这里的token是用来鉴权的一种方式
    r = requests.get(img_url, stream=True)
    print(r.status_code) # 返回状态码
    if r.status_code == 200:
        open(lujing+name+'.jpg', 'wb').write(r.content) # 将内容写入图片
        print("done")
    del r

class helpp(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        #self.lisr = lisr
    def run(self):
        print ("Starting " + self.name)
        grouo_h = mirai_def.group_msg_extract(get_msg)[0]
        with open('F:\\技术\\项目\\姬缃核\\taootao\\mirai\\help.txt','r',encoding='utf-8') as h:
            help_data = h.read()
        mirai_def.msg_group(session=session,target=grouo_h,msg=help_data,host=group_host)
        print("stop" + self.name)

class setu_group(threading.Thread):
    def __init__(self, threadID, name,lisr,x):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.lisr = lisr
        self.x = x
    def run(self):
        print ("Starting " + self.name)
        print(type(self.lisr))
        #times = datetime.datetime.now()
        #shicha_nei = (times-self.shicha).seconds
        if self.lisr[0] in suijibieming:
            if self.x[0] == 'on':    
                grouo_suiji = mirai_def.group_msg_extract(get_msg)[0]
                at_person = mirai_def.group_msg_extract(get_msg)[1]
                mirai_def.msg_group(session=session,target=grouo_suiji,msg="那好吧，真是的学长，不要光满脑子想着涩图，偶尔注意我一下啊（声音越来越小）",host=group_host)
                imageId_g_suiji = setu.suiji_updimage(session=session,type='group')
                json_group = {
                    "sessionKey": session,
                    "target": grouo_suiji,
                    "messageChain": [
                        {   "type": "At",
                            "target": at_person,
                        },
                        { "type": "Plain", "text":"学长你要的涩图来了，（小声）：要是这么喜欢涩图我变成涩图也不是不行啦\n---------（我是分割君）---------\n" },
                        {
                            "type": "Image",
                            "imageId": imageId_g_suiji
                        }
                    ]
                }
                ID = mirai_def.post(host=group_host,data=json_group)
                ID_msg = json.loads(ID)
                time.sleep(recall_time)
                json_recall = {
                    "sessionKey": session,
                    "target": ID_msg['messageId']
                }
                mirai_def.post(host=recall_host,data=json_recall)
            else:
                mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg="本群尚未开启此功能",host=group_host)
            #cd_lengq = datetime.datetime.now()
            #print(cd_lengq)
        elif self.lisr[0] in sosuobieming:
            if self.x[1] == 'on':
                grouo_sosuo = mirai_def.group_msg_extract(get_msg)[0]
                at_person_sosuo = mirai_def.group_msg_extract(get_msg)[1]
                mirai_def.msg_group(session=session,target=grouo_sosuo,msg="那好吧，真是的学长，不要光满脑子想着喜欢的二次元人物啊，偶尔注意我一下啊（声音越来越小）",host=group_host)
                imageId_g_sosuo = setu.search_updimage(session=session,type='group',person=self.lisr[1])
                json_group = {
                    "sessionKey": session,
                    "target": grouo_sosuo,
                    "messageChain": [
                        {   "type": "At",
                            "target": at_person_sosuo,
                        },
                        { "type": "Plain", "text":"学长你要的关于"+self.lisr[1]+"涩图来了，（小声）：要是这么喜欢涩图我变成涩图也不是不行啦\n---------（我是分割君）---------\n" },
                        {
                            "type": "Image",
                            "imageId": imageId_g_sosuo
                        }
                    ]
                }
                ID = mirai_def.post(host=group_host,data=json_group)
                ID_msg = json.loads(ID)
                time.sleep(recall_time)
                json_recall = {
                "sessionKey": session,
                "target": ID_msg['messageId']
                }
                mirai_def.post(host=recall_host,data=json_recall)
            #cd_lengq = datetime.datetime.now()
            #print(cd_lengq)
            else:
                mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg="本群尚未开启此功能",host=group_host)

class wangyiyun_group(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("Starting " + self.name)
        grouo_wyy = mirai_def.group_msg_extract(get_msg)[0]
        data_g = "学长又抑郁了哎\n"
        data_g = data_g + wangyiyun.reping()
        mirai_def.msg_group(session=session,target=grouo_wyy,msg=data_g,host=group_host)
        print ("Exiting " + self.name)


if __name__ == '__main__':
    try:
        session = mirai_def.auth(json_authKey,auth_host)#保存session
        mirai_def.verify(session=session,qq_number=bot_qq,host=session_host)#绑定session
        ws = create_connection(ws_host+session)#开启ws监听
        while 1:
            result = ws.recv()
            get_msg = json.loads(result)
            print(get_msg)
            if 'messageChain' in get_msg:
                msg_type = get_msg['type']
                messageChain = get_msg['messageChain']
                if len (messageChain) >1:
                    type_text = messageChain[1]
                    genre = type_text['type']
                    if sleep ==0:
                        if genre == 'Plain':
                            content = type_text['text']
                            content_list = content.split( )
                            if len(content_list) <1:
                                content_list = ['fgiaglufjedshyu']
                            if (msg_type == 'GroupMessage'):
                                print (content_list)
                                if mirai_def.group_msg_extract(get_msg)[0] in master_group:
                                    if "睡觉" in content_list[0]:
                                        sleep = 1
                                        mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='洮洮已经休眠啦',host=group_host)
                                    elif content_list[0] == '管理':
                                        if content_list[1] == '涩图搜索':
                                            y = joblib.load(setlujing+content_list[2]+"\\function.pkl")
                                            y[1] = content_list[3]
                                            print(y)
                                            joblib.dump(y,setlujing+content_list[2]+"\\function.pkl")
                                            mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='已完成',host=group_host)
                                        elif content_list[1] == '随机涩图':
                                            y = joblib.load(setlujing+content_list[2]+"\\function.pkl")
                                            y[0] = content_list[3]
                                            print(y)
                                            joblib.dump(y,setlujing+content_list[2]+"\\function.pkl")  
                                            mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='已完成',host=group_host)
                                        elif content_list[1] == '网易云':
                                            y = joblib.load(setlujing+content_list[2]+"\\function.pkl")
                                            y[2] = content_list[3]
                                            print(y)
                                            joblib.dump(y,setlujing+content_list[2]+"\\function.pkl")  
                                            mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='已完成',host=group_host)
                                        elif content_list[1] == '对话':
                                            y = joblib.load(setlujing+content_list[2]+"\\function.pkl")
                                            y[3] = content_list[3]
                                            print(y)
                                            joblib.dump(y,setlujing+content_list[2]+"\\function.pkl")
                                            mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='已完成',host=group_host)
                                        elif content_list[1] == '冷却时间':
                                            y = joblib.load(setlujing+content_list[2]+"\\function.pkl")
                                            y[5] = int(content_list[3])
                                            print(y)
                                            joblib.dump(y,setlujing+content_list[2]+"\\function.pkl")
                                            mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='已完成',host=group_host)
                                        elif content_list[1] == '资源':
                                            y = joblib.load(setlujing+content_list[2]+"\\function.pkl")
                                            y[4] = content_list[3]
                                            print(y)
                                            joblib.dump(y,setlujing+content_list[2]+"\\function.pkl")
                                            mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='已完成',host=group_host)
                                    elif content_list[0] == '上传':
                                        if content_list[1] == '资源简介':
                                            #print('test')
                                            with open('F:\\技术\\项目\\姬缃核\\taootao\\resource\\resfile\\'+content_list[2]+'.txt','w',encoding='utf-8') as sj:
                                                del content_list[0]
                                                del content_list[0]
                                                del content_list[0]
                                                wr = "\n".join(content_list)
                                                sj.write(wr)
                                                sj.close()
                                            mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='已完成',host=group_host)
                                        elif content_list[1] == '资源图片':
                                            if len(messageChain) == 3:
                                                Image_all = messageChain[2]
                                                url = Image_all['url']
                                                download_img(url,content_list[2],ziyuanlujing)
                                            mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='已完成',host=group_host)
                                        elif content_list[1] == '今日更新':
                                            if len(messageChain) == 3:
                                                Image_all = messageChain[2]
                                                url = Image_all['url']
                                                download_img(url,content_list[1],evey)
                                            mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='已完成',host=group_host)
                                        elif content_list[1] == '资源链接':
                                            with open('F:\\技术\\项目\\姬缃核\\taootao\\resource\\allres.txt','a+',encoding='utf-8') as lj:
                                                del content_list[0]
                                                del content_list[0]
                                                wr = '\n'.join(content_list)
                                                wr = wr +'\n'
                                                lj.write(wr)
                                                lj.close()
                                            mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='已完成',host=group_host) 
                                    #elif len(content_list) == 3:
                                    elif content_list[0] == '说明文档':
                                        if content_list[1] == '写入':
                                            del content_list[0]
                                            del content_list[0]
                                            wr = "\n".join(content_list)
                                            with open('F:\\技术\\项目\\姬缃核\\taootao\\mirai\\help.txt','w',encoding='utf-8') as g:
                                                g.write(wr)
                                                g.close()
                                            mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='已完成',host=group_host)
                                        elif content_list[1] == '查看':
                                            xianceng = xianceng + 1
                                            thread = helpp(xianceng, "Thread-"+str(xianceng))
                                            thread.start()

                                    elif len(content_list) == 3:
                                        if content_list[0] == '删除':
                                            if content_list[1] == '资源简介':
                                                if os.path.isfile('F:\\技术\\项目\\姬缃核\\taootao\\resource\\resfile\\'+content_list[2]+'.txt'):
                                                    os.unlink('F:\\技术\\项目\\姬缃核\\taootao\\resource\\resfile\\'+content_list[2]+'.txt')
                                                    mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='已完成',host=group_host)
                                                else:
                                                   mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='文件不存在请检查',host=group_host) 
                                            elif content_list[1] == '资源图片':
                                                if os.path.isfile('F:\\技术\\项目\\姬缃核\\taootao\\resource\\resfile\\'+content_list[2]+'.jpg'):
                                                    os.unlink('F:\\技术\\项目\\姬缃核\\taootao\\resource\\resfile\\'+content_list[2]+'.jpg')
                                                    mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='已完成',host=group_host)
                                                else:
                                                   mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='文件不存在请检查',host=group_host) 
                                            elif content_list[1] == '资源链接':
                                                with open('F:\\技术\\项目\\姬缃核\\taootao\\resource\\allres.txt','r',encoding='utf-8') as rlj:
                                                    data = rlj.read()
                                                    #lj.close()
                                                    print(data)
                                                    data_list = data.split('\n')
                                                    print(data_list)
                                                    if content_list[2] in data_list:
                                                        rm_diz = data_list.index(content_list[2])
                                                        del data_list[rm_diz]
                                                        del data_list[rm_diz]
                                                        #print(data_list)
                                                        wr = '\n'.join(data_list)
                                                        wr = wr+'\n'
                                                        with open('F:\\技术\\项目\\姬缃核\\taootao\\resource\\allres.txt','w',encoding='utf-8') as wlj:
                                                            wlj.write(wr)
                                                            wlj.close()
                                                        mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='已完成',host=group_host)
                                                    else:
                                                       mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='未找到该资源',host=group_host) 
                                    elif content_list[0] == '身体状况':
                                        mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg=health.zhu(),host=group_host)
                                        #elif content_list[0] == '上传':
                                            
                                                
                                    elif len(content_list) == 2:
                                        if content_list[0] == '查看群设置':
                                            y = joblib.load(setlujing+content_list[1]+"\\function.pkl")
                                            printf = "目前群：" + content_list[1]+" 的设置\n随机涩图："+y[0] + "\n涩图搜索:"+y[1]+"\n涩图冷却："+str(y[5])+"s\n网易云:"+y[2]+"\n资源:"+y[4]+"\n对话:" + y[3]
                                            mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg=printf,host=group_host)

                                else:
                                    if content_list[0] == '姬缃核'  or content_list[0] == '洮洮' or content_list[0] == '.'  or content_list[0] == '。':
                                        if len(content_list) == 1:
                                            msg = moren_list[random.randint(0,len(moren_list)-1)]
                                            mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg=msg,host=group_host)
                                        else:
                                            del content_list[0]
                                            x = joblib.load(setlujing+str(mirai_def.group_msg_extract(get_msg)[0])+"\\function.pkl")
                                            if content_list[0] in wyybm:
                                                if x[2] == 'on':
                                                    xianceng = xianceng + 1
                                                    thread = wangyiyun_group(xianceng, "Thread-"+str(xianceng))
                                                    thread.start()
                                                else:
                                                    mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg="本群尚未开启此功能",host=group_host)
                                            elif "涩图" in content_list[0] or "色图" in content_list[0]:
                                                times = datetime.datetime.now()
                                                shicha = (times-cd_lengq).seconds
                                                print(shicha)
                                                if shicha >= x[5]:
                                                    xianceng = xianceng +1
                                                    thread = setu_group(xianceng, "Thread-"+str(xianceng),content_list,x)
                                                    thread.start()
                                                    cd_lengq = datetime.datetime.now()
                                                else:
                                                    grouo_suiji = mirai_def.group_msg_extract(get_msg)[0]
                                                    mirai_def.msg_group(session=session,target=grouo_suiji,msg="学长，涩图看多了脑袋会变笨的，洮洮不想学长变成呆子，洮洮发自拍给学长看好不好",host=group_host)
                                            elif "help" in content_list[0] or '帮助' in content_list[0]:
                                                xianceng = xianceng + 1
                                                thread = helpp(xianceng, "Thread-"+str(xianceng))
                                                thread.start()
                                            elif "资源" in content_list[0]:
                                                if x[4] == 'on':
                                                    xianceng = xianceng+1
                                                    thread = ziyuan_group(xianceng, "Thread-"+str(xianceng),content_list)
                                                    thread.start()
                                            else:
                                                if x[3] == 'on':
                                                    duihua.zhu(content_list[0])
                    else:
                        if (msg_type == 'GroupMessage'):
                        #if mirai_def.group_msg_extract(get_msg)[0] in master_group:
                            content = type_text['text']
                            content_list = content.split( )
                            if mirai_def.group_msg_extract(get_msg)[0] in master_group:
                                if "起床" in content_list[0]:
                                    mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='啊哈，又能见到学长了好开心，梦里都梦到他了呢',host=group_host)
                                    sleep = 0
                                elif "来吃饭" in content_list[0]:
                                    mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='正在吃饭啊',host=group_host)
                                    xianceng = 0
                                    sleep = 0
                                    mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg='学长~我吃完了呀~',host=group_host)

    except KeyboardInterrupt:
        ws.close()
        sys.exit()
    except:
        time.sleep(10)
        system('python3 /home/ubuntu/mirai/jixianghe_V1/V1.py')