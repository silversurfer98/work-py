from openpyxl import load_workbook
filename=['Check list_HAIFA_H10-GD-B-86101.xlsx',
'Check list_HAIFA_H10-GD-B-86102.xlsx',
'Check list_HAIFA_H10-GD-B-86103.xlsx',
'Check list_HAIFA_H10-GD-B-86104.xlsx',
'Check list_HAIFA_H10-GD-B-86105.xlsx',
'Check list_HAIFA_H10-GD-B-86106.xlsx',
'Check list_HAIFA_H10-GD-B-86107.xlsx',
'Check list_HAIFA_H10-GD-B-86108.xlsx',
'Check list_HAIFA_H10-GD-B-86109.xlsx',
'Check list_HAIFA_H10-GD-B-86110.xlsx',
'Check list_HAIFA_H10-GD-B-86111.xlsx',
'Check list_HAIFA_H10-GD-B-86112.xlsx',
'Check list_HAIFA_H10-GD-B-86113.xlsx',
'Check list_HAIFA_H10-GD-B-86114.xlsx',
'Check list_HAIFA_H10-GD-B-86115.xlsx',
'Check list_HAIFA_H10-GD-B-86116.xlsx',
'Check list_HAIFA_H10-GD-B-86117.xlsx',
'Check list_HAIFA_H10-GD-B-86118.xlsx',
'Check list_HAIFA_H10-GD-B-86119.xlsx',
'Check list_HAIFA_H10-GD-B-86120.xlsx',
'Check list_HAIFA_H10-GD-B-86122.xlsx',
'Check list_HAIFA_H10-GD-B-86123.xlsx',
'Check list_HAIFA_H10-GD-B-86125.xlsx',
'Check list_HAIFA_H10-GD-B-86126.xlsx',
'Check list_HAIFA_H10-GD-B-86127.xlsx',
'Check list_HAIFA_H10-GD-B-86128.xlsx',
'Check list_HAIFA_H10-GD-B-86129.xlsx',
'Check list_HAIFA_H10-GD-B-86130.xlsx',
'Check list_HAIFA_H10-GD-B-86131.xlsx',
'Check list_HAIFA_H10-GD-B-86132.xlsx',
'Check list_HAIFA_H10-GD-B-86133.xlsx',
'Check list_HAIFA_H10-GD-B-86134.xlsx',
'Check list_HAIFA_H10-GD-B-86135.xlsx',
'Check list_HAIFA_H10-GD-B-86136.xlsx',
'Check list_HAIFA_H10-GD-B-86137.xlsx',
'Check list_HAIFA_H10-GD-B-86138.xlsx',
'Check list_HAIFA_H10-GD-B-86139.xlsx',
'Check list_HAIFA_H10-GD-B-86140.xlsx',
'Check list_HAIFA_H10-GD-B-86141.xlsx',
'Check list_HAIFA_H10-GD-B-86142.xlsx',
'Check list_HAIFA_H10-GD-B-86143.xlsx',
'Check list_HAIFA_H10-GD-B-86144.xlsx',
'Check list_HAIFA_H10-GD-B-86145.xlsx',
'Check list_HAIFA_H10-GD-B-86146.xlsx',
'Check list_HAIFA_H10-GD-B-86147.xlsx',
'Check list_HAIFA_H10-GD-B-86148.xlsx',
'Check list_HAIFA_H10-GD-B-86149.xlsx',
'Check list_HAIFA_H10-GD-B-86150.xlsx',
'Check list_HAIFA_H10-GD-B-86151.xlsx',
'Check list_HAIFA_H10-GD-B-86152.xlsx',
'Check list_HAIFA_H10-GD-B-86153.xlsx',
'Check list_HAIFA_H10-GD-B-86154.xlsx',
'Check list_HAIFA_H10-GD-B-86155.xlsx',
'Check list_HAIFA_H10-GD-B-86156.xlsx',
'Check list_HAIFA_H10-GD-B-86157.xlsx',
'Check list_HAIFA_H10-GD-B-86158.xlsx',
'Check list_HAIFA_H10-GD-B-86160.xlsx',
'Check list_HAIFA_H10-GD-B-86161.xlsx',
'Check list_HAIFA_H10-GD-B-86121_01.xlsx',
'Check list_HAIFA_H10-GD-B-86121_02.xlsx',
'Check list_HAIFA_H10-GD-B-86124_01.xlsx',
'Check list_HAIFA_H10-GD-B-86124_02.xlsx',
'Check list_HAIFA_H10-GD-B-86159_01.xlsx',
'Check list_HAIFA_H10-GD-B-86159_02.xlsx']

sheetname = ['PR-06-001_1',
'PR-06-001_2',
'PR-06-001_3',
'PR-06-001_4',
'PR-06-001_5',
'PR-06-001_6',
'PR-06-001_7',
'PR-06-001_8',
'PR-06-001_9'
]

i=0

for x in filename:
    print("----------------------------------")
    print(i+1,". ",x)
    rootch = int(input("polama : "))
    if(rootch==1):
        #load excel file
        workbook = load_workbook(filename=x)

        #sheet 1 changes
        sheet1 = workbook[sheetname[0]]
        rev = input("enter rev : ")
        sheet1["G5"]= "Rev. " + rev
        sheet1["E29"]= "PR ROSHAN"
        sheet1["A28"]= "Signature: PRR"
        date = input("enter date : ")
        sheet1["G28"]= "Date: " + date

        if(sheet1["G21"].value!="N/A"):
            sheet1["G21"]="X"
            sheet1["H21"]=""
        if(sheet1["G25"]=="N/A"):
            haz = int(input("is hazop true : "))
            if(haz==1):
                sheet1["G25"]="X"

        #sheet 2 changes
        sheet2 = workbook[sheetname[1]]
        sheet2["G11"]="X"

        #sheet 3 changes
        sheet3 = workbook[sheetname[2]]
        flowch = int(input("is there a FI here ? : "))
        if(flowch == 1):
            sheet3["G22"]="X"
            sheet3["H22"]=""

        #sheet 4 changes
        sheet4 = workbook[sheetname[3]]
        if(sheet4["G10"].value=="X"):
            cvbp = int(input("is cv bypass on hold : "))
            if(cvbp==1):
                sheet4["G11"]="N/A"
            else:
                sheet4["G11"]="X"
        else:
            cv_p=int(input("is cv present : "))
            if(cv_p==1):
                sheet4["G10"]="X"
                cvbp = int(input("is cv bypass on hold : "))
                if(cvbp==1):
                    sheet4["G11"]="N/A"
                else:
                    sheet4["G11"]="X"
        
        #sheet 5 changes
        sheet5 = workbook[sheetname[4]]
        if(sheet5["G8"].value =="C"):
            vess_hold=int(input("is vess on hold : "))
            if(vess_hold==1):
                sheet5["H8"]="Further consistency check to be done in IFC"
            else:
                sheet5["G8"]="X"
                vess = int(input("do vessel have tie pt :"))
                if(vess==1):
                    sheet5["H8"]="Tiein point information provided and further consistency to be done in IFC"
                else:
                    sheet5["H8"]=""

        if(sheet5["G22"].value =="C"):
            tank_hold=int(input("is tank on hold : "))
            if(tank_hold==1):
                sheet5["H8"]="Further consistency check to be done in IFC"
            else:
                sheet5["G22"]="X"
                tank = int(input("do tank have tie pt :"))
                if(tank==1):
                    sheet5["H22"]="Tiein point information provided and further consistency to be done in IFC"
                else:
                    sheet5["H22"]=""

        #sheet 6 changes
        sheet6 = workbook[sheetname[5]]
        if(sheet6["G8"].value =="C"):
            hx_hold=int(input("is hx on hold : "))
            if(hx_hold==1):
                sheet6["H8"]="Further consistency check to be done in IFC"
            else:
                sheet6["G8"]="X"
                sheet6["G10"]="X"
                sheet6["H10"]=""
                hx = int(input("do hx have tie pt :"))
                if(hx==1):
                    sheet6["H8"]="Tiein point information provided and further consistency to be done in IFC"
                else:
                    sheet6["H8"]=""

        #sheet 7 changes
        sheet7 = workbook[sheetname[6]]
        if(sheet7["G8"].value =="C"):
            pp_hold=int(input("is pump on hold : "))
            if(hx_hold==1):
                sheet7["H8"]="Further consistency check to be done in IFC"
            else:
                sheet7["G8"]="X"
                sheet7["G12"]="X"
                sheet7["H12"]=""
                sheet7["G14"]="X"
                sheet7["H14"]=""
                pp = int(input("do pump have tie pt :"))
                if(pp==1):
                    sheet7["H8"]="Tiein point information provided and further consistency to be done in IFC"
                else:
                    sheet7["H8"]=""

        #sheet 8 changes
        sheet8 = workbook[sheetname[7]]
        if(sheet8["G8"].value =="C"):
            pp_hold=int(input("is FH on hold : "))
            if(hx_hold==1):
                sheet8["H8"]="Further consistency check to be done in IFC"
            else:
                sheet8["G8"]="X"
                sheet8["G9"]="X"
                sheet8["G10"]="X"
                sheet8["G11"]="X"
                sheet8["G12"]="X"
                sheet8["G13"]="X"
                sheet8["G14"]="X"
                sheet8["H9"]=""
                sheet8["H10"]=""
                sheet8["H11"]=""
                sheet8["H12"]=""
                sheet8["H13"]=""
                sheet8["H14"]=""
                fh = int(input("do fire heater have tie pt :"))
                if(fh==1):
                    sheet8["H8"]="Tiein point information provided and further consistency to be done in IFC"
                else:
                    sheet8["H8"]=""

        #sheet 9 changes
        sheet9 = workbook[sheetname[8]]
        if(sheet9["G8"].value =="C"):
            sheet9["G8"]="X"
            sheet9["H8"]=""
            sheet9["G13"]="X"

        #save the file
        workbook.save(filename=x)
        i=i+1

    else:
        print("skipping this file --> ",x)
        i=i+1
        continue