# coding=utf-8
__author__ = 'yiming'

import urllib.request
import urllib.parse
import json


def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36')
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8', 'ignore')
    return html


def get_addrCoor(addr):
    key = "fa1cd1b8018b0834eaccb7628cb9fec4"
    url = "http://restapi.amap.com/v3/geocode/geo?key=" + key + "&address=" + urllib.parse.quote(
        addr) + "&city=" + urllib.parse.quote("北京")
    # print(url)
    html = url_open(url)
    target = json.loads(html)
    print(target)
    if target['geocodes'] != []:
        location = target['geocodes'][0]['location']
        return location
    else:
        return ''
