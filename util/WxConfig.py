# encoding: utf-8
# module WeChatConfig

from urllib.parse import urlencode

class WxConfig:
    #外网域名
    sWebUrl: str = r'http://hongbey.vicp.io:20925/mobile/'

    #微信企业号唯一标识CorpID
    sCorpID: str = r'wxe0348a7abe64af77'
    #微信token
    sToken: str = r'weixin'
    #主动调用：管理组凭证密钥
    sEncodingAESKey: str = r'EfSjLjGdJLos3JSvfpSlvHOYS7O78mbFeXq9PAUCNtz'
    sAccessTokenUrl: str = r'https://api.weixin.qq.com/cgi-bin/token?'
    sGrantType: str      = r'grant_type'

    @classmethod
    def get_config(cls) -> dict:
        config = {
            'token': cls.sToken,
            'encoding_aes_key': cls.sEncodingAESKey,
            'corp_id': cls.sCorpID,
        }
        return config

    @classmethod
    def get_access_token_method(cls) -> str:
        param = {
            'grant_type': cls.sGrantType,
            'appid' : cls.sToken,
            'secret' : cls.sEncodingAESKey,
        }

        access_method = cls.sAccessTokenUrl + urlencode(param)
        return  access_method

