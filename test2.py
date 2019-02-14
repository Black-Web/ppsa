# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import numpy as np
import ppsa as psa

def impedance_of_line(length, x, voltage, Sb):
    return length * x/(voltage**2 / Sb)
def impedance_of_transformer(Vs, Sb, Sn):
    return Vs * Sb / Sn
def impedance_of_generator(Xd, Sb, Sn):
    return Xd * Sb/Sn
impedance_of_load = impedance_of_generator

grid2 = psa.power_grid(node_num= 4, Sb= 60)
grid2.add_generator((1,0), Sn=60, Xd_2=0.15j, ref_vol = 1.05)
grid2.add_generator((4,0), Sn=150, Xd_2=0.2j, ref_vol = 1.05)
grid2.add_transformer((1,2), Sn=60, Vs=0.12)
grid2.add_transformer((3,4), Sn=90, Vs=0.12)
grid2.add_line((2,3), voltage=115, x=0.4, length=80)
grid2.add_line((2,3), voltage=115, x=0.4, length=80)
grid2.add_load(loc=(3,0), Sn= 120, Xld_2= 0.35j, ref_vol = 0.8)

X_g1 =impedance_of_generator(Sn=60, Xd=0.15, Sb =grid2.Sb)
X_g2 =impedance_of_generator(Sn=150, Xd=0.2, Sb =grid2.Sb)
X_l = 0.5 * impedance_of_line(Sb=grid2.Sb,voltage=115, x=0.4, length=80)
X_ld = impedance_of_load(Sn= 120, Xd= 0.35,Sb=grid2.Sb)
X_t1 = impedance_of_transformer(Sb=grid2.Sb,Sn=60, Vs=0.12)
X_t2 = impedance_of_transformer(Sb=grid2.Sb,Sn=90, Vs=0.12)

def short_circuit1(self,f,loc,Ii,zf=0):
    Z = self.impedance_matrix()
    E=np.zeros((self.node_num,len(loc)),dtype=np.complex128)
    loc = np.array(loc) - 1
    E[loc,range(len(loc))]=Ii
    Ue = Z.dot(E)
    I = Ue[f-1]/(Z[f-1,f-1]+zf)
    return I
if __name__ == '__main__':
    Ib = (grid2.Sb/np.sqrt(3)/115)
    print('短路前各结点电压：',grid2.nodes_voltage(),\
        '\n--------------------------------------\n')
    print('3结点短路:')
    Uf = grid2.short_circuit(3)[0]
    I = short_circuit1(grid2,3,(1,4,3),(1.05/X_g1,1.05/X_g2,0.8/X_ld))
    kim = np.array((1.8,1.85,1.0))
    Is = sum(I*kim)
    Iim = sum(np.sqrt(1+2*(kim-1)**2)*I)
    print('短路后各结点电压：',Uf)
    print('次暂态电流标幺值:',sum(I),'有名值:',sum(I)*Ib,'kA')
    print('冲击电流标幺值：',Is,'有名值：',np.sqrt(2)*Is*Ib,'kA')
    print('短路功率标幺值：',Iim,'有名值：',Iim*60,'MVA')
    print('--------------------------------------')
    print('2结点短路:')
    Uf = grid2.short_circuit(2)[0]
    I = short_circuit1(grid2,2,(1,4,3),(1.05/X_g1,1.05/X_g2,0.8/X_ld))
    kim = np.array((1.8,1.8,1.0))
    Is = sum(I*kim)
    Iim = sum(np.sqrt(1+2*(kim-1)**2)*I)
    print('短路后各结点电压：',Uf)
    print('次暂态电流标幺值:',sum(I),'有名值:',sum(I)*Ib,'kA')
    print('冲击电流标幺值：',Is,'有名值：',np.sqrt(2)*Is*Ib,'kA')
    print('短路功率标幺值：',Iim,'有名值：',Iim*60,'MVA')