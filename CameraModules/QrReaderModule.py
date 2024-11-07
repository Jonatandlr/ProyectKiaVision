# QrReaderModule.py
from qreader import QReader

class QrReaderModule:
    def __init__(self, model_size='n', min_confidence=0.2):
        self.qreader = QReader(model_size=model_size, min_confidence=min_confidence, reencode_to='utf-8')

    def detect_qr(self, image, is_bgr=True):
        return self.qreader.detect(image=image, is_bgr=is_bgr)

    def decode_qr(self, image, detection_result):
        return self.qreader.decode(image=image, detection_result=detection_result)
