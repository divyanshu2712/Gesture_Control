def Mouse_Control(acquire=False):
    #Importing Required Libraries
    import cv2
    from gccs import HandDetector
    import time
    from utility_control import Utility_Control
    from aircanvas import Air_Canvas
    import numpy as np
    import pyautogui
    ###################################################
    # Globals and Constants
    k=0
    wcam=640 # Camera Width
    rf=110 #reduced frame
    hcam=480 # Camera Height
    wscreen,hscreen=pyautogui.size() # Desktop width and height
    pyautogui.FAILSAFE=False # False so that it do not stop if cursor reach corner
    smoothing=2 # To smoothen the movement of cursor 
    # For movement of Mouse
    plocX,plocY=0,0 # prev location
    clocX,clocY=0,0 # current location
    # for drag and drop
    dragging = False 
    drag_start_x, drag_start_y = 0, 0 # 
    # For Fps (Not Neccessary)
    ptime=0
    ###################################################
    # Capturing the frames from web cam
    cap=cv2.VideoCapture(0)
    # Setting width and height respectively
    cap.set(3,wcam)
    cap.set(4,hcam)
    #Declaring HandDetector Object
    detector=HandDetector(maxHands=2)
    #Constantly Capturing frames and doing Operations
    while acquire:
        #Reading Frames
        success,img=cap.read()
        img=cv2.flip(img,1)
        #Getting Hands
        hands,img=detector.findHands(img,flipType=False)
        # If only one hand in frame
        if len(hands)==1:
            hand1=hands[0]
            # For right do this
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
                    #Smoothening
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
                        # If index and middle finger up then left click also there dist is less than 35
                        if length<35:
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

                # If index and middle finger, ring finger up then right click also there dist is less
                if fingers_up[1]==1 and fingers_up[2]==1 and fingers_up[3]==1:
                    x1,y1=lm_list[12][:2]
                    x2,y2=lm_list[16][:2]
                    length,info,img=detector.findDistance((x1,y1),(x2,y2),img,color=(144,238,144),scale=10)
                    if length<27:
                        pyautogui.click(button='right')
                # Scroll Down
                if fingers_up[1]==1 and fingers_up[2]==1 and fingers_up[3]==1 and fingers_up[4]==1:
                    pyautogui.scroll(-200)
            # Scroll up with left hand
            else:
                fingers_up=detector.fingersUp(hand1)
                # Scroll Up
                if fingers_up[1]==1 and fingers_up[2]==1 and fingers_up[3]==1 and fingers_up[4]==1:
                    pyautogui.scroll(200)
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
            elif first==3 and second==3:
                cap.release()
                Air_Canvas(True)
                cap=cv2.VideoCapture(0)
                

        #Frame Rate
        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
        cv2.putText(img,f"FPS: {str(int(fps))}",(30,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        #Displaying
        cv2.imshow("Mouse_Control",img)
        cv2.waitKey(1)
        # ESC Press then quit and release camera
        if k==27:
            cap.release()
            break

    # Closing all windows
    cv2.destroyWindow("Mouse_Control")