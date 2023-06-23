import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d as ip

df = pd.read_csv("curve_data.csv")
eff_graph = np.array(df['eff'])
rp_graph = np.array(df['rp'])
# plt.plot(rp_graph,eff_graph)
rp_limits = np.array([np.min(rp_graph), np.max(rp_graph)])
eff_limits = np.array([np.min(eff_graph), np.max(eff_graph)])

fs = ip(rp_graph, eff_graph, kind='cubic')
rp_test = np.linspace(rp_limits[0], rp_limits[1], 100)
# plt.plot(rp_graph,eff_graph,'r-')
# plt.plot(rp_test, fs(rp_test), 'b:')

ey = fs(rp_graph)
print("\n\nMean squared Error between the data and interpolation is ", ((np.square(eff_graph - ey)).mean(axis=0)))
print("\n\n")

MW = 2 #g/mol
Psuc = 21.21 #KscG
Pdis = 32.93 #KscG
PLOSS = 1 #%

MW = float(input("Enter the molecular weight in g/mol : "))
Psuc = float(input("Enter the suction pressure in KscG : "))
Pdis = float(input("Enter the discharge pressure in KscG : "))
PLOSS = float(input("Enter the PLoss in percent (Normally its 1%) : "))

Psuc = Psuc + 1.0332
Pdis = Pdis + 1.0332

stage_no = np.linspace(1,10,10)
Ploss = np.zeros(10)
rp = np.zeros(10)

Ploss = ((100-PLOSS)/100)** (stage_no-1)
rp = (Pdis/(Psuc*Ploss))** (1/stage_no)
# print(rp)

stage_no = stage_no[(rp>=rp_limits[0])*(rp<=rp_limits[1])]
rp = rp[(rp>=rp_limits[0])*(rp<=rp_limits[1])]
delW = np.zeros(rp.size)
eff = fs(rp)
if(MW<4):
    delW = (100*((100/eff)-1))+4
else:
    delW = (100*((100/eff)-1))+1

print("viable options : \n")
print("Stages\trp\teff\tDelW\n")
for i,j,k,l in zip(stage_no, rp, eff, delW):
    print("%d\t%.2f\t%.2f\t%.2f" %(i, j, k, l))