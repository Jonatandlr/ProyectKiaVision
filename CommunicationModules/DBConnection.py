# DBConnection.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

class DBConnection:
    def __init__(self):
        load_dotenv()
        supabase_url = os.getenv("Project_URL")
        supabase_key = os.getenv("API_Key")
        self.supabase: Client = create_client(supabase_url, supabase_key)

    def update_location(self, qr_id, new_location):
        try:
            response = self.supabase.table('carros').update({"Ubicacion": new_location}).eq('id', qr_id).execute()
            return response
        except Exception as e:
            print(f"Error updating location: {e}")
            return None
