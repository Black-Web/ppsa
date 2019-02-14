# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import numpy as np
import ppsa as psa

Sb = 31.5
f = 3    #短路点
Xt1 = psa.impedance_of_transformer(0.105,Sb,31.5)
Xg1 = psa.impedance_of_generator(0.1138,Sb,25/0.8)
Xl1_2=psa.impedance_of_line(100,0.4,115,Sb)
Xl1_1=Xl1_2
Xl1_0=3*Xl1_2
Xl2_2=psa.impedance_of_line(50,0.4,115,Sb)
Xl2_1=Xl2_2
Xl2_0=3*Xl2_1
Xt2_1,Xt2_2,Xt2_3 = 0.1075,0.0625,0

gd4_1 = psa.power_grid(5,Sb)
gd4_2 = psa.power_grid(5,Sb)
gd4_0 = psa.power_grid(3,Sb)
# 正序网络
gd4_1.add_load((1,0),800,0.6j,ref_vol=1j)
gd4_1.add_line((1,3),115,0.4,100)
gd4_1.add_line((1,2),115,0.4,30)
gd4_1.add_line((2,3),115,0.4,60)
gd4_1.add_transformer((3,4),31.5,0.105)
gd4_1.add_transformer((3,5),31.5,Xt2_1)
gd4_1.add_generator((4,0),25/0.8,0.1138j,ref_vol=1j)
gd4_1.add_generator((5,0),25/0.8,0.1138j,ref_vol=1j)
# 负序网络
gd4_2.add_load((1,0),800,0.6j)
gd4_2.add_line((1,3),115,0.4,100)
gd4_2.add_line((1,2),115,0.4,30)
gd4_2.add_line((2,3),115,0.4,60)
gd4_2.add_transformer((3,4),31.5,0.105)
gd4_2.add_transformer((3,5),31.5,Xt2_1)
gd4_2.add_generator((4,0),25/0.8,0.1138j)
gd4_2.add_generator((5,0),25/0.8,0.1138j)
# 零序网络
gd4_0.add_load((1,0),800,0.6j)
gd4_0.add_line((1,3),115,0.4,100)
gd4_0.add_line((1,2),115,0.4*3,30)
gd4_0.add_line((2,3),115,0.4*3,60)
gd4_0.add_transformer((2,0),20,0.105)
gd4_0.add_transformer((3,0),31.5,Xt2_1)

a = np.e**(np.pi*2/3)
def part2total(a1,a2,a0):
    a = np.e**(np.pi*2/3)
    abc = np.dot([[1 ,1, 1],
                 [a**2,a,1],
                 [a,a**2,1]],[a1,a2,a0])
    return abc

Ub =115
Ib = 31.5/(np.sqrt(3)*Ub)

Z1 = gd4_1.Z;Z2 = gd4_2.Z;Z0 = gd4_0.Z    #各序阻抗矩阵
U = gd4_1.nodes_voltage()
Ifa1 = U[f-1]/(Z1[f-1,f-1]+Z2[f-1,f-1]+Z0[f-1,f-1])    #a相正序电流
Ifa = 3*Ifa1    #a相电流总合
Ufa1= U[f-1] - Z1[f-1,f-1]*Ifa1    #短路后3结点正序电压
Ufa2= -Z2[f-1,f-1]*Ifa1
Ufa0= -Z0[f-1,f-1]*Ifa1
print('f1短路后a相正、负、零序电流：',Ifa1*Ib,'\n','正、负、零序电压：',Ufa1*Ub,'\t',Ufa2*Ub,'\t',Ufa0*Ub)
Il1_2 = (Ufa2-0)/Xl1_2    #流过L1的负序电流
Il1_0 = (Ufa0-0)/Xl1_0
Il1_1 = (Ufa1-U[0])/Xl1_1
Il_abc=part2total(Il1_1,Il1_2,Il1_0)
print('流过L1的负序电流:',Il1_2*Ib,'零序电流:',Il1_0*Ib)
print('流过L1的各相电流:',Il_abc*Ib)
print('------------------------------')
It1_1 = (Ufa1-1j)/(Xt1*1j+Xg1*1j)
It1_2 = Ufa2/(Xt1*1j+Xg1*1j)
It1 = It1_1+It1_2
U4 = Ufa1+Ufa2-It1_1*Xt1*1j-It1_2*Xt1*1j
print('变压器T1三角侧的短路电流:',It1*Ib)
print('变压器T1三角侧的短路电压:',U4*10.5)
print('------------------------------')

Zeq_1 = Z1[f-1,f-1]+1j*Xl2_1
Zeq_2 = Z2[f-1,f-1]+1j*Xl2_2
Zeq_0 = Z0[f-1,f-1]+1j*Xl2_0
Z_delta = Zeq_0*Zeq_2/(Zeq_0+Zeq_2)
Il2_1 = U[f-1]/(Z_delta+Zeq_1)
Il2_2 = -Il2_1*Zeq_0/(Zeq_0+Zeq_2)
Il2_0 = -Il2_1*Zeq_2/(Zeq_0+Zeq_2)
Uf_1 = Z_delta*Il2_1
Ufa = 3*Uf_1
Il1_0= Uf_1/1j/Xl1_0
print('L2零序电流：',Il2_0,'L1零序电流：',Il1_0)
print('L2末端电压：',Ufa)