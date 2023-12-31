def Utility_Control(cap,acquire=False):

    #Importing Necessary Library
    import cv2
    import numpy as np
    import time
    from modules.gccs import HandDetector
    from modules.mouse_control import Mouse_Control
    from modules.aircanvas import Air_Canvas
    from modules.virtual_keyboard import Virtual_Keyboard
    from comtypes import CLSCTX_ALL
    import win32gui,win32con
    from plyer import notification
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from screen_brightness_control import set_brightness
    import os
    #########################################
    # GLOBALS & CONSTANTS
    w_cam=1280
    h_cam=720
    opt=-1
    k=0
    #########################################
    # cap=cv2.VideoCapture(0) #Getting the camera '0' signify the default camera
    detector=HandDetector(detectionCon=0.8,minTrackCon=0.75,maxHands=2)# Declaring HandDetector Object
    cap.set(3,w_cam)#prop id for width is 3
    cap.set(4,h_cam)#prop id for height is 4 
    #For FPS
    prev_time=0
    #Audio Control
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
        if value<30:
            os.system("shutdown /s /t 1")
            # print("Shutdown")


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
    

    cv2.namedWindow("Utility Control")
    hwnd = win32gui.FindWindow(None, "Utility Control")
    icon_path = os.path.abspath("icons/maintenance.ico")
    win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))
    
    #Continously getting frames 
    while acquire:
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
                # If One the Go for Volume Control
                if opt==1:
                    dist,info,img=detector.findDistance(lm_list[4][:2],lm_list[8][:2],img,scale=8)
                    volume_control(dist)
                    cv2.putText(img,"Volume Control",(10,100),cv2.FONT_HERSHEY_PLAIN,2,(34,129,253),4)
                    gui_rectangle(img,dist)
                # 2 Means Brightness Control
                if opt==2:
                    #Finding Distance between index and thumb
                    dist,info,img=detector.findDistance(lm_list[4][:2],lm_list[8][:2],img,scale=8)
                    brightness_control(dist)
                    cv2.putText(img,"Brightness Control",(10,100),cv2.FONT_HERSHEY_PLAIN,2,(34,129,253),4)
                    gui_rectangle(img,dist)
                # 3 Signifies shutdown
                if opt==3:
                    dist,info,img=detector.findDistance(lm_list[4][:2],lm_list[8][:2],img,scale=8)
                    shutdown(dist)
                    cv2.putText(img,"Power Control",(10,100),cv2.FONT_HERSHEY_PLAIN,2,(34,129,253),4)
        
        elif len(hands)==2:
                first_hand=hands[0]
                second_hand=hands[1]
                left_count=0
                right_count=0
                if first_hand['type']=="Left":
                    left_count=detector.fingersUp(first_hand)[1:].count(1)
                    right_count=detector.fingersUp(second_hand)[1:].count(1)
                elif second_hand['type']=="Left":
                    left_count=detector.fingersUp(second_hand)[1:].count(1)
                    right_count=detector.fingersUp(first_hand)[1:].count(1)
                # left_count=detector.fingersUp(first_hand)[1:].count(1)
                # second=detector.fingersUp(second_hand)[1:].count(1)
                # print(left_count,right_count)
                if  left_count==4 and right_count==0:
                    icon_path = os.path.abspath("icons/maintenance.ico")
                    notification.notify( title="Utility Control", message="Closed Utility Control", timeout=2, app_icon=icon_path)
                    k=27
                elif left_count==4 and right_count==2:
                    # cap.release()
                    # icon_path = "icons\maintenance.ico"
                    icon_path = os.path.abspath("icons/maintenance.ico")
                    notification.notify( title="Utility Control", message="Opening Mouse Control", timeout=2, app_icon=icon_path)
                    time.sleep(1)
                    cv2.destroyWindow("Utility Control")
                    try:
                        Mouse_Control(cap,acquire=True)
                    except Exception as e:
                        notification.notify(title="Error", message=f"Something unexpected happened while opening mouse control: {e}", timeout=5, app_icon=os.path.abspath("icons/warning.ico")) 
                    time.sleep(1)
                    cv2.namedWindow("Utility Control")
                    hwnd = win32gui.FindWindow(None, "Utility Control")
                    icon_path = os.path.abspath("icons/maintenance.ico")
                    win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))

                    # cap=cv2.VideoCapture(0)
                elif left_count==4 and right_count==3:
                    # cap.release()
                    # icon_path = "icons\maintenance.ico"
                    icon_path = os.path.abspath("icons/maintenance.ico")
                    notification.notify( title="Utility Control", message="Opening Air Canvas", timeout=2, app_icon=icon_path)
                    time.sleep(1)
                    cv2.destroyWindow("Utility Control")
                    try:
                        Air_Canvas(cap,True)
                    except Exception as e:
                        notification.notify(title="Error", message=f"Something unexpected happened while opening air canvas: {e}", timeout=5, app_icon=os.path.abspath("icons/warning.ico")) 
                    time.sleep(1)
                    cv2.namedWindow("Utility Control")
                    hwnd = win32gui.FindWindow(None, "Utility Control")
                    icon_path = os.path.abspath("icons/maintenance.ico")
                    win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))

                
                elif left_count==2 and right_count==4:
                    # cap.release()
                    # icon_path = "icons\maintenance.ico"
                    icon_path = os.path.abspath("icons/maintenance.ico")
                    notification.notify( title="Utility Control", message="Opening Virtual Keyboard", timeout=2, app_icon=icon_path)
                    time.sleep(1)
                    cv2.destroyWindow("Utility Control")
                    try:
                        Virtual_Keyboard(cap,True)
                    except Exception as e:
                        notification.notify(title="Error", message=f"Something unexpected happened while opening virtual keyboard:  {e}", timeout=5, app_icon=os.path.abspath("icons/warning.ico")) 
                    time.sleep(1)
                    cv2.namedWindow("Utility Control")
                    hwnd = win32gui.FindWindow(None, "Utility Control")
                    icon_path = os.path.abspath("icons/maintenance.ico")
                    win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))

                    

        #Frame Rate
        c_time=time.time()
        fps=1/(c_time-prev_time)
        prev_time=c_time
        cv2.putText(img,f"FPS: {str(int(fps))}",(10,60),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
        #Display
        cv2.imshow("Utility Control",img)
        
        cv2.waitKey(1)
        if k==27:
            acquire=False
            break

    # Releasing the Camera
    # cap.release()
    #Destroying All Windows
    cv2.destroyWindow("Utility Control")

if __name__=="__main__":
    import cv2
    cap=cv2.VideoCapture(0)
    Utility_Control(cap,True)