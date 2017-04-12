"""
WeChat: 自定义菜单管理

https://mp.weixin.qq.com/wiki/13/43de8269be54a0a6f64413e4dfa94f39.html
http://admin.wechat.com/wiki/index.php?title=Create

自定义菜单接口可实现多种类型按钮，如下
1、click：点击推事件
用户点击click类型按钮后，微信服务器会通过消息接口推送消息类型为event	的结构给开发者（参考消息接口指南），
并且带上按钮中开发者填写的key值，开发者可以通过自定义的key值与用户进行交互；
2、view：跳转URL
用户点击view类型按钮后，微信客户端将会打开开发者在按钮中填写的网页URL，可与网页授权获取用户基本信息接口结合，获得用户基本信息。
......
"""

class WechatMenu:

    @classmethod
    def create(cls):
        pass

    @classmethod
    def query(cls):
        pass

    @classmethod
    def delete(cls):
        pass
