# -*- coding: UTF-8 -*- 
import re
import random
import requests
import mirai_def
import json

sosu = ["资源搜索","搜索资源"]
xiaz = ["资源下载","下载资源"]
jiaj = ["资源简介","资源介绍"]
suij = ["随机资源"]
everyday = ["今日更新","今日资源"]
libiao = ["资源目录","资源列表"]
updata_host = 'http://127.0.0.1:8080/uploadImage'
host = 'http://127.0.0.1:8080'
friend_host = host + '/sendFriendMessage'
group_host = host + '/sendGroupMessage'

with open ('F:\\技术\\项目\\姬缃核\\taootao\\resource\\allres.txt','r',encoding='utf-8') as m:
    data = m.read()

def post(host,files,data):#post请求
    post_respose = requests.post(url=host,data=data,files=files)
    post_rest = post_respose.text
    print(post_rest)
    return post_rest

def updimage(session,lujing):
    image_data={
        "img": open(lujing, "rb")
    }
    data = {
        'sessionKey':session,
        'type':'group'
    }
    print(image_data)
    json_imag_rest = json.loads(post(host = updata_host,files=image_data,data=data))
    url = json_imag_rest['imageId']
    print(url)
    return url

def zhu(msg,session,get_msg):
    if msg[0] in sosu:
        xiang = 0
        pattern = re.compile(r'(.*{}.*)'.format(msg[1]))
        find_data = pattern.findall(data)
        find_data_str = str(find_data)
        cangdu = len(find_data)

        if re.match(r'(.*提取码.*)',find_data_str,re.M):
            printf ="什么也没有为学长找到啊,一定是洮洮太笨了啊"
        else:
            printf = "共为学长找到 %s 个资源\n"%(cangdu)
            for x in find_data:
                xiang = xiang+1
                printf = printf + str(xiang)+'.' +x +'\n'
            printf = printf+"---------（我是分割君）---------\n找到合适的请发送 资源下载 资源名\n如果需要查看详细请发送 资源简介 资源名\n（哼~我才不会告诉学长你资源简介有图呢）"
        mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg=printf,host=group_host)
    elif msg[0] in xiaz:
        data_list = data.split('\n')
        if msg[1] in data_list:
            data_weizhi=data_list.index(msg[1])+1
            find_data = data_list[data_weizhi]
            printf = "学长要的资源来啦，学长看多了h对身体不好哦，你身边不是还有我吗?不然以后不能让我生小宝宝就...啊不是。资源在这\n"+ "资源名："+msg[1]+'\n'+find_data+"\n解压密码为：淘宝店铺次元穿梭姬免费获取资源"+"\n（小声bb）不过你偶尔玩一玩也是无所谓的，但希望他能记住我是最重要的哎"
        else:
            printf = "哼~真是个笨蛋学长。。。真拿你没办法请你检查后再来，如果真的忘了那就emm~发送资源搜索 资源名给我吧"
        mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg=printf,host=group_host)
    elif msg[0] in jiaj:
        data_list = data.split('\n')
        if msg[1] in data_list:
            grouo_suiji = mirai_def.group_msg_extract(get_msg)[0]
            at_person = mirai_def.group_msg_extract(get_msg)[1]
            with open ('F:\\技术\\项目\\姬缃核\\taootao\\resource\\resfile'+msg[1]+".txt",'r',encoding='utf-8') as j:
                printf = j.read()
                jj_url = updimage(session=session,lujing='/home/ubuntu/ziyunamulu/游戏简介目录/'+msg[1]+".jpg")
            printf ='\n学长这是游戏的简介你看是有图片吧洮洮可没骗你哦\n'+ printf+"---------（我是分割君）---------\n学长如果喜欢请发送 资源下载 资源名 给我哦"
            json_group = {
                "sessionKey": session,
                "target": grouo_suiji,
                "messageChain": [
                    {   "type": "At",
                        "target": at_person,
                    },
                    { "type": "Plain", "text":printf },
                    {
                        "type": "Image",
                        "imageId": jj_url
                    }
                ]
            }
            mirai_def.post(host=group_host,data=json_group)
        else:
            printf ="什么也没有为学长找到啊,一定是洮洮太笨了啊"
    elif msg[0] in suij:
        data_list = data.split('\n')
        printf = "既然你都要了，那我就给你几个吧\n"
        xiang = 0
        data_list = data.split('\n')
        data_cd = len(data_list)/2
        print(data_cd)
        while xiang<random.randint(1,15):
            xiang = xiang+1
            emm = data_list[random.randint(1,data_cd)*2]
            printf = printf + str(xiang)+'.' +emm +'\n'
        printf = printf+"---------（我是分割君）---------\n找到合适的请发送 资源下载 资源名\n如果需要查看详细请发送 资源简介 资源名\n（哼~我才不会告诉学长你资源简介有图呢）"
        mirai_def.msg_group(session=session,target=mirai_def.group_msg_extract(get_msg)[0],msg=printf,host=group_host)
    elif msg[0] in everyday:
        grouo_every =  mirai_def.group_msg_extract(get_msg)[0]
        at_person = mirai_def.group_msg_extract(get_msg)[1]
        every_url = updimage(session=session,lujing='/home/ubuntu/ziyunamulu/每日更新.jpg')
        json_group = {
                "sessionKey": session,
                "target": grouo_every,
                "messageChain": [
                    {   "type": "At",
                        "target": at_person,
                    },
                    {
                        "type": "Image",
                        "imageId": every_url
                    }
                ]
            }
        mirai_def.post(host=group_host,data=json_group)
    return printf