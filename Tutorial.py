import cv2
from pyzbar.pyzbar import decode
import numpy as np
#Video captura (elegir la camara)
cap = cv2.VideoCapture(1)

#Lectura de los codigos (leer los frames que nos da la camara)

while True:
   ret, frame = cap.read()

   for codes in decode(frame):
   
   info = codes.data.decode('utf-8')
   #lee los dos primeros digitos de la info del qr
   tipo = info[0:2]
   tipo = int(tipo)

   #extracción de coordenadas
   pts = np.array([codes.polygon],np.int32)
   x1,y1 = codes.rect.left, codes.rect.top

   #redimensionar
   pts = pts.reshape((-1,1,2))

   #señalar el tipo de puesto del qr que se esta leyendo, en este caso E =69

   if tipo == 69:
      #dibujar el recuadro
      cv2.polylines(frame,[pts],True,(255,255,0),5)
      cv2.putText(frame,'E0'+str(info[2:]),(x1-15,y1-15),cv2.FONT_HERSHEY_SIMPLEX,1,(255,55,0),2)
      print("El ususario es accionista de la empresa \n"
            "No. De dentificación: E",str(info[2:]))
    print(info)
#Se pueden realizar mas para identificar más usuarios
#Mostramos FPS
cv2.imshow("Lector de QR",frame)

#leemos el teclado
t = cv2.waitKey(5)
if t == 27:
   break
cv2.destroyAllWindows()
cap.realease()


