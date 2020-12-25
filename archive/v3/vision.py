import cv2 as cv
import numpy as np
import math
import pyautogui as ui
import time
import datetime as datetime
import copy

'''
2017 Aug 26
Albert Hsueh
This module handles the vision algorithms.
'''

count = 0   # keeps track of how many samples have been taken

def reset_sample_count():
    global count
    count = 0
    return

def sample(filepath='samples/unnamed',savefile = 0):
    '''
    Sampling is done by taking a screenshot of the primary display using the 
    py auto gui library and the screenshot is returned as an PIL object.
    Using the cvtPIL2np, we automatically convert image to numpy array.
    Sampling by default will not save the screen shot, but for demonstration
    we can choose to save it. Give it a file path and a prefix and each time
    sample is called, the file will be saved. 
    Saving to disk costs time: avg 0.13~0.16 sec
    Compared to not saving: avg 0.04~0.06 sec
    '''
    global count
    if savefile == 1:
        im =  ui.screenshot(filepath + '-' + str(count) +'.png')
        count += 1
    else:
        im = ui.screenshot()
    
    return cvtPIL2np(im)

def cvtPIL2np(im):
    return np.array(im)[:,:,::-1].copy()    # The PIL image is in RGB mode
                                            # you can tell if you print the PIL obj

def filter_bgr(im,obj):
    '''
    Call this on a nom cat screen capture and it returns a mask of all the obj
    using color segmentation.
    '''
    return cv.inRange(im, obj.get_bgr_lb(), obj.get_bgr_ub())

def filter_hsv(im,obj):
    '''
    Call this on a nom cat screen capture and it returns a mask of all the obj
    using hsv color segmentation.
    '''
    hsv = cv.cvtColor(im,cv.COLOR_BGR2HSV)
    return cv.inRange(hsv, obj.get_hsv_lb(), obj.get_hsv_ub())

def define_contours(mask):
    '''
    Call this on a mask and we use centroid finding algorithm to localize all
    objects and return a vector of xy coordinates.
    '''
    __, contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return contours

def isolate_contours(contours,obj):
    ret = []
    for each in contours:
        if each.shape[0] >= obj.get_contour_min():
            ret.append(each)
    return ret

def eval_centroids(contours):
    ret = []
    for each in contours:
        M = cv.moments(each)
        ret.append( (int(M['m10']/M['m00']),int(M['m01']/M['m00'])) )
    return ret

def make_objs(cent_snapshots, obj, time):
    snap1, snap2 = cent_snapshots
    objects = []
    dt = (time[-1]-time[0]).total_seconds() # get the elapsed time in seconds
    for each in snap2:
        if len(snap1)==0:
            break
        i = calculate_distance(each,snap1)
        
        new_obj = copy.deepcopy(obj)
        new_obj.set_vel(( (each[0]-snap1[i][0])/dt, (each[1]-snap1[i][1])/dt ))
        new_obj.set_dis(each)
        
        objects.append(new_obj)
        del snap1[i]
    return objects
        
def calculate_distance(obj,obj_list):
    _min = 99999999
    _idx = 0
    for idx,each in enumerate(obj_list):
        _min = min(_min, math.sqrt((obj[0]-each[0])**2+(obj[1]-each[1])**2))
        _idx = idx
    return _idx
        