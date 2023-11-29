import numpy as np
from gccs import HandDetector
import cv2
import time
import os

########################
########################
drawColor=(0,0,255)
thick=15
erase_thick=100
xp=0
yp=0
Canvas=np.full((720,1280,3),255,np.uint8)# its format is height,width, channel, dtype=unsigned int(0-255)
########################
########################
img_folder="aircanvastop"
mylist=os.listdir(img_folder)
overlaylist=[]
for impath in mylist:
    image=cv2.imread(f"{img_folder}/{impath}")
    overlaylist.append(image)

header=overlaylist[0]

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector=HandDetector(detectionCon=0.85)
while True:
    mask=np.zeros_like(img)
    success,img=cap.read()
    #Placing Header Image
    img=cv2.flip(img,1)
    img[0:127,0:1280]=header
    Canvas[0:127,0:1280]=header
    #Finding hands
    hands,img=detector.findHands(img,flipType=False,draw=False)
    if len(hands)==1:
        hand=hands[0]
        lmlist=hand['lmList']
        # print(lmlist)
        #tip of index and middle finger
        x1,y1=lmlist[8][:2]
        x2,y2=lmlist[12][:2]

        fingers=detector.fingersUp(hand)
        cv2.circle(mask,(x1,y1),100,(255,255,255),-1)
        if fingers[1] and fingers[2]:
            #Checking for click
            xp,yp=x1,y1
            if y1<132:
                if 200<x1<400:
                    header=overlaylist[0]
                    drawColor=(0,0,255)
                elif 450<x1<600:
                    header=overlaylist[1]
                    drawColor=(255,0,0)
                elif 650<x1<800:
                    header=overlaylist[2]
                    drawColor=(0,255,0)
                elif 850<x1<1000:
                    header=overlaylist[3]
                    drawColor=(255,255,255)
                elif 1050<x1<1200:
                    header=overlaylist[4]

        if fingers[1]==1 and fingers[2]==0 and fingers[1:].count(1)==1:
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            if xp==0 and yp==0:
                xp,yp=x1,y1
            #drawing
            #special condition for eraser
            if drawColor==(255,255,255):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,erase_thick)
                cv2.line(Canvas,(xp,yp),(x1,y1),drawColor,erase_thick)
            else:    
                cv2.line(img,(xp,yp),(x1,y1),drawColor,thick)
                cv2.line(Canvas,(xp,yp),(x1,y1),drawColor,thick)
            xp,yp=x1,y1
    cv2.imshow("Image",img)
    Canvas=cv2.addWeighted(Canvas,0.5,mask,0.5,0)
    cv2.imshow("Canvas",Canvas)
    if cv2.waitKey(1)==27:
        break
cv2.destroyAllWindows()