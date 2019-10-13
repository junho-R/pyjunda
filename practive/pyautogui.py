import pyautogui
import time

pyautogui.moveTo(1170, 201, 1)
pyautogui.doubleClick()

time.sleep(1)
pyautogui.typewrite(['a','b','c','enter'])
