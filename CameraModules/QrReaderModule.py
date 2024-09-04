import cv2
class QRREADER:
    def __init__(self):
        self.qr = cv2.QRCodeDetector()
        self.qrData = None

    def readQrCode(self, frame):
        self.qrData, points, straight_qrcode = self.qr.detectAndDecode(frame)
        if self.qrData:
            return self.qrData
        else:
            return None