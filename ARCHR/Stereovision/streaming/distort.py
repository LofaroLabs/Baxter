import numpy as np
import cv2
import time

cap = cv2.VideoCapture(1)

cap.set(3, 320) #width
cap.set(4, 240) #height
cap.set(5, 15)  #frame rate
time.sleep(2)

while(cap.isOpened()):

    ret, frame = cap.read()
    width  = frame.shape[1]
    height = frame.shape[0]
    distCoeff = np.zeros((4,1),np.float64)
    k1 = -1.0e-5;
    k2 = 0.0;
    p1 = 0.0;
    p2 = 0.0;
    distCoeff[0,0] = k1;
    distCoeff[1,0] = k2;
    distCoeff[2,0] = p1;
    distCoeff[3,0] = p2;
    cam = np.eye(3,dtype=np.float32)
    cam[0,2] = width/2.0  # define center x
    cam[1,2] = height/2.0 # define center y
    cam[0,0] = 10.        # define focal length x
    cam[1,1] = 10.        # define focal length y
    dst = cv2.undistort(frame,cam,distCoeff)    
    cv2.imshow('dst',dst)
    cv2.imshow("captured videoL", frame)
    if cv2.waitKey(33) == ord('q'):
    	break

cap.release()
cv2.destroyAllWindows()