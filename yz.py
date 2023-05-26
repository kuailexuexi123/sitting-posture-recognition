import http.client
import mimetypes
import random
import json
# def duanxin_yz(sjh):
yzm=""
for i in range(7):
  yzm=str(random.randint(0, 9))+yzm
# print(yzm)
conn = http.client.HTTPSConnection("vip.veesing.com")
payload = 'appId=6VCME4WQVW16&appKey=95HV86WP22263HWD&phone=15396637953&templateId=1043&variables='
payload=payload+yzm
headers = {
  'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
}
conn.request("POST", "/smsApi/verifyCode", payload, headers)
res = conn.getresponse()
data = res.read()
data1=json.loads(data.decode("utf-8"))
print(data1)
  # return yzm
