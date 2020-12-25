import cv2 as cv
import copy
import os
from physics_model import *


class Memory():
    ''' Singleton '''
    def __init__(self,init_time,name='test',window_name = 'Memory'):
        self.name = name
        self.snaps = []
        self.times = []
        self.cntrs = []
        self.objs = []
        self.plans = []
        self.ids_inuse = []
        self.obj_count_snap = []
        self.obj_count = 0
        self.init_time = init_time
        self.window_name = window_name
        self.reset_count = 0
    
    def store(self,snapshot,cntrs):
        self.snaps.append(snapshot)
        self.cntrs.append(cntrs)

    def store_adv(self,time,objs):
        self.times.append(time)
        self.objs.append(objs)
    
    def store_plans(self,plans):
        self.plans.append(plans)
        
    def compile_img(self,i):
        ''' cntrs,times,snaps,objs are arrays of particular time instances ''' 
        # first draw every single cntr found at time i
        for obj_type in self.cntrs[i]:
            cv.drawContours(self.snaps[i],obj_type,-1,(255,280,199),thickness=3)
        # code to generate and visualize the trajectory
        n = 100
        look_ahead = 0.25
        dt = look_ahead/n
        for obj_type in self.objs[i]:
            for each in obj_type:
                tf = 0.0
                # step by step generate the trajectory based on the physics model
                for step in range(n):
                    tf += dt
                    x,y = eval_trajectory(each, tf)
                    x=int(x)
                    y=int(y)
                    cv.putText(self.snaps[i],'+',(x,y),cv.FONT_HERSHEY_TRIPLEX,.45,(0,140,255))
                tf = 0.0
                # step by step generate the velocity vector
                for step in range(int(n/3)):
                    tf += dt
                    vx, vy = each.get_vel()
                    x, y = each.get_dis()
                    cv.putText(self.snaps[i],'+',(x+vx*dt,y+vy*dt),cv.FONT_HERSHEY_TRIPLEX,.45,(90,180,0))
        # then for each obj identified at time i, put the text for id and impact time 
        for obj_type in self.objs[i]:
            for each in obj_type:
                x,y = each.get_dis()
                x += 10
                y += 5
                cv.putText(self.snaps[i],str(each.get_id())+', '+str(round(each.get_time2impact(),5)),(x,y),cv.FONT_HERSHEY_TRIPLEX,.5,(0,0,0))                     
        # top left corner we put the snapshot time and snapshot step and number of objs identified
        cv.putText(self.snaps[i],str(self.times[i])+'    step: '+str(i)+'    objs: '+str(self.obj_count_snap[i]),(10,85),cv.FONT_HERSHEY_TRIPLEX,.5,(255,255,255))
        # bottom left corner we put the snapshot time and snapshot step and number of objs identified
        cv.putText(self.snaps[i],'LEFT plans: '+str(self.plans[i][0]),(10,725),cv.FONT_HERSHEY_TRIPLEX,.4,(255,255,255))
        cv.putText(self.snaps[i],'RIGHT plans: '+str(self.plans[i][1]),(10,740),cv.FONT_HERSHEY_TRIPLEX,.4,(255,255,255))
        # show image
        cv.imshow(self.window_name,self.snaps[i])
        # save image
        try:
            os.makedirs('samples/'+self.name+str(self.reset_count))
        except FileExistsError:
            pass
        cv.imwrite('samples/'+self.name+str(self.reset_count)+'/'+str(i)+'.png',self.snaps[i])
        cv.waitKey(100)  
          
    def compile_all(self):
        for i in range(len(self.snaps)):
            self.compile_img(i)
    
    def mem_reset(self,reset_time):
        self.snaps = []
        self.times = []
        self.cntrs = []
        self.objs = []
        self.ids_inuse =[]
        self.obj_count = 0
        self.init_time = reset_time
        self.reset_count += 1
    
    def get_objs(self,ind=-1):
        try:
            return self.objs[ind]
        except IndexError:
            return [[],[]]
    
    def get_time(self,ind=-1):
        try:
            return self.times[-1]
        except IndexError:
            return self.init_time
    
    def acquire_id(self):
        self.ids_inuse.append(self.obj_count)
        self.obj_count += 1
        return self.ids_inuse[-1]
    
    def release_id(self,id):
        self.ids_inuse.remove(id)
        return
    
    def snap_obj_count(self):
        self.obj_count_snap.append(self.obj_count)
        
        