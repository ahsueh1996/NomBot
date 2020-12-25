import cv2
import numpy as np
import pyautogui as ui

def nullMethod(self):
    pass

mode = input('00,01,10, or 11 - [RGB/HSV][camera/image file]: ')
mode = int(mode)    

cv2.namedWindow('Filter Mixer')
if mode < 10:
    cv2.createTrackbar('R ub', 'Filter Mixer', 0, 255, nullMethod)
    cv2.createTrackbar('R lb', 'Filter Mixer', 0, 255, nullMethod)
    cv2.createTrackbar('G ub', 'Filter Mixer', 0, 255, nullMethod)
    cv2.createTrackbar('G lb', 'Filter Mixer', 0, 255, nullMethod)
    cv2.createTrackbar('B ub', 'Filter Mixer', 0, 255, nullMethod)
    cv2.createTrackbar('B lb', 'Filter Mixer', 0, 255, nullMethod)
else: 
    cv2.createTrackbar('H ub', 'Filter Mixer', 0, 179, nullMethod)
    cv2.createTrackbar('H lb', 'Filter Mixer', 0, 179, nullMethod)
    cv2.createTrackbar('S ub', 'Filter Mixer', 0, 255, nullMethod)
    cv2.createTrackbar('S lb', 'Filter Mixer', 0, 255, nullMethod)
    cv2.createTrackbar('V ub', 'Filter Mixer', 0, 255, nullMethod)
    cv2.createTrackbar('V lb', 'Filter Mixer', 0, 255, nullMethod)
    
if (mode+1.0)%2 == 0.0:
    file = input('filename: ')
    if file == 'screenshot':
        raw = np.array(ui.screenshot())[:,:,::-1].copy()
    else:
        raw = cv2.imread(file)
    if mode >=10:
        raw = cv2.cvtColor(raw,cv2.COLOR_BGR2HSV)
else:
    stream = cv2.VideoCapture(0)

while True:
    
    if (mode+1.0)%2 != 0.0: 
        _, raw = stream.read()
        
        if mode >= 10:
            raw = cv2.cvtColor(raw,cv2.COLOR_BGR2HSV)
            
    if mode <10:
        ub1 = cv2.getTrackbarPos('B ub', 'Filter Mixer')
        ub2 = cv2.getTrackbarPos('G ub', 'Filter Mixer')
        ub3 = cv2.getTrackbarPos('R ub', 'Filter Mixer')
        lb1 = cv2.getTrackbarPos('B lb', 'Filter Mixer')
        lb2 = cv2.getTrackbarPos('G lb', 'Filter Mixer')
        lb3 = cv2.getTrackbarPos('R lb', 'Filter Mixer')
    else:
        ub1 = cv2.getTrackbarPos('H ub', 'Filter Mixer')
        ub2 = cv2.getTrackbarPos('S ub', 'Filter Mixer')
        ub3 = cv2.getTrackbarPos('V ub', 'Filter Mixer')
        lb1 = cv2.getTrackbarPos('H lb', 'Filter Mixer')
        lb2 = cv2.getTrackbarPos('S lb', 'Filter Mixer')
        lb3 = cv2.getTrackbarPos('V lb', 'Filter Mixer')
    
    lb = np.array([lb1,lb2,lb3])
    ub = np.array([ub1,ub2,ub3])
    
    mask = cv2.inRange(raw, lb, ub)
    
    result = cv2.bitwise_and(raw,raw,mask=mask)
    
    cv2.imshow("raw",raw)
    cv2.imshow("mask",mask)
    #cv2.imshow("result",result)
    
    
    if cv2.waitKey(1) == 27:
        break

if (mode+1.0)%2 != 0.0: 
    stream.release()
cv2.destroyAllWindows()
