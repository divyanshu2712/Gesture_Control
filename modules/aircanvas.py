def Air_Canvas(cap,acquire=False,file=None):

    #Importing Required Libraries
    import numpy as np
    import cv2
    import time
    import os
    from PIL import Image
    import shutil
    import img2pdf
    import win32gui,win32con
    from datetime import datetime
    import joblib
    from plyer import notification
    from modules.gccs import HandDetector
    from modules.utility_control import Utility_Control
    from modules.mouse_control import Mouse_Control
    from modules.virtual_keyboard import Virtual_Keyboard
    ########################
    ########################
    #Globals and Constants
    drawColor=(0,0,255) # Drawing Color
    thickness=10 # Thickness
    thick=1 # Option for thickness
    erase_thick=thickness*10 # Eraser Thickness
    # Save button cool down after 10 sec logic
    newpage_interval = 10  
    last_newpage_time = time.time()
    # Prev button cool down after 5 sec logic 
    prev_interval=5 # Prev Button cool down after 5 sec
    last_prev_time = time.time()
    # next button cool down after 5 sec logic
    next_interval=5 # next Button cool down after 5 sec
    last_next_time = time.time()
    # Download button cool down after 10 sec logic
    download_interval=10 # Download Button cool down time
    last_download_time = time.time()

    # Save button cool down after 10 sec logic
    save_interval=10 # next Button cool down after 5 sec
    last_save_time = time.time()
    # auto Time:
    autosave_time=time.time()
    auto_save=180
    # Drawing Logic to store previous x,y
    xp=0
    yp=0
    # Page Numbering
    num=1
    prev=None
    next=None
    curr=1
    k=0

    img_files=[]
    ########################
    ########################
    # Top Overlay
    # print(os.getcwd())
    img_folder=os.path.abspath("aircanvastop")
    mylist=os.listdir(img_folder)
    overlaytop=[]
    overlayright=cv2.imread(os.path.abspath("aircanvasright/1.png"))
    for impath in mylist:
        image=cv2.imread(f"{img_folder}/{impath}")
        overlaytop.append(image)

    header=overlaytop[0]
    #Right Overlay
    right=overlayright
    # Capturing Video Frames
    # cap=cv2.VideoCapture(0)
    #Setting width and height respectively
    cap.set(3,1280)
    cap.set(4,720)
    #Declaring HandDetector Object
    detector=HandDetector(detectionCon=0.85,minTrackCon=0.75,maxHands=2)
    # Removing output directory and creating new for cleaning previous saves of img
    if os.path.exists(os.path.abspath("output")):
        shutil.rmtree(os.path.abspath("output"))
        os.makedirs(os.path.abspath("output"))
    else:
        os.makedirs(os.path.abspath("output"))
    if not os.path.exists(os.path.abspath("notes")):
        os.makedirs(os.path.abspath("notes"))
    
    if not os.path.exists(os.path.abspath("saves")):
        os.makedirs(os.path.abspath("saves"))
    
    def save_images_to_folder(images, folder_path):
        for i, image_array in enumerate(images):
            # Convert NumPy array to PIL Image
            rgb_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_image)
        
            # Save the image to the folder
            image_path = os.path.join(folder_path, f"{i + 1}.png")
            image.save(image_path)

    def read_images_from_folder(folder_path):
        image_list = []

        # Ensure the folder path exists
        if os.path.exists(folder_path):
        # Loop through all files in the folder
            for filename in os.listdir(folder_path):
                # Check if the file is an image (you can customize this check based on file extensions)
                if filename.endswith(('.jpg', '.jpeg', '.png')):
                    # Construct the full file path
                    file_path = os.path.join(folder_path, filename)

                    # Read the image using OpenCV
                    image = cv2.imread(file_path)

                    # Append the image to the list
                    image_list.append(image)
        else:
            print(f"The folder path {folder_path} does not exist.")

        return image_list

    
    
    if file!=None:
        # print(file)
        saved=joblib.load(file)
        # print(saved_img)
        save_images_to_folder(saved['images'],os.path.abspath("output"))
        
        Canvas=cv2.imread(os.path.abspath(f"output/{saved['current']}.png"))
        curr=saved['current']
        num=saved['num']
        next=saved['next']
        prev=saved['previous']
    else:
        # print("No")
        # Creating White Canvas
        Canvas=np.full((720,1280,3),255,np.uint8)# its format is height,width, channel, dtype=unsigned int(0-255)
        
    
    cv2.namedWindow("Canvas")
    hwnd = win32gui.FindWindow(None, "Canvas")
    icon_path = os.path.abspath("icons/icon.ico")
    win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))
    
    
    
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
                            if time.time() - last_newpage_time >= newpage_interval:
                                last_newpage_time = time.time()
                                cv2.imwrite(os.path.abspath(f"output/{num}.png"), Canvas)
                                if num==1:
                                    prev=1
                                    next=None
                                else:
                                    prev=num
                                    # next=prev+1
                                num=num+1
                                curr=num
                            Canvas=np.full((720,1280,3),255,np.uint8)
                            Canvas[0:127,0:1280]=header
                            Canvas[127:720,1208:1280]=right
                            cv2.circle(Canvas,(1220,50),thickness,(0,117,252),cv2.FILLED)
                            cv2.putText(Canvas,f"Thickness",(1185,95),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)
                    elif x1>1208:
                        if 130<y1<250:
                            #NextPage
                            # print("Next")
                            ll=os.listdir(os.path.abspath("output"))
                            if next!=None and time.time() - last_next_time >= next_interval:
                                last_next_time = time.time()
                                cv2.imwrite(os.path.abspath(f"output/{curr}.png"),Canvas)
                                if curr==num:
                                    curr=num
                                else:
                                    curr=curr+1
                                # print(next)
                                # if next!=num:
                                Canvas=cv2.imread(os.path.abspath(f"output/{next}.png"))
                            
                                if next==num:
                                    prev=next-1
                                    # curr=num
                                else:
                                    prev=next-1
                                    next=next+1
                                    # curr=next-1
                        elif 260<y1<350:
                            #Previous Logic
                            # print("Previous")
                            if prev!=None and time.time() - last_prev_time >= prev_interval:
                                last_prev_time = time.time()
                                cv2.imwrite(os.path.abspath(f"output/{curr}.png"),Canvas)
                                # cv2.imwrite(f"output/{curr}.png",Canvas)
                                if curr==1:
                                    curr=1
                                else:
                                    curr=curr-1
                                # if (prev+1)==num:
                                    # cv2.imwrite(f"output/{num}.png",Canvas)
                                    # curr=num
                                    # num=num+1
                                if prev!=None:
                                    # curr=prev
                                    next=curr+1
                                # print(prev)
                                if os.listdir(os.path.abspath("output"))!=[]:
                                    Canvas=cv2.imread(os.path.abspath(f"output/{prev}.png"))
                                if prev>1:
                                    prev=prev-1
                        elif 358<y1<430:
                            #Download
                            # print("Download")
                            if time.time() - last_download_time >= download_interval:
                                last_download_time = time.time()
                                cv2.imwrite(os.path.abspath(f"output/{curr}.png"),Canvas)
                                # cv2.imwrite(f"output/{curr}.png",Canvas)
                                pdf_dir = os.path.abspath('notes')
                                img_dir = os.path.abspath('output')
                                img_files = [os.path.join(img_dir, f) for f in os.listdir(img_dir)]

                                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                                if img_files!=[]:
                                    with open(os.path.join(pdf_dir, f'{current_time}.pdf'), 'wb') as f:
                                        f.write(img2pdf.convert(img_files))
                                    notification_title = "Download Success"
                                    notification_text = f"File saved at notes/{current_time}"
                                    notification_timeout = 5  # Notification display time in seconds
                                    icon_path = os.path.abspath("icons/icon.ico")
                                    notification.notify(title=notification_title, message=notification_text, timeout=notification_timeout, app_icon=icon_path)
                                    # print("Downloading")
                                savings={}
                                savings['images']=read_images_from_folder(img_dir)
                                savings['current']=curr
                                savings['next']=next
                                savings['previous']=prev
                                savings['num']=num
                                if file==None:
                                    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                                    joblib.dump(savings,os.path.abspath(f"saves/{current_time}.air"))
                                else:
                                    joblib.dump(savings,file)
                        elif 450<y1<510:
                            if time.time()-last_save_time >= save_interval:
                                # print("Saving")
                                last_save_time=time.time()
                                cv2.imwrite(os.path.abspath(f"output/{curr}.png"),Canvas)
                                notification.notify( title="File Saved", message="File Saved Successfully", timeout=3, app_icon=os.path.abspath("icons/icon.ico"))
                # print(f"Curr:{curr}, Prev:{prev},Next:{next},Num:{num}")
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
                cv2.imwrite(os.path.abspath(f"output/{curr}.png"),Canvas)
                icon_path = os.path.abspath("icons/icon.ico")
                notification.notify( title="Air Canvas", message="Closed Air Canvas", timeout=2, app_icon=icon_path)
                img_dir = os.path.abspath('output')
                savings={}
                savings['images']=read_images_from_folder(img_dir)
                savings['current']=curr
                savings['next']=next
                savings['previous']=prev
                savings['num']=num
                if file==None:
                    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                    joblib.dump(savings,os.path.abspath(f"saves/{current_time}.air"))
                else:
                    joblib.dump(savings,file)
                k=27
            elif left_count==4 and right_count==1:
                # cap.release()
                icon_path = os.path.abspath("icons/icon.ico")
                # icon_path = "icons\icon.ico"
                notification.notify( title="Air Canvas", message="Opening Utility Control", timeout=2, app_icon=icon_path)
                time.sleep(1)
                try:
                    Utility_Control(cap,acquire=True)
                except Exception as e:
                    notification.notify(title="Error", message=f"Something unexpected happened while opening utility control: {e}", timeout=5, app_icon=os.path.abspath("icons/warning.ico")) 
                time.sleep(1)
                cv2.namedWindow("Canvas")
                hwnd = win32gui.FindWindow(None, "Canvas")
                icon_path = os.path.abspath("icons/icon.ico")
                win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))
            elif left_count==4 and right_count==2:
                # cap.release()
                # icon_path = "icons\icon.ico"
                icon_path = os.path.abspath("icons/icon.ico")
                notification.notify( title="Air Canvas", message="Opening Mouse Control", timeout=2, app_icon=icon_path)
                time.sleep(1)
                try:
                    Mouse_Control(cap,True)
                except Exception as e:
                    notification.notify(title="Error", message=f"Something unexpected happened while opening mouse control: {e}", timeout=5, app_icon=os.path.abspath("icons/warning.ico")) 
                time.sleep(1)
                cv2.namedWindow("Canvas")
                hwnd = win32gui.FindWindow(None, "Canvas")
                icon_path = os.path.abspath("icons/icon.ico")
                win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))

            elif left_count==2 and right_count==4:

                icon_path = os.path.abspath("icons/icon.ico")
                notification.notify( title="Air Canvas", message="Opening Virtual Keyboard", timeout=2, app_icon=icon_path)
                time.sleep(1)
                try:
                    Virtual_Keyboard(cap,True)
                except Exception as e:
                    notification.notify(title="Error", message=f"Something unexpected happened while opening virtual keyboard: {e}", timeout=5, app_icon=os.path.abspath("icons/warning.ico")) 
                time.sleep(1)
                cv2.namedWindow("Canvas")
                hwnd = win32gui.FindWindow(None, "Canvas")
                icon_path = os.path.abspath("icons/icon.ico")
                win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))

        if time.time()-autosave_time>auto_save:
            autosave_time=time.time()
            cv2.imwrite(os.path.abspath(f"output/{curr}.png"),Canvas)
        # Displaying Canvas Copy
        cv2.imshow("Canvas",Canvas_Copy)
        
        cv2.waitKey(1)
        if k==27:
            acquire=False
            break

    cv2.destroyWindow("Canvas")

if __name__=="__main__":
    import cv2
    import sys
    import os
    cap=cv2.VideoCapture(0)
    if len(sys.argv)==2:
        file_path=sys.argv[1]
        # print(file_path)
        Air_Canvas(cap,True,file_path)
    else:
        Air_Canvas(cap,True)