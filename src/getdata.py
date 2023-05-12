import requests
import json

def get_user_profile(number):
    url='http://127.0.0.1:5000/get_user_profile/'
    url=url+number
    response=requests.get(url)
    datas=json.loads(response.content.decode('utf-8'))
    data=datas['datas']
    return data[0]


def get_picture_usage_record(number):
    url="http://127.0.0.1:5000/get_picture_record/"
    url=url+number
    response = requests.get(url)
    datas=json.loads(response.content.decode('utf-8'))
    data=datas["datas"]
    return data

def get_video_usage_record(number):
    url="http://127.0.0.1:5000/get_video_record/"
    url=url+number
    response = requests.get(url)
    datas=json.loads(response.content.decode('utf-8'))
    data=datas["datas"]
    return data

def get_camera_usage_record(number):
    url="http://127.0.0.1:5000/get_camera_record/"
    url=url+number
    response = requests.get(url)
    datas=json.loads(response.content.decode('utf-8'))
    data=datas["datas"]
    return data

if __name__=='__main__':
    a=1