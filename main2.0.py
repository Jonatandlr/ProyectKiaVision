# main.py
import cv2
import numpy as np
from CameraModules.CameraControllerModule import CameraController
from CameraModules.QrReaderModule import QrReaderModule
from CommunicationModules.DBConnection import DBConnection
from utils.preprocessFrame import preprocess_image
from utils.get_Parking_spots_boxes import get_Parking_spots_boxes
from utils.calculate_iou import calculate_iou

# Configuración
camera = CameraController()
qr_reader = QrReaderModule()
db_connection = DBConnection()

MASK_PATH = "./images/paterns/mascaraBuena.png"
mask = cv2.imread(MASK_PATH, cv2.IMREAD_GRAYSCALE)
mask_height, mask_width = mask.shape
_, binary_image = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)
connectedComponents = cv2.connectedComponentsWithStats(binary_image, connectivity=8, ltype=cv2.CV_32S)
spots = get_Parking_spots_boxes(connectedComponents)

while True:
    ret, frame = camera.get_frame()
    if not ret:
        break

    frame_height, frame_width = frame.shape[:2]
    framePreprocess = preprocess_image(frame)
    frameDetection = frame.copy()
    frameDecode = framePreprocess.copy()
    
    detections = qr_reader.detect_qr(image=framePreprocess, is_bgr=True)
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
        identifier_text = f'QR {i+1}'
        decoded_qr = qr_reader.decode_qr(image=framePreprocess, detection_result=detection)

        if decoded_qr:
            cv2.rectangle(frameDecode, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frameDecode, decoded_qr, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            iou_threshold = 0.01
            for spot in resized_spots:
                spot_x1, spot_y1, spot_x2, spot_y2 = spot
                qr_box = (x1, y1, x2, y2)
                spot_box = (spot_x1, spot_y1, spot_x2, spot_y2)
                iou = calculate_iou(qr_box, spot_box)
                if iou > iou_threshold:
                    occupied_spots.append(spot)
                    spot_number = resized_spots.index(spot) + 1
                    new_location = f"Spot {spot_number}"
                    db_connection.update_location(decoded_qr, new_location)

    # Visualización (similar a lo que tienes en tu código original)
    cv2.imshow('Detection', frameDetection)
    cv2.imshow('Decoding', frameDecode)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
