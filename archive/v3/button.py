import numpy as np

class Button():
    def __init__(self,v=(0,0),s=(0,0),t=0):
        self.__HSV_UB = np.array([112,255,255])     # HSV scheme
        self.__HSV_LB = np.array([110,183,255])
        self.__CONTOUR_MIN = 50                 # contours of bombs are at least this big
        self.v = v
        self.s = s
        self.t = t
        self.NAME = 'playagain'
    
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
        