def Squint_detection(Squint_detection_data):#p0,p11,p12
    middle_w=(Squint_detection_data[1]+Squint_detection_data[2])/2
    if abs(middle_w-Squint_detection_data[0])<40:
        return 1
    else:
        return 2