def Physical_detection(Physical_detection_data):#p0,p11,p12
    if abs(Physical_detection_data[1]-Physical_detection_data[2])<10:
        return 1
    if Physical_detection_data[1]>Physical_detection_data[2]+10:
        return 2
    if Physical_detection_data[1]+10<Physical_detection_data[2]:
        return 3
