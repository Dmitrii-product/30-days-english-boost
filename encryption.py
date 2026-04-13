import os
import hashlib
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

def get_cipher() -> Fernet:
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise RuntimeError("ENCRYPTION_KEY is not set in environment variables.")
    try:
        return Fernet(key.encode('utf-8'))
    except Exception as e:
        raise RuntimeError(f"ENCRYPTION_KEY is invalid: {e}") from e

def ensure_encryption_ready():
    get_cipher()

def encrypt_id(chat_id: int) -> str:
    cipher = get_cipher()
    chat_id_str = str(chat_id).encode('utf-8')
    encrypted = cipher.encrypt(chat_id_str)
    return encrypted.decode('utf-8')

def decrypt_id(encrypted_id: str) -> int:
    cipher = get_cipher()
    decrypted = cipher.decrypt(encrypted_id.encode('utf-8'))
    return int(decrypted.decode('utf-8'))

def hash_id(chat_id: int) -> str:
    key = os.getenv("ENCRYPTION_KEY", "default").encode('utf-8')
    h = hashlib.sha256()
    h.update(str(chat_id).encode('utf-8'))
    h.update(key)
    return h.hexdigest()
