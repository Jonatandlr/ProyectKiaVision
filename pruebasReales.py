import cv2
import numpy as np
from qreader import QReader
from utils.preprocessFrame import preprocess_image
from utils.get_Parking_spots_boxes import get_Parking_spots_boxes
from utils.calculate_iou import calculate_iou

# Instancia de la clase QReader
qreader = QReader(model_size='n', min_confidence=0.2, reencode_to='utf-8')

# Ruta a la máscara
MASK_PATH = "./images/paterns/MASKITA.png"

# Lee la máscara en escala de grises
mask = cv2.imread(MASK_PATH, cv2.IMREAD_GRAYSCALE)
# Obtén las propiedades iniciales de la máscara
mask_height, mask_width = mask.shape
_, binary_image = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)

# Obtén las estadísticas de los componentes conectados en la máscara
connectedComponents = cv2.connectedComponentsWithStats(binary_image, connectivity=8, ltype=cv2.CV_32S)
spots = get_Parking_spots_boxes(connectedComponents)
# print(spots)

cap = cv2.VideoCapture(3)
while True:
    # Captura un frame
    ret, frame = cap.read()
    if not ret:
        break

    # Obtén el tamaño del frame de la cámara
    frame_height, frame_width = frame.shape[:2]

    # Preprocesa la imagen para la detección
    framePreprocess = preprocess_image(frame)
    
    # Crea una copia para mostrar las detecciones
    frameDetection = frame.copy()
    frameDecode = framePreprocess.copy()

    # Detecta los códigos QR en el frame preprocesado
    detections = qreader.detect(image=framePreprocess, is_bgr=True)

    # Redimensiona la máscara y las coordenadas de los cuadros de estacionamiento
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

    # Marca todos los lugares de estacionamiento como vacíos inicialmente
    occupied_spots = []

    # Procesa las detecciones de códigos QR
    for i, detection in enumerate(detections):
        decoded_qr = qreader.decode(image=framePreprocess, detection_result=detection)
        # Convertir las coordenadas a enteros
        x1, y1, x2, y2 = map(int, detection['bbox_xyxy'])
        # print(f"x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}")

        confidence = detection['confidence']
        identifier_text = f'QR {i+1}'
        
        if decoded_qr:
            # Dibuja el bounding box y el texto del QR decodificado en la copia del frame preprocesado
            cv2.rectangle(frameDecode, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frameDecode, decoded_qr, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            

        # Dibuja el bounding box y la confianza en la copia del frame original
        cv2.rectangle(frameDetection, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frameDetection, f'{identifier_text} - Confidence: {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(frameDetection, (x1, y1), radius=5, color=(255, 0, 0), thickness=-1)  # Punto azul en (x1, y1)
        cv2.circle(frameDetection, (x2, y2), radius=5, color=(0, 0, 255), thickness=-1)  # Punto rojo en (x2, y2)

        # Verifica si el QR está dentro de algún cuadro de estacionamiento
        iou_threshold = 0.1  # Umbral de intersección
        # counter=0
        for spot in resized_spots:
            # if counter==0:
            #     counter+=1
            #     pass
            spot_x1, spot_y1, spot_x2, spot_y2 = spot
            # Bounding box del QR
            qr_box = (x1, y1, x2, y2)
            # Bounding box del lugar de estacionamiento (spot)
            spot_box = (spot_x1, spot_y1, spot_x2, spot_y2)
            # Calcula IoU entre el QR y el spot
            iou = calculate_iou(qr_box, spot_box)
            if iou > iou_threshold:
                # Marca el lugar de estacionamiento como ocupado
                occupied_spots.append(spot)
          
            # counter+=1
                


    # Dibuja los cuadros de estacionamiento
    for spot in resized_spots:
        spot_x1, spot_y1, spot_x2, spot_y2 = spot
        if spot in occupied_spots:
            # Marca el lugar de estacionamiento ocupado
            cv2.rectangle(frame, (spot_x1, spot_y1), (spot_x2, spot_y2), color=(0, 0, 255), thickness=2)
        else:
            # Marca el lugar de estacionamiento vacío
            cv2.rectangle(frame, (spot_x1, spot_y1), (spot_x2, spot_y2), color=(0, 255, 0), thickness=2)

    # Muestra el frame con los bounding boxes de detección
    cv2.imshow('Detection', frameDetection)
    
    # Muestra el frame con los códigos QR decodificados
    cv2.imshow('Decoding', frameDecode)

    # Muestra el frame con los lugares de estacionamiento
    cv2.imshow('Parking Spots', frame)

    # Salir del loop si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera los recursos
cap.release()
cv2.destroyAllWindows()
