from cryptography.fernet import Fernet

FERNET_KEY = b'X6xI6rJIWVNaDPR9blDms7YRCQI4reFwbJGHahwQSbY='  # your key here
cipher = Fernet(FERNET_KEY)

def encrypt_data(data: bytes) -> bytes:
    return cipher.encrypt(data)

def decrypt_data(token: bytes) -> bytes:
    return cipher.decrypt(token)
