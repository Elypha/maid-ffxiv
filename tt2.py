import time
from ctypes import windll

import cv2
import numpy as np
import win32gui
import win32ui
from PIL import Image


def takescreen(hwnd, width, height, filename):
    # hwnd is window handle
    # width, height are in pixels
    # filename is name of screenshot file

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    # image_array = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4))
    # image_array = cv2.cvtColor(image_array, cv2.COLOR_BGRA2BGR)
    # cv2.imwrite(filename, image_array)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    # if result == 1:
        # PrintWindow Succeeded
    # im.save(filename)
    # time.sleep(1)
    numpy_array = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)




# sample usage
hwnd = win32gui.FindWindow(None, '最终幻想XIV')
# takescreen(hwnd, 3440, 1440, 'screenshot.png')

import time

LOOP=100
t0 = time.time()
for i in range(LOOP):
    takescreen(hwnd, 3440, 1440, 'screenshot.png')

print(f"Time: {(time.time() - t0) / LOOP}")
