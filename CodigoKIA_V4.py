# VERSIÓN 4
#Se incluye el recuado sobre el QR cuando lo lee 
import cv2
from pyzbar import decode
from supabase import create_client, Client
from datetime import datetime
import numpy as np  

# Configurar Supabase
url: str = "https://rucchmdwalvfpsmdjawg.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ1Y2NobWR3YWx2ZnBzbWRqYXdnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjUwMzU1NDgsImV4cCI6MjA0MDYxMTU0OH0.qkaWcGeR-KqLe_UJS0uYfoPjxFfQXTLNB80vrGg_Tv0"
supabase: Client = create_client(url, key)

# Configuración de cámaras y su asignación de estacionamientos
camaras = [
    {"id": 0, "estacionamiento": "Estacionamiento 1"},  # cámara web
    #{"id": 1, "estacionamiento": "Estacionamiento 5"},  # cámara ipad
    #{"id": 4, "estacionamiento": "Estacionamiento 3"}   
]

# Inicializar las cámaras
capturas = [cv2.VideoCapture(cam["id"]) for cam in camaras]

# Se registra la hora y fecha actual
def infhora():
    inf = datetime.now()
    fecha = inf.strftime('%Y-%m-%d')
    hora = inf.strftime('%H-%M-%S')
    return hora, fecha

# Lectura de QR
try:
    while True:
        for i, camara in enumerate(camaras):
            ret, frame = capturas[i].read()
            if not ret:
                print(f"No se puede capturar el frame de la cámara {camara['id']}")
                continue

            # Se identifica el códigos QR 
            for codes in decode(frame):
                codigo = codes.data.decode('utf-8')
                
                
                puntos = codes.polygon
                if len(puntos) == 4:  
                    pts = [(p.x, p.y) for p in puntos]
                    cv2.polylines(frame, [np.array(pts)], isClosed=True, color=(0, 255, 0), thickness=3)

                # Se dibuja el cuadrado sobre el QR
                (x, y, w, h) = codes.rect
                cv2.putText(frame, codigo, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                # Se revisa si el código ya existe en la DB
                response = supabase.table("ubicación").select("*").eq("codigo_qr", codigo).execute()
                registros = response.data

                if len(registros) == 0:
                    # Si no existe el QR, se hace un nuevo registro
                    supabase.table("ubicación").insert({
                        "codigo_qr": codigo,
                        "Estacionamiento": camara["estacionamiento"],
                        "Historial_Ubicaciones": camara["estacionamiento"],
                        "fecha_registro": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }).execute()
                    print(f"Nuevo código registrado en {camara['estacionamiento']}: {codigo}")
                else:
                    # Revisión de que si cambió de estacionamiento
                    registro = registros[0]
                    ubicacion_actual = registro["Estacionamiento"]
                    historial = registro.get("Historial_Ubicaciones", "")

                    if ubicacion_actual != camara["estacionamiento"]:
                        # Actualización de la ubicación 
                        nuevo_historial = historial + f", {camara['estacionamiento']}" if historial else camara['estacionamiento']
                        supabase.table("ubicación").update({
                            "Estacionamiento": camara["estacionamiento"],
                            "Historial_Ubicaciones": nuevo_historial
                        }).eq("codigo_qr", codigo).execute()
                        print(f"El código {codigo} se ha movido a {camara['estacionamiento']}")

            # Ventanas de cámaras
            cv2.imshow(f"Lectura de código QR - {camara['estacionamiento']}", frame)

        # ESC para salir del bucle
        if cv2.waitKey(1) == 27:  
            break

except Exception as e:
    print(f"Ocurrió un error: {e}")

finally:
    # Cerrar cámaras
    for captura in capturas:
        captura.release()
    cv2.destroyAllWindows()
