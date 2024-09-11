import cv2

class QRREADER:
    def __init__(self):
        self.qr = cv2.QRCodeDetector()
        self.qrData = None

    def readQrCode(self, frame):
        """Lee el código QR en el frame y dibuja una caja delimitadora si se detecta."""
        qr_data, points, _ = self.qr.
        if points is not None:
            # Dibuja una caja delimitadora alrededor del código QR
            points = points[0]  # points es una lista de puntos, tomamos el primero
            for i in range(len(points)):
                pt1 = tuple(map(int, points[i]))
                pt2 = tuple(map(int, points[(i + 1) % 4]))
                cv2.line(frame, pt1, pt2, (255, 255, 0), 5)  # Dibuja una línea verde
        return qr_data