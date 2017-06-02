#coding=utf-8
import requests

url="http://192.168.0.112:9002/"

#数据上传
payload = {
    "type":'PM4152',
    "number":'2017X03-2234',
    "maxPress":400,
    "minPress":300,
    "press":350,
    "maxPressPosition":80.0,
    "minPressPosition":60.0,
    "pressPosition":70.0,
    "minPressPower":4.5,
    "pressPower":5.0,
    "maxBack":-300,
    "minBcak":-400,
    "back":-350,
    "maxBackPosition":130.0,
    "minBackPosition":140.0,
    "backPosition":135.0,
    "minBackPower":4.5,
    "backPower":4.8,
    #"testTime":2017-6-1 21:41:00,
    "tester":"李某某",
    "testTool":"RPi3"
}

r = requests.post(url+'v1.0/upload', json=payload)
print r.text
