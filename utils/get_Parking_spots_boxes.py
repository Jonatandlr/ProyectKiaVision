import cv2
def get_Parking_spots_boxes(connectedComponents):
    """
    Get the parking spots boxes.
    """
    (totalLabels, labels_ids,values, centroids) = connectedComponents
    slots = []
    coef=1
    for i in range(1, totalLabels):
        x1 = int(values[i, cv2.CC_STAT_LEFT]*coef)
        y1 = int(values[i, cv2.CC_STAT_TOP]*coef)
        x2 = int(values[i, cv2.CC_STAT_WIDTH]*coef)+x1
        y2 = int(values[i, cv2.CC_STAT_HEIGHT]*coef)+y1
        slots.append((x1,y1,x2,y2))

    return slots