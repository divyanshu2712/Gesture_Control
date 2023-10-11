import cv2
from gccs import HandDetector
import numpy as np
import time
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from screen_brightness_control import set_brightness
import os


#########################################
# GLOBALS & CONSTANTS
w_cam=1920
h_cam=1080
opt=-1
#########################################
cap=cv2.VideoCapture(0) #Getting the camera '0' signify the default camera
detector=HandDetector(detectionCon=0.75,maxHands=2,)
cap.set(3,w_cam)#prop id for width is 3
cap.set(4,h_cam)#prop id for height is 4 
prev_time=0
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

def volume_control(value):
    '''
    Function to control volume
    @param:
    value: It is a distance between finger passed to change volume accordingly 
    '''
    vol_value=np.interp(value,[30,210],[-65.25,0])
    # print(value,vol_value)
    volume.SetMasterVolumeLevel(vol_value, None)

def brightness_control(value):
    '''
    Function to control brightness
    @param:
    value: It is a distance between finger passed to change brightness accordingly 
    '''
    new_brightness=np.interp(value,[30,210],[0,100])
    # print(value,new_brightness)
    set_brightness(new_brightness)

def shutdown(value):
    '''
    Function to shutdown the pc when the distance between fingers become low
    @param:
    value: It is a distance between finger passed to it. 
    '''
    if value<25:
        # os.system("shutdown /s /t 1")
        print("Shutdown")


def gui_rectangle(img,bar=400):
    '''
    It is a function used to show a bar to showcase current level of volume or brightness.
    @param:
    img: It is the image matrix on which the rectangle is to be drawn
    bar: It is value passed of the current distance between fingers
    '''
    bar=np.interp(bar,[30,210],[400,200])
    cv2.rectangle(img,(30,200),(60,400),(0,255,0),3)
    cv2.rectangle(img,(30,int(bar)),(60,400),(0,255,0),cv2.FILLED)
#Continously getting frames 
while True:
    success,img=cap.read()
    #img is the frame captured
    #success is the value which tell whether read is successful or not
    img=cv2.flip(img,1) ## Flipping the image so that there is no confusion
    hands,img=detector.findHands(img,flipType=False) ## Getting hands
    # Perform work if there is only a single hand in frame
    if len(hands)==1:
        hand1=hands[0]
        if hand1['type']=="Left":
            #If hand is left then it counts the fingers
            opt=detector.fingersUp(hand1)[1:].count(1)
            # print(opt)
        if hand1['type']=="Right":
            #If the hand is right then it perform the control work
            lm_list=hand1['lmList']
            if opt==1:
                dist,info,img=detector.findDistance(lm_list[4][:2],lm_list[8][:2],img,scale=8)
                volume_control(dist)
                cv2.putText(img,"Volume Control",(10,100),cv2.FONT_HERSHEY_PLAIN,2,(34,129,253),4)
                gui_rectangle(img,dist)
            if opt==2:
                dist,info,img=detector.findDistance(lm_list[4][:2],lm_list[8][:2],img,scale=8)
                brightness_control(dist)
                cv2.putText(img,"Brightness Control",(10,100),cv2.FONT_HERSHEY_PLAIN,2,(34,129,253),4)
                gui_rectangle(img,dist)
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