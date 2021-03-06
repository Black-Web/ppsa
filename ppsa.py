# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
python power system analysis
'''
import numpy as np
#import scipy as sp
#import matplotlib.pyplot as plt
#import networkx as nx


class power_grid():
    def __init__(self, node_num, Sb=100):
        self.Sb = Sb
        self.node_num = node_num
        self.admat_with_earth = np.zeros((node_num+1,node_num+1)\
                                        ,dtype=np.complex128)
        self.admat=self.admat_with_earth[1:,1:]
        self.source = self.admat_with_earth[1:,0]
        self.load = self.admat_with_earth[0,1:]
    @property
    def Y(self):
        return self.admat_with_earth[1:,1:]
    @property
    def Z(self):
        return self.impedance_matrix()
    def impedance_matrix(self):
        return np.linalg.inv(self.admat)
    def nodes_voltage(self,node=None):
        '''docstring
        return the voltage of each node based on the current grid structure,
        if parament node given,only return voltage at node
        * parament:

        node : legal numpy array index

        * return:numpy array representing voltage at different node
        '''
        U = np.dot(self.impedance_matrix(),self.source+self.load)
        if node:
            return U[node]
        else:
            return U
    def add_device(self,loc,para, para_is_admittance = False):
        '''docstring
        basic function of the power_grid.
        used by other functions that will change the grid's admittance matrix such as *add_transformer*,*add_generator*
        '''
        if para_is_admittance:
            addup = para
        else: 
            addup = 1/para
        
        if not isinstance(loc,(tuple,list)):
            loc = loc,
        
        if len(loc)==1:
            # when add a node that links to an existing node
            #* to be correctified
            ind2 = self.node_num
            self.node_num += 1
            new_mat = np.zeros((self.node_num,self.node_num)\
                                ,dtype=np.complex128)
            new_mat[:-1,:-1]=self.admat_with_earth[:,:]
            self.admat_with_earth = new_matd
            self.admat = self.admat_with_earth[1:,1:]
            del new_mat
            
            ind1 = loc[0]
            self.admat_with_earth[ind1,ind2] = -addup
            self.admat_with_earth[ind2,ind1] = -addup 
            self.admat_with_earth[ind2,ind2] = addup
            self.admat_with_earth[ind1,ind1] += addup
        if len(loc)==2:
            # when add a branch between two nodes
            if loc[0]==loc[1]:
                pass
            elif 0 in loc:
                ind = loc[0]+loc[1]
                self.admat_with_earth[ind,ind] += addup
            elif 0 not in loc:
                ind1 = loc[0]
                ind2 = loc[1]
                self.admat_with_earth[ind1,ind2] -= addup
                self.admat_with_earth[ind2,ind1] -= addup
                self.admat_with_earth[ind2,ind2] += addup
                self.admat_with_earth[ind1,ind1] += addup
    def add_generator(self,loc,Sn,Xd_2,device_name= None,*args, **kw):
        para = Xd_2 * self.Sb/Sn
        ref_vol = 1
        if 'ref_vol' in kw:
            ref_vol *= kw['ref_vol']
        self.add_device(loc, para, False)
        if 0 in loc:
            self.source[loc[0] + loc[1] -1] += ref_vol/para
        else:
            self.source[loc[0]-1] += ref_vol/para
            self.source[loc[1]-1] -= ref_vol/para
    def add_line(self,loc,voltage,x,length,line_label= None,*args, **kw):
        Xb = voltage**2 / self.Sb
        para = length * x / Xb
        self.add_device(loc,para*1j,False)
        if 'b' in kw:
            para = kw['b'] * length * 10**-6 * Xb / 2
            self.add_device((loc[0],0),para*1j,True)
            self.add_device((loc[1],0),para*1j,True)
    def add_transformer(self,loc,Sn,Vs,device_name= None,*args, **kw):
        para = Vs * self.Sb / Sn
        self.add_device(loc,para*1j,False)
    def add_load(self,loc,Sn,Xld_2,device_name= None,*args, **kw):
        para = Xld_2 * self.Sb/Sn
        ref_vol = 1
        if 'ref_vol' in kw:
            ref_vol *= kw['ref_vol']
        self.add_device(loc, para, False)
        if 0 in loc:
            self.load[loc[0] + loc[1] -1] += ref_vol/para
        else:
            self.load[loc[0]-1] += ref_vol/para
            self.load[loc[1]-1] -= ref_vol/para
    def add_phase_modifier(self,loc,Sn,Xld_2,device_name= None,*args, **kw):
        pass
    def short_circuit(self,f,Zf=0):
        '''docstring
        return the subtransient voltage of each node after short circuit at node f
        '''
        Uf = self.nodes_voltage()
        Z = self.impedance_matrix()[f-1]
        If = Uf[f-1]/(Z[f-1]+Zf)
        Uf -= Uf[f-1]*Z/Z[f-1]
        return Uf,If
class device(object):
    """docstring for device"""
    def __init__(self, arg):
        super(device, self).__init__()
        self.arg = arg
def impedance_of_line(length, x, voltage, Sb):
    return length * x/(voltage**2 / Sb)
def impedance_of_transformer(Vs, Sb, Sn):
    return Vs * Sb / Sn
def impedance_of_generator(Xd, Sb, Sn):
    return Xd * Sb/Sn
impedance_of_load = impedance_of_generator
def current_distribution(admat,U):
    U= np.array(U)
    U= U.reshape((-1,1))-U.reshape((1,-1))
    I = -U * admat
    return I
if __name__ == '__main__':
    grid = power_grid(node_num= 5, Sb= 120)
    grid.add_generator(loc=(1,0),Sn=120 ,Xd_2= 0.23)
    grid.add_generator(loc=(2,0),Sn=60 ,Xd_2= 0.14)
    grid.add_transformer(loc=(1,3),Sn= 120, Vs= 0.105)
    grid.add_transformer(loc=(2,4),Sn= 60, Vs= 0.105)
    grid.add_line(loc=(3,4),voltage=115, x= 0.4, b= 2.8, length= 120)
    grid.add_line(loc=(3,5),voltage=115, x= 0.4, b= 2.8, length= 80)
    grid.add_line(loc=(4,5),voltage=115, x= 0.4, b= 2.8, length= 70)
    print('grid\'s admittance matrix:\n',grid.admat)
    print('5结点短路：',grid.admat[:-1,:-1])
    grid.add_line(loc=(4,5),voltage=115, x= 0.4, b= 2.8, length= -70)
    grid.add_line(loc=(4,0),voltage=115, x= 0.4, b= 2.8, length= 35)
    grid.add_line(loc=(0,5),voltage=115, x= 0.4, b= 2.8, length= 35)
    print('L3中点短路：',grid.admat)
