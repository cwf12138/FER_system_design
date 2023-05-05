import requests
import json
params={'number':'18212139396'}
url = "http://127.0.0.1:5000/add_picture_record/"
picture_address='./input/test/happy3.jpg'
#picture_address=picture_address.replace('/','//')
data = {'number': '18212139396', 'result': 'anger','picture_address':picture_address}

response = requests.post(url,json=data)
print(response.json)
'''data=json.loads(response.content.decode('utf-8'))
data1=data['datas']
print(data1)
for da in data1:
    print(da['vid'])
print(data["lens"])'''
