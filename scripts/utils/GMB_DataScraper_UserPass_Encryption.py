import os
from cryptography.fernet import Fernet
from configparser import ConfigParser


class Credentials:
    @staticmethod
    def cred_invoker():
        file_path = os.path.dirname(os.path.abspath(__file__)) + "\Credentials.ini"
        ini_file = file_path
        config = ConfigParser()
        config.read(ini_file)
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        username = config.get('credentials', 'username')
        password = config.get('credentials', 'password')
        encrypted_username = cipher_suite.encrypt(str.encode(username))
        encrypted_password = cipher_suite.encrypt(str.encode(password))
        hashed_username = cipher_suite.decrypt(encrypted_username)
        hashed_password = cipher_suite.decrypt(encrypted_password)
        formatted_username_to_string = hashed_username.decode('utf-8')
        formatted_password_to_string = hashed_password.decode('utf-8')

        return formatted_username_to_string, formatted_password_to_string
