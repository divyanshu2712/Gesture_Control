import numpy as np
from gccs import HandDetector
import cv2
import time
import os
import shutil
import img2pdf
from datetime import datetime
from plyer import notification
########################
########################
drawColor=(0,0,255)
thickness=10
thick=1
erase_thick=thickness*10
save_interval = 10  # Save every 10 seconds
prev_interval=5 # Prev Button Enable after 20 sec
next_interval=5 # Prev Button Enable after 20 sec
download_interval=10
last_save_time = time.time()
last_prev_time = time.time()
last_next_time = time.time()
last_download_time = time.time()
xp=0
yp=0
Canvas=np.full((720,1280,3),255,np.uint8)# its format is height,width, channel, dtype=unsigned int(0-255)
num=1
prev=-1
next=1
########################
########################
img_folder="aircanvastop"
mylist=os.listdir(img_folder)
overlaytop=[]
overlayright=cv2.imread("aircanvasright/1.png")
for impath in mylist:
    image=cv2.imread(f"{img_folder}/{impath}")
    overlaytop.append(image)

header=overlaytop[0]
right=overlayright
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector=HandDetector(detectionCon=0.85)
shutil.rmtree("output")
os.makedirs("output")
while True:
    success,img=cap.read()
    #Placing Header Image
    img=cv2.flip(img,1)
    Canvas[0:127,0:1280]=header
    Canvas[127:720,1208:1280]=right
    #Finding hands
    cv2.circle(Canvas,(1220,50),thickness,(0,117,252),cv2.FILLED)
    cv2.putText(Canvas,f"Thickness",(1185,95),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)
    hands,img=detector.findHands(img,flipType=False,draw=False)
    Canvas_Copy=Canvas.copy()
    if thick<1:
        thickness=2
        erase_thick=5
    else:
        thickness=thick*5
        erase_thick=thickness*10

    if len(hands)==1:
        hand=hands[0]
        if hand['type']=='Left':
            thick=detector.fingersUp(hand)[1:].count(1)
        if hand['type']=="Right":
            lmlist=hand['lmList']
            # print(lmlist)
            #tip of index and middle finger
            x1,y1=lmlist[8][:2]
            x2,y2=lmlist[12][:2]
            fingers=detector.fingersUp(hand)
            if fingers[1] and fingers[2]:
                #Checking for click
                xp,yp=x1,y1
                if y1<132:
                    if 200<x1<400:
                        header=overlaytop[0]
                        drawColor=(0,0,255)
                        right=overlayright
                    elif 450<x1<600:
                        header=overlaytop[1]
                        drawColor=(255,0,0)
                        right=overlayright
                    elif 650<x1<800:
                        header=overlaytop[2]
                        drawColor=(0,255,0)
                        right=overlayright
                    elif 850<x1<1000:
                        header=overlaytop[3]
                        drawColor=(255,255,255)
                        right=overlayright
                    elif 1050<x1<1200:
                        #New Page Logic and Saving Previous
                        if time.time() - last_save_time >= save_interval:
                            last_save_time = time.time()
                            cv2.imwrite(f'output/{num}.png', Canvas)
                            if num==1:
                                prev=1
                                next=1
                            else:
                                prev=num
                                next=prev+1
                            num=num+1
                        Canvas=np.full((720,1280,3),255,np.uint8)
                        Canvas[0:127,0:1280]=header
                        Canvas[127:720,1208:1280]=right
                        cv2.circle(Canvas,(1220,50),thickness,(0,117,252),cv2.FILLED)
                        cv2.putText(Canvas,f"Thickness",(1185,95),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)
                elif x1>1208:
                    if 130<y1<250:
                        #NextPage
                        # print("Next")
                        ll=os.listdir("output")
                        if time.time() - last_next_time >= next_interval:
                            last_next_time = time.time()
                            print(next)
                            if next!=num:
                                Canvas=cv2.imread(f"output/{next}.png")
                            if next==1:
                                prev=-1
                            elif next==num:
                                prev=next-1
                            else:
                                next=next+1
                                prev=prev+1
                    elif 260<y1<350:
                        #Previous Logic
                        # print("Previous")
                        if time.time() - last_prev_time >= prev_interval:
                            last_prev_time = time.time()
                            if (prev+1)==num:
                                cv2.imwrite(f"output/{num}.png",Canvas)
                                num=num+1
                            if prev!=-1:
                                next=prev+1
                            print(prev)
                            if os.listdir("output")!=[]:
                                Canvas=cv2.imread(f"output/{prev}.png")
                            if prev>1:
                                prev=prev-1
                    elif 358<y1<480:
                        #Download
                        # print("Download")
                        if time.time() - last_download_time >= download_interval:
                            last_download_time = time.time()
                            img_dir = 'output'
                            pdf_dir = 'notes'
                            img_files = [os.path.join(img_dir, f) for f in os.listdir(img_dir)]

                            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                            if img_files!=[]:
                                with open(os.path.join(pdf_dir, f'{current_time}.pdf'), 'wb') as f:
                                    f.write(img2pdf.convert(img_files))
                                notification_title = "Download Success"
                                notification_text = f"File saved at notes/{current_time}"
                                notification_timeout = 10  # Notification display time in seconds
                                icon_path = "logo/icon.ico"
                                notification.notify( title=notification_title, message=notification_text, timeout=notification_timeout, app_icon=icon_path)
            if fingers[1]==1 and fingers[2]==0 and fingers[1:].count(1)==1:
                cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
                if xp==0 and yp==0:
                    xp,yp=x1,y1
                #drawing
                #special condition for eraser
                if drawColor==(255,255,255):
                    cv2.line(Canvas,(xp,yp),(x1,y1),drawColor,erase_thick)
                else:    
                    cv2.line(Canvas,(xp,yp),(x1,y1),drawColor,thickness+5)
                xp,yp=x1,y1
            Canvas_Copy=Canvas.copy()
            if drawColor==(255,255,255):
                cv2.circle(Canvas_Copy,(x1,y1),thickness,(15,10,20),cv2.FILLED)
            else:
                cv2.circle(Canvas_Copy,(x1,y1),thickness,(15,10,20),cv2.FILLED)
                    
    cv2.imshow("Canvas",Canvas_Copy)
    if cv2.waitKey(1)==27:
        break
cv2.destroyAllWindows()
cap.release()