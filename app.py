#!/usr/bin/python3

from vk_api import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from getpass import getpass
from print_msg import print_msg
import os.path
from datetime import datetime, timedelta
from pyrogram import Client
from threading import Thread
import sys


# Сделать шифрование для файла по пинкоду (mb, hz poka chto).


def auth() -> list:
    """User enters his login information."""
    username = input('Enter the email or mobile phone number (VK): ')
    passwd = getpass('Enter the password (VK): ')
    telegram_login = input('Enter the Telegram username: ')
    return username, passwd, telegram_login


def login() -> vk.VkApi:
    """Sign in to vk.com with login and password."""
    login, password, tg_login = auth()
    vk_session = vk.VkApi(login, password)
    del login
    del password
    try:
        vk_session.auth(token_only=True)
        print_msg('ok', 'Connected succesfully.')
    except vk.AuthError as err:
        print_msg('error', f'{err}!')
        exit()

    return vk_session, tg_login


def init_telegram() -> Client:
    with open('token') as f:
        token = f.read()

    app = Client(token)
    app.start()
    return app


def listen(longpoll: VkLongPoll, api: vk.VkApiMethod, app: Client, tg_login: str):
    try:
        # Попробовать сделать "затирание" символа ^C при прерывании.
        print_msg('status', 'Listening...')
        print_msg('status', 'Press Ctrl + C to stop.')
        counter = 0
        # print('', flush=False)
        # pw = getpass(prompt='')
        # Разобраться со стикерами.
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                user_info = api.users.get(user_id=event.user_id)
                msg_time = event.datetime
                msg_time += timedelta(hours=5)
                # Debug only!
                counter += 1
                print_msg('status', f'New messages: {counter}', end='\r')
                app.send_message(tg_login,
                                 f'{msg_time.strftime("%H:%M:%S")} by {user_info[0]["first_name"]} {user_info[0]["last_name"]}: "{event.text}"')
    except KeyboardInterrupt:
        # print(' ', flush=False)
        print_msg('status', 'Interrupted by user.')
        print_msg('ok', 'Quit...')


def main():
    vk_session, telegram_login = login()
    api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    # Set up the multithreading.
    sys.stdout = sys.stderr
    app = init_telegram()
    try:
        listen_thread = Thread(target=listen, args=(
            longpoll, api, app, telegram_login))
        listen_thread.start()
    except Exception as err:
        print_msg('error', err)
    # try:
    #     app_thread = Thread(target=init_telegram)
    #     app_thread.start()
    #
    # except Exception as err:
    #     print_msg('error', err)


if __name__ == '__main__':
    main()
