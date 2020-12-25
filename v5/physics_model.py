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

def eval_trajectory(obj, delta_t=-1, pos=(-1,-1), g=1):
    '''
    Solves the trajectory given the final displacement or the delta time.
    Input -1 for any piece of information that is uneeded.
    ie. delta_t = -1 pos=(-1,20)
    '''
    v = obj.get_vel()
    si = obj.get_dis()
    ti = 0  # obj.get_time() gives datetime
    if g == 1:
        g = obj.get_g()
    x_guess = None
    y_guess = None
    delta = 5
    
    if g==-1:
        ''' solbe for g GIVEN delta_t and position'''
        fy = projectile_model(v,si,ti,tf=delta_t,sf=pos)
        y_guess = 9.8
    
    elif delta_t>=0 and g!=-1:
        ''' solve for the POSITION GIVEN delta_t'''
        fx, fy = projectile_model(v, si, ti, tf=delta_t, g=g)
        x_guess = v[0] + delta
        y_guess = v[1] + delta

    elif (pos[0]>=0 or pos[1]>=0) and g!=-1:
        ''' solve for delta_t GIVEN position'''
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
    if delta_t>=0:
        return (x_sol, y_sol)
    elif pos[0]>=0 and pos[1]>=0:
        return x_sol if x_sol==y_sol else None
    elif pos[0]>=0 or pos[1]>=0:
        return x_sol if y_guess==None else y_sol
    return -1

def calculate_distance_from_quad(linked_obj,obj_list,min_max_zone):
    ''' given a linked obj and a list of obj, match the first object that lies on the
    trajectory and is in between the ancestor obj and the destination. It is a given
    that the destinations match the linked obj's destination.'''
    small, big = min_max_zone
    quad = linked_obj.get_trajectory()
    obj = linked_obj.get_instances()[-1]
    _idx = None
    for idx,each in enumerate(obj_list):
        # check for same destination
        if each.get_dest() != linked_obj.get_dest():
            continue
        ok = 0
        cents = (each .get_dis(),each.get_dis_minus_dt())
        for i in range(2):
            # check if object lies between the last instance and the dest
            if not is_between(cents[i], obj.get_dis_minus_dt(), obj.get_dest()):
                break
            # calculate the y position given the x position of the potential match
            dy = abs(quad(cents[i][0])-cents[i][1])
            # both snapshots from the small time multi sample step must be within margin
            # this removes objects that happen to be in transit with each other
            if dy>=small and dy<=big:
                ok += 1
            else:
                break
        if ok >=2:
            return _idx
    return idx

def is_between(p,p1,p2):
    ''' return true if p lies in between p1 and p2 in xy coord'''
    x_range = sorted([p1[0],p2[0]])
    y_range = sorted([p1[1],p2[1]])
    if p[0]-x_range[0]>x_range[1]-x_range[0]:
        return True # we only care about x range for now
        if p[1]-y_range[0]>y_range[1]-y_range[0]:
            return True
    return False

def quadratic_eqn(p1,p2,p3):
    ''' input 3 points that will uniquely solve for a quadratic eqn in the
    form y = ax^2+bx+c. Returned as a lambda function of x.'''
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    if p1 == p2:
        x2+=1
        y2-=1
    if p2 == p3:
        x3+=1
        y3-=1
    if p3 == p1:
        x1-=1
        y1+=1
    Y = np.array([[y1],[y2],[y3]])
    X = np.array([[x1*x1,x1,1],[x2*x2, x2, 1],[x3*x3, x3, 1]])
    coe = np.matmul(np.linalg.inv(X),Y)
    return lambda x: coe[0][0]*x**2+coe[1][0]*x+coe[2][0]

