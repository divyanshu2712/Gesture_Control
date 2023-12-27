from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["comtypes", "img2pdf", "imutils", "joblib", "numpy", "cv2", "PIL", "plyer", "pyautogui", "pycaw", "screen_brightness_control", "mediapipe","plyer.platforms.win.notification","PyQt5"],
    "includes": ["win32gui", "win32con", "sys", "time", "os", "datetime"],
    "include_files": [
        ("icons", "icons"),
        ("aircanvasright", "aircanvasright"),
        ("aircanvastop", "aircanvastop"),
        ("modules", "modules"),
        ("splash", "splash"),
    ],
    "excludes": ["tkinter"],  # Exclude tkinter to avoid conflicts with PyQt5
    "include_msvcr": True,  # Include MSVCR runtime
}

# base = None
base = "Win32GUI"  # Use this for GUI applications

executables = [Executable("Integrated.py", base=base, icon="icons/integrated.ico")]

setup(
    name="GCCS",
    version="1.0",
    description="Gesture Controlled Computer System",
    options={"build_exe": build_exe_options},
    executables=executables,
)
