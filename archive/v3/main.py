import pyautogui as emu
import datetime as datetime
import time
import threading
import sys

from cat import Cat
from bomb import Bomb
from fish import Fish
from button import Button
from vision import *
from _datetime import date


''' define these'''
curStage = ((508,103),(858,725))
matches = 3
fish_freq = 5
gg_freq = 50
''''''

w = lambda abcd: abcd[1][0]-abcd[0][0]
h = lambda abcd: abcd[1][1]-abcd[0][1]
c = lambda abcd: (int(w(abcd)/2+abcd[0][0]),int(h(abcd)/2+abcd[0][1]))

refStage = ((508,103),(858,725))   # top left, bottom right of the reference playing area on my fujitsu lifebook

scale = (w(curStage)/w(refStage),h(curStage)/h(refStage))       # finds the scale factor
refCent = c(refStage)                                           # findes the centers/ centroid of playing area
curCent = c(curStage)

# define the location of play again button
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
bomb = Bomb()
fish = Fish()
button = Button()

cv.namedWindow('Computer Vision')
cv.moveWindow('Computer Vision', 1656, 140)
cv.waitKey(1)
    
for match in range(int(matches)):
    step = 0
    gameOver = False
    logging = []
    
    emu.click(playagain[0][0][0],playagain[0][0][1])
    time.sleep(1)
    emu.click(playagain[0][1][0],playagain[0][1][1])
    time.sleep(1)

    start = datetime.datetime.now()
    leftCat.act(cmd = 1) 
    rightCat.act(cmd = 1)
    leftCat.gg = 0
    rightCat.gg = 0
    
    t_lock = threading.Lock()
    t_leftCat = threading.Thread(target=leftCat._timed_actor, args=(t_lock,))
    t_rightCat = threading.Thread(target=rightCat._timed_actor, args=(t_lock,))
        
    '''******************************
    nom bot loop
    ********************************* '''
#     t_leftCat.start()
#     t_rightCat.start()


    while not gameOver:
        bomb_cents = []
        fish_cents = []
        bombs = []
        fishs = []
        times = []
        
        print('step starts:')
        print(datetime.datetime.now())
        # take two snapshots to analysis
        for i in range(2):
            print('sample\t'+str(datetime.datetime.now()))
            t_lock.acquire()  
            raw = sample()
            # we will call the time immediately after the last sample t=0
            times.append(datetime.datetime.now())
            t_lock.release()
            print('sample\t'+str(datetime.datetime.now()))
            # identify the fish and bomb centroids
            print('bcent\t'+str(datetime.datetime.now()))
            bomb_cntrs = isolate_contours( define_contours( filter_bgr(raw,bomb) ), bomb )        
            bomb_cents.append(eval_centroids( bomb_cntrs ))
            print('bfcent\t'+str(datetime.datetime.now()))
            fish_cntrs = isolate_contours( define_contours( filter_hsv(raw,fish) ), fish )        
            fish_cents.append(eval_centroids( fish_cntrs ))
            print('fcent\t'+str(datetime.datetime.now()))
            
                  
        # make the list of bombs and fish
        print('make\t'+str(datetime.datetime.now()))
        bombs = make_objs(bomb_cents, bomb, times)
        fishs = make_objs(fish_cents, fish, times)
        print('make\t'+str(datetime.datetime.now()))
        # plan the actions
        
        print('plan\t'+str(datetime.datetime.now()))
        leftCat.plan(bombs,fishs,times[-1])
        print('plan\t'+str(datetime.datetime.now()))
        rightCat.plan(bombs,fishs,times[-1])
        print('plan\t'+str(datetime.datetime.now()))
        
        
        # cats will act via the thread for the cat timed_actor
        
        ''' optional real time display code '''
#         print('plans----')
#         print(leftCat.plans)
#         print(rightCat.plans)
#         cv.drawContours(raw,bomb_cntrs,-1,(255,280,199),thickness=3)
#         cv.drawContours(raw,fish_cntrs,-1,(255,280,199),thickness=3)
#         cv.imshow('Computer Vision',raw)
#         cv.waitKey(1)
#         print(step)
        time.sleep(0.005)

        if step % gg_freq == 5:
            mask = filter_hsv(raw,button)
            gg_cntrs = define_contours(mask)
            if len(gg_cntrs)>=1:
                t_lock.acquire()
                gameOver = True
                end = datetime.datetime.now()
                leftCat.no_action(gg=1)
                rightCat.no_action(gg=1)
                t_lock.release()
        step += 1
        print(datetime.datetime.now()) 
        print('step ends:')
            
    ''' ****************************** '''
    
#     t_leftCat.join()
#     t_rightCat.join()
    
    print('reporting match #'+str(match)+': ')

    sample('samples/runs',savefile=1)
    
    
    
