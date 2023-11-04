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
dragging = False
drag_start_x, drag_start_y = 0, 0
cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
detector=HandDetector(maxHands=2)
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
            #Moving Mouse
            if fingers_up[1]==1 and fingers_up[2]==0 and fingers_up[3]==0:
                x1,y1=lm_list[8][:2]
                #Frame Rectangle
                cv2.rectangle(img,(rf,rf),(wcam-rf,hcam-rf),(255,0,255),5)
                #Convert coordinates
                x3=np.interp(x1,(rf,wcam-rf),(0,wscreen))
                y3=np.interp(y1,(rf,hcam-rf),(0,hscreen))
                clocX=plocX+(x3-plocX)/smoothing
                clocY=plocY+(y3-plocY)/smoothing
                plocX,plocY=clocX,clocY
                cv2.circle(img,(x1,y1),15,(144, 238, 144),cv2.FILLED)
                pyautogui.moveTo(clocX,clocY)
            #Clicking Mode
            if fingers_up[1]==1 and fingers_up[2]==1 and fingers_up[3]==0:
                    x1,y1=lm_list[8][:2]
                    #Frame Rectangle
                    cv2.rectangle(img,(rf,rf),(wcam-rf,hcam-rf),(255,0,255),5)
                    #Convert coordinates
                    x3=np.interp(x1,(rf,wcam-rf),(0,wscreen))
                    y3=np.interp(y1,(rf,hcam-rf),(0,hscreen))
                    clocX=plocX+(x3-plocX)/smoothing
                    clocY=plocY+(y3-plocY)/smoothing
                    plocX,plocY=clocX,clocY
                    x2,y2=lm_list[12][:2]
                    length,info,img=detector.findDistance((x1,y1),(x2,y2),img,color=(144,238,144),scale=10)
                    if length<35:
                    # If index and middle,ring finger up then right click also there dist is less
                        if fingers_up[0]==1:
                            pyautogui.click(button='left')
                        # If Dragging False then make it true and press left button with thumb open 
                        elif not dragging and fingers_up[0]==0:
                            pyautogui.mouseDown(button='left')
                            dragging = True
                            drag_start_x, drag_start_y = clocX, clocY
                        # If dragging
                        else:
                            # Calculate the movement for dragging
                            dx = clocX - drag_start_x
                            dy = clocY - drag_start_y
                            pyautogui.move(dx, dy)
                            drag_start_x, drag_start_y = clocX, clocY
                    # If Distance greater stop drag and release up button
                    else:
                        dragging = False    
                        pyautogui.mouseUp(button='left')

            if fingers_up[1]==1 and fingers_up[2]==1 and fingers_up[3]==1:
                x1,y1=lm_list[12][:2]
                x2,y2=lm_list[16][:2]
                length,info,img=detector.findDistance((x1,y1),(x2,y2),img,color=(144,238,144),scale=10)
                if length<27:
                # If index and middle finger, ring finger up then right click also there dist is less
                    pyautogui.click(button='right')
            # Scroll Down
            if fingers_up[1]==1 and fingers_up[2]==1 and fingers_up[3]==1 and fingers_up[4]==1:
                pyautogui.scroll(-200)
        else:
            fingers_up=detector.fingersUp(hand1)
            # Scroll Up
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