#!/usr/bin/python3

from Crypto import Random
from Crypto.Cipher import AES


class Crypt:

    def __init__(self, file='vk_config.v2.json'):
        self.CONFIG_FILE = file

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, key):
        """Encrypts config file to avoid unauthorized access."""
        with open(self.CONFIG_FILE, 'rb') as fo:
            plaintext = fo.read()
            enc = self.encrypt(plaintext, key)
        with open(self.CONFIG_FILE + '.enc', 'wb') as fo:
            fo.write(enc)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, key):
        """Decrypt existing file to sign in."""
        with open(self.CONFIG_FILE, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, key)
        with open(self.CONFIG_FILE[:-4], 'wb') as fo:
            fo.write(dec)
