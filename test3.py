# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Sat Dec  9 19:53:52 2017

@author: Dawn
"""
import numpy as np
import ppsa as psa

grid3 = psa.power_grid(5)
grid3.add_generator((1,0),100,0.15j)
grid3.add_generator((5,0),100,0.22j)
grid3.add_device((2,4),0.08j)
grid3.add_device((2,3),0.065j)
grid3.add_device((3,4),0.05j)
grid3.add_device((1,2),0.105j)
grid3.add_device((4,5),0.184j)

def current_distribution(admat,U):
    U= np.array(U)
    U= U.reshape((-1,1))-U.reshape((1,-1))
    I = -U * admat
    return I
print('导纳矩阵：\n',grid3.admat)
#print('阻抗矩阵：\n',grid3.impedance_matrix())
Uf,If= grid3.short_circuit(3)
print('3结点短路后各结点电压：\n',Uf)
print('短路电流：\n',If)
print('电流分布：\n',current_distribution(grid3.admat,Uf))