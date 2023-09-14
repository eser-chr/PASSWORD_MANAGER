from cryptography.fernet import Fernet
import pickle
from pandas import read_json, Series


class KeyManager():
    def __init__(self, path: str):
        self.path = path
        self.__key = None
        # self.load_key()

    def key_generator(self) -> None:
        fernet = Fernet(Fernet.generate_key())
        with open(self.path, 'wb') as f:
            pickle.dump(fernet, f)

    def load_key(self) -> None:
        # ERROR Handling if key is not a Fernet object
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
        self.key_manager.load_key()
        self.passwords_path = passwords_path
        self.passwords = None
        try:
            self.passwords = read_json(passwords_path)
        except:
            self.passwords = Series({})
    
    def checkpoint(self):
        self.passwords.to_json(self.passwords_path)

    def encrypt(self, text: str) -> str:
        fkey = self.key_manager.get_key()
        return fkey.encrypt(text.encode())

    def add_encrypted(self, name: str, encrypted: str) -> None:
        if name in self.passwords.keys():
            raise KeyError
        self.passwords[name] = [encrypted]

    def alter(self, key_name:str, encrypted:str) -> None:
        self.passwords[key_name][0] = encrypted

    def decrypt(self, encrypted: str) -> str:
        fkey = self.key_manager.get_key()
        return fkey.decrypt(encrypted).decode()
    
    def decrypt_from_dict(self, name: str) -> str:
        try:
            return self.decrypt(self.passwords[name][0])
        except:
            print('This key name does not exist')
            raise KeyError
        
    def delete_password(self, key_name:str) ->None:
        del self.passwords[key_name]
