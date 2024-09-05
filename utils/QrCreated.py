#Script for creating QR code from a string of id and saving it in a image file 
import qrcode

def generar_qr(data, filename):
    # Crear el código QR
    qr = qrcode.make(data)
    # Guardar la imagen QR en un archivo
    qr.save(filename)

# Ejemplo de uso
generar_qr("898ffc19-3185-4144-a15b-a08e0d06f39c", "codigo_qr.png")