def Head_forward(Head_forward_data):#p0,p11,p12
    middle_h=(Head_forward_data[1]+Head_forward_data[2])/2
    if abs(Head_forward_data[0]-middle_h)<100:
        return 1
