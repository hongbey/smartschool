import logging

from django.http import HttpResponse, HttpRequest
from .WxConfig import WxConfig
from ..tools.WxBizMsgCrypt.WXBizMsgCrypt import WXBizMsgCrypt
from ..tools.WxBizMsgCrypt.WxErrorCode import iErrorCode

logger = logging.getLogger(__name__)

class WxUtil:

    def VerifyUrl(sVerifyMsgSig: str = '',
                  sVerifyTimeStamp: str = '',
                  sVerifyNonce: str = '',
                  sVerifyEchoStr: str = ''):
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
        WxCpt = WXBizMsgCrypt(WxConfig.sToken, WxConfig.sEncodingAESKey, WxConfig.sCorpID)

        Ret, sEchoStr = WxCpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
        logger.debug(str(Ret) + " " + str(sEchoStr))
        if (Ret != iErrorCode.WXBizMsgCrypt_OK):
            logger.error("ERR: VerifyURL Ret: " + str(Ret))
            return Ret, None

        return Ret, sEchoStr

    def DecryptMsg(self, sPostData: str = '',
                         sMsgSignature: str = '',
                         sTimeStamp: str = '',
                         sNonce: str = ''):

        WxCpt = WXBizMsgCrypt(WxConfig.sToken, WxConfig.sEncodingAESKey, WxConfig.sCorpID)

        Ret, Content = WxCpt.DecryptMsg(sPostData, sMsgSignature, sTimeStamp, sNonce)
        logger.debug(str(Ret) + " " + str(Content))
        if (Ret != iErrorCode.WXBizMsgCrypt_OK):
            logger.error("ERR: DecryptMsg Ret: " + str(Ret))
            return Ret, None

        return Ret, Content

    def EncryptMsg(self, sMsg: str = '',
                         sNonce: str = '',
                         timestamp = None):
        WxCpt = WXBizMsgCrypt(WxConfig.sToken, WxConfig.sEncodingAESKey, WxConfig.sCorpID)

        Ret, Content = WxCpt.EncryptMsg(sMsg, sNonce, timestamp)
        logger.debug(str(Ret) + " " + str(Content))
        if (Ret != iErrorCode.WXBizMsgCrypt_OK):
            logger.error("ERR: DecryptMsg Ret: " + str(Ret))
            return Ret, None

        return Ret, Content

