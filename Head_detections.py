def Head_detection(Head_detection_data):#p0，p2，p5
    if Head_detection_data[1]>Head_detection_data[2]+6:
        return 1
    if Head_detection_data[1]+6<Head_detection_data[2]:
        return 2
    if abs(Head_detection_data[1]-Head_detection_data[2])<6:
        return 3
