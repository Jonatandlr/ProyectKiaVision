import cv2
# from pyzbar import pyzbar

def preprocess_image(frame):
    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicar desenfoque Gaussiano para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Mejorar el contraste con ecualización del histograma
    equalized = cv2.equalizeHist(blurred)
    
    # Aplicar umbral adaptativo para resaltar bordes
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    _, binary = cv2.threshold(thresh, 0, 255, cv2.THRESH_BINARY)

    
    return gray