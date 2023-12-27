def Virtual_Keyboard(cap,acquire=False):
    import cv2
    import numpy as np
    import pyautogui
    import winsound
    import time
    import imutils
    from modules.gccs import HandDetector
    from modules.mouse_control import Mouse_Control
    from modules.aircanvas import Air_Canvas
    from modules.utility_control import Utility_Control
    from plyer import notification
    import win32gui,win32con
    import os


    # cap=cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)

    detector=HandDetector(detectionCon=0.8,minTrackCon=0.75,maxHands=2)
    #Keys
    caps_on=False
    other=False
    alt=False
    ctrl=False
    k=0
    shift=False
    bgr=np.full((720,1280,3),255,np.uint8)
    keys=[['1','2','3','4','5','6','7','8','9','0','-','+'],
        ["q",'w','e','r','t','y','u','i','o','p',"Bksp"],
        ["Caps",'a','s','d','f','g','h','j','k','l',"Enter"],
        ['z','x','c','v','b','n','m',"Alt","Ctrl","Space"],
        ["Other Important Keys"]]

    keys_2=[['!','@','#','$','%','^','&','*','(',')','_','='],
        ["Tab",'{','}','[',']','\\','|','/',':',"~","Bksp"],
        [";",'"',"'",'<','>',',','.','?','`',"Esc","Enter"],
        ['->','<-','up','down',"Space","Shift"],
        ["Other Important Keys"]]

    #Drawing All Function
    def draw(img,pos,text,size,font,color=(255,0,255)):
        if text in ["Caps","Alt",'Ctrl',"up","Esc","Tab"]:
            cv2.rectangle(img,pos,(pos[0]+size[0],pos[1]+size[1]),color,cv2.FILLED)
            cv2.putText(img,text,(pos[0]+5,pos[1]+55),cv2.FONT_HERSHEY_PLAIN,font+1,(255,255,255),font+1)
        elif text=="Space":
            cv2.rectangle(img,pos,(pos[0]+size[0],pos[1]+size[1]),color,cv2.FILLED)
            cv2.putText(img,text,(pos[0]+40,pos[1]+65),cv2.FONT_HERSHEY_PLAIN,font,(255,255,255),font)
        elif text in ["->","<-","down"]:
            cv2.rectangle(img,pos,(pos[0]+size[0],pos[1]+size[1]),color,cv2.FILLED)
            cv2.putText(img,text,(pos[0]+2,pos[1]+50),cv2.FONT_HERSHEY_PLAIN,font,(255,255,255),font)
        else:
            cv2.rectangle(img,pos,(pos[0]+size[0],pos[1]+size[1]),color,cv2.FILLED)
            cv2.putText(img,text,(pos[0]+20,pos[1]+65),cv2.FONT_HERSHEY_PLAIN,font,(255,255,255),font)
    def drawAll(img,buttonList,color=(255,0,255)):
        for btn in buttonList:
            draw(img,btn.pos,btn.text,btn.size,btn.font,color)
        return img



    # Button Class
    class Button():
        def __init__(self, pos, text,size=[85,85],font=4):
            self.pos=pos
            self.text=text
            self.size=size
            self.font=font



    buttonList=[]
    buttonList2=[]
    for i in range(len(keys)):
        for j,key in enumerate(keys[i]):
            if key=="Bksp":
                buttonList.append(Button([100*j+50,100*i+50],key,[185,85]))
            elif key=="Caps" or key=="Alt" or key=="Ctrl":
                buttonList.append(Button([100*j+50,100*i+50],key,[85,85],1))
            elif key=="Enter":
                buttonList.append(Button([100*j+50,100*i+50],key,[185,85],3))
            elif key=="Space":
                buttonList.append(Button([100*j+50,100*i+50],key,[285,85]))
            elif key=="Other Important Keys":
                buttonList.append(Button([100*j+50,100*i+50],key,[835,85]))
            else:
                buttonList.append(Button([100*j+50,100*i+50],key))

    for i in range(len(keys_2)):
        for j,key in enumerate(keys_2[i]):
            if key=="Bksp":
                buttonList2.append(Button([100*j+50,100*i+50],key,[185,85]))
            elif key =="Tab" or key=="Esc" or key=="Del" or key=="up":
                buttonList2.append(Button([100*j+50,100*i+50],key,[85,85],1))
            elif key=="Enter":
                buttonList2.append(Button([100*j+50,100*i+50],key,[185,85],3))
            elif key=="Space":
                buttonList2.append(Button([100*j+50,100*i+50],key,[285,85]))
            elif key=="Shift":
                buttonList2.append(Button([700+50,100*i+50],key,[185,85]))
            elif key=="->" or key=="<-" or key=="down":
                buttonList2.append(Button([100*j+50,100*i+50],key,[85,85],2))
            elif key=="Other Important Keys":
                buttonList2.append(Button([100*j+50,100*i+50],key,[835,85]))
            else:
                buttonList2.append(Button([100*j+50,100*i+50],key))


    cv2.namedWindow("Keyboard")
    hwnd = win32gui.FindWindow(None, "Keyboard")
    icon_path = os.path.abspath("icons/keyboard.ico")
    win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))

    while acquire:
        success,img=cap.read()
        img=imutils.resize(img,width=1280,height=720)
        img=cv2.flip(img,1)
        hands,img=detector.findHands(img,flipType=False)
        bgr=np.full((720,1280,3),255,np.uint8)
        if caps_on:
            for btn in buttonList:
                if btn.text.isalpha() and len(btn.text)==1:
                    btn.text=btn.text.capitalize()
        else:
            for btn in buttonList:
                if btn.text.isalpha() and len(btn.text)==1:
                    btn.text=btn.text.lower()
        #Drawing BUTTONS
        if other:
            bgr=drawAll(bgr,buttonList2,(0,255,0))
        else:
            bgr=drawAll(bgr,buttonList)
        bgr_copy=bgr.copy()
        # Finding Hands
        if len(hands)==1:
            hand=hands[0]
            if detector.fingersUp(hand)[1:].count(1)==4:
                alt=False
                ctrl=False
                shift=False
            lmlist=hand['lmList']
            if detector.fingersUp(hand)[1:].count(1)!=0:
                if other:
                    for btn in buttonList2:
                        x,y=btn.pos
                        w,h=btn.size
                        idx_x,idx_y=lmlist[8][0],lmlist[8][1]
                        if x < idx_x < x+w and y < idx_y < y+h:
                            draw(bgr,btn.pos,btn.text,btn.size,btn.font,color=(0,175,0))
                            length,info,img=detector.findDistance(lmlist[8][:2],lmlist[12][:2],img)
                            length=length.__round__(2)
                            # print(length)
                            if length<60:
                                draw(bgr,btn.pos,btn.text,btn.size,btn.font,(0,0,0))
                                if btn.text=="Bksp":
                                    pyautogui.press("backspace")
                                elif btn.text=="Caps":
                                    if caps_on:
                                        caps_on=False
                                    else:
                                        caps_on=True
                                    pyautogui.press("capslock")
                                elif btn.text=="Alt":
                                    alt=True
                                elif btn.text=="Ctrl":
                                    ctrl=True
                                elif btn.text=="Shift":
                                    shift=True
                                elif btn.text=="Other Important Keys":
                                    if other:
                                        other=False
                                    else:
                                        other=True
                                elif btn.text=="->":
                                    pyautogui.press("right")
                                elif btn.text=="<-":
                                    pyautogui.press("left")
                                else:
                                    if alt:
                                        pyautogui.hotkey('alt',btn.text)
                                    elif ctrl:
                                        pyautogui.hotkey('ctrl',btn.text)
                                    elif shift:
                                        pyautogui.hotkey('shift',btn.text)
                                    else:
                                        pyautogui.press(btn.text.lower())
                                winsound.Beep(1200, 100)
                                time.sleep(0.20)
                    
                else:
                    for btn in buttonList:
                        x,y=btn.pos
                        w,h=btn.size
                        idx_x,idx_y=lmlist[8][0],lmlist[8][1]
                        if x < idx_x < x+w and y < idx_y < y+h:
                            draw(bgr,btn.pos,btn.text,btn.size,btn.font,color=(175,0,175))
                            length,info,img=detector.findDistance(lmlist[8][:2],lmlist[12][:2],img)
                            # print(length)
                            length=length.__round__(2)
                            if length<60:
                                draw(bgr,btn.pos,btn.text,btn.size,btn.font,(0,0,0))
                                if btn.text=="Bksp":
                                    pyautogui.press("backspace")
                                elif btn.text=="Caps":
                                    if caps_on:
                                        caps_on=False
                                    else:
                                        caps_on=True
                                    pyautogui.press("capslock")
                                elif btn.text=="Alt":
                                    alt=True
                                elif btn.text=="Ctrl":
                                    ctrl=True
                                elif btn.text=="Shift":
                                    shift=True
                                elif btn.text=="Other Important Keys":
                                    if other:
                                        other=False
                                    else:
                                        other=True
                                else:
                                    if alt:
                                        pyautogui.hotkey('alt',btn.text)
                                    elif ctrl:
                                        pyautogui.hotkey('ctrl',btn.text)
                                    elif shift:
                                        pyautogui.hotkey('shift',btn.text)
                                    else:
                                        pyautogui.press(btn.text.  lower())
                                winsound.Beep(1200, 100)
                                time.sleep(0.20)
            bgr_copy=bgr.copy()
            cv2.circle(bgr_copy,lmlist[8][:2],5,(0,0,0),cv2.FILLED)
        
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
            if  left_count==4 and right_count==0:
                icon_path = os.path.abspath("icons/keyboard.ico")
                notification.notify( title="Virtual Keyboard", message="Closed Virtual Keyboard", timeout=2, app_icon=icon_path)
                k=27
            elif left_count==4 and right_count==1:
                icon_path = os.path.abspath("icons/keyboard.ico")
                notification.notify( title="Virtual Keyboard", message="Opening Utility Control", timeout=2, app_icon=icon_path)
                time.sleep(1)
                cv2.destroyWindow("Keyboard")
                try:
                    Utility_Control(cap,acquire=True)
                except Exception as e:
                    notification.notify(title="Error", message=f"Something unexpected happened while opening utility control: {e}", timeout=5, app_icon=os.path.abspath("icons/warning.ico") )
                time.sleep(1)
                cv2.namedWindow("Keyboard")
                hwnd = win32gui.FindWindow(None, "Keyboard")
                icon_path = os.path.abspath("icons/keyboard.ico")
                win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))
            elif left_count==4 and right_count==2:
                icon_path = os.path.abspath("icons\keyboard.ico")
                notification.notify( title="Virtual Keyboard", message="Opening Mouse Control", timeout=2, app_icon=icon_path)
                time.sleep(1)
                cv2.destroyWindow("Keyboard")
                try:
                    Mouse_Control(cap,True)
                except Exception as e:
                    notification.notify(title="Error", message=f"Something unexpected happened while opening mouse control: {e}", timeout=5, app_icon=os.path.abspath("icons/warning.ico") )
                time.sleep(1)
                cv2.namedWindow("Keyboard")
                hwnd = win32gui.FindWindow(None, "Keyboard")
                icon_path = os.path.abspath("icons/keyboard.ico")
                win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))
            
            elif left_count==4 and right_count==3:
                icon_path = os.path.abspath("icons/keyboard.ico")
                notification.notify( title="Virtual Keyboard", message="Opening Air Canvas", timeout=2, app_icon=icon_path)
                time.sleep(1)
                cv2.destroyWindow("Keyboard")
                try:
                    Air_Canvas(cap,True)
                except Exception as e:
                    notification.notify(title="Error", message=f"Something unexpected happened while opening air canvas: {e}", timeout=5, app_icon=os.path.abspath("icons/warning.ico") )
                time.sleep(1)
                cv2.namedWindow("Keyboard")
                hwnd = win32gui.FindWindow(None, "Keyboard")
                icon_path = os.path.abspath("icons/keyboard.ico")
                win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))

        cv2.imshow("Keyboard",bgr_copy)
        cv2.resizeWindow("Keyboard", 1280, 600) 
        cv2.setWindowProperty("Keyboard", cv2.WND_PROP_TOPMOST, 1)
        
        cv2.waitKey(1)

        if k==27:
            acquire=False
            break
    cv2.destroyWindow("Keyboard")



if __name__=="__main__":
    import cv2
    cap=cv2.VideoCapture(0)
    Virtual_Keyboard(cap,True)