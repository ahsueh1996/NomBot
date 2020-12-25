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

def sample(filepath='samples/unnamed',savefile = 0,region=(-1,-1,-1,-1)):
    '''
    Sampling is done by taking a screenshot of the primary display using the 
    py auto gui library and the screenshot is returned as an PIL object.
    Using the cvtPIL2np, we automatically convert image to numpy array.
    Sampling by default will not save the screen shot, but for demonstration
    we can choose to save it. Give it a file path and a prefix and each time
    sample is called, the file will be saved. 
    Saving to disk costs time: avg 0.1045 sec
    Compared to not saving: avg 0.034 sec
    '''
    global count
    if savefile == 1:
        im =  ui.screenshot(filepath + '-' + str(count) +'.png')
        count += 1
    else:
        if region == (-1,-1,-1,-1):
            im = ui.screenshot()
        else:
            im = ui.screenshot(region=region)
    
    return im

def cvtPIL2np(im):
    ''' adds 0.01097sec '''
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

def make_objs(cent_snapshots, obj, time, dest=((0,0),(0,0)), stage=((0,0),(0,0))):
    ''' using a small time multi sample technique, we can make objects that with estimates
    for velocity. A pirori knowledge used here is that if object is heading left, it's destination
    is the left cat's mouth. But if the vx of that object is unreliable, we know that all objects
    appearing near the right side of the stage will head left and similar is true for objs heading 
    right.'''
    snap1, snap2 = cent_snapshots
    objects = []
    dt = (time[-1]-time[0]).total_seconds() # get the elapsed time in seconds
    # set the time for the objects to be made
    obj.set_time(time[-1])
    # for each snap2, find a ancestor from snap1 by defining a search min/max square. 
    for each in snap2:
        # when there is not ancestors left to match snap2 items, break
        if len(snap1)==0:
            break
        i = calculate_distance(each,snap1,(5,50))
        # if nothing matches, just continue
        if i == None:
            continue
        # for the match, make a new object
        new_obj = copy.deepcopy(obj)
        # calculate the velocity using assumption that the object has travelled only
        # a small distance in the time dt
        vx,vy = ( (each[0]-snap1[i][0])/dt, (each[1]-snap1[i][1])/dt )
        mag = math.sqrt(vx**2+vy**2)
        # filtering the velocity estimates. Invalid velocity will point straight up
        # with vy <=-5000
        if mag >= 1400:
            vy = -5000
            x_range = sorted([stage[0][0],stage[1][0]])
            vx = -1  # default the velocity to go to the left cat then test for correctness
            if abs(x_range[0]-each[0])<abs(x_range[1]-each[0]):
                # closer to the left cat means it's probably heading to the right cat
                vx = 1
        new_obj.set_vel((vx,vy))
        # a prior knowlege: obj going left will end up in dest[0],
        # obj going right will end up in dest[1]
        if vx<0:
            new_obj.set_dest(dest[0])
        elif vx>0:
            new_obj.set_dest(dest[1])
        # set the positions
        new_obj.set_dis(each)
        new_obj.set_dis_minus_dt(snap1[i])
        # put the new obj in the list and move on
        objects.append(new_obj)
        del snap1[i]
    return objects
        
def calculate_distance(cent,cent_list,min_max_zone):
    ''' given a centroid and a list of centroids, match the closest centroid
    that lies within the min_max_zone '''
    small, big = min_max_zone
    _min = 99999999
    _idx = None
    for idx,each in enumerate(cent_list):
        dx = abs(cent[0]-each[0])
        dy = abs(cent[1]-each[1])
        if dx>=small or dy>=small:
            if dx<=big or dy<=big:
                r = math.sqrt(dx**2+dy**2)
                if r<_min:
                    _idx = idx
                    _min = r
    return idx
        