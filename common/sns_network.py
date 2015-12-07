#!/usr/bin/python
# -*- coding: utf-8 -*-


import socket
import copy
import urllib,urllib2
from urllib2 import Request
from random import choice
import httplib

try:
    import json
except ImportError:
    import simplejson as json


#from sns_sig import hmac_sha1_sig

class SNSNetwork(object):
    _iplist = ['172.27.0.91',]

    def __init__(self,iplist=None):
        '''
        iplist:         ip列表，也可以传入域名
        '''
        #self._secret = secret
        if iplist:
            self._iplist = copy.deepcopy(iplist)

        #if sig_name:
        #    self._sig_name = sig_name

    def _mk_send_data(self, method, url_path, params):
        '''
        返回datapair:ec_params
        '''
        #sig = hmac_sha1_sig(method, url_path, params, self._secret)
        #params[self._sig_name] = sig

        #ec_params = urllib.urlencode(params)
        ec_params = json.dumps(params)
        return ec_params


    def _http_send(self, method, url_path, ec_params):
        '''
        提供一个统一的调用API接口
        '''

        uri = 'http://%s%s' % (choice(self._iplist), url_path)

        if method.lower() == 'post':
            r = Request(url=uri)
            r.add_header('x-wl-platform-version', '6.0.0')
            r.add_header("Accept", "text/javascript, text/html, application/xml, text/xml, */*")
            r.add_header("Accept-Encoding","gzip, deflate")
            r.add_header("Accept-Language","zh_CN")
            r.add_header("User-Agent"," Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A404 (5088988208)/Worklight/6.0.0")
            r.add_header("x-wl-app-version","2.11")
            #r.add_header("WL-Instance-Id","30ioui943lnq9lt5jei1rknp2b")
            r.add_header("Connection","keep-alive")
            r.add_header("X-Requested-With", "XMLHttpRequest")
            data = urllib2.urlopen(r, ec_params).read()
        elif method.lower() == 'get':
            if ec_params:
                dest_url = '%s?%s' % (uri, ec_params)
            else:
                dest_url = uri
            data = urllib2.urlopen(dest_url).read()
        else:
            raise TypeError, 'method invalid:%s' % method

        return data

    def _https_send(self, method, url_path, ec_params):
        #conn = httplib.HTTPSConnection(choice(self._iplist))
        method = method.upper()
        uri = 'https://%s%s' % (choice(self._iplist), url_path)
        if method == 'GET':
            if ec_params:
                dest_url = '%s?%s' % (uri, ec_params)
            else:
                dest_url = uri
            r = Request(url=dest_url)
            r.add_header('x-wl-platform-version', '6.0.0')
            r.add_header("Accept", "text/javascript, text/html, application/xml, text/xml, */*")
            r.add_header("Accept-Encoding","gzip, deflate")
            r.add_header("Accept-Language","zh_CN")
            r.add_header("User-Agent"," Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A404 (5088988208)/Worklight/6.0.0")
            r.add_header("x-wl-app-version","2.11")
            #r.add_header("WL-Instance-Id","30ioui943lnq9lt5jei1rknp2b")
            r.add_header("Connection","keep-alive")
            r.add_header("X-Requested-With", "XMLHttpRequest")
            data = urllib2.urlopen(r).read()
        else:
            r = Request(url=uri)
            r.add_header('x-wl-platform-version', '6.0.0')
            r.add_header("Accept", "text/javascript, text/html, application/xml, text/xml, */*")
            r.add_header("Accept-Encoding","gzip, deflate")
            r.add_header("Accept-Language","zh_CN")
            r.add_header("User-Agent"," Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A404 (5088988208)/Worklight/6.0.0")
            r.add_header("x-wl-app-version","2.11")
            #r.add_header("WL-Instance-Id","30ioui943lnq9lt5jei1rknp2b")
            r.add_header("Connection","keep-alive")
            r.add_header("X-Requested-With", "XMLHttpRequest")
            data = urllib2.urlopen(r, ec_params).read()
        return data


    def open(self, method, url_path, params, protocol='http'):
        '''
        对外提供使用
        '''

        ec_params = self._mk_send_data(method, url_path, copy.deepcopy(params))

        if protocol == 'http':
            data = self._http_send(method, url_path, ec_params)
        elif protocol == 'https':
            data = self._https_send(method, url_path, ec_params)
        else:
            raise TypeError,'protocol invalid:%s' % protocol

        return data


def main():
    api = SNSNetwork('wokao&')
    print api.open('get', '/user/info', {'openid':1, 'openkey':2})

if __name__ == '__main__':
    socket.setdefaulttimeout(5)
    main()
