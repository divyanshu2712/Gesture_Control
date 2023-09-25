import cv2
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector
import time

###################################################
wcam=1920
hcam=1080
###################################################
cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
detector=HandDetector(detectionCon=0.75,maxHands=2)
while True:
    _,img=cap.read()
    img=cv2.flip(img,1)
    hands,img=detector.findHands(img,flipType=False)
    cv2.imshow("Mouse_Control",img)
    k=cv2.waitKey(1)
    if k==27:
        cap.release()
        break

cv2.destroyAllWindows()