import cv2 as cv
import copy
import os
from physics_model import *


class Memory():
    ''' Singleton '''
    def __init__(self,init_time,name='test',window_name = 'Memory'):
        self.name = name
        self.snaps = []
        self.subsnaps = []
        self.times = []
        self.cntrs = []
        self.subcntrs = []
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
    
    def store_subsnaps(self,snap,cntrs):
        self.subsnaps.append(snap)
        self.subcntrs.append(cntrs)
        
    def compile_img(self,i):
        ''' cntrs,times,snaps,objs are arrays of particular time instances ''' 
        # first draw every single cntr found at time i
        for obj_type in self.cntrs[i]:
            cv.drawContours(self.snaps[i],obj_type,-1,(255,280,199),thickness=3)
        for obj_type in self.subcntrs[i]:
            cv.drawContours(self.subsnaps[i],obj_type,-1,(255,280,199),thickness=3)
        # code to generate and visualize the trajectory
        n = 100
        look_ahead = 0.25
        dt = look_ahead/n
        for obj_type in self.objs[i]:
            for each in obj_type:
                '''
                tf = 0.0
                # step by step generate the trajectory based on the physics model
                for step in range(n):
                    tf += dt
                    x,y = eval_trajectory(each, tf)
                    x=int(x)
                    y=int(y)
                    cv.putText(self.snaps[i],'+',(x,y),cv.FONT_HERSHEY_TRIPLEX,.45,(0,140,255))
                    '''
                # draw the unique parabola on the subsnaps
                y = quadratic_eqn(each.get_dest(), each.get_dis(), each.get_dis_minus_dt())
                for step in range(n*2):
                    x2,_ = each.get_dest()
                    x1,_ = each.get_dis_minus_dt()
                    per = step/(n*2)
                    x = int((x2-x1)*per)+x1
                    cv.putText(self.subsnaps[i],'+',(x,int(round(y(x),0))),cv.FONT_HERSHEY_TRIPLEX,.45,(50,60,255))
                # draw the min and max substep radiuses
                small = 3
                big = 50
                cv.circle(self.snaps[i],each.get_dis(),small,(255,0,0))
                cv.circle(self.subsnaps[i],each.get_dis(),small,(255,0,0))
                cv.circle(self.snaps[i],each.get_dis(),big,(255,0,0))
                cv.circle(self.subsnaps[i],each.get_dis(),big,(255,0,0))    
                # step by step generate the velocity vector
                tf = 0.0
                vx, vy = each.get_vel()
                x, y = each.get_dis()
                for step in range(int(n/2)):
                    tf += dt
                    cv.putText(self.snaps[i],'+',(int(round(x+vx*tf,0)),int(round(y+vy*tf,0))),cv.FONT_HERSHEY_TRIPLEX,.45,(90,180,0))
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
        cv.imwrite('samples/'+self.name+str(self.reset_count)+'/'+str(i)+'b.png',self.snaps[i])
        cv.imwrite('samples/'+self.name+str(self.reset_count)+'/'+str(i)+'a.png',self.subsnaps[i])
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
        
        