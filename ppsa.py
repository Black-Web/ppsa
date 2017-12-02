'''
python power system analysis
'''
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import networkx as nx


class power_grid():
    def __init__(self, node_num=0, Sb=100):
        self.Sb = Sb
        self.node_num = node_num
        self.admittance_matrix = \
        np.array([[0 for ele in range(0,node_num)] for ele in range(0,node_num)],dtype=np.complex128)
        
    def add_generator(self, device_name= None, **paraments):
        para = Xd_2 * self.Sb/Sn
        self.add_device(loc, para, False)
    def add_line(self,line_label= None,para):
        
    def add_transformer(self,device_name= None, para):
        pass
    def add_device(self,loc,para, para_is_admittance = False):
        '''docstring
        pass
        '''
        if para_is_admittance:
            addup = para*1j
        else: 
            addup = 1/(para*1j)
        
        if not isinstance(loc,(tuple,list)):
            loc = loc,
        
        if len(loc)==1:
            '''
            增加结点/树枝的情况
            '''
            ind2 = self.node_num
            self.node_num += 1
            new_mat = \
            np.array([[0 for ele in range(0,self.node_num)] for ele in range(0,self.node_num)],dtype=np.complex128)
            new_mat[:-1,:-1]=self.admittance_matrix[:,:]
            self.admittance_matrix = new_mat
            del new_mat
            
            ind1 = loc[0]-1
            self.admittance_matrix[ind1,ind2] = -addup
            self.admittance_matrix[ind2,ind1] = -addup 
            self.admittance_matrix[ind2,ind2] = addup
            self.admittance_matrix[ind1,ind1] += addup
        if len(loc)==2:
            '''
            增加连枝的情况
            '''
            if loc[0]==loc[1]:
                raise ValueError('invalid edge:' +str(loc))
            if 0 in loc:
                ind = loc[0]-1
                if ind < 0:
                    ind = loc[1]-1
                self.admittance_matrix[ind,ind] += addup
                
            if 0 not in loc:
                ind1 = loc[0]-1
                ind2 = loc[1]-1
                self.admittance_matrix[ind1,ind2] -= addup
                self.admittance_matrix[ind2,ind1] -= addup
                self.admittance_matrix[ind2,ind2] += addup
                self.admittance_matrix[ind1,ind1] += addup

    def add_devices(self, devices):
        for each in devices:
            self.add_device(self, each)