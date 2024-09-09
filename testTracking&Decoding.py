import cv2
import numpy as np
from qreader import QReader
from utils.preprocessFrame import preprocess_image

# Instancia de la clase QReader
qreader = QReader(model_size='n', min_confidence=0.2, reencode_to='utf-8')

# Captura de video desde la cámara (cambia el índice si tienes múltiples cámaras)
cap = cv2.VideoCapture(3)

while True:
    # Captura un frame
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocesa la imagen para la detección
    framePreprocess = preprocess_image(frame)
    
    # Crea una copia para mostrar las detecciones
    frameDetection = frame.copy()

    # Detecta los códigos QR en el frame preprocesado
    detections = qreader.detect(image=framePreprocess, is_bgr=True)

    # Copia del frame preprocesado para mostrar la decodificación
    frameDecode = framePreprocess.copy()

    # Procesa las detecciones
    for detection in detections:
        decoded_qr = qreader.decode(image=framePreprocess, detection_result=detection)
        # Convertir las coordenadas a enteros
        x1, y1, x2, y2 = map(int, detection['bbox_xyxy'])
        confidence = detection['confidence']
        
        if decoded_qr:
            # Dibuja el bounding box y el texto del QR decodificado en la copia del frame preprocesado
            cv2.rectangle(frameDecode, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frameDecode, decoded_qr, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Dibuja el bounding box y la confianza en la copia del frame original
        cv2.rectangle(frameDetection, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frameDetection, f'{confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Muestra el frame con los bounding boxes de detección
    cv2.imshow('Detection', frameDetection)
    
    # Muestra el frame con los códigos QR decodificados
    cv2.imshow('Decoding', frameDecode)

    # Salir del loop si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera los recursos
cap.release()
cv2.destroyAllWindows()
