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
import random

# Сделать шифрование для файла по пинкоду (mb, hz poka chto).


def get_blacklist():
    """Get blocked chats ids to define show them or not."""
    file_name = 'blacklist.txt'
    if os.path.isfile(file_name):
        with open(file_name) as f:
            return [line.rstrip() for line in f]
    else:
        return []


def get_whitelist():
    file_name = 'whitelist.txt'
    if os.path.isfile(file_name):
        with open(file_name) as f:
            return [line.strip() for line in f]
    else:
        return []


def auth() -> list:
    # print(get_blocked_chats())
    """User enters his login information."""
    username = input('Enter the email or mobile phone number (VK): ')
    passwd = getpass('Enter the password (VK): ')
    telegram_login = input('Enter the Telegram username: ')
    return username, passwd, telegram_login


def login() -> vk.VkApi:
    """Sign in to vk.com with login and password."""
    login, password, tg_login = auth()
    vk_session = vk.VkApi(login, password)
    # Free login and password memory.
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
    """Initialize Telegram API."""
    with open('token') as f:
        token = f.read()

    app = Client(token)
    app.start()
    return app


"""Сделать общий счетчик новых сообщений. Сделать команду, по которой можно будет запросить этот счетчик."""


def answer_message(id: int, api: vk.VkApiMethod):
    api.messages.send(user_id=id, message='Hello',
                      random_id=random.randint(0, 1000000))


def listen(longpoll: VkLongPoll, api: vk.VkApiMethod, app: Client, tg_login: str):
    """Listening to incoming messages from VK and resending it to Telegram."""
    try:
        # Попробовать сделать "затирание" символа ^C при прерывании.
        print_msg('status', 'Listening...')
        print_msg('status', 'Press Ctrl + C to stop.')
        counter = 0
        # blocked_chats = get_blacklist()

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text and str(event.user_id) in get_whitelist():
                user_info = api.users.get(user_id=event.user_id)
                msg_time = event.datetime
                msg_time += timedelta(hours=5)
                # Debug only!
                counter += 1
                print_msg('status', f'New messages: {counter}', end='\r')
                app.send_message(tg_login,
                                 f'{msg_time.strftime("%H:%M:%S")} `{event.user_id}` **{user_info[0]["first_name"]} {user_info[0]["last_name"]}**: __{event.text}__')
    except KeyboardInterrupt:
        print_msg('status', 'Interrupted by user.')
        print_msg('ok', 'Quit...')


def main():
    vk_session, telegram_login = login()
    api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    app = init_telegram()

    # Set up the multithreading.
    try:
        listen_thread = Thread(target=listen, args=(
            longpoll, api, app, telegram_login))
        listen_thread.start()
    except Exception as err:
        print_msg('error', err)


if __name__ == '__main__':
    main()
