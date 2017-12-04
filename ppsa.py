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
        np.array([[0 for ele in range(0,node_num)] for ele in range(0,node_num)],\
            dtype=np.complex128)
        
    def add_generator(self,loc,Sn,Xd_2,device_name= None,*args, **kw):
        para = Xd_2 * self.Sb/Sn
        self.add_device(loc, para, False)
    def add_line(self,loc,voltage,x,length,line_label= None,*args, **kw):
        Xb = voltage**2 / self.Sb
        para = length * x / Xb
        self.add_device(loc,para,False)
        if 'b' in kw:
            para = kw['b'] * length * 10**-6 * Xb / 2
            self.add_device((loc[0],0),para,True)
            self.add_device((loc[1],0),para,True)
    def add_transformer(self,loc,Sn,Vs,device_name= None,*args, **kw):
        para = Vs * self.Sb / Sn
        self.add_device(loc,para,False)
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
            np.array([[0 for ele in range(0,self.node_num)] \
                for ele in range(0,self.node_num)],dtype=np.complex128)
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
                pass
                # raise ValueError('invalid edge:' +str(loc))
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


if __name__=='__main__':
    grid = power_grid(node_num= 5, Sb= 120)
    grid.add_generator(loc=(1,0),Sn=120 ,Xd_2= 0.23)
    grid.add_generator(loc=(2,0),Sn=60 ,Xd_2= 0.14)
    grid.add_transformer(loc=(1,3),Sn= 120, Vs= 0.105)
    grid.add_transformer(loc=(2,4),Sn= 60, Vs= 0.105)
    grid.add_line(loc=(3,4),voltage=115, x= 0.4, b= 2.8, length= 120)
    grid.add_line(loc=(3,5),voltage=115, x= 0.4, b= 2.8, length= 80)
    grid.add_line(loc=(4,5),voltage=115, x= 0.4, b= 2.8, length= 70)
    print('初始导纳矩阵：\n',grid.admittance_matrix)
    print('5结点短路的矩阵：\n',grid.admittance_matrix[:4,:4])
    grid.add_line(loc=(4,5),voltage=115, x= 0.4, b= 2.8, length= -70)
    grid.add_line(loc=(0,5),voltage=115, x= 0.4, b= 2.8, length= 35)
    grid.add_line(loc=(4,0),voltage=115, x= 0.4, b= 2.8, length= 35)
    print('L-3中点短路的矩阵：\n',grid.admittance_matrix)