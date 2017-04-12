# encoding: utf-8
"""
Wechat Access Token Module
"""
import json
import logging
import ssl
from urllib       import request
from urllib.parse import urlencode
from datetime     import timedelta, datetime

from django.db    import models
from django.utils import timezone

from util.wx_config import WxConfig


logger = logging.getLogger(__name__)

class AccessToken(models.Model):

    access_token = models.CharField(max_length=512)
    update_time:datetime  = models.DateTimeField()
    expires_in   = models.IntegerField()

    def __str__(self):
        return self.access_token + ":" + self.update_time.astimezone().strftime(r'%Y-%m-%d %H:%M:%S')

    @classmethod
    def create(cls, access_token:str, update_time:datetime, expires_in:int):
        new_obj = cls(access_token=access_token, update_time=update_time, expires_in=expires_in)
        return new_obj

    @classmethod
    def get_token(self):
        token: AccessToken = None
        try:
            token = AccessToken.objects.get(pk=1)
            ret = token.access_token
        except AccessToken.DoesNotExist:
            logger.error('Access token does not exist')
            ret = None

        return ret

    @classmethod
    def refresh_access_token(cls):

        # retrieve the last wechat access token
        wechat_token:AccessToken = None
        try:
            wechat_token = AccessToken.objects.get(pk=1)
        except AccessToken.DoesNotExist:
            logger.error('Wechat Access token does not exist');
            # create an expired access token
            update_time = timezone.now() - timedelta(hours=3)
            two_hours = 2 * 60 * 60
            wechat_token = AccessToken.create(access_token='wechat access token',
                                              update_time=update_time, expires_in=two_hours)
        logging.info('wechat_token: ' + str(wechat_token))
        logging.info('timezone.now():' + timezone.now().astimezone().strftime(r'%Y-%m-%d %H:%M:%S') )
        elapsed_time : timedelta = timezone.now() - wechat_token.update_time

        # if passed_seconds < one_hour, do not update access token
        # access_token的有效期目前为2个小时，需定时刷新, 这里每小時刷新一次
        one_hour = 1 * 60 * 60
        # if elapsed_time.seconds < wechat_token.expires_in:
        if elapsed_time.seconds < one_hour:
            logger.info('passed_seconds less than one_hour, do not update access token')
            return

        # get wechat access token
        """
        Request Description:
        HTTP request method: GET
        https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET

        Parameter Description:
        @ grant_type: Fill in "client_credential" to obtain the access token
        @ appid: The unique certificate of a third-party user
        @ secret: AppSecret, the key of a third-party user's certificate

        Return Description:
        An example of a successful JSON response is as follows:
        {"access_token":"ACCESS_TOKEN","expires_in":7200}

        An example of an unsuccessful JSON response is as follows (Invalid AppID):
        {"errcode": 40013, "errmsg": "invalid appid"}
        """
        #https: // qyapi.weixin.qq.com / cgi - bin / gettoken?corpid = id & corpsecret = secrect
        url = r'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
        req_param = {
            'corpid': WxConfig.CORP_ID,
            'corpsecret': WxConfig.CORP_ENCODING_AES_KEY,
        }

        req = request.Request(url=url + urlencode(req_param))
        context = ssl._create_unverified_context()
        with request.urlopen(req, context=context) as response:
            # unpack response json result
            wechat_ret:dict = json.loads(response.read().decode('utf-8'))
            logger.debug("wechat token: " + repr(wechat_ret))
            wechat_token.update_time = timezone.now()
            try:
                wechat_token.access_token = wechat_ret['access_token']
                wechat_token.expires_in = wechat_ret['expires_in']
            except:
                logger.error("refresh wechat access token failed")
                logger.error("error code:" + repr(wechat_ret['errcode']))
                logger.error("error msg:" + repr(wechat_ret['errmsg']))
                return

            # update wechat access token
            wechat_token.save()

        logger.info(repr(wechat_token))



    class Meta:
        db_table     = 'wechat_access_token'
        verbose_name = 'Wechat Access Token'
