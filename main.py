from cryptography.fernet import Fernet
from dataclasses import dataclass
import pickle
import pandas as pd


@dataclass
class Paths:
    key_path: str = './key'
    passwords_path: str = './passwords.json'


class KeyManager():
    def __init__(self, path: str):
        self.path = path
        self.__key = None

    def key_generator(self) -> None:
        fernet = Fernet(Fernet.generate_key())
        with open(self.path, 'wb') as f:
            pickle.dump(fernet, f)

    def load_key(self) -> None:
        if self.__key != None:
            raise TypeError
        with open(self.path, 'rb') as f:
            self.__key = pickle.load(f)

    def get_key(self) -> Fernet:
        if self.__key == None:
            self.load_key()
        return self.__key


class EncryptionManager():
    def __init__(self, key_manager: KeyManager, passwords_path: str):
        self.key_manager = key_manager
        self.passwords_path = passwords_path
        try:
            self.passwords = pd.read_json(passwords_path)
        except:
            self.passwords = pd.Series({})

    # def __del__(self):
    #     # self.checkpoint()
    #     print('Goodbye')
    #     #  self.passwords.to_json(self.passwords_path)

    def checkpoint(self):
        self.passwords.to_json(self.passwords_path)

    def encrypt(self, text: str) -> str:
        fkey = self.key_manager.get_key()
        return fkey.encrypt(text.encode())

    def save_encrypted(self, name: str, encrypted: str) -> None:
        if name in self.passwords.keys():
            raise KeyError
        self.passwords[name] = encrypted

    def add_password(self, name: str, text: str) -> None:
        encrypted = self.encrypt(text)
        self.save_encrypted(name, encrypted)

    def decrypt(self, encrypted: str) -> str:
        fkey = self.key_manager.get_key()
        return fkey.decrypt(encrypted).decode()

    def decrypt_from_dict(self, name: str) -> str:
        try:
            return self.decrypt(self.passwords[name])
        except:
            print('This key name does not exist')
            raise KeyError

    # def encrypt_dict(self, dictionary: dict) -> dict:
    #     mypasswords = {}
    #     for key in dictionary.keys():
    #         mypasswords[key] = encrypt(fkey, dictionary[key])
    #         self.save_encrypted(key, )
    #     return mypasswords


# if __name__ == "main":

