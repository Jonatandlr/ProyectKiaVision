from CameraModules import CameraController

def main():
    camera_controller = CameraController()
    camera_controller.start_camera()
    camera_controller.show_camera()
    camera_controller.release_camera()




if __name__ == "__main__":
    main()