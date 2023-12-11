import cv2
import numpy as np
from gccs import HandDetector
import pyautogui
import winsound
from time import sleep

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector=HandDetector(detectionCon=0.8)
#Keys

keys=[['`','1','2','3','4','5','6','7','8','9','0','-'],
      ['+',"q",'w','e','r','t','y','u','i','o','p','['],
      [']',"\\",'a','s','d','f','g','h','j','k','l',';'],
      ["'",'z','x','c','v','b','n','m',',','.','/']]

#Drawing All Function
def draw(img,pos,text,size,color=(255,0,255)):
    cv2.rectangle(img,pos,(pos[0]+size[0],pos[1]+size[1]),color,cv2.FILLED)
    cv2.putText(img,text,(pos[0]+20,pos[1]+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
def drawAll(img,buttonList):
    for btn in buttonList:
        draw(img,btn.pos,btn.text,btn.size)
    return img



# Button Class
class Button():
    def __init__(self, pos, text,size=[85,85]):
        self.pos=pos
        self.text=text
        self.size=size



buttonList=[]
for i in range(len(keys)):
    for j,key in enumerate(keys[i]):
        buttonList.append(Button([100*j+50,100*i+50],key))



print(len(pyautogui.KEYBOARD_KEYS))
while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    hands,img=detector.findHands(img,flipType=False)

    #Drawing BUTTONS
    img = drawAll(img,buttonList)
    # Finding Hands
    if len(hands)==1:
        hand=hands[0]
        lmlist=hand['lmList']
        for btn in buttonList:
            x,y=btn.pos
            w,h=btn.size
            idx_x,idx_y=lmlist[8][0],lmlist[8][1]
            if x < idx_x < x+w and y < idx_y < y+h:
                draw(img,btn.pos,btn.text,btn.size,color=(175,0,175))
                length,info,img=detector.findDistance(lmlist[8][:2],lmlist[12][:2],img)
                # print(length)
                if length<55:
                    draw(img,btn.pos,btn.text,btn.size,(0,255,255))
                    pyautogui.press(btn.text)
                    winsound.Beep(500, 100)
                    sleep(0.15)

    cv2.imshow("Keyboard",img)
    if cv2.waitKey(1)==27:
        break
cv2.destroyAllWindows()



