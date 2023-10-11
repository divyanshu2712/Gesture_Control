import cv2
import mediapipe as mp
from gccs import HandDetector
import time
import numpy as np
import pyautogui
###################################################
wcam=640
rf=100 #reduced frame
hcam=480
wscreen,hscreen=pyautogui.size()
pyautogui.FAILSAFE=False
###################################################
cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
detector=HandDetector(detectionCon=0.5,maxHands=2)
ptime=0
while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    #Getting Hands
    hands,img=detector.findHands(img,flipType=False)
    if len(hands)==1:
        hand1=hands[0]
        if hand1['type']=='Right':
            #Getting Landmarks
            lm_list=hand1['lmList']
            fingers_up=detector.fingersUp(hand1)
            # print(fingers_up)
            #Moving Mouse
            if fingers_up[1]==1 and fingers_up[2]==0:
                x1,y1=lm_list[8][:2]
                # print(x1,y1)
                #Frame Rectangle
                cv2.rectangle(img,(rf,rf),(wcam-rf,hcam-rf),(255,0,255),5)
                #Convert coordinates
                x3=np.interp(x1,(rf,wcam-rf),(0,wscreen))
                y3=np.interp(y1,(rf,hcam-rf),(0,hscreen))
                cv2.circle(img,(x1,y1),15,(144, 238, 144),cv2.FILLED)
                pyautogui.moveTo(x3,y3)
            #Clicking Mode
            if fingers_up[1]==1 and fingers_up[2]==1:
                #index finger
                x1,y1=lm_list[8][:2]
                #middle finger
                x2,y2=lm_list[12][:2]
                length,info,img=detector.findDistance((x1,y1),(x2,y2),img,color=(144,238,144),scale=10)
                # cv2.circle(img,(x1,y1),15,(144, 238, 144),cv2.FILLED)
                # cv2.circle(img,(x2,y2),15,(144, 238, 144),cv2.FILLED)
                # print(length)            
                if length<30:
                    cv2.circle(img,(info[-2],info[-1]),15,(144, 238, 144),cv2.FILLED)
                    pyautogui.leftClick()
                    
    
    
    
    
    
    
    
    #Frame Rate
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,f"FPS: {str(int(fps))}",(30,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    #Displaying
    cv2.imshow("Mouse_Control",img)
    k=cv2.waitKey(1)
    if k==27:
        cap.release()
        break

cv2.destroyAllWindows()