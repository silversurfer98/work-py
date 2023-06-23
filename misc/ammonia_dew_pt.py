import numpy as np

# constants for T_sat calculation
c1 = 90.483
c2 = -4669.7
c3 = -11.607
c4 = 1.72E-02
c5 = 1


# set ur tolerance factor --> lower the number higher the loop count
tolerance = 1e-08

print("\n______This is a progarm to calc saturation temperature of ammonia at given pressure above -33 Deg Cel _____\n")
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

    t0 = 235.15
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
    print("Saturated temperature of ammonia at %5.2f Bar G is %5.3f C +- 0.159 (%5.3f    %5.3f)" %(p_from_user, t0 - 273.15, t0 - 273.15 + 0.158723209270989, t0 - 273.15 - 0.158723209270989))
    print("________________________________________________________________")
    # return t0 - 273.15

def test():
    pressure = [-0.61,-0.59,-0.58,-0.57,-0.55,-0.53,-0.52,-0.5,-0.49,-0.47,-0.46,-0.43,-0.42,-0.4,-0.38,-0.37,
    -0.34,-0.32,-0.3,-0.28,-0.26,-0.24,-0.21,-0.19,-0.17,-0.15,-0.12,-0.1,-0.07,-0.04,-0.01,0.01,0.04,
    0.0800000000000001,0.1,0.13,0.17,0.19,0.23,0.26,0.3,0.33,0.37,0.4,0.44,0.48,0.52,0.56,0.6,0.63,
    0.68,0.72,0.77,0.81,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25,1.31,1.36,1.42,1.48,1.54,1.59,1.65,1.72,1.78,
    1.84,1.91,1.97,2.04,2.11,2.18,2.25,2.32,2.4,2.47,2.55,2.63,2.7,2.79,2.87,2.95,3.03,3.12,4.05,5.15,6.42,
    7.88,8.86,9,9.2,9.4,9.5,9.7,9.9,10.1,10.3,10.5,10.7,10.9,11.1,11.3,11.5,11.7,11.9,12.1,12.3,12.5,12.7,
    12.9,13.2,13.4,13.6,13.8,14.1,14.3,14.5,14.8,15,15.3,15.5,15.8,16,16.3,16.5,16.8,17.1,17.4,17.6,17.9,
    18.2,18.5,18.7,23.2,37.7,57.8,85,102,112]

    i = 0
    # t=[]
    for p in pressure:
        # t[i] = find_satT(p)
        # i = i+1
        # print(t[i])
        print(find_satT(p))
        i = i+1


def driver():
    get_data()
    find_satT(mop)

# test()   
driver()
print("    ")
ch = int(input("Enter 1 for positive\nEnter any to quit\nDo u wanna run calc again : "))
print("\n\n")
while(ch==1):
    driver()
    ch = int(input("Do u wanna calc again : "))

print("\n *************** BYE !! ************** \n")

