import os
from typing import Optional, List, Tuple
from supabase import create_client, Client
from encryption import encrypt_id, decrypt_id, hash_id
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase: Optional[Client] = None
if url and key:
    supabase = create_client(url, key)
else:
    print("Warning: SUPABASE_URL or SUPABASE_KEY not set. DB functions will silently fail.")

def init_db():
    pass

def add_or_update_user(chat_id: int, level: str):
    if not supabase: return
    id_hash = hash_id(chat_id)
    encrypted_id = encrypt_id(chat_id)
    try:
        supabase.table('users').upsert({"id_hash": id_hash, "encrypted_id": encrypted_id, "level": level}).execute()
    except Exception as e:
        print(f"Error adding user to DB: {e}")

def get_user_level(chat_id: int) -> Optional[str]:
    if not supabase: return None
    id_hash = hash_id(chat_id)
    try:
        response = supabase.table('users').select('level').eq('id_hash', id_hash).execute()
        if response.data:
            return response.data[0]['level']
    except Exception as e:
        print(f"Error getting user level: {e}")
    return None

def get_all_users() -> List[Tuple[int, str]]:
    if not supabase: return []
    try:
        response = supabase.table('users').select('encrypted_id, level').execute()
        users = []
        for row in response.data:
            enc_id = row['encrypted_id']
            lvl = row['level']
            real_id = decrypt_id(enc_id)
            if real_id:
                users.append((real_id, lvl))
        return users
    except Exception as e:
        print(f"Error fetching all users: {e}")
        return []
