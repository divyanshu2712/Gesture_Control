import cv2
import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from modules.gccs import HandDetector
from modules.mouse_control import Mouse_Control
from modules.utility_control import Utility_Control
from modules.aircanvas import Air_Canvas
from modules.virtual_keyboard import Virtual_Keyboard
from plyer import notification
import win32gui, win32con
import time
import os
exe_path = sys.executable
exe_dir = os.path.dirname(exe_path)
# os.chdir(exe_dir) #Uncomment when making exe
# Setting Capture to None Initially
cap=None
# Splash Screen
class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a splash screen
        global cap
        splash_pix = QPixmap(os.path.abspath('splash/splash.png'))
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())

        # Add a progress label to the splash screen
        progress_label = QLabel("Loading...", splash)
        font = progress_label.font()
        font.setPointSize(12)
        progress_label.setFont(font)

        # Center the progress label
        layout = QVBoxLayout(splash)
        layout.addWidget(progress_label, 0, Qt.AlignBottom | Qt.AlignHCenter)

        # Show the splash screen
        splash.show()

        # Simulating some initialization work (e.g., loading resources)
        try:
            global cap
            cap=cv2.VideoCapture(0)
        except:
            notification.notify(title="Error", message="Cannot detect the web cam", timeout=5, app_icon=os.path.abspath("icons/warning.ico"))
        cap.set(3,1280)
        cap.set(4,720)

        # Close the splash screen after a delay (e.g., 2 seconds)
        # QTimer.singleShot(1000, splash.close)
        splash.close()





app = QApplication(sys.argv)
sp = SplashScreen()

detector=HandDetector(detectionCon=0.8,minTrackCon=0.75,maxHands=2)
file_path=None
if len(sys.argv)==2:
    file_path=sys.argv[1]
    _,extension=os.path.splitext(file_path)
    if extension!=".air":
            notification.notify(title="Error", message="Cannot open file with this extension", timeout=5, app_icon=os.path.abspath("icons/warning.ico"))
            sys.exit(1)
if file_path!=None:
    Air_Canvas(cap,True,file_path)
    sys.exit(1)    
cv2.namedWindow("GCCS")
hwnd = win32gui.FindWindow(None, "GCCS")
icon_path = os.path.abspath("icons/integrated.ico")
win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))
while True:
    success,img=cap.read()
    acquire=True
    img=cv2.flip(img,1)
    hands,img=detector.findHands(img,flipType=False)
    if len(hands)==2:
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
        # print(left_count,right_count)
        if left_count==4 and right_count==0:
            icon_path = os.path.abspath("icons/integrated.ico")
            notification.notify( title="GCCS", message="Closed GCCS", timeout=2, app_icon=icon_path)
            cap.release()
            break
        elif left_count==4 and right_count==1:
            # icon_path = "icons/integrated.ico"
            icon_path = os.path.abspath("icons/integrated.ico")
            notification.notify( title="GCCS", message="Opening Utility Control", timeout=2, app_icon=icon_path)
            time.sleep(1)
            cv2.destroyWindow("GCCS")
            try:
                Utility_Control(acquire=acquire,cap=cap)            
            except Exception as e:
                notification.notify(title="Error", message=f"Something unexpected happened while opening utility control: {e}", timeout=5, app_icon=os.path.abspath("icons/warning.ico")) 
            time.sleep(1)
            cv2.namedWindow("GCCS")
            hwnd = win32gui.FindWindow(None, "GCCS")
            icon_path = os.path.abspath("icons/integrated.ico")
            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))
            acquire=False
        elif left_count==4 and right_count==2:
            # icon_path = "icons/integrated.ico"
            icon_path = os.path.abspath("icons/integrated.ico")
            notification.notify( title="GCCS", message="Opening Mouse Control", timeout=2, app_icon=icon_path)
            time.sleep(1)
            cv2.destroyWindow("GCCS")
            try:
                Mouse_Control(acquire=acquire,cap=cap)
            except Exception as e:
                notification.notify(title="Error", message=f"Something unexpected happened while opening mouse control: {e}", timeout=5, app_icon=os.path.abspath("icons/warning.ico")) 
            time.sleep(1)
            acquire=False
            cv2.namedWindow("GCCS")
            hwnd = win32gui.FindWindow(None, "GCCS")
            icon_path = os.path.abspath("icons/integrated.ico")
            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))
        elif left_count==4 and right_count==3:
            icon_path = os.path.abspath("icons/integrated.ico")
            notification.notify( title="GCCS", message="Opening Air Canvas", timeout=2, app_icon=icon_path)
            time.sleep(1)
            cv2.destroyWindow("GCCS")
            try:
                Air_Canvas(acquire=acquire,cap=cap)
            except Exception as e:
                notification.notify(title="Error", message=f"Something unexpected happened while opening air canvas : {e}", timeout=5, app_icon=os.path.abspath("icons/warning.ico")) 
            time.sleep(1)
            acquire=False
            cv2.namedWindow("GCCS")
            hwnd = win32gui.FindWindow(None, "GCCS")
            icon_path = os.path.abspath("icons/integrated.ico")
            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))
        elif left_count==2 and right_count==4:
            # icon_path = "icons/integrated.ico"
            icon_path = os.path.abspath("icons/integrated.ico")
            notification.notify( title="GCCS", message="Opening Virtual Keyboard", timeout=2, app_icon=icon_path)
            time.sleep(1)
            cv2.destroyWindow("GCCS")
            try:
                Virtual_Keyboard(acquire=acquire,cap=cap)
            except Exception as e:
                notification.notify(title="Error", message=f"Something unexpected happened while opening virtual keyboard: {e}", timeout=5, app_icon=os.path.abspath("icons/warning.ico")) 
            time.sleep(1)
            acquire=False
            cv2.namedWindow("GCCS")
            hwnd = win32gui.FindWindow(None, "GCCS")
            icon_path = os.path.abspath("icons/integrated.ico")
            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE))
    cv2.waitKey(1)
    cv2.imshow("GCCS",img)
    


cv2.destroyWindow("GCCS")
