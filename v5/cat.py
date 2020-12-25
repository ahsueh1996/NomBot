import pyautogui as ui
import numpy as np
import datetime as datetime
from _datetime import date
import time
import threading
import copy

from linked_obj import Linked_Obj
from physics_model import *

class Cat():
    def __init__(self, control, mouth, zone=((0,0),(500,500))):
        self.control = control
        self.zone = self.__order_zone(zone) # use as upper and lower limits
        self.mouth = mouth
        self.cmd = 1
        self.plans = {}  # id:(execution time, cmd)
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
    
    def learn(self,objs,linked_objs,memory,now):
        ''' 
        This function is a learning model to determine which instances
        are from the same object and the corresponding gravity parameter such that a impact
        time can be calculated in the planning step. The difference from the vision's
        object linking algorithm is that some longer dt has passed and thus we cannot make the
        same small time delta assumption and search very close to the obj's initial position.
        Instead this function uses the a priori knowledge that the bombs travel in a parabolic
        trajectory and that it will land at a predetermined location. The double sample + the
        known destination allows us to determine uniquely this trajectory as a function of x.
        The object linking can now be independent of the velocity estimate (which is error prone).
        
        Learning the gravity can be accomplished by averaging the result for gravity using all pairs
        of instances satisfying (any instance, all instance with valid velocity).
        '''
        # destroy dropped objects
        for i,obj_type in enumerate(linked_objs):
            for j,linked_obj in enumerate(obj_type):
                if linked_obj.get_impactTime() <= now:
                    del linked_objs[i][j]
        # link the objects frist
        for i,obj_type in enumerate(linked_objs):
            for linked_obj in obj_type:
                # for each linked obj, find it's predecessor
                idx = calculate_distance_from_quad(linked_obj, objs, (0,8))
                if idx == None:
                    continue
                # store the object as an instance of the linked obj. This step calculates the gravity
                # automatically
                linked_obj.store(copy.deepcopy(objs[i][idx]))
                del objs[i][idx]
        # the remaining, un matched objects are the roots of new linked objects
        for i,obj_type in enumerate(objs):
            for obj in obj_type:
                new = Linked_Obj(obj)
                new.set_id(memory.acquire_id())
                new.set_trajectory(quadratic_eqn(obj.get_dest(), obj.get_dis(), obj.get_dis_minus_dt()))
                linked_objs[i].append(new)
        return linked_objs

    def plan(self,linked_objs,now):
        '''
        This function does the planning. Ultimately it buffers a
        command to be executed by the "act" phase
        '''
        saftey_t = 0.001
        
        for obj_type in linked_objs:
            # define the action to be planned based on the object type
            try:
                if obj_type[0].get_type() == 'bomb':
                    cmd = self.CLOSE
                else:
                    cmd = self.OPEN
            except IndexError:
                continue
            # proceed to calculate time2impact and record the plan
            for linked_obj in obj_type:    
                # skip irrelevant objects
                if self._skip_protocol(linked_obj):
                    continue
                linked_obj.calculate_time2impact(now)
                # append the times to close mouth
                tar = now + datetime.timedelta(seconds=linked_obj.get_time2impact()-saftey_t)
                try:
                    self.plans[linked_obj.get_id()]
                except KeyError:
                    self.plans[linked_obj.get_id()] = (tar,cmd)
        # sort the plans from soonest to latest
#         self.plans = sorted(self.plans, key = lambda x:x[0])
        return
    
    def _skip_protocol(self,linked_obj):
        # skip all bombs heading past the cat
        if linked_obj.get_dest() != self.mouth:
            return True
        # skip all bombs that have passed the cat
        if (linked_obj.get_instances()[-1].get_dis()[0]-self.mouth[0])*self.REL_DIR>=0:
            return True
    
    def _timed_actor(self,lock):
        safety = datetime.timedelta(seconds=0.03)
        while (self.gg == 0):
#             print(self.control)
            time.sleep(0.0001)
            lock.acquire()
            now_safe = datetime.datetime.now()+safety
            for key in self.plans:
                tar, cmd = self.plans[key]
                if tar<=now_safe:
                    self.act(cmd=cmd)
                    self.prune.append(key)
                    del self.plans[key]
                    break
            lock.release()
