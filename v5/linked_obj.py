import numpy as np
from physics_model import *
import datetime as datetime

class Linked_Obj():
    def __init__(self, instance):
        self.id = -1
        self.type = instance.NAME
        self.trajectory = None
        self.instances = []
        self.invInstances = []
        self.valInstances = []
        self.avg_g = 9.8
        self.gs = []
        self.time2impact = -999
        self.impactTime = None
        self.store_instance(instance)
        
    def get_id(self):
        return self.id
    
    def set_id(self,id):
        self.id = id
        
    def get_type(self):
        return self.type
    
    def set_trajectory(self,trajectory):
        self.trajectory = trajectory
        
    def get_trajectory(self):
        return self.trajectory
    
    def get_dest(self):
        return self.instances[-1].get_dest()
    
    def get_time2impact(self):
        return self.time2impact
    
    def get_impactTime(self):
        return self.impactTime
    
    def calculate_time2impact(self,now):
        '''
        Calculates the time2impact for every instance with valid velocity using the avg_g.
        The final time2impact is also an fused value of the resulting time2impact values.
        '''
        if len(self.valInstances)<=0:
            return
        time2impacts = []
        for each in self.valInstances:
            # because each instance was recorded at a different time, the time deltas from eval trajectory need to be
            # offeset accordingly to represent the impact time relative to the 'now'
            dt = eval_trajectory(each, pos=(-1,self.get_dest()[1]), g=self.avg_g)
            time2impact = each.get_time() + datetime.timedelta(seconds=dt) - now
            time2impacts.append(time2impact.total_seconds())
        # for now, we will try simple average as a fusion technique
        self.time2impact = sum(time2impacts)/len(time2impacts)
        self.impactTime = now + datetime.timedelta(seconds=self.time2impact)
    
    def store_instance(self,instance):
        if instance.NAME != self.type:
            return
        instance.set_id(self.id)
        instance.set_trajectory(self.trajectory)
        self.instances.append(instance)
        if instance.get_vel()[1] == -5000:
            self.invInstances.append(instance)
        else:
            self.valInstances.append(instance)
        self.calc_gs()
            
    def get_instances(self):
        return self.instances  
    
    def calc_gs(self):
        '''
        Calculate gravity for every pair satisfying (valid velocity, any)
        and store them in a matrix to save computation. Assume an addition of
        max one instance or one valinstance and one invinstance at a time.
        A priori: gravity is greater than zero. 
        Uncalculated cells always appear in a row or in a column.
        Instead of searching for uncalculated cells in the matrix, use this fact
        to append calculated values.
        Use column 0 to tally the row avg, we skip the negative gravities when summing.
        Calculating row avg makes sense because the row g all comes from one velocity
        estimate. It should be treated as one sample when calulating the final avg grav.
        '''
        # if there are no valid instances, even with gravity we cannot calculate time
        # to impact. Skip the gravity calc
        if len(self.valInstances) == 0:
            self.gs = []
            return
        # If there is at least 1 valid instance then the gs should be populated
        # collect the corrent shape of the gs
        try:
            m,_ = np.shape(self.gs)
        except ValueError:
            # np.shape return (0,)
            m = 0
        # insert the row first if necessary
        if m != len(self.valInstances):
            row = []
            _sum = 0
            num = 0
            for every in self.instances:
                new_g = eval_trajectory(self.valInstances[-1],
                                            abs(self.valInstances[-1].get_time()-every.get_time()).total_seconds(), 
                                            every.get_dis(), g=-1)
                # if the valid instance is paired with an ancestor object, we need to adjust the sign of the calculated
                # gravity
                if self.valInstances[-1].get_time()<every.get_time():
                    new_g *= -1
                row.append(new_g)
                # enforce the g>0 a priori. Note that if the instances are the same, the new_g will result as 0
                if row[-1]>0:
                    _sum += row[-1]
                    num += 1.0
            row.insert(0, _sum/num)
            self.gs.append(row)
        # get the shape again
        try:
            _,n = np.shape(self.gs)
        except ValueError:
            # np.shape return (m,)
            n = -1
        if n-1!=len(self.instances):
            r = len(self.instances)
            if n == -1:
                r -= 1
            n = len(self.gs[0])-1
            # for every row
            for i in range(r):
                new_g = eval_trajectory((self.valInstances[i],
                                            abs(self.valInstances[i].get_time()-self.instances[-1].get_time()).total_seconds()), 
                                            every.get_dis(), g=-1)
                # if the valid instance is paired with an ancestor object, we need to adjust the sign of the calculated
                # gravity
                if self.valInstances.get_time()<self.instances[-1].get_time():
                    new_g *= -1
                # enforce the g>0 a priori. Note that if the instances are the same, the new_g will result as 0
                if new_g >0:
                    self.gs[i].append(new_g)
                    # update the row average
                    self.gs[i][0] = new_g/(n+1)+self.gs[i][0]*n/(n+1)
        _sum = 0
        for row in self.gs:
            _sum += row[0]
        self.avg_g = _sum/len(self.gs)
        
    def get_avg_g(self):
        return self.avg_g
    
