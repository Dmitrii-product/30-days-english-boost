import os
import hashlib
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

def get_cipher():
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        print("WARNING: ENCRYPTION_KEY is not set in environment variables.")
        return None
    # Ensure key is bytes
    return Fernet(key.encode('utf-8'))

def encrypt_id(chat_id: int) -> str:
    cipher = get_cipher()
    if not cipher:
        return str(chat_id)
    
    chat_id_str = str(chat_id).encode('utf-8')
    encrypted = cipher.encrypt(chat_id_str)
    return encrypted.decode('utf-8')

def decrypt_id(encrypted_id: str) -> int:
    cipher = get_cipher()
    if not cipher:
        return int(encrypted_id)
    
    try:
        decrypted = cipher.decrypt(encrypted_id.encode('utf-8'))
        return int(decrypted.decode('utf-8'))
    except Exception as e:
        print(f"Failed to decrypt ID {encrypted_id}, attempting to read as plaintext: {e}")
        try:
            return int(encrypted_id)
        except ValueError:
            return 0

def hash_id(chat_id: int) -> str:
    key = os.getenv("ENCRYPTION_KEY", "default").encode('utf-8')
    h = hashlib.sha256()
    h.update(str(chat_id).encode('utf-8'))
    h.update(key)
    return h.hexdigest()
