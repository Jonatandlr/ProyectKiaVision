import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
supabase_url = os.getenv("Project_URL")
supabase_key = os.getenv("API_Key")
supabase: Client = create_client(supabase_url, supabase_key)

def updateLocation(id, newUbication):
    try:
        response = supabase.table('carros').update({"Ubicacion": newUbication}).eq('id', id).execute()
        print(response)

        if response.status_code == 200:
            print(f"Registro actualizado: {response.data}")
        else:
            print(f"Error al actualizar")
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")

updateLocation('d7fbf7fe-345a-4403-a04c-5ec74c43eeeb', "Spot 1")
