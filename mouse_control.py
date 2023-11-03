import cv2
# import mediapipe as mp
from gccs import HandDetector
import time
import numpy as np
import pyautogui
###################################################
wcam=640
rf=110 #reduced frame
hcam=480
wscreen,hscreen=pyautogui.size()
pyautogui.FAILSAFE=False
smoothing=2
plocX,plocY=0,0
clocX,clocY=0,0
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
                clocX=plocX+(x3-plocX)/smoothing
                clocY=plocY+(y3-plocY)/smoothing
                cv2.circle(img,(x1,y1),15,(144, 238, 144),cv2.FILLED)
                pyautogui.moveTo(clocX,clocY)
                plocX,plocY=clocX,clocY
            #Clicking Mode
            x1,y1=lm_list[8][:2]
            x2,y2=lm_list[12][:2]
            length,info,img=detector.findDistance((x1,y1),(x2,y2),img,color=(144,238,144),scale=10,draw=False)
            if fingers_up[1]==1 and fingers_up[2]==1 and length<40 and fingers_up[4]==0:
                # If index and middle finger up then left click also there dist is less
                pyautogui.leftClick()
                x3,y3=lm_list[16][:2]
                length,info,img=detector.findDistance((x2,y2),(x3,y3),img,color=(144,238,144),scale=10,draw=False)
                if fingers_up[3]==1 and length<40:
                    # If index and middle,ring finger up then right click also there dist is less
                    pyautogui.rightClick()
            if fingers_up[1]==1 and fingers_up[2]==1 and fingers_up[3]==1 and fingers_up[4]==1:
                pyautogui.scroll(-200)
        else:
            fingers_up=detector.fingersUp(hand1)
            if fingers_up[1]==1 and fingers_up[2]==1 and fingers_up[3]==1 and fingers_up[4]==1:
                pyautogui.scroll(200)
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