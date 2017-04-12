# encoding: utf-8
"""
custom django-admin commands:
https://docs.djangoproject.com/en/1.10/howto/custom-management-commands/
"""
import logging

from django.core.management.base import BaseCommand, CommandError
from util.wx_menu import WxMenu
from contrib.access_token.models.access_token import AccessToken
from contrib.address_list.models.address_list import AddressList

logger = logging.getLogger(__name__)

class Command( BaseCommand ):
    help = """Usage: python manage.py wechat refresh_access_token"""

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            'command',
            default=None,
            help='Update wechat access token',)

    def handle(self, *args, **options):
        command = options.pop('command',None)
        logger.info(repr(command))

        if command == 'refresh_access_token':
            AccessToken.refresh_access_token()
        elif command == 'refresh_address_list':
            AddressList.refresh_address_list()
        elif command == 'create_menu_list':
            WxMenu.create()
        elif command == 'get_menu_list':
            WxMenu.query()
        elif command == 'del_menu_list':
            WxMenu.delete()
        pass
