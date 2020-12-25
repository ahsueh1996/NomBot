import math
import numpy as np
from scipy.optimize import fsolve

'''
2017 Aug 26
Albert Hsueh
Describes a model for predicting tragetories.
'''

G = 9.8
g = G

CABINET_PORPORTION = 0.3        # measured form screen the ratio the cabinets take up on the game screen

def adjust_gravity(play_field_height):
    '''
    The play field height might be scaled on different screen sizes
    so here we adjust the gravitational accel based on the factor
    parametraized by the play field height.
    '''
    return G * play_field_height * CABINET_PORPORTION      # take the cabinet to be approx 1m and use as conversion to pixels

def projectile_model(v, si, ti , tf=-1, sf=(-1,-1), g = -1):
    '''
    This is a grade 12 phy model for projectiles. Given velocity, initial displacement
    initial time, and either of the final time or final displacement, get a lambda func
    in the x and y directions with the other optional info as the variable.
    
    v: tuple, vx and vy
    si: tuple, xi and yi
    ti: float
    ft: float
    sf: tuple, xf and yf
    
    Note the space coords:
    0,0 ---------> x,0
     |
     |
     v
    0,y            x,y
    so g should be (+); going downwards
    '''
    # these functions are in the 0 = f(x) - x form
    # if there is not specified gravity then we will return an equation to solve for gravity
    if g==-1:
        return lambda g: si[1] + v[1] * (tf-ti) + 0.5 * g * (tf-ti)**2       - sf[1]
    fx = lambda xt: si[0] + v[0] * (xt[1]-ti)                              - xt[0]
    fy = lambda yt: si[1] + v[1] * (yt[1]-ti) + 0.5 * g * (yt[1]-ti)**2    - yt[0]
    if tf>=0:
        return (lambda xf: fx((xf,tf)), lambda yf: fy((yf,tf)))
    elif sf[0]>=0 or sf[1]>=0:
        return (lambda tf: fx((sf[0],tf)), lambda tf: fy((sf[1],tf)))

def eval_trajectory(obj, t=-1, pos=(-1,-1), g=1):
    '''
    Solves the trajectory given the final displacement or the time.
    Input -1 for any piece of information that is uneeded.
    ie. t = -1 pos=(-1,20)
    '''
    v = obj.get_vel()
    si = obj.get_dis()
    ti = obj.get_time()
    if g == 1:
        g = obj.get_g()
    x_guess = None
    y_guess = None
    delta = 5
    
    if g==-1:
        ''' solbe for g GIVEN t and position'''
        fy = projectile_model(v,si,ti,tf=t,sf=pos)
        y_guess = 9.8
    
    elif t>=0 and g!=-1:
        ''' solve for the POSITION GIVEN t'''
        fx, fy = projectile_model(v, si, ti, tf=t, g=g)
        x_guess = v[0] + delta
        y_guess = v[1] + delta

    elif (pos[0]>=0 or pos[1]>=0) and g!=-1:
        ''' solve for t GIVEN position'''
        fx, fy = projectile_model(v, si, ti, sf=pos, g=g)
        if pos[0] > -1:
            x_guess = ti + delta
        if pos[1] > -1:
            y_guess = ti + delta
    
    # solve    
    if x_guess != None:
        x_sol = fsolve(fx, x_guess)[0]
    if y_guess != None:
        y_sol = fsolve(fy, y_guess)[0]
    
    if g==-1:
        return y_sol
    if t>=0:
        return (x_sol, y_sol)
    elif pos[0]>=0 and pos[1]>=0:
        return x_sol if x_sol==y_sol else None
    elif pos[0]>=0 or pos[1]>=0:
        return x_sol if y_guess==None else y_sol
    return -1

def calculate_distance(obj,obj_list):
    _min = 99999999
    _idx = 0
    cent = obj.get_dis()
    for idx,each in enumerate(obj_list):
        cent2 = each.get_dis()
        _min = min(_min, math.sqrt((cent[0]-cent2[0])**2+(cent[1]-cent2[1])**2))
        _idx = idx
    return _idx
