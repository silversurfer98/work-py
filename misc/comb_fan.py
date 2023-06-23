def Flue_gas_fan():
    mdr = -5.0 # min pressure / draft at radiant sec 
    pd_at_top_all = [5.0,10.0,15.0]
    pd_crossover = 15.0
    pd_stack_effect = 10.0
    pd_aph_all = [150.0, 150.0, 250.0]
    pd_foul_aph = 30.0
    pd_all_coils = 200.0
    pd_inlet_fluegas = 30.0

    print("****************************************************")
    print("Flue gas fan calc\n")
    # choices
    pd_aph = 0.0
    pd_at_top = 0.0
    pd_flctuations = 0.0

    try:
        print("Choose type of furnace\n1. Single furnace\n2. Duplex furnace\n3. Double duplex furnace")
        type_of_furnace = int(input("what is the type of furnace ? : ")) - 1
        pd_at_top = pd_at_top_all[type_of_furnace]
    except:
        print("enakune varuveengala da")

    try:
        print("Choose type of air pre heaters\n1. Single\n2. Double")
        type_of_aph = int(input("what is the type of aph ? : ")) - 1
        if type_of_aph==1:
            no_of_ref_tubes = int(input("Enter no. of reformer tubes : "))
            if no_of_ref_tubes**2 > 120:
                type_of_aph = type_of_aph + 1
        pd_aph = pd_aph_all[type_of_aph]
    except:
        print("enakune varuveengala da")

    ste = str(input("Is flue gas flowing from top to bottom - downflow (y/n):"))
    if ste=='y':
        pd_stack_effect = pd_stack_effect * -1.0

    ch = str(input("Is major part of reformer fuel is PSA off gas (y/n): "))
    if ch=='y':
        pd_flctuations = 10.0
    else:
        print("ok")

    p = mdr - (pd_aph + pd_at_top + pd_crossover + pd_foul_aph + pd_all_coils + pd_inlet_fluegas) - pd_flctuations


    print("\n pressure increse should be : ",p, "\n\n")

    print("****************************************************")


def CA_blower():
    # air blower settings
    print("****************************************************")
    print("CA blower calc\n")
    air_filter = 20
    flow_element = 10

    duct_steamAPH = 60
    SteamAPH = 25

    DuctAPH = 30
    APH = 100

    Duct_burners = 100
    Dampers = 20
    Burners = 200

    no_SAPH = int(input("No. of SAPH : "))
    no_APH = int(input("No. of APH : "))

    p = air_filter + flow_element + no_SAPH*(duct_steamAPH + SteamAPH) + no_APH*(DuctAPH + APH) + Duct_burners + Dampers + Burners

    print("Pressure needed : ", p)
    print("\n****************************************************")



print("****************************************************")
print("What do u wanna calc \n1. CA blower\n2. Flue gas fan")
ch = int(input("choice ? : "))
if ch==1:
    CA_blower()
elif ch==2:
    Flue_gas_fan()
else:
    print("en")

'''
### Flue gas fan

Minimum draft in top of radiant section (Pradiant top) 5 
Pressure drop from reformer top to pressure transmitter (ΔPmix, top)  
- Single furnace 5 
- Duplex furnace 10 
- Double duplex furnace 15 
Pressure drop in cross-over (ΔPcross-over) 15 
Negative stack effect1 of WHS duct 10 
                                                
1 The stack effect is caused by the density difference between ambient air and flue gas. The effect is negative when 
flow is downflow and positive when flow is upward. 

Air preheat coil 
- Single 150 
- Double 2x75 if Ntub (2) < 120, else 2x125 
Fouling on air preheaters 30 
Remaining coils (total, including fouling)3 200 
Pressure drop around blower (ΔPfan, inlet) 30 

2 Number of reformer tubes 

P = Pradiant top – ΔPmix, top - ΔPfluctuations 

ΔPfluctuations count for the fluctuations primarily caused by fluctuations in PSA off-gas. Values for 
ΔPfluctuations (mmWG):
Major part of fuel is PSA off-gas = 10 
Else = 0 
'''