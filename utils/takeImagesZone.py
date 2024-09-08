import cv2
import time
from pruebas import preprocess_image

# Abre la cámara (3 en este caso, puede ser diferente dependiendo del sistema)
cap = cv2.VideoCapture(3)

# # Ajustar la resolución de la cámara (opcional, puedes cambiar los valores según tus necesidades)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Ajustar el ancho de la imagen
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # Ajustar la altura de la imagen

# # Ajustar otros parámetros como brillo y contraste (opcional)
# cap.set(cv2.CAP_PROP_BRIGHTNESS, 1)   # Ajustar el brillo (0.0 a 1.0, el rango puede variar según la cámara)
# cap.set(cv2.CAP_PROP_CONTRAST, 0.5)     # Ajustar el contraste (0.0 a 1.0, el rango puede variar según la cámara)
# Ajustar la resolución de la cámara
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Ajustar otros parámetros
# cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.3)
# cap.set(cv2.CAP_PROP_CONTRAST, 0.5)
# cap.set(cv2.CAP_PROP_EXPOSURE, -6)  # Ajustar según las condiciones de iluminación
# cap.set(cv2.CAP_PROP_GAIN, 0.5)
# cap.set(cv2.CAP_PROP_SATURATION, 0.5)
# cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4000)
# cap.set(cv2.CAP_PROP_FOCUS, 1.0)  # Ajustar si es manual
# cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # Desactiva el autoenfoque si es necesario
# cap.set(cv2.CAP_PROP_FPS, 30)  # Ajustar según las necesidades de tu aplicación

if not cap.isOpened():
    print("No se pudo abrir la cámara")
    exit()

print("Cámara abierta")
# Captura un frame (imagen)
for i in range(8):
    ret, frame = cap.read()
    # Espera un momento para que la cámara ajuste sus parámetros
    time.sleep(1)  # Espera 2 segundos, ajusta el tiempo si es necesario

print("Foto tomada")
if ret:
    # Define el nombre de la imagen a guardar
    image_name = "areaWithCodesWyB.png"
    framecito=preprocess_image(frame)
    
    # Guarda la imagen en el disco
    cv2.imwrite(image_name, framecito)
    print(f"Foto guardada como {image_name}")

else:
    print("No se pudo capturar la imagen")

# Libera la cámara
cap.release()

# Cierra todas las ventanas abiertas (aunque no se mostraron en este caso)
cv2.destroyAllWindows()



# #aqui veo que se captura la imagen y se guarda en un archivo
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Error al capturar frame.")
#         break
    
#     cv2.imshow('Píxeles Oscuros Resaltados', frame)
        
#     # Salir del bucle si se presiona la tecla 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Liberar la cámara y cerrar las ventanas
# cap.release()
# cv2.destroyAllWindows()
