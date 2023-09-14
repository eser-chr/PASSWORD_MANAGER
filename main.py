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

def listing(enc_manager:EncryptionManager) -> None:
    print(list(enc_manager.passwords.keys()))

def alter(enc_manager:EncryptionManager, key_name:str, password:str) -> None:
    encrypted = enc_manager.encrypt(password)
    enc_manager.alter(key_name, encrypted)
    enc_manager.checkpoint()

def delete(enc_manager:EncryptionManager, key_name:str) -> None:
    enc_manager.delete_password(key_name)
    enc_manager.checkpoint()

def gen(path:str) -> None:
    new_key_manager = KeyManager(path)
    new_key_manager.key_generator()

def get_key(path:str) -> KeyManager|int:
    try:
        key_manager = KeyManager(path)
        return key_manager
    except:
        print('The provided path does not point to a key file!')
        return 1

def translate(enc_manager:EncryptionManager, new_key_path:str) -> None:    
    key_manager = get_key(new_key_path)
    if key_manager == 1:
        pass
    enc_manager_2 = EncryptionManager(key_manager, Paths.passwords_path)
    for entry in enc_manager_2.passwords.keys():
        password = enc_manager.decrypt_from_dict(entry)
        new_encrypted = enc_manager_2.encrypt(password)
        enc_manager_2.alter(entry, new_encrypted)
    del enc_manager
    enc_manager_2.checkpoint()


action_map = {'save':save, 'read':read, 'listing':listing,
                  'alter':alter, 'delete':delete, 'gen':gen, 'translate':translate}

def call(key_arg:str, enc_manager: EncryptionManager, options:list) -> None:
    if key_arg == 'gen':
        action_map[key_arg](*options)
    elif key_arg == 'listing':
        action_map[key_arg](enc_manager)
    else:
        action_map[key_arg](enc_manager, *options)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description = 'Perform various actions using the appropriate flag. If more actions are defined then they will follow the C.R.U.D order.')

   
    parser.add_argument('-s', '--save', nargs=2, metavar=('KEY_NAME', 'PASSWORD'), type = str, help='Save a key-value pair by providing a key_name and the associated password.\n\n')

    parser.add_argument('-r', '--read', nargs = 1, type = str, metavar = ('KEY_NAME'),help='Read the password associated with a key_name.\n\n')

    parser.add_argument('-l', '--listing', action='store_true', help='List all the existing password domains.\n\n')
    
    parser.add_argument('-a', '--alter', type = str, nargs=2, metavar=('KEY_NAME', 'PASSWORD'),help='Alter the password for a given key_name. If the key_name does not exist, the password will not be added.\n\n')
    
    parser.add_argument('-d', '--delete', nargs = 1, type = str, metavar =('KEY_NAME'), help='Delete the password associated with a key_name.\n\n')

    parser.add_argument('-g', '--gen', nargs = 1, type=str, metavar = ('<KEY_PATH>'), help='Generate a new key. The key will be stored in the path provided. The passwords are not translated automatically. See option -t, --translation.\n\n')

    parser.add_argument('-t', '--translate', nargs = 1, type = str, metavar = ('<NEW_KEY_PATH>'), help='Encrypt all the old passwords with a new key. Make sure you change the path in the paths.py file\n\n')

    args = vars(parser.parse_args()) 

    try:   
        key_manager = KeyManager(Paths.key_path)
        enc_manager = EncryptionManager(key_manager, Paths.passwords_path)
        for key_arg in args.keys():
            # print(args[key_arg])
            if args[key_arg]!=None and args[key_arg]:
                call(key_arg, enc_manager, args[key_arg])
        
    except:
        print('No key found in the path provided at file paths.py.')
        x = input('Do you want to generate a new one ? [y/n]  ')
        if x=='y':
            path = input('Provide the path:')
            gen(path)
        else:
            pass   

    
    









   