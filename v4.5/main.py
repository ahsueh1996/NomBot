import pyautogui as emu
import datetime as datetime
import time
import threading
import sys
import numpy as np

from cat import Cat
from bomb import Bomb
from fish import Fish
from button import Button
from memory import Memory
from vision import *
from _datetime import date


''' define these'''
curStage = ((508,103),(858,725))
matches = 1000
fish_freq = 5
gg_freq = 200
trial_name = 'data'
''''''

w = lambda abcd: abcd[1][0]-abcd[0][0]
h = lambda abcd: abcd[1][1]-abcd[0][1]
c = lambda abcd: (int(w(abcd)/2+abcd[0][0]),int(h(abcd)/2+abcd[0][1]))

refStage = ((508,103),(858,725))   # top left, bottom right of the reference playing area on my fujitsu lifebook

scale = (w(curStage)/w(refStage),h(curStage)/h(refStage))       # finds the scale factor
refCent = c(refStage)                                           # findes the centers/ centroid of playing area
curCent = c(curStage)

# define the location of play again buttoni
a = (679-refCent[0])*scale[0]+curCent[0]
playagain = [[(a,(684-refCent[1])*scale[1]+curCent[1]),(a,(398-refCent[1])*scale[1]+curCent[1])],
             [(64,128,255),(64,128,255)]]

# initialize cats
leftCat = Cat('left',(608, 495),zone=((802, 309),(534, 555)))
rightCat = Cat('right',(743, 494),zone=((802, 309),(534, 555)))

if matches == None:
    matches = input('Enter number of matches to start: ')
    for count in range(3):    
        print(str(3-count))
        time.sleep(1.5)
    print('start!')

matchRecords = []
init_grav = leftCat.calibrate_grav(h(curStage))
bomb = Bomb(g=init_grav)
bfish = Fish(g=init_grav,color='blue')
gfish = Fish(g=init_grav,color='gold')
button = Button(g=0)

window_name = 'Computer Vision'
cv.namedWindow(window_name)
cv.moveWindow(window_name, 1656, 140)
cv.waitKey(1)

memory = Memory(datetime.datetime.now(),name=trial_name,window_name = window_name)

region = ( min(curStage[0][0],curStage[1][0]), min(curStage[0][1],curStage[1][1]), w(curStage), h(curStage) )
screen = sample()
leftCatZone = ((400,580),(520,660))
rightCatZone = ((400,689),(520,730))

    
for match in range(int(matches)):
    step = 0
    gameOver = False
    logging = []
    
    emu.click(playagain[0][0][0],playagain[0][0][1])
    time.sleep(1)
    emu.click(playagain[0][1][0],playagain[0][1][1])
    time.sleep(1)
        
    '''******************************
    nom bot loop
    ********************************* '''
    state = 1
    while not gameOver:
        acted = 0
        # take two snapshots to analysis
#         st_t = datetime.datetime.now()
        raw = sample()
#         print((datetime.datetime.now()-st_t).total_seconds())
        # identify the fish and bomb cntrs
        left_bomb_mask = filter_bgr(raw[400:520,590:660],bomb)
        if len(np.nonzero(left_bomb_mask)[0])>50:
            leftCat.act(cmd=-1)
            state = -1
            acted = 1
        else:
            leftCat.act(cmd=1)
            state = 1
        
        right_bomb_mask = filter_bgr(raw[400:527,689:730],bomb)
        if len(np.nonzero(right_bomb_mask)[0])>50:
            rightCat.act(cmd=-1)
            state = -1
            acted = 1 
        else:
            rightCat.act(cmd=1)
            state = 1
            
        if acted == 1:
            time.sleep(0.003) 
                   
        if state == -1:
            acted = 0
            left_fish_mask = cv.bitwise_and(filter_hsv(raw[400:520,590:660], bfish),filter_hsv(raw[400:520,590:660], gfish)) 
            right_fish_mask = cv.bitwise_and(filter_hsv(raw[400:527,689:730], bfish),filter_hsv(raw[400:527,689:730], gfish))
            
            if len(np.nonzero(left_fish_mask)[0])>50:
                leftCat.act(cmd=1)
                state = 1
                acted = 1 
                
            if len(np.nonzero(right_fish_mask)[0])>50:
                rightCat.act(cmd=1)
                state = 1
                acted = 1 
                
        if acted == 1:
            time.sleep(0.003) 
            
        if step % gg_freq == 5:
            mask = filter_hsv(raw,button)
            gg_cntrs = define_contours(mask)
            if len(gg_cntrs)>=1:
                gameOver = True
                end = datetime.datetime.now()
                leftCat.no_action(gg=1)
                rightCat.no_action(gg=1)
        step += 1
        
            
    ''' ****************************** '''
    
    print('reporting match #'+str(match)+': ')
    sample('samples/v5reactive'+str(match),savefile=1)
    
    
