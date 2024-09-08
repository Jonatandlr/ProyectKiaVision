# import cv2 as cv
# import numpy as np
# from matplotlib import pyplot as plt
# img = cv.imread('areaWithCodes.png', cv.IMREAD_GRAYSCALE)
# assert img is not None, "file could not be read, check with os.path.exists()"


# ret,th1 = cv.threshold(img,75,255,cv.THRESH_BINARY)

# th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
#             cv.THRESH_BINARY,11,2)
# blur = cv.GaussianBlur(img,(5,5),0)
# # th3 = cv.adaptiveThreshold(blur,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
# #             cv.THRESH_BINARY,11,2)

# ret3,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
# titles = ['Original Image', 'Global Thresholding (v = 127)',
#             'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
# images = [img, th1, th2, th3]
# # for i in range(4):
# #     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
# #     plt.title(titles[i])
# #     plt.xticks([]),plt.yticks([])
# # plt.show()
# plt.imshow(th1, cmap='gray')
# plt.title('Adaptive Gaussian Thresholding')
# plt.axis('off')  # Ocultar los ejes si lo prefieres
# plt.show()

import cv2
from pyzbar import pyzbar

def preprocess_image(frame):
    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicar desenfoque Gaussiano para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Mejorar el contraste con ecualización del histograma
    equalized = cv2.equalizeHist(blurred)
    
    # Aplicar umbral adaptativo para resaltar bordes
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

    
    return thresh

def decode_qr_barcodes(frame):
    # Decodificar códigos en la imagen
    decoded_objects = pyzbar.decode(frame)
    
    for obj in decoded_objects:
        # Obtener el punto superior izquierdo y el ancho/alto del bounding box
        (x, y, w, h) = obj.rect
        # Dibujar la caja alrededor del código
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Extraer el tipo de código y el texto
        barcode_data = obj.data.decode("utf-8")
        barcode_type = obj.type
        # Mostrar la información del código en la imagen
        text = f"{barcode_type}: {barcode_data}"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame


def main():
    # Abrir la cámara (0 es el dispositivo predeterminado)
    cap = cv2.VideoCapture(3)
    
    while True:
        # Capturar frame de la cámara
        ret, frame = cap.read()
        
        if not ret:
            print("Error al abrir la cámara.")
            break
        
        # Preprocesar la imagen para mejorar la detección
        processed_frame = preprocess_image(frame)
        
        # Intentar decodificar en la imagen preprocesada
        # frame_with_barcodes = decode_qr_barcodes(processed_frame)

        # Mostrar la imagen original con bounding boxes
        # cv2.imshow('QR/Barcode Scanner', frame_with_barcodes)

        # Mostrar la imagen en escala de grises
        cv2.imshow('Grayscale Image', processed_frame)

        # Romper el ciclo con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la cámara y cerrar las ventanas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()



