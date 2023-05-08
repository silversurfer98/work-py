import os
import subprocess
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import shutil

def create_input(ss, ts, k, calcno):
    dataframe = pd.read_excel("input_from_gips.xlsx")
    dataframe['C'][0]

    with open('input_skeleton.txt') as inp_skel:
        all_lines = inp_skel.readlines()

    inp = open("input.txt","w")

    print(all_lines[0], end = "",flush =True,file=inp)
    print(all_lines[1], end = "",flush =True,file=inp)
    print(all_lines[2], end = "",flush =True,file=inp)
    print(int(calcno), end = "\n",flush =True,file=inp)
    print(all_lines[3], end = "",flush =True,file=inp)
    print(dataframe['C'][1]/1000," ",dataframe['C'][2]/1000,file=inp)
    print(all_lines[4], end = "",flush =True,file=inp)
    print(dataframe['C'][3],file=inp)

    print(all_lines[5], end = "",flush =True,file=inp)
    print("20", end = "\n",flush =True,file=inp)
    print(all_lines[6], end = "",flush =True,file=inp)
    print("5", end = "\n",flush =True,file=inp)

    print(all_lines[7], end = "",flush =True,file=inp)
    print(int(dataframe['C'][4]),file=inp)

    print(all_lines[8], end = "",flush =True,file=inp)
    print(dataframe['C'][5],file=inp)

    print(all_lines[9], end = "",flush =True,file=inp)
    print(dataframe['C'][6]," ",dataframe['C'][7],file=inp)

    print(all_lines[10], end = "",flush =True,file=inp)
    print(dataframe['C'][8]," ",dataframe['C'][9],file=inp)

    print(all_lines[11], end = "",flush =True,file=inp)
    print(dataframe['C'][10]," ",dataframe['C'][11],file=inp)

    print(all_lines[12], end = "",flush =True,file=inp)
    print(dataframe['C'][12]," ",dataframe['C'][13],file=inp)

    print(all_lines[13], end = "",flush =True,file=inp)
    print(dataframe['C'][14],file=inp)

    print(all_lines[14], end = "",flush =True,file=inp)
    print(dataframe['C'][15],file=inp)

    print(all_lines[15], end = "",flush =True,file=inp)
    print(dataframe['C'][16],file=inp)

    print(all_lines[16], end = "",flush =True,file=inp)
    print(dataframe['C'][17],file=inp)

    print(all_lines[17], end = "",flush =True,file=inp)
    print(k, end = "\n",flush =True,file=inp)

    print(all_lines[18], end = "",flush =True,file=inp)
    print(ss, end = "\n",flush =True,file=inp)
    print(all_lines[19], end = "",flush =True,file=inp)
    print(ts, end = "\n",flush =True,file=inp)

    print(all_lines[20], end = "",flush =True,file=inp)
    print(all_lines[21], end = "",flush =True,file=inp)
    print(all_lines[22], end = "",flush =True,file=inp)
    print(all_lines[23], end = "",flush =True,file=inp)
    print(all_lines[24], end = "",flush =True,file=inp)

    inp.close()


'''
the code below will execute and produce output txt
'''
def execute(command, fileno):
    popen = subprocess.Popen(command, stdout=subprocess.PIPE)
    lines_iterator = iter(popen.stdout.readline, b"")
    filename_out = "output" + str(fileno) + ".txt"
    file1 = open(filename_out,"w")
    while popen.poll() is None:
        for line in lines_iterator:
            nline = line.rstrip()
            print(nline.decode("latin"), end = "\r\n",flush =True, file=file1) # yield line
    file1.close()



def create_data(fileno, ss, ts, max_t):
    filename_tem = "TEMPERATUREPROFILE" + str(fileno) + ".txt"
    shutil.copy("TEMPERATUREPROFILE.txt", filename_tem)
    with open(filename_tem) as f:
        lines = f.readlines()

    data = np.array(lines[2:])
    h = np.vectorize(lambda s: s.strip())(data)

    l=[]
    t=[]
    for i in h:
        j = i.split('        ')
        l.append(float(j[0]))
        t.append(float(j[1]))

    len = np.array(l, dtype=float)
    temp = np.array(t, dtype=float)

    coat_len = 0.0
    count = -1
    for i in temp:
        if i>=max_t:
            count = count + 1
    count = count + 1
    if count>0:
        coat_len = len[count]
        print("we need coating upto %2.2f for shell side fouling: %1.7f and tube side fouling: %1.7f" %(len[count],ss,ts))
    else:
        print("we dont need any coating for shell side fouling: %1.7f and tube side fouling: %1.7f" %(ss,ts)) 

    return len, temp, coat_len


def plot_data(len, temp, ss, ts, max_t, coat_len):
    plt.plot(len, temp)
    label = "Temperature profile graph at shell side fouling: " + str(ss) + " and tube side fouling: " + str(ts)
    plt.title(label)
    plt.xlabel("Tube length -> m")
    plt.ylabel("Temperature -> Deg C")
    plt.axhline(y=max_t, color="red", linestyle="-")
    plt.axvline(x=coat_len, color="green", linestyle=":")
    plt.show()

def main():
    print("**************** This program is to make my life easier ************")
    print("copy and paste gexexport to that excel file save and close it before doing anything")


    ss=0.0005
    ts=0.0001
    k=31.0
    calcno=1234567
    c = "whb.exe"

    ss = float(input("Enter the shell side fouling factor : "))
    ts = float(input("Enter the tube side fouling factor : "))
    k = float(input("Enter tube k conductivity : "))
    max_t = float(input("Enter enter max tube wall temperature : "))

    create_input(0, 0, k, calcno)
    execute(c,1)
    len, temp, coat_len = create_data(1,0,0,max_t)
    plot_data(len, temp,0,0,max_t, coat_len)

    create_input(0, ts, k, calcno)
    execute(c,2)
    len, temp, coat_len = create_data(2,0,ts,max_t)
    plot_data(len, temp,0,ts,max_t, coat_len)

    create_input(ss, 0, k, calcno)
    execute(c,3)
    len, temp, coat_len = create_data(3,ss,0,max_t)
    plot_data(len, temp,ss,0,max_t, coat_len)

    create_input(ss, ts, k, calcno)
    execute(c,4)
    len, temp, coat_len = create_data(4,ss,ts,max_t)
    plot_data(len, temp,ss,ts,max_t, coat_len)

if __name__ == "__main__":
    main()