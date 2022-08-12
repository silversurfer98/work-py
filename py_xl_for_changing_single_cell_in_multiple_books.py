from openpyxl import load_workbook

# 'H10-GD-D-86001_CHECKLIST.xlsx',
# 'H10-GD-D-86010_CHECKLIST.xlsx',
# 'H10-GD-D-86011_CHECKLIST.xlsx',
# 'H10-GD-D-86012_CHECKLIST.xlsx',
# 'H10-GD-D-86013_CHECKLIST.xlsx',
# 'H10-GD-D-86014_CHECKLIST.xlsx',
# 'H10-GD-D-86015_CHECKLIST.xlsx',
# 'H10-GD-D-86016_CHECKLIST.xlsx',
# 'H10-GD-D-86017_CHECKLIST.xlsx',
# 'H10-GD-D-86018_CHECKLIST.xlsx',
# 'H10-GD-D-86019_CHECKLIST.xlsx'


save_filename=['H10-GD-D-86080_CHECKLIST.xlsx',
'H10-GD-D-86071_CHECKLIST.xlsx',
'H10-GD-D-86086_CHECKLIST.xlsx',
'H10-GD-D-86085_CHECKLIST.xlsx']

file = ['H10-GD-D-86080',
'H10-GD-D-86071',
'H10-GD-D-86086',
'H10-GD-D-86085']

sheetname = 'PR-02-002'

open_filename = ['1 (1).xlsx',
'1 (2).xlsx',
'1 (3).xlsx',
'1 (4).xlsx']

i=0

for x in open_filename:
    print("----------------------------------")
    print(i+1,". ",x)
    rootch = int(input("polama : "))
    if(rootch==1):
        #load excel file
        workbook = load_workbook(filename=x)

        #sheet 1 changes
        sheet1 = workbook[sheetname]
        sheet1["D5"] = "Document nr. " + file[i]
        sheet1["A27"] = "Signature: PUSHKER MAHENDRA"
        sheet1["G27"] = "Date: 04.07.2022"
        
        #save the file
        workbook.save(filename=save_filename[i])
        i=i+1

    else:
        print("skipping this file --> ",x)
        i=i+1
        continue