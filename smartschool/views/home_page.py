# encoding: utf-8

import logging
from datetime import time
from django.http import HttpRequest
from django.http import HttpResponse

from tools.wx_biz_msg_crypt.wx_error_code import iErrorCode
from util.wx_util import WxUtil
from util.wx_xml_parse import WxXMLParse

logger = logging.getLogger( __name__ )

class HomePage:
    @staticmethod
    def Home(request: HttpRequest):

        logger.debug(request.method)
        logger.debug(request.body)
        logger.debug(request.content_type)
        logger.debug(request.content_params)
        logger.debug(request.get_raw_uri())

        # handle validation
        if request.method == 'GET':

            signature = request.GET.get("msg_signature", "")
            timestamp = request.GET.get("timestamp", "")
            nonce = request.GET.get("nonce", "")
            echostr = request.GET.get("echostr", "")

            ret, msg = WxUtil.verify_url(signature, timestamp, nonce, echostr)

            if ret == iErrorCode.WXBizMsgCrypt_OK:
                return HttpResponse(msg)
            else:
                logger.info('WECHART validation: non wechat client')
                return HttpResponse("VerifyUrl Fail!")

        # handle validation
        if request.method == 'POST':

            # extract Encrypt
            msg_tags = ['ToUserName', 'Encrypt']
            request_xml = request.body.decode()
            """:type : str"""
            xml_parser = WxXMLParse()
            msg_map = xml_parser.extract(xml=request_xml, tags=msg_tags)
            logger.info(repr(msg_map))

            # decrypt
            logger.info('call WECHART util')
            msg_signature = request.GET.get("msg_signature", "")
            timestamp = request.GET.get("timestamp", "")
            nonce     = request.GET.get("nonce", "")
            ret, msg_xml = WxUtil.decrypt_msg(msg_map['Encrypt'], msg_signature, timestamp, nonce)
            logger.info(repr(msg_xml))

            msg_tags = ['ToUserName', 'FromUserName', 'CreateTime', 'MsgType', 'Content', 'MsgId']
            msg_map = xml_parser.extract(xml=msg_xml, tags=msg_tags)
            logger.debug(repr(msg_map))

            # get FromUserName ?

            # replay
            create_time = str(int(time.time()))
            msg_map = {
                'ToUserName' : msg_map['FromUserName'],
                'FromUserName': msg_map['ToUserName'],
                'CreateTime': create_time,
                'MsgType': 'text',
                'Content': 'Hello:' + msg_map['Content'],
            }
            xml_msg = xml_parser.generate(xml_map=msg_map)
            logger.debug(repr(xml_msg))
            Ret,signature,repl_msg= WxUtil.encrypt_msg(msg=xml_msg, timestamp=timestamp, nonce=nonce)
            logger.debug(Ret + " <--->" + repr(repl_msg))

            return HttpResponse(repl_msg, content_type="text/xml")
