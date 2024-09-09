import cv2
from qrdet import QRDetector
from preprocessFrame import preprocess_image

# Crear el detector de QR
detector = QRDetector(model_size='n', conf_th=0.2)

# Abrir la cámara (0 es el dispositivo por defecto, puedes cambiar el número si tienes varias cámaras)
cap = cv2.VideoCapture(3)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

while True:
    # Capturar cada cuadro de la cámara
    ret, frame = cap.read()

    if not ret:
        print("Error: No se pudo capturar el cuadro.")
        break

    framePreprocess=preprocess_image(frame)
    # Detectar códigos QR en el frame
    detections = detector.detect(image=framePreprocess, is_bgr=True)


    # Dibujar las detecciones
    for detection in detections:
        # Convertir las coordenadas a enteros
        x1, y1, x2, y2 = map(int, detection['bbox_xyxy'])
        confidence = detection['confidence']

        # Dibujar el rectángulo en la imagen
        cv2.rectangle(framePreprocess, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
        cv2.putText(framePreprocess, f'{confidence:.2f}', (x1, y1 - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, color=(0, 255, 0), thickness=2)

    # Mostrar el frame con los rectángulos de detección
    cv2.imshow('QR/Barcode Scanner', framePreprocess)

    # Salir del loop si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()



