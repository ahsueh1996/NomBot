import pyautogui as emu
import datetime as datetime
import time
import threading
import sys

from cat import Cat
from bomb import Bomb
from fish import Fish
from button import Button
from linked_obj import Linked_Obj
from memory import Memory
from vision import *
from _datetime import date


''' define these'''
curStage = ((508,103),(858,725))
matches = 50
fish_freq = 5
gg_freq = 50
trial_name = 'data'
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
leftCat = Cat('left',(608, 520),zone=((802, 309),(534, 555)))
rightCat = Cat('right',(746, 520),zone=((802, 309),(534, 555)))

if matches == None:
    matches = input('Enter number of matches to start: ')
    for count in range(3):    
        print(str(3-count))
        time.sleep(1.5)
    print('start!')

matchRecords = []
init_grav = leftCat.calibrate_grav(h(curStage))
bomb = Bomb(g=init_grav)
fish = Fish(g=init_grav)
button = Button(g=0)

window_name = 'Computer Vision'
cv.namedWindow(window_name)
cv.moveWindow(window_name, 1656, 140)
cv.waitKey(1)

memory = Memory(datetime.datetime.now(),name=trial_name,window_name = window_name)


    
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
        bomb_cntrs = []
        fish_cntrs = []
        bombs = []
        linked_bombs = []
        fishs = []
        linked_fishs = []
        times = []
        raws = []
        rawPILs = []
        # take two snapshots to analysis
        t_lock.acquire()
        for i in range(2):
            rawPILs.append(sample())
            # we will call the time immediately after the last sample t=0
            times.append(datetime.datetime.now())
        t_lock.release()
        # identify the fish and bomb centroids
        for i in range(2):
            raws.append(cvtPIL2np(rawPILs[i]))
            bomb_cntrs.append(isolate_contours( define_contours( filter_bgr(raws[i],bomb) ), bomb ))        
            bomb_cents.append(eval_centroids( bomb_cntrs[i] ))
            fish_cntrs.append(isolate_contours( define_contours( filter_hsv(raws[i],fish) ), fish ))        
            fish_cents.append(eval_centroids( fish_cntrs[i] ))
        # store the latest snapshot to memory    
        memory.store(raws[-1],[bomb_cntrs[-1],fish_cntrs[-1]])   
        memory.store_subsnaps(raws[0],[bomb_cntrs[0],fish_cntrs[0]])    
        # make the list of bombs and fish
        bombs = make_objs(bomb_cents, bomb, times, dest=(leftCat.mouth,rightCat.mouth),stage=curStage)
        fishs = make_objs(fish_cents, fish, times, dest=(leftCat.mouth,rightCat.mouth),stage=curStage)
        # link objs and learn gravity values and commit to memory (adv storing). One cat can update the whole snapshot
        linked_bombs,linked_fishs = leftCat.learn([bombs,fishs],[linked_bombs,linked_fishs],memory,times[-1])
        memory.store_adv(times[-1],[bombs,fishs])
        memory.snap_obj_count()
        # plan the actions
        t_lock.acquire()
        leftCat.plan([linked_bombs,linked_fishs],times[-1])
        rightCat.plan([linked_bombs,linked_fishs],times[-1])
        memory.store_plans([leftCat.plans,rightCat.plans])
        t_lock.release()
        
        # cats will act via the thread for the cat timed_actor
#         time.sleep(0.05)

        if step % gg_freq == 5:
            mask = filter_hsv(raws[-1],button)
            gg_cntrs = define_contours(mask)
            if len(gg_cntrs)>=1:
                t_lock.acquire()
                gameOver = True
                end = datetime.datetime.now()
                leftCat.no_action(gg=1)
                rightCat.no_action(gg=1)
                t_lock.release()
        step += 1
            
    ''' ****************************** '''
#     t_leftCat.join()
#     t_rightCat.join()
        
    print('reporting match #'+str(match)+': ')
    memory.compile_all()
    memory.mem_reset(datetime.datetime.now())
    
    
    
