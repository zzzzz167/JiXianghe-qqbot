import requests
import json
def zhu(msg):
    url = "http://127.0.0.1:8808/message"
    data = {"msg":msg}
    res = requests.post(url=url,data=data)
    get_msg = json.loads(res.text)

    msg = get_msg['text']
    if msg=='':
        msg = "我听不懂"
    print(msg)
    return msg