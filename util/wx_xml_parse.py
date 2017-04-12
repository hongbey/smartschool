# encoding: utf-8
# module WXBizMsgCrypt
import logging
from xml.parsers.expat import ParserCreate

logger = logging.getLogger(__name__)


class WxXMLParse:
    """Extract encrypted text from xml data package and generate xml reply message."""

    Encrypt_ELEMENT = 'Encrypt'
    ToUserName_ELEMENT = 'ToUserName'

    def __init__(self):
        self.element = ''
        self.result = {}
        self.isfinal = {}
        self.tags = []

    # handler functions
    def start_element_handler(self, name, attrs):
        if name in self.tags:
            self.element = name

    def char_data_handler(self, data):
        if (self.element in self.tags) and (not self.isfinal[self.element]):
            self.result[self.element] = data
            self.isfinal[self.element] = True

    def extract(self, xml: str = '', tags: list = []) -> dict:
        """
        Extract text from xml data package

        :param xml: xml data package
        :param tags: element tags
        :return: dict of {'tag':'value'}
        """
        self.__init__()
        logger.debug("extract xml=" + xml)
        for tag in tags:
            self.isfinal[tag] = False
            self.result[tag] = ''

        self.tags = tags
        self.parser = ParserCreate()
        self.parser.StartElementHandler = self.start_element_handler
        self.parser.CharacterDataHandler = self.char_data_handler
        self.parser.Parse(xml)
        return self.result

    def generate(self, xml_map: dict = {}) -> str:
        msg_fmt_list = ['<?xml version="1.0" encoding="UTF-8"?>\n<xml>\n']
        for key in xml_map.keys():
            msg_fmt_list.append('    <')
            msg_fmt_list.append(key)
            msg_fmt_list.append(r'><![CDATA[{')
            msg_fmt_list.append(key)
            msg_fmt_list.append('}]]></')
            msg_fmt_list.append(key)
            msg_fmt_list.append('>\n')
        msg_fmt_list.append('</xml>')
        msg_format = ''.join(msg_fmt_list)

        return msg_format.format(**xml_map)


if __name__ == '__main__':

    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(name)s.%(funcName)s - %(lineno)s - %(message)s',
                        level=logging.DEBUG)

    try:
        logger.info("Step 1: Test extract")
        post_data = """<xml>
        <ToUserName><![CDATA[gh_10f6c3c3ac5a]]></ToUserName>
        <Encrypt><![CDATA[hQM/NS0ujPGbF+/8yVe61E3mUVWVO1izRlZdyv26zrVUSE3zUEBdcXITxjbjiHH38kexVdpQLCnRfbrqny1yGvgqqKTGKxJWWQ9D5WiiUKxavHRNzYVzAjYkp7esNGy7HJcl/P3BGarQF3+AWyNQ5w7xax5GbOwiXD54yri7xmNMHBOHapDzBslbnTFiEy+8sjSl4asNbn2+ZVBpqGsyKDv0ZG+DlSlXlW+gNPVLP+YxeUhJcyfp91qoa0FJagRNlkNul4mGz+sZXJs0WF7lPx6lslDGW3J66crvIIx/klpl0oa/tC6n/9c8OFQ9pp8hrLq7B9EaAGFlIyz5UhVLiWPN97JkL6JCfxVooVMEKcKRrrlRDGe8RWVM3EW/nxk9Ic37lYY5j97YZfq375AoTBdGDtoPFZsvv3Upyut1i6G0JRogUsMPlyZl9B8Pl/wcA7k7i4LYMr2yK4SxNFrBUw==]]></Encrypt>
        </xml>"""

        parser = WxXMLParse()
        result = parser.extract(xml=post_data, tags=['ToUserName', 'Encrypt'])
        ToUserName = result['ToUserName']
        Encrypt = result['Encrypt']
        logger.info("ToUserName:" + ToUserName)
        logger.info("Encrypt:" + Encrypt)

        logger.info("Step 2: Test generate")
        encrypt = 'encrypt'
        signature = 'signature'
        timestamp = 'timestamp'
        nonce = 'nonce'
        result_map = {
            'Encrypt': encrypt,
            'MsgSignature': signature,
            'TimeStamp': timestamp,
            'Nonce': nonce
        }
        msg = parser.generate(result_map)
        logger.info(msg)

        logger.info("TEST Success . . .")
    except Exception as e:
        logger.error(repr(e))
        logger.info("TEST Fail . . .")
