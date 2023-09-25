import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import time
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from screen_brightness_control import set_brightness
import os


#########################################
# GLOBALS & CONSTANTS
w_cam=1080 
h_cam=640
opt=-1
#########################################
cap=cv2.VideoCapture(0)
detector=HandDetector(detectionCon=0.75,maxHands=2,)
cap.set(3,w_cam)#prop id for width is 3
cap.set(4,h_cam)#prop id for height is 4 
prev_time=0
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)


def volume_control(value):
    vol_value=np.interp(value,[30,210],[-65.25,0])
    print(value,vol_value)
    volume.SetMasterVolumeLevel(vol_value, None)

def brightness_control(value):
    new_brightness=np.interp(value,[30,210],[0,100])
    print(value,new_brightness)
    set_brightness(new_brightness)

def shutdown(value):
    if value<25:
        os.system("shutdown /s /t 1")

while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    hands,img=detector.findHands(img,flipType=False)
    if len(hands)==1:
        hand1=hands[0]
        if hand1['type']=="Left":
            opt=detector.fingersUp(hand1).count(1)-1
            print(opt)
        if hand1['type']=="Right":
            lm_list=hand1['lmList']
            if opt==1:
                dist,info,img=detector.findDistance(lm_list[4][:2],lm_list[8][:2],img,scale=8)
                volume_control(dist)
                cv2.putText(img,"Volume Control",(10,100),cv2.FONT_HERSHEY_PLAIN,2,(34,129,253),4)
            if opt==2:
                dist,info,img=detector.findDistance(lm_list[4][:2],lm_list[8][:2],img,scale=8)
                brightness_control(dist)
                cv2.putText(img,"Brightness Control",(10,100),cv2.FONT_HERSHEY_PLAIN,2,(34,129,253),4)
            if opt==3:
                dist,info,img=detector.findDistance(lm_list[4][:2],lm_list[8][:2],img,scale=8)
                shutdown(dist)
                cv2.putText(img,"Power Control",(10,100),cv2.FONT_HERSHEY_PLAIN,2,(34,129,253),4)
  



    #Frame Rate
    c_time=time.time()
    fps=1/(c_time-prev_time)
    prev_time=c_time
    cv2.putText(img,f"FPS: {str(int(fps))}",(10,60),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
    #Display
    cv2.imshow("Vaayu",img)
    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()