# 导入requests包
import requests
import re
import time
import send_message

def keep_token(token):
    url = "https://yuyue.njucm.edu.cn/gym/?state=1#/pages/index"
    my_params = {"token": token}  # 字典格式，推荐使用，它会自动帮你按照k-v拼接url
    res = requests.get(url=url, params=my_params)
    if res.status_code == 200:
        str1 = '成功：维持token时效...   ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    else:
        str1 = '失败：维持token时效...   ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        send_message.send('token刷新异常，可能导致预约失败，请尽快查看。')
    return str1


def oppoint(token,ptId):
    url = "http://yuyue.njucm.edu.cn/ccms-gym/gym/queue/appointMulti"
    my_params = {"token": token, "dateId": 2, "ptId": ptId,
                 "areaId": 3}  # 字典格式，推荐使用，它会自动帮你按照k-v拼接url
    res = requests.get(url=url, params=my_params)
    if res.status_code == 200:
        chinese = re.findall('[\u4e00-\u9fa5]', res.text)  # 汉字的范围为"\u4e00-\u9fa5"
        tips = ''
        for i in range(len(chinese)):
            tips = tips + chinese[i]
        str2 = tips + '           ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        send_message.send(tips)
    else:
        str2 = '预约失败...     ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        send_message.send('请求失败，可能导致预约失败，请尽快查看。')
    return str2
