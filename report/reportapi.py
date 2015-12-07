#!/usr/bin/python
#coding=utf-8

import copy
import json

from common.sns_network  import SNSNetwork

OPEN_HTTP_TRANSLATE_ERROR = 1801

class ReportApi(object):
    __api = None

    def __init__(self, iplist=('ip.taobao.com',)):
        super(ReportApi, self).__init__()
        self.__api = SNSNetwork(iplist)

    def call(self,  params, url_path='/otsmobile/invoke', method='get', protocol='https'):
        cp_params = copy.deepcopy(params)
        try:
            data = self.__api.open(method, url_path, cp_params, protocol)
        except Exception, e:
            msg = 'exception occur.msg[%s], traceback[%s]' % (str(e), __import__('traceback').format_exc())
            return {'ret':OPEN_HTTP_TRANSLATE_ERROR, 'msg':msg}
        else:
            #print data
            return json.loads(data)

    def post_data(self, data):
        jdata = self.call(data)
        return jdata
    def get_data(self, data):
        jdata = self.call(data,url_path='/collect_service/getdata/')
        return jdata