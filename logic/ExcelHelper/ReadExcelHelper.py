import os.path

import xlrd

from common.LoggerHelper import logger


def read_excel(filename, sheet_name, *args):
    if not filename:
        raise ValueError("The parameter: filename can not be null!")
    cur_path = os.path.dirname(os.path.dirname(__file__))
    project_path = os.path.dirname(cur_path)
    excel_path = os.path.join(project_path, "excelfile", filename)
    if not os.path.exists(excel_path):
        raise ValueError("Put the excel file in the path: %s", os.path.join(project_path, "excelfile"))
    logger.debug("Read the file: %s ", excel_path)
    try:
        data = xlrd.open_workbook(excel_path)
        table = data.sheet_by_name(sheet_name)
        table_dict = {}
        print(table)
        if len(args) == 0:
            for i in range(table.nrows):
                row_data = table.row_values(i)
                table_dict[i+1] = row_data
        else:
            row1_data = table.row_values(0)
            col_nums = []
            for arg in args:
                col_num = row1_data.index(arg)
                col_nums.append(col_num)
            for row in range(table.nrows - 1):
                row_data = []
                for col in col_nums:
                    value = table.cell_value(row + 1, col)
                    if type(value) is int:
                        value = str(int(value))
                    elif type(value) is float:
                        if value.is_integer():
                            value = str(int(value))
                    else:
                        value = str(value)
                    row_data.append(value)
                table_dict[row+2] = row_data
        logger.debug("Read excel file to dict: %s", table_dict)

        return table_dict
    except Exception as e:
        logger.error(e)
        raise e


if __name__ == "__main__":
    # tab = read_excel("应用信息.xls", "Sheet1", "应用名称", "应用地址")
    tab = read_excel("应用信息.xls", "Sheet1")
    print(tab)
