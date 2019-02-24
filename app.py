#!/usr/bin/python3

from vk_api import vk_api
from getpass import getpass
from print_msg import print_msg
from crypto import Crypt
import os.path

# Сделать сохранение данных учетной записи на пк где-то в шифрованном хранилище.


def auth():
    """User enters his login information."""
    username = input('Enter the email or mobile phone number: ')
    passwd = getpass('Enter the password: ')
    return username, passwd


def login():
    """Sign in to vk.com with login and password."""
    login, password = auth()
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth()
        print_msg('ok', 'Connected succesfully.')
    except vk_api.AuthError as err:
        print_msg('error', f'{err}!')
        exit()

    return vk_session


def check_credentials():
    """Check existing of config file with stored login data.
    If exists - decrypt it to login."""
    cr = Crypt()
    if os.path.isfile(cr.CONFIG_FILE):
        pass


def main():
    vk_session = login()
    api = vk_session.get_api()
    # tools = vk_api.VkTools(vk_session)
    # print(api.wall.post(message='Hello world!'))


if __name__ == '__main__':
    main()
