import numpy as np

class Bomb():
    def __init__(self,v=(0,0),s=(0,0),t=0,g=9.8):
        self.__BGR_UB = np.array([0,0,255])     # BGR scheme
        self.__BGR_LB = np.array([0,0,110])
        self.__CONTOUR_MIN = 52                 # contours of bombs are at least this big
        self.v = v
        self.s = s
        self.t = t
        self.id = -1
        self.g = g
        self.NAME = 'bomb'
        self.time2impact = -1
    
    def get_bgr_ub(self):
        return self.__BGR_UB
    
    def get_bgr_lb(self):
        return self.__BGR_LB
    
    def get_contour_min(self):
        return self.__CONTOUR_MIN
    
    def get_vel(self):
        return self.v
    
    def set_vel(self,v):
        self.v = v
    
    def get_dis(self):
        return self.s
    
    def set_dis(self,s):
        self.s = s
        
    def get_time(self):
        return self.t
        
    def set_time(self,t):
        self.t = t
        
    def set_id(self,id):
        self.id = id
        
    def get_id(self):
        return self.id
    
    def set_g(self,g):
        self.g = g
    
    def get_g(self):
        return self.g
    
    def set_time2impact(self,time2impact):
        self.time2impact = time2impact
        
    def get_time2impact(self):
        return self.time2impact
        