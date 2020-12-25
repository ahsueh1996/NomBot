import pyautogui as ui
import numpy as np
import datetime as datetime
from physics_model import *
from _datetime import date
import time
import threading

class Cat():
    def __init__(self, control, mouth, zone=((0,0),(500,500))):
        self.control = control
        self.zone = self.__order_zone(zone) # use as upper and lower limits
        self.mouth = mouth
        self.cmd = 1
        self.plans = []  # (execution time, cmd)
        self.gg = 0
        self.OPEN = 1
        self.CLOSE = -1
        self.impatient = 0
        self.IMPATIENT_LIM = 15
        if self.control == 'left':
            self.REL_DIR = -1
        else:
            self.REL_DIR = 1
    
    def __order_zone(self,zone): 
        ''' 
        orders the rectangle search zone into min x and 
        min y format for easy comparison
        zone is tuple of tuples
        '''
        p1,p2 = zone
        x1,y1 = p1
        x2,y2 = p2
        return (sorted([x1,x2]),sorted([y1,y2]))   
        
    def act(self,cmd=-2):
        '''
        There are two commands, 1 and -1 for mouth open and
        mouth close respectively.
        '''
        if cmd!= -2:
            self.cmd = cmd
        if self.cmd>=self.OPEN:
            ui.keyDown(self.control,_pause=False)
        elif self.cmd<=self.CLOSE:
            ui.keyUp(self.control,_pause=False)
        return
    
    def no_action(self,gg=0):
        '''
        The default no action. Currently set to be mouth close
        '''
        self.act(cmd=self.CLOSE)
        self.gg=gg
        return

    def plan(self,bombs,fishs,now):
        '''
        This function does the planning. Ultimately it buffers a
        command to be executed by the "act" phase
        '''
        self.plans = []
        saftey_t = 0.001
        
        if len(bombs)>0:    
            for each in bombs:
                # skip irrelevant objects
                if self._skip_protocol(each):
                    continue
                # always make the ti for bombs zero... that way we get the delta t
                # as an ouput of eval trajectory
                # this is the time until the bomb hits the mouth
                delta_t = eval_trajectory(each, pos=(-1,self.mouth[1]))
                # append the times to close mouth
                tar_close = now + datetime.timedelta(seconds=delta_t-saftey_t)
                self.plans.append((tar_close,self.CLOSE))
                
        if len(fishs)>0:   
            for each in fishs:
                if self._skip_protocol(each):
                    continue
                # always make the ti for bombs zero... that way we get the delta t
                # as an ouput of eval trajectory
                # this is the time until the bomb hits the mouth
                delta_t = eval_trajectory(each, pos=(-1,self.mouth[1]))
                # append the times to close mouth
                tar_open = now + datetime.timedelta(seconds=delta_t-saftey_t)
                self.plans.append((tar_open,self.OPEN))   
            
        # sort the plans from soonest to latest
#         self.plans = sorted(self.plans, key = lambda x:x[0])
        return
    
    def _skip_protocol(self,obj):
        # skip all bombs heading past the cat
        if obj.get_vel()[0]*self.REL_DIR<=0:
            return True
        # skip all bombs that have passed the cat
        if (obj.get_dis()[0]-self.mouth[0])*self.REL_DIR>=0:
            return True
        # skip all bombs that are too high
        # note the screen's space coord is inverted in y axis
        if obj.get_dis()[1]<self.zone[1][0]:
            return True
        
    
    def _timed_actor(self,lock):
        while (self.gg == 0):
#             print(self.control)
            time.sleep(0.0001)
            now = datetime.datetime.now()
            
            for each in self.plans:
                if each[0]>=now:
                    lock.acquire()
                    self.act(cmd=each[1])
                    lock.release()
                    break
        