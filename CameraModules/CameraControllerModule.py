import cv2

class CameraController:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.camera = None

    def start_camera(self):
        """Inicia la cámara."""
        self.camera = cv2.VideoCapture(self.camera_id)
        if not self.camera.isOpened():
            print("No se pudo abrir la cámara.")
            return False
        return True

    def capture_frame(self):
        """Captura un solo frame."""
        if self.camera is not None and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                return frame
            else:
                print("Error al capturar el frame.")
        return None

    def show_camera(self):
        """Muestra el video en tiempo real."""
        if self.camera is not None and self.camera.isOpened():
            while True:
                ret, frame = self.camera.read()
                if ret:
                    cv2.imshow('Video en vivo', frame)

                    # Presionar 'q' para salir del video
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    print("Error al leer el frame.")
                    break
        else:
            print("La cámara no está inicializada. Llama a start_camera() primero.")

    def save_frame(self, filename):
        """Captura y guarda un frame como imagen."""
        frame = self.capture_frame()
        if frame is not None:
            cv2.imwrite(filename, frame)
            print(f"Frame guardado como {filename}")
        else:
            print("No se pudo guardar el frame.")

    def release_camera(self):
        """Libera la cámara y cierra las ventanas abiertas."""
        if self.camera is not None:
            self.camera.release()
        cv2.destroyAllWindows()

# # Ejemplo de uso
# if __name__ == "__main__":
#     camera_controller = CameraController()

#     # Iniciar la cámara
#     if camera_controller.start_camera():
#         # Mostrar la cámara en tiempo real
#         camera_controller.show_camera()

#         # Guardar un frame capturado
#         # camera_controller.save_frame("captura.jpg")

#         # Liberar la cámara al terminar
#         camera_controller.release_camera()
