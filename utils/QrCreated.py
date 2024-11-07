# #Script for creating QR code from a string of id and saving it in a image file 
# import qrcode

# def generar_qr(data, filename):
#     # Crear el código QR
#     qr = qrcode.make(data)
#     # Guardar la imagen QR en un archivo
#     qr.save(filename)

# # Ejemplo de uso
# generar_qr("898ffc19-3185-4144-a15b-a08e0d06f39c", "codigo_qr.png")
import qrcode
from PIL import Image, ImageEnhance

def create_large_qr_code(data, file_path):
    # Crear una instancia de QRCode
    qr = qrcode.QRCode(
        version=1,  # Tamaño del código QR, puedes aumentarlo si necesitas más datos
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Tamaño de cada caja del QR (aumenta este valor para agrandar el QR)
        border=4,  # Bordes alrededor del código QR
    )
    
    # Añadir datos al QR
    qr.add_data(data)
    qr.make(fit=True)
    
    # Crear una imagen del código QR
    img = qr.make_image(fill='black', back_color='white')
    
    # Guardar la imagen inicial
    img.save(file_path)
    
    # Abrir la imagen para ajustar el contraste
    img = Image.open(file_path)
    
    # Aumentar el tamaño de la imagen
    img = img.resize((img.width * 3, img.height * 3), Image.NEAREST)  # Aumenta la imagen 3 veces

    # Ajustar el contraste de la imagen
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)  # Ajusta el valor para mejorar el contraste

    # Guardar la imagen ajustada
    img.save(file_path)
    
    print(f'Código QR guardado en {file_path}')

def main():
    data = "898ffc19-3185-4144-a15b-a08e0d06f39c"  # Datos que quieres codificar
    file_path = 'large_qr_code.png'  # Ruta del archivo para guardar el QR
    create_large_qr_code(data, file_path)

if __name__ == "__main__":
    main()
