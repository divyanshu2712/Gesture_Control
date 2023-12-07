def Air_Canvas(acquire=False):

    #Importing Required Libraries
    import numpy as np
    from gccs import HandDetector
    import cv2
    import time
    import os
    import shutil
    import img2pdf
    from datetime import datetime
    from plyer import notification
    from utility_control import Utility_Control
    from mouse_control import Mouse_Control
    ########################
    ########################
    #Globals and Constants
    drawColor=(0,0,255) # Drawing Color
    thickness=10 # Thickness
    thick=1 # Option for thickness
    erase_thick=thickness*10 # Eraser Thickness
    # Save button cool down after 10 sec logic
    save_interval = 10  
    last_save_time = time.time()
    # Prev button cool down after 5 sec logic 
    prev_interval=5 # Prev Button cool down after 5 sec
    last_prev_time = time.time()
    # next button cool down after 5 sec logic
    next_interval=5 # next Button cool down after 5 sec
    last_next_time = time.time()
    # Download button cool down after 10 sec logic
    download_interval=10 # Download Button cool down time
    last_download_time = time.time()
    # Drawing Logic to store previous x,y
    xp=0
    yp=0
    # Creating White Canvas
    Canvas=np.full((720,1280,3),255,np.uint8)# its format is height,width, channel, dtype=unsigned int(0-255)
    # Page Numbering
    num=1
    prev=-1
    next=1
    k=0
    ########################
    ########################
    # Top Overlay
    img_folder="aircanvastop"
    mylist=os.listdir(img_folder)
    overlaytop=[]
    overlayright=cv2.imread("aircanvasright/1.png")
    for impath in mylist:
        image=cv2.imread(f"{img_folder}/{impath}")
        overlaytop.append(image)

    header=overlaytop[0]
    #Right Overlay
    right=overlayright
    # Capturing Video Frames
    cap=cv2.VideoCapture(0)
    #Setting width and height respectively
    cap.set(3,1280)
    cap.set(4,720)
    #Declaring HandDetector Object
    detector=HandDetector(detectionCon=0.85)
    # Removing output directory and creating new for cleaning previous saves of img
    shutil.rmtree("output")
    os.makedirs("output")
    # Constantly Capturing Frames
    while acquire:
        #Reading Frames
        success,img=cap.read()
        #Fliping Images
        img=cv2.flip(img,1)
        #Placing Header Image, Right Section and Thickness depiction
        Canvas[0:127,0:1280]=header
        Canvas[127:720,1208:1280]=right
        cv2.circle(Canvas,(1220,50),thickness,(0,117,252),cv2.FILLED)
        cv2.putText(Canvas,f"Thickness",(1185,95),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)
        #Finding hands
        hands,img=detector.findHands(img,flipType=False,draw=False)
        #For having a pointer of the pen
        Canvas_Copy=Canvas.copy()
        if thick<1:
            thickness=2
            erase_thick=5
        else:
            thickness=thick*5
            erase_thick=thickness*10
        # If single hand then work
        if len(hands)==1:
            hand=hands[0]
            # Select thickness with left hand
            if hand['type']=='Left':
                thick=detector.fingersUp(hand)[1:].count(1)
            # Draw using right hand
            if hand['type']=="Right":
                lmlist=hand['lmList']
                # print(lmlist)
                #tip of index and middle finger
                x1,y1=lmlist[8][:2]
                x2,y2=lmlist[12][:2]
                # Count of fingers open
                fingers=detector.fingersUp(hand)
                # If index and middle up 
                if fingers[1] and fingers[2]:
                    #Checking for click
                    xp,yp=x1,y1 # Moving logic
                    # Changing Colors, selecting erasers and creating New Page
                    if y1<132:
                        if 200<x1<400:
                            # Red Color
                            header=overlaytop[0]
                            drawColor=(0,0,255)
                            right=overlayright
                        elif 450<x1<600:
                            # Blue Color
                            header=overlaytop[1]
                            drawColor=(255,0,0)
                            right=overlayright
                        elif 650<x1<800:
                            # Green Color
                            header=overlaytop[2]
                            drawColor=(0,255,0)
                            right=overlayright
                        elif 850<x1<1000:
                            # Eraser (White Color)
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
                # Drawing with single finger
                if fingers[1]==1 and fingers[2]==0 and fingers[1:].count(1)==1:
                    cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
                    if xp==0 and yp==0:
                        xp,yp=x1,y1
                    #drawing
                    #special condition for eraser it has more thickness
                    if drawColor==(255,255,255):
                        cv2.line(Canvas,(xp,yp),(x1,y1),drawColor,erase_thick)
                    else:    
                        cv2.line(Canvas,(xp,yp),(x1,y1),drawColor,thickness+5)
                    xp,yp=x1,y1
                # Copying Canvas and drawing the current pen or pointer position with black circle
                Canvas_Copy=Canvas.copy()
                if drawColor==(255,255,255):
                    cv2.circle(Canvas_Copy,(x1,y1),thickness,(15,10,20),cv2.FILLED)
                else:
                    cv2.circle(Canvas_Copy,(x1,y1),thickness,(15,10,20),cv2.FILLED)
        
        elif len(hands)==2:
                first_hand=hands[0]
                second_hand=hands[1]
                first=detector.fingersUp(first_hand)[1:].count(1)
                second=detector.fingersUp(second_hand)[1:].count(1)
                if  first==0 and second==0:
                    k=27
                elif first==1 and second==1:
                    cap.release()
                    Utility_Control(True)
                    cap=cv2.VideoCapture(0)
                elif first==2 and second==2:
                    cap.release()
                    Mouse_Control(True)
                    cap=cv2.VideoCapture(0)
                    
        # Displaying Canvas Copy
        cv2.imshow("Canvas",Canvas_Copy)
        # if cv2.waitKey(1)==27:
            # break
        cv2.waitKey(1)
        if k==27:
            cap.release()
            acquire=False
            break

    cv2.destroyWindow("Canvas")