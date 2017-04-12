# encoding: utf-8

import logging
import sys
import ssl
import json
import traceback
from urllib import request
from urllib.parse import urlencode

from django.http import HttpResponse, HttpRequest

from .wx_config import WxConfig
from tools.wx_biz_msg_crypt.wx_biz_msg_crypt import WXBizMsgCrypt
from tools.wx_biz_msg_crypt.wx_error_code import iErrorCode


logger = logging.getLogger(__name__)

class WxUtil:

    def verify_url(verify_msg_sig: str = '',
                   verify_time_stamp: str = '',
                   verify_nonce: str = '',
                   verify_echo_str: str = ''):
        """
        ------------验证回调URL---------------
         *企业开启回调模式时，企业号会向验证url发送一个get请求
         假设点击验证时，企业收到类似请求：
         * GET /cgi-bin/wxpush?msg_signature=5c45ff5e21c57e6ad56bac8758b79b1d9ac89fd3&timestamp=1409659589&nonce=263014780&echostr=P9nAzCzyDtyTWESHep1vC5X9xho%2FqYX3Zpb4yKa9SKld1DsH3Iyt3tP3zNdtp%2B4RPcs8TgAE7OaBO%2BFZXvnaqQ%3D%3D
         * HTTP/1.1 Host: qy.weixin.qq.com

         接收到该请求时，企业应	1.解析出Get请求的参数，包括消息体签名(msg_signature)，时间戳(timestamp)，随机数字串(nonce)以及公众平台推送过来的随机加密字符串(echostr),
         这一步注意作URL解码。
         2.验证消息体签名的正确性
         3. 解密出echostr原文，将原文当作Get请求的response，返回给公众平台
         第2，3步可以用公众平台提供的库函数VerifyURL来实现。
        """
        WxCpt = WXBizMsgCrypt(WxConfig.TOKEN, WxConfig.ENCODING_AES_KEY, WxConfig.CORP_ID)

        Ret, sEchoStr = WxCpt.VerifyURL(verify_msg_sig, verify_time_stamp, verify_nonce, verify_echo_str)
        logger.debug(str(Ret) + " " + str(sEchoStr))
        if (Ret != iErrorCode.WXBizMsgCrypt_OK):
            logger.error("ERR: VerifyURL Ret: " + str(Ret))
            return Ret, None
        return Ret, sEchoStr

    def decrypt_msg(self, post_data: str = '',
                    msg_signature: str = '',
                    timestamp: str = '',
                    nonce: str = ''):

        WxCpt = WXBizMsgCrypt(WxConfig.TOKEN, WxConfig.ENCODING_AES_KEY, WxConfig.CORP_ID)

        Ret, Content = WxCpt.DecryptMsg(post_data, msg_signature, timestamp, nonce)
        logger.debug(str(Ret) + " " + str(Content))
        if (Ret != iErrorCode.WXBizMsgCrypt_OK):
            logger.error("ERR: DecryptMsg Ret: " + str(Ret))
            return Ret, None

        return Ret, Content

    def encrypt_msg(self, msg: str = '',
                    nonce: str = '',
                    timestamp = None):
        WxCpt = WXBizMsgCrypt(WxConfig.TOKEN, WxConfig.ENCODING_AES_KEY, WxConfig.CORP_ID)

        Ret, Signature, EncryptContent = WxCpt.EncryptMsg(msg, nonce, timestamp)

        logger.debug(str(Ret) + " " + str(Signature) + " " + str(EncryptContent))
        if (Ret != iErrorCode.WXBizMsgCrypt_OK):
            logger.error("ERR: DecryptMsg Ret: " + str(Ret))
            return Ret, None

        return Ret, Signature, EncryptContent


    def call_wx_api(cls, url: str = 'http://localhost/', params: dict = {}, data: str = '', method='GET') -> dict:
        """
        call wechat api

        :param params: url params
        :param data:   http request data
        :param method: GET | POST
        """

        wx_ret = {}
        try:
            # request wechat {url} api
            if len(params) != 0:
                url += urlencode(params)
            req = request.Request(url=url,
                                  data=data.encode(),
                                  method=method)
            context = ssl._create_unverified_context()

            # parse the result
            with request.urlopen(req, context=context) as response:
                # unpack response json result
                wx_ret: dict = json.loads(response.read().decode())
                errocde: int =  wx_ret.get('errcode', 0)
                if errocde != 0:
                    logger.error("errcode:" + repr(wx_ret['errcode']))
                    logger.error("errmsg:" +  repr(wx_ret['errmsg']))
                else:
                    wx_ret['errcode'] = 0

        except Exception as e:
            wx_ret = {'errcode': 99999, 'errmsg': 'communication error'}
            logger.error("Unexpected error:" + str(sys.exc_info()[0]))
            logger.error('\n'.join((traceback.format_exc().splitlines())))

        return wx_ret