#--*-- coding:utf-8 --*--
import requests
import json


def post(host,data):#post请求
    post_respose = requests.post(url=host,json=data)
    post_rest = post_respose.text
    print(post_rest)
    return post_rest

def auth(date,host):#获取session
    rest_data = json.loads(post(host=host,data=date))
    session = rest_data['session']
    #print(session)
    return session

def verify(session,qq_number,host):#session绑定及校验
    json_verify = {'sessionKey':session,"qq":qq_number}
    post(host=host,data=json_verify)

def msg_friend(session,friend_qq,msg,host):#向好友列表中的人发送信息
    json_friend = {
        "sessionKey": session,
        "target": friend_qq,
        "messageChain": [
            { "type": "Plain", "text":msg }
        ]
    }
    rest=post(host,json_friend)
    return rest

def msg_group(session,target,msg,host):#发送群组消息
    json_group = {
        "sessionKey": session,
        "target": target,
        "messageChain": [
            { "type": "Plain", "text":msg },
        ]
    }
    rest=post(host=host,data=json_group)
    return rest

def friend_msg_extract(msg):#解析私聊信息
    content = ''
    messageChain = msg['messageChain']
    type_text = messageChain[1]
    genre = type_text['type']#判断信息类型避免不必要的解析错误
    if genre == 'Plain':
        content = type_text['text']
    if genre =='Image':
        content = type_text['url']
    if genre == 'Source':
        content = "我还听不懂语音，用文字吧，（；´д｀）ゞ'"
    if genre == 'face':
        content = "表情是个好东西，可惜我看不懂，（；´д｀）ゞ"

    sender = msg['sender']
    qq_number = sender['id']
    qq_name = sender['nickname']

    return qq_number,qq_name,content,genre

def group_msg_extract(msg):#解析群聊数据
    content = ''
    messageChain = msg['messageChain']
    type_text = messageChain[1]
    genre = type_text['type']
    if genre == 'Plain':#判断信息避免不必要的错误
        content = type_text['text']
    if genre =='Image':
        content = type_text['url']
    if genre == 'Face':
        content = "表情是个好东西，可惜我看不懂，（；´д｀）ゞ"
    
    sender = msg['sender']
    qq_number = sender['id']
    qq_name = sender['memberName']
    group_info = sender['group']
    group = group_info['id']
    sender_identity = sender['permission']
    
    return group,qq_number,qq_name,sender_identity,content,genre

def send_image(session,msg_type,qq_number,group,url,hsot):#图片发送
    if msg_type == 'FriendMessage':#判断消息发送位置
        json_image_qq={
            "sessionKey": session,
            "qq": qq_number,
            "urls": [url]
        }
        rest=post(host=hsot,data=json_image_qq)
        return rest
    if msg_type == 'GroupMessage':
        json_image_group={
            "sessionKey": session,
            "group": group,
            "urls": [url]
        }
        rest=post(host=hsot,data=json_image_group)#发送post请求
        return rest

