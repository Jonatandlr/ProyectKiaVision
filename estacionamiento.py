import cv2
from utils.get_Parking_spots_boxes import get_Parking_spots_boxes

MASK_PATH = "./images/paterns/mask.png"

mask = cv2.imread(MASK_PATH, 0)

cap = cv2.VideoCapture(3)
mask_height, mask_width = mask.shape

connectedComponents = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
spots = get_Parking_spots_boxes(connectedComponents)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_height, frame_width = frame.shape[:2]
    resized_mask = cv2.resize(mask, (frame_width, frame_height), interpolation=cv2.INTER_LINEAR)
    resized_spots = [
        (
            int(spot[0] * (frame_width / mask_width)),
            int(spot[1] * (frame_height / mask_height)),
            int(spot[2] * (frame_width / mask_width)),
            int(spot[3] * (frame_height / mask_height))
        )
        for spot in spots
    ]
    counter=0
    for spot in resized_spots:
        frame = cv2.rectangle(frame, (spot[0], spot[1]), (spot[2], spot[3]), color=(0, 255, 0), thickness=2)
        print(spot)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
