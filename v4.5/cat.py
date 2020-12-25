import pyautogui as ui
import numpy as np
import datetime as datetime
from physics_model import *
from _datetime import date
import time
import threading
import copy

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
    
    def calibrate_grav(self,play_field_height):
        return adjust_gravity(play_field_height)
        
    def act(self,cmd=-2):
        '''
        There are two commands, 1 and -1 for mouth open and
        mouth close respectively.
        '''
        if cmd!= -2:
            self.cmd = cmd
        if self.cmd==self.OPEN:
            ui.keyDown(self.control,_pause=False)
        elif self.cmd==self.CLOSE:
            ui.keyUp(self.control,_pause=False)
        return
    
    def no_action(self,gg=0):
        '''
        The default no action. Currently set to be mouth close
        '''
        self.act(cmd=self.CLOSE)
        self.gg=gg
        return
    
    def learn(self,bombs,fishs,now,memory,curStage):
        xmin,xmax = self.__order_zone(curStage)[0]
        p_bombs, p_fishs = memory.get_objs()
        tf = (now-memory.get_time()).total_seconds() # note because t0 = 0 for the objs, dt = tf
        # learn the bombs
        n_bombs = self.learnHelper(bombs, p_bombs, xmax, xmin, memory, tf)
        # learn the fish
        n_fishs = self.learnHelper(fishs, p_fishs, xmax, xmin, memory, tf)
        return n_bombs, n_fishs
    
    def learnHelper(self,objs,p_objs,xmax,xmin,memory,tf):
        n_objs = []
        p_objs_outs = []
        for each in p_objs:
            ''' assume that every old obj is now a new obj if the new
            obj location is anticipated to be within the x range of the stage '''
            sf = eval_trajectory(each, tf) # get the anticipated location of the bombs
            if sf[0]>xmax or sf[0]<xmin:
                p_objs_outs.append(each)
                continue
            # find the nearest new obj to the old obj
            if len(objs) == 0:
                p_objs_outs.append(each)
                continue
            i = calculate_distance(each, objs)
            # set the id of the objects to be the same
            objs[i].set_id(each.get_id())
            # calulate the new g value and set it as the new g value
            new_g = eval_trajectory(each, tf, objs[i].get_dis(), g=-1)
            objs[i].set_g(new_g)
            # append this object to the new obj list
            n_objs.append(copy.deepcopy(objs[i]))
            # and remove it from the working list so that it can't be matched to again
            del objs[i]
        for each in objs:
            ''' first time bombs are those who did not have a old obj as ancestor '''
            each.set_id(memory.acquire_id())
            n_objs.append(copy.deepcopy(each))
        for each in p_objs_outs:
            ''' out of play bombs are those who do not have a new obj as descendent '''
            memory.release_id(each.get_id())
        return n_objs

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
                # this is the time (s) until the bomb hits the mouth
                delta_t = eval_trajectory(each, pos=(-1,self.mouth[1]))
                each.set_time2impact(delta_t)
                # append the times to close mouth
                tar_close = now + datetime.timedelta(seconds=delta_t-saftey_t)
                self.plans.append((tar_close,self.CLOSE))
                
        if len(fishs)>0:   
            for each in fishs:
                if self._skip_protocol(each):
                    continue
                # always make the ti for fish zero... that way we get the delta t
                # as an ouput of eval trajectory
                # this is the time until the fish hits the mouth
                delta_t = eval_trajectory(each, pos=(-1,self.mouth[1]))
                each.set_time2impact(delta_t)
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
#         if obj.get_dis()[1]<self.zone[1][0]:
#             return True
        
    
    def _timed_actor(self,lock):
        safety = datetime.timedelta(seconds=0.03)
        while (self.gg == 0):
#             print(self.control)
            time.sleep(0.0001)
            lock.acquire()
            now_safe = datetime.datetime.now()+safety
            for each in self.plans:
                if each[0]<=now_safe:
                    self.act(cmd=each[1])
                    break
            lock.release()
