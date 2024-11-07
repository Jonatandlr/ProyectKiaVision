# Importamos las librerias
from ultralytics import (YOLO)
import cv2

# Leer nuestro modelo
model = YOLO("./yolov8n.pt")

# Realizar VideoCaptura
cap = cv2.VideoCapture(3)

# Bucle
while True:
    # Leer nuestros fotogramas
    ret, frame = cap.read()

    # Leemos resultados
    resultados = model.predict(frame, conf=0.50)

    # Mostramos resultados
    anotaciones = resultados[0].plot()

    # Mostramos nuestros fotogramas
    cv2.imshow("DETECTION SYSTEM", anotaciones)

    # Cerrar nuestro programa
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
