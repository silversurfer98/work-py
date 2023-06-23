import numpy as np

# constants for T_sat calculation
c1 = 73.649	
c2 = -7258.2
c3 = -7.3037
c4 = 4.17E-06
c5 = 2

# set ur tolerance factor --> lower the number higher the loop count
tolerance = 1e-08

print("\n______This is a progarm to calc saturation temperature of steam at given pressure above 100 Deg Cel _____\n")
print("tolerance factor for newton raphson is set at %2.8f \n\n" %(tolerance))

#get data
def get_data():
    print("------------------ INPUT -----------------------------")
    global mop
    mop = float(input("enter the maximum operating pressure in barG: "))
    print("------------------------------------------------------\n")

# ---------- NEWTON RAPHSON -------------------------
def func(t,p):
    ans = p - np.exp(c1 + c2/t + c3*np.log(t) + c4*np.power(t,c5))
    return ans

def dev_func(t):
    dev_ans = (-np.exp(c1 + c2/t + c3*np.log(t) + c4*np.power(t,c5))) * (-c2/(t*t) + c3/t + c4*c5*t)
    return dev_ans
# ----------------------------------------------------

# driver code for above --> prints T Design in multiples of 5
def find_satT(p_from_user):
    #p_from_user = 3.5 #bar G
    p = (1.0 + p_from_user) * 100000

    t0 = 350.15
    t_new = 0.0

    # i=0
    error = 0.1
    while error>=tolerance:
    #for i in range(0,1000):
        t_new = t0 - func(t0,p)/dev_func(t0)
        # print(i," --> ",t_new)
        error = abs(t_new - t0)
        t0 = t_new
        # i=i+1
    print("----------------------------------------------------------------")
    print("Saturated temperature of steam at %5.2f Bar G is %5.3f Deg C" %(p_from_user, t0 - 273.15 - 0.01694563))
    print("________________________________________________________________")



def driver():
    get_data()
    find_satT(mop)
    
driver()
print("    ")
ch = int(input("Enter 1 for positive\nEnter any to quit\nDo u wanna run calc again : "))
print("\n\n")
while(ch==1):
    driver()
    ch = int(input("Do u wanna calc again : "))

print("\n *************** BYE !! ************** \n")