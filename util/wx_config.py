# encoding: utf-8
# module WeChatConfig

from urllib.parse import urlencode

class WxConfig:
    #外网域名
    WEB_URL = r'http://hongbey.vicp.io:20925/mobile/'

    #获取accesstoken的URL
    #https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid = id & corpsecret = secrect
    GET_TOKEN_URL = r'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'

    #获取微信服务器地址列表的URL
    #https://qyapi.weixin.qq.com/cgi-bin/getcallbackip?access_token = ACCESS_TOKEN
    GET_ADDRESS_LIST_URL = r'https://qyapi.weixin.qq.com/cgi-bin/getcallbackip?'

    #菜单的相关URL
    #https://qyapi.weixin.qq.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN&agentid=AGENTID
    CREATE_MENU_URL = r'https://qyapi.weixin.qq.com/cgi-bin/menu/create?'
    #https://qyapi.weixin.qq.com/cgi-bin/menu/get?access_token=ACCESS_TOKEN&agentid=AGENTID
    GET_MENU_URL = r'https://qyapi.weixin.qq.com/cgi-bin/menu/get?'
    #https://qyapi.weixin.qq.com/cgi-bin/menu/delete?access_token=ACCESS_TOKEN&agentid=AGENTID
    DEL_MENU_URL = r'https://qyapi.weixin.qq.com/cgi-bin/menu/delete?'

    #微信企业号唯一标识CorpID
    CORP_ID = r'xxx'
    CORP_ENCODING_AES_KEY = r'xxxx'
    #微信token
    TOKEN = r'weixin'
    #主动调用：管理组凭证密钥
    ENCODING_AES_KEY = r'EfSjLjGdJLos3JSvfpSlvHOYS7O78mbFeXq9PAUCNtz'
    ACCESS_TOKEN_URL = r'https://api.weixin.qq.com/cgi-bin/token?'
    GRANT_TYPE       = r'grant_type'

    @classmethod
    def get_config(cls) -> dict:
        config = {
            'token': cls.TOKEN,
            'encoding_aes_key': cls.ENCODING_AES_KEY,
            'corp_id': cls.CORP_ID,
        }
        return config

    @classmethod
    def get_access_token_method(cls) -> str:
        param = {
            'grant_type': cls.GRANT_TYPE,
            'appid' : cls.TOKEN,
            'secret' : cls.ENCODING_AES_KEY,
        }

        access_method = cls.ACCESS_TOKEN_URL + urlencode(param)
        return  access_method

