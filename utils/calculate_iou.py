def calculate_iou(boxA, boxB):
    # Coordenadas de la intersección
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # Calcula el área de la intersección
    interArea = max(0, xB - xA) * max(0, yB - yA)
    
    # Calcula el área de los dos rectángulos (QR y spot)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    
    # Calcula el área total combinada
    iou = interArea / float(boxAArea + boxBArea - interArea)

    return iou