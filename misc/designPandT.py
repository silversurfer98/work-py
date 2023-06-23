import numpy as np

# constants for T_sat calculation
c1 = 73.649	
c2 = -7258.2
c3 = -7.3037
c4 = 4.17E-06
c5 = 2

# set ur tolerance factor --> lower the number higher the loop count
tolerance = 0.0001

print("\n______This is a progarm to calc Design Pressure and temperature _____\n")
print("tolerance factor for newton raphson is set at %2.8f \n\n" %(tolerance))

#get data
def get_data():
    print("------------------ INPUT -----------------------------")
    global mop
    mop = float(input("enter the maximum operating pressure in barG: "))
    global mot
    mot = float(input("enter the maximum operating temperature in Deg C: "))
    print("------------------------------------------------------\n")

def vessel_t_and_p():
    global t_des_normal
    global mdp
    t_des_normal = int(mot) + 30
    if t_des_normal < 70:
        t_des_normal = 70
    if mop < 100.0:
        # as per IN-818-EN
        dp = [3.5,0,0]
        dp[1] = mop + 2.0
        dp[2] = mop/0.9
        mdp = np.ceil(max(dp))

    else:
        # for synloop IN-765-EN
        dp = [0.0,0.0]
        dp[0] = mop + 2.0
        dp[1] = mop/0.9
        mdp = np.ceil(max(dp))
        if mdp<dp[1]:
            print("special care should be taken check for PSV's")

    while t_des_normal%5!=0:
            t_des_normal = t_des_normal + 1

# ---------- NEWTON RAPHSON -------------------------
def func(t,p):
    ans = p - np.exp(c1 + c2/t + c3*np.log(t) + c4*np.power(t,c5))
    return ans

def dev_func(t):
    dev_ans = (-np.exp(c1 + c2/t + c3*np.log(t) + c4*np.power(t,c5))) * (-c2/(t*t) + c3/t + c4*c5*t)
    return dev_ans
# ----------------------------------------------------

# driver code for above --> prints T Design in multiples of 5
def find_satP(p_from_user):
    #p_from_user = 3.5 #bar G
    p = (1 + p_from_user) * 100000

    t0 = 350.0
    t_new = 0.0

    #i=0
    error = 0.1
    while error>=tolerance:
    #for i in range(0,1000):
        t_new = t0 - func(t0,p)/dev_func(t0)
        #print(i," --> ",t_new)
        error = abs(t_new - t0)
        t0 = t_new
        #i=i+1
    print("Saturated temperature of steam at %5.2f Bar G is %5.3f Deg C" %(p_from_user, t0 - 273.15 - 0.01694563))
    t_des = int(t0-273.15)
    while t_des%5!=0:
        t_des = t_des + 1

    global t_des_normal
    t_des_normal = t_des



def loop_pressure():
    # for grey and blue ammonia loops
    circ_suc = int(input("Enter circulator suction pressure : "))
    circ_dis = int(input("Enter circulator discharge pressure : "))
    blue_amm_loop_des_pres = ((circ_dis-circ_suc)*1.1 + (1 + circ_suc))/0.9
    green_amm_des_pres = 1.2 * circ_dis
    print("\n#####################  OUTPUT #########################\n")
    print("the design pressure for blue and grey ammonia layout is %5.2f Bar G" %(blue_amm_loop_des_pres))
    print("the design pressure for green ammonia layout is %5.2f Bar G" %(green_amm_des_pres))
    print("Design temperature for vessel : %5d Deg C" %(t_des_normal))
    print("\n#######################################################\n\n\n")


def print_data():
    print("\n\n#####################  RESULTS #########################\n")
    print("the design pressure is %5.2f Bar G" %(mdp))
    print("Design temperature for vessel : %5d Deg C" %(t_des_normal))
    print("\n#######################################################\n\n\n")

def choice():
    # assign_0()
    print("1. Design temperature and presure calulation for vessels\n")
    print("2. Design temperature and presure calulation for vessels with steam\n")
    print("3. Design temperature and presure for ammonia loop\n")
    ch = int(input(" Yout choice -->  "))
    if ch==1:
        get_data()
        vessel_t_and_p()
        print_data()
    elif ch==2:
        get_data()
        print("\nThe vessel temperature %f Deg.C, doesnot involved in calculation\n" %(mot))
        print("\nThe Design temperature is calculated from saturated temperature of design pressure\n")
        vessel_t_and_p()
        find_satP(mdp)
        print_data()
    elif ch==3:
        get_data()
        vessel_t_and_p()
        loop_pressure()
    else:
        choice()


choice()
ch = int(input("Enter 1 for positive\nEnter any to quit\nDo u wanna run calc again : "))
print("\n\n")
while(ch==1):
    choice()
    ch = int(input("Do u wanna calc again : "))

print("\n *************** BYE !! ************** \n")