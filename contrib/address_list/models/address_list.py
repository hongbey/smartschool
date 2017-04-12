# encoding: utf-8
"""
 Wechat IP Address List

 To better guarantee the security of API calls, developers can use this API
 to obtain the IP address list for WeChat Official Account System servers and
 API call limits.
"""
import logging
import ssl
import json
from datetime import datetime, timedelta
from urllib import request
from urllib.parse import urlencode

from django.db import models
from django.utils.timezone import now

from util.wx_config import WxConfig
from contrib.access_token.models.access_token import AccessToken

logger = logging.getLogger(__name__)

class AddressList(models.Model):

    ip_list = models.TextField()
    update_time:datetime = models.DateTimeField()

    class Meta:
        db_table     = 'wechat_address_list'
        verbose_name = 'Wechat Address List'

    def __str__(self):
        return "IP Address List:" + self.ip_list

    @classmethod
    def create(cls, ip_list:str, update_time:datetime):
        new_obj = cls(ip_list=ip_list, update_time=update_time)
        return new_obj

    @staticmethod
    def refresh_address_list():
        """
        Request Description:
        HTTP request method: GET
        English:
        https://api.wechat.com/cgi-bin/getcallbackip?access_token=ACCESS_TOKEN
        Chinese:
        https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=ACCESS_TOKEN

        Parameter Description:
        @accesstoken: Access token of an official account

        Return Description:
        {"ip_list":["127.0.0.1","127.0.0.1"]}

        An example of an unsuccessful JSON response (due to an invalid AppID) is as follows:
        {"errcode":40013,"errmsg":"invalid appid"}
        """
        #https: // qyapi.weixin.qq.com / cgi - bin / getcallbackip?access_token = ACCESS_TOKEN
        # retrieve the last wechat access token
        address_list : AddressList = None
        try:
            address_list = AddressList.objects.get(pk=1)
        except AddressList.DoesNotExist:
            logger.info('address_list1 does not exist, this is the first refresh')
            update_time = now() - timedelta(days=2)
            address_list = AddressList.create(ip_list='["127.0.0.1","127.0.0.1"]',
                                              update_time=update_time)

        # refresh rate: every day
        elapsed_time = now() - address_list.update_time
        one_day = 24 * 60 * 60
        if elapsed_time.total_seconds() < one_day:
            logger.info('passed_days less than one_day, do not refresh address list')
            return

        # get access token
        try:
            token = AccessToken.objects.get(pk=1)
        except AccessToken.DoesNotExist:
            logger.error('get access_token failed, please refresh_access_token')
            return

        # request wechat {get_address_list} api
        url = WxConfig.GET_ADDRESS_LIST_URL
        req_param = {
            'access_token': token.access_token,
        }
        logging.info("url: " + url + urlencode(req_param))

        req = request.Request(url=url + urlencode(req_param))

        context = ssl._create_unverified_context()

        # parse the result
        with request.urlopen(req, context=context) as response:
            try:
                # unpack response json result
                wechat_ret = json.loads(response.read().decode('utf-8'))
                logger.debug("address_list1: " + repr(wechat_ret))
                address_list.ip_list = wechat_ret['ip_list']

                # save the result
                address_list.update_time = now()
                address_list.save()
            except KeyError:
                logger.error("errcode:" + repr(wechat_ret['errcode']))
                logger.error("errmsg:" + repr(wechat_ret['errmsg']))
