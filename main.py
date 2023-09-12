from cryptography.fernet import Fernet
from dataclasses import dataclass
import pickle
import pandas as pd
import argparse
from lib import KeyManager, EncryptionManager
from paths import Paths
import os

def save(enc_manager:EncryptionManager, key_name:str, password:str) -> None:
    encrypted = enc_manager.encrypt(password)
    enc_manager.add_encrypted(key_name, encrypted)
    enc_manager.checkpoint()

def read(enc_manager: EncryptionManager, key_name:str) -> None:
    print(enc_manager.decrypt_from_dict(key_name))

def alter(enc_manager:EncryptionManager, key_name:str, password:str) -> None:
    encrypted = enc_manager.encrypt(password)
    enc_manager.alter(key_name, encrypted)
    enc_manager.checkpoint()

def delete(enc_manager:EncryptionManager, key_name:str) -> None:
    enc_manager.delete_password(key_name)
    enc_manager.checkpoint()

def gen(enc_manager, path:str) -> None: # enc_manager is useless
    key_manager = KeyManager(path)
    key_manager.key_generator()

def translate(enc_manager:EncryptionManager, new_key_path:str) -> None:
    enc_manager_2 = EncryptionManager(KeyManager(new_key_path), Paths.passwords_path)
    for entry in enc_manager_2.passwords.keys():
        password = enc_manager.decrypt_from_dict(entry)
        new_encrypted = enc_manager_2.encrypt(password)
        enc_manager_2.alter(entry, new_encrypted)
    del enc_manager
    enc_manager_2.checkpoint()


action_map = {'save':save, 'read':read, 
                  'alter':alter, 'delete':delete, 'gen':gen, 'translate':translate}

def call(key_arg:str, enc_manager: EncryptionManager, options:list) -> None:
    action_map[key_arg](enc_manager, *options)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description = 'Perform various actions using the appropriate flag')

    # TODO What if more than one actions are defined??

    parser.add_argument('-s', '--save', nargs=2, metavar=('KEY_NAME', 'PASSWORD'), type = str, help='Save a key-value pair by providing a key_name and the associated password.\n\n')

    parser.add_argument('-r', '--read', nargs = 1, type = str, metavar = ('KEY_NAME'),help='Read the password associated with a key_name.\n\n')
    
    parser.add_argument('-a', '--alter', type = str, nargs=2, metavar=('KEY_NAME', 'PASSWORD'),help='Alter the password for a given key_name. If the key_name does not exist, the password will not be added.\n\n')
    
    parser.add_argument('-d', '--delete', nargs = 1, type = str, metavar =('KEY_NAME'), help='Delete the password associated with a key_name.\n\n')

    parser.add_argument('-g', '--gen', nargs = 1, type=str, metavar = ('<KEY_PATH>'), help='Generate a new key. The key will be stored in the current folder. The passwords are not translated automatically. See option -t, --translation.\n\n')

    parser.add_argument('-t', '--translate', nargs = 1, type = str, metavar = ('<NEW_KEY_PATH>'), help='Encrypt all the old passwords with a new key.\n\n')

    args = vars(parser.parse_args())
   
    
    
    key_manager = KeyManager(Paths.key_path)
    #Maybe add a code like a 2 step identification. Makes totally sense.
    enc_manager = EncryptionManager(key_manager, Paths.passwords_path)
    print(enc_manager.passwords)


    for key_arg in args.keys():
        if args[key_arg]!=None:
           call(key_arg, enc_manager, args[key_arg])








   