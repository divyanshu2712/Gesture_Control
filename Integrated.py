import cv2
import numpy as np
from gccs import HandDetector
from mouse_control import Mouse_Control
from utility_control import Utility_Control
from aircanvas import Air_Canvas
# Mouse_Control(acquire=True)
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
detector=HandDetector(detectionCon=0.65,minTrackCon=0.65)
while True:
    success,img=cap.read()
    acquire=True
    img=cv2.flip(img,1)
    hands,img=detector.findHands(img,flipType=False)
    if len(hands)==2:
        first_hand=hands[0]
        second_hand=hands[1]
        first_count=detector.fingersUp(first_hand)[1:].count(1)
        second_count=detector.fingersUp(second_hand)[1:].count(1)
        # print(first_count,second_count)
        if first_count==0 and second_count==0:
            cap.release()
            break
        elif first_count==1 and second_count==1:
            #Utility
            cap.release()
            Utility_Control(acquire=acquire)            
            acquire=False
            cap=cv2.VideoCapture(0)
        elif first_count==2 and second_count==2:
            # Mouse Control
            cap.release()
            Mouse_Control(acquire=acquire)
            acquire=False
            cap=cv2.VideoCapture(0)
        elif first_count==3 and second_count==3:
            # Air Canvas
            cap.release()
            Air_Canvas(acquire=acquire)
            acquire=False
            cap=cv2.VideoCapture(0)
            
    if cv2.waitKey(1)==27:
        break
    cv2.imshow("GCCS",img)
cap.release()
cv2.destroyWindow("GCCS")
