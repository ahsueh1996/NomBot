import numpy as np

class Fish():
    def __init__(self,v=(0,0),s=(0,0),t=0):
        self.__HSV_UB = np.array([125,161,255])     # HSV scheme
        self.__HSV_LB = np.array([120,19,81])
        self.__CONTOUR_MIN = 52                 # contours of bombs are at least this big
        self.v = v
        self.s = s
        self.t = t
        self.NAME = 'fish'
    
    def get_hsv_ub(self):
        return self.__HSV_UB
    
    def get_hsv_lb(self):
        return self.__HSV_LB
    
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
        