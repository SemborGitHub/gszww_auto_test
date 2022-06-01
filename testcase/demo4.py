import xlrd

data = xlrd.open_workbook('../logic/应用信息.xls')
table = data.sheet_by_name('Sheet1')
info_dict = {}
for i in range(table.nrows - 1):
    info_list = []
    application_name = table.cell_value(i + 1, 2)
    application_address = table.cell_value(i + 1, 3)
    info_list.append(application_name)
    info_list.append(application_address)
    info_dict[i] = info_list
print(info_dict)

for i in info_dict:
    print(info_dict[i])

