import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener los valores de las variables de entorno
supabase_url = os.getenv("Project_URL")
supabase_key = os.getenv("API_Key")
supabase: Client = create_client(supabase_url, supabase_key)

#  Crear cliente de Supabase
# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def updateLocation(id, newUbication):
    try:
        # Actualiza el campo 'nombre' del usuario con el id especificado
        response = supabase.table('carros').update({"Ubicacion": newUbication}).eq('id', id).execute()
        print(response)

        if response.status_code == 200:
            print(f"Registro actualizado: {response.data}")
        else:
            print(f"Error al actualizar")
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Ejemplo: Actualizar el usuario con ID 1, cambiar su nombre a "Juan Pérez"
updateLocation('d7fbf7fe-345a-4403-a04c-5ec74c43eeeb', "Spot 1")
