import subprocess
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import shutil

class whb:
    def __init__(self,ss,ts,k,temp,*args):
        self.ss = ss
        self.ts = ts
        self.k = k
        self.max_t = temp

        self.input_excel= "input_from_gips.xlsx"
        self.input_skel = "input_skeleton.txt"
        self.calcno = 123456
        self.command = "whb.exe"

        self.fouling = [[0,0],[0,self.ts],[self.ss,0],[self.ss,self.ts]]
        self.fileno = [1,2,3,4]

        self.inp = "input.txt"
        
        if len(args)>1:
            if args[0] != "input_from_gips.xlsx":
                self.input_excel = args[0]
            if args[1] != "input_skeleton.txt":
                self.input_skel = args[1]
            if args[2] != "whb.exe":
                self.command = args[2]


    def create_input(self, fouling):
        dataframe = pd.read_excel(self.input_excel)
        dataframe['C'][0]

        with open(self.input_skel) as inp_skel:
            all_lines = inp_skel.readlines()

        inp = open("input.txt","w")

        print(all_lines[0], end = "",flush =True,file=inp)
        print(all_lines[1], end = "",flush =True,file=inp)
        print(all_lines[2], end = "",flush =True,file=inp)
        print(int(self.calcno), end = "\n",flush =True,file=inp)
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
        print(self.k, end = "\n",flush =True,file=inp)

        print(all_lines[18], end = "",flush =True,file=inp)
        print(fouling[0], end = "\n",flush =True,file=inp) # ss
        print(all_lines[19], end = "",flush =True,file=inp)
        print(fouling[1], end = "\n",flush =True,file=inp) # ts

        print(all_lines[20], end = "",flush =True,file=inp)
        print(all_lines[21], end = "",flush =True,file=inp)
        print(all_lines[22], end = "",flush =True,file=inp)
        print(all_lines[23], end = "",flush =True,file=inp)
        print(all_lines[24], end = "",flush =True,file=inp)

        inp.close()


    ''' the code below will execute and produce output txt '''
    def execute(self, fileno):
        popen = subprocess.Popen(self.command, stdout=subprocess.PIPE)
        lines_iterator = iter(popen.stdout.readline, b"")
        filename_out = "output" + str(fileno) + ".txt"
        file1 = open(filename_out,"w")
        while popen.poll() is None:
            for line in lines_iterator:
                nline = line.rstrip()
                print(nline.decode("latin"), end = "\r\n",flush =True, file=file1) # yield line
        file1.close()


    def create_data(self, fileno, fouling):
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
            if i>=self.max_t:
                count = count + 1
        count = count + 1
        if count>0:
            coat_len = len[count]
            print("we need cladding upto %2.2f for shell side fouling: %1.7f and tube side fouling: %1.7f \n" %(len[count],fouling[0], fouling[1]))
        else:
            print("we dont need any coating for shell side fouling: %1.7f and tube side fouling: %1.7f \n" %(fouling[0], fouling[1])) 

        return len, temp, coat_len
    

    def plot_data(self, len, temp, fouling, coat_len):
        plt.plot(len, temp)
        label = "Temperature profile graph at U-shell = " + str(fouling[0]) + " and U-tube = " + str(fouling[1])
        plt.title(label)
        plt.xlabel("Tube length -> m")
        plt.ylabel("Temperature -> Deg C")
        plt.axhline(y=self.max_t, color="red", linestyle="-")
        plt.axvline(x=coat_len, color="green", linestyle=":")
        plt.show()

    def do_stuff(self):
        for i in self.fileno:
            self.create_input(self.fouling[i-1])
            self.execute(i)
            len, temp, coat_len = self.create_data(i, self.fouling[i-1])
            self.plot_data(len,temp,self.fouling[i-1],coat_len)


def main():
    print("\n\n**************** This program is to make my life easier ************\n")
    print("copy and paste gexexport to that excel file save and close it before doing anything\n\n")

    ''' Testing purposes '''
    # ss=0.0001
    # ts=0.0005
    # k=31.0
    # max_t=400.0

    ss = float(input("Enter the shell side fouling factor : "))
    ts = float(input("Enter the tube side fouling factor : "))
    k = float(input("Enter tube k conductivity : "))
    max_t = float(input("Enter enter max tube wall temperature : "))

    my_whb = whb(ss,ts,k,max_t)
    my_whb.do_stuff()

if __name__ == "__main__":
    main()
