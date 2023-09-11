import pickle

with open('passwords', 'rb') as f:
    password = pickle.load(f)
print(password)

print('***********')

with open('key', 'rb') as f:
    fernet = pickle.load(f)

print(fernet.decrypt(password))
