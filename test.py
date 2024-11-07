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
    cap = cv2.VideoCapture(3)
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error al abrir la cámara.")
            break
        processed_frame = preprocess_image(frame)
        cv2.imshow('Grayscale Image', processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()



