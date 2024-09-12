import cv2
import numpy as np
from qreader import QReader
from utils.preprocessFrame import preprocess_image
from utils.get_Parking_spots_boxes import get_Parking_spots_boxes
from utils.calculate_iou import calculate_iou
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno
load_dotenv()

# Obtener los valores de las variables de entorno
supabase_url = os.getenv("Project_URL")
supabase_key = os.getenv("API_Key")
supabase: Client = create_client(supabase_url, supabase_key)

def updateLocation(qr_id, new_ubication):
    """Actualiza la ubicación de un carro en la base de datos."""
    try:
        # Actualiza el campo 'Ubicacion' del registro con el ID especificado
        response = supabase.table('carros').update({"Ubicacion": new_ubication}).eq('id', qr_id).execute()
        print(response)

        if response.status_code == 200:
            print(f"Registro actualizado: {response.data}")
        else:
            print(f"Error al actualizar")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Instancia de la clase QReader
qreader = QReader(model_size='n', min_confidence=0.2, reencode_to='utf-8')

# Ruta a la máscara
MASK_PATH = "./images/paterns/mascaraBuena.png"

# Lee la máscara en escala de grises
mask = cv2.imread(MASK_PATH, cv2.IMREAD_GRAYSCALE)
mask_height, mask_width = mask.shape
_, binary_image = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)

# Obtener los lugares de estacionamiento de la máscara
connectedComponents = cv2.connectedComponentsWithStats(binary_image, connectivity=8, ltype=cv2.CV_32S)
spots = get_Parking_spots_boxes(connectedComponents)

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_height, frame_width = frame.shape[:2]
    frameBefore = frame.copy()
    framePreprocess = preprocess_image(frame)
    frameDetection = frame.copy()
    frameDecode = framePreprocess.copy()

    # Detectar códigos QR
    detections = qreader.detect(image=framePreprocess, is_bgr=True)

    # Redimensionar la máscara y las coordenadas de los lugares de estacionamiento
    resized_mask = cv2.resize(mask, (frame_width, frame_height), interpolation=cv2.INTER_LINEAR)
    resized_spots = [
        (
            int(spot[0] * (frame_width / mask_width)),
            int(spot[1] * (frame_height / mask_height)),
            int(spot[2] * (frame_width / mask_width)),
            int(spot[3] * (frame_height / mask_height))
        )
        for spot in spots
    ]

    occupied_spots = []

    for i, detection in enumerate(detections):
        x1, y1, x2, y2 = map(int, detection['bbox_xyxy'])
        confidence = detection['confidence']
        qr_region = frameBefore[y1-10:y2+10, x1-10:x2+10]
        qr_region_gray = cv2.cvtColor(qr_region, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(qr_region_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        _, binary = cv2.threshold(qr_region_gray, 0, 255, cv2.THRESH_BINARY)
        
        decoded_qr = qreader.decode(image=binary, detection_result=detection)

        if decoded_qr:
            # Dibuja el bounding box y el texto del QR decodificado
            cv2.rectangle(frameDecode, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frameDecode, decoded_qr, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Verifica si el QR está dentro de algún lugar de estacionamiento
            for spot in resized_spots:
                spot_x1, spot_y1, spot_x2, spot_y2 = spot
                qr_box = (x1, y1, x2, y2)
                spot_box = (spot_x1, spot_y1, spot_x2, spot_y2)
                iou = calculate_iou(qr_box, spot_box)

                if iou > 0.1:
                    occupied_spots.append(spot)
                    spot_number = resized_spots.index(spot) + 1
                    new_location = f"Spot {spot_number}"
                    
                    # Actualizar ubicación del carro en la base de datos
                    updateLocation(decoded_qr, new_location)

    for spot in resized_spots:
        spot_x1, spot_y1, spot_x2, spot_y2 = spot
        color = (0, 0, 255) if spot in occupied_spots else (0, 255, 0)
        cv2.rectangle(frame, (spot_x1, spot_y1), (spot_x2, spot_y2), color=color, thickness=2)

    cv2.imshow('Parking Spots', frame)
    cv2.imshow('QR Detection', frameDetection)
    cv2.imshow('frame decode', frameDecode)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
