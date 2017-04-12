# encoding: utf-8
"""
 WeChat: Custom-defined Menu

 The user-defined menu enriches official account interfaces so that the users
 can better and quickly understand the official account's features.
"""

import os
import logging
import ssl
import json
from datetime import datetime, timedelta
from urllib import request
from urllib.parse import urlencode

from util.wx_util import WxUtil
from util.wx_config import WxConfig

logger = logging.getLogger(__name__)


class WxMenu:

    @classmethod
    def create(cls):
        """
         A user-defined menu can include up to three level-one menus, and
         each level-one menu can include up to five level-two menus. A
         user-defined menu will show on WeChat client 24 hours after it is
         created due to the client's caching function. You can unfollow the
         official account and then re-follow it to check the menu's status.

         Request Description:

         HTTP request method: POST (Use Https protocol)
         English:
         https://api.wechat.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN
         Chinese:
         https://api.weixin.qq.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN
         Corporation:
         :TODO:
        """
        # get access token
        from contrib.access_token.models.access_token import AccessToken

        token = AccessToken.get_token()
        if token == None:
            return

        # load the menu
        menu: str = ''
        with open('util/menu.json', encoding='utf-8', mode='r') as fin:
            menu = fin.read()
        logger.debug(menu)

        # request wechat {create_menu} api
        url = WxConfig.CREATE_MENU_URL
        req_param = {
            'access_token': token,
            'agentid':6,
        }
        logger.info("URL:" + url + urlencode(req_param))

        ret = WxUtil.call_wx_api(cls, url=(url + urlencode(req_param)),
                           params=req_param,
                           data=menu,
                           method='POST')

        logger.info(repr(ret))
        if ret['errcode'] != 0:
            logger.error("call wx api failed!")
            return

    @classmethod
    def query(cls):
        from contrib.access_token.models.access_token import AccessToken

        token = AccessToken.get_token()
        if token == None:
            return

        url = WxConfig.GET_MENU_URL
        req_param = {
            'access_token': token,
            'agentid':6,
        }
        logger.info("URL:" + url + urlencode(req_param))

        ret = WxUtil.call_wx_api(cls, url=(url + urlencode(req_param)),
                           params=req_param,
                           data='',
                           method='POST')
        logger.info(repr(ret))
        if ret['errcode'] != 0:
            logger.error("call wx api failed!")
            return

    @classmethod
    def delete(cls):
        from contrib.access_token.models.access_token import AccessToken

        token = AccessToken.get_token()
        if token == None:
            return

        url = WxConfig.DEL_MENU_URL
        req_param = {
            'access_token': token,
            'agentid':6,
        }
        logger.info("URL:" + url + urlencode(req_param))

        ret = WxUtil.call_wx_api(cls, url=(url + urlencode(req_param)),
                           params=req_param,
                           data='',
                           method='POST')
        logger.info(repr(ret))
        if ret['errcode'] != 0:
            logger.error("call wx api failed!")
            return

def main():
    # setup
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartschool.settings")
    django.setup()

    from contrib.access_token.models.access_token import AccessToken
    WxMenu.create()

if __name__ == '__main__':
    main()
