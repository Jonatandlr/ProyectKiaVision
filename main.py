from CameraModules import CameraController
from CameraModules import QRREADER
import cv2


def main():
    camera_controller = CameraController()
    qr_reader = QRREADER()
    # Iniciar la cámara
    if camera_controller.start_camera():
        while True:
            # Captura un frame
            frame = camera_controller.capture_frame()
            if frame is not None:
                cv2.imshow('Video en vivo', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("Error al leer el frame.")
                break

        # Liberar la cámara al terminar
        camera_controller.release_camera()




if __name__ == "__main__":
    main()