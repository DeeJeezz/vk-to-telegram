#!/usr/bin/python3

from vk_api import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from getpass import getpass
from print_msg import print_msg
import os.path
from datetime import datetime, timedelta


# Сделать шифрование для файла по пинкоду

def auth() -> list:
    """User enters his login information."""
    username = input('Enter the email or mobile phone number: ')
    passwd = getpass('Enter the password: ')
    return username, passwd


def login() -> vk.VkApi:
    """Sign in to vk.com with login and password."""
    login, password = auth()
    vk_session = vk.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
        print_msg('ok', 'Connected succesfully.')
    except vk.AuthError as err:
        print_msg('error', f'{err}!')
        exit()

    return vk_session


def main():
    vk_session = login()
    api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    try:
        # Попробовать сделать "затирание" символа ^C при прерывании.
        print_msg('status', 'Listening...')
        print_msg('status', 'Press Ctrl + C to stop.')
        # print('', flush=False)
        # pw = getpass(prompt='')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                user_info = api.users.get(user_id=event.user_id)
                msg_time = event.datetime
                msg_time += timedelta(hours=5)
                print(f'{msg_time.strftime("%H:%M:%S")} by {user_info[0]["first_name"]} {user_info[0]["last_name"]}: "{event.text}"')
    except KeyboardInterrupt:
        # print(' ', flush=False)
        print_msg('status', 'Interrupted by user.')
        print_msg('ok', 'Quit...')

    # tools = vk.VkTools(vk_session)

    # response = api.wall.get(count=1)
    # if response['items']:
        # print(response['items'][0])
    # tools = vk_api.VkTools(vk_session)
    # print(api.wall.post(message='Hello world!'))


if __name__ == '__main__':
    main()
