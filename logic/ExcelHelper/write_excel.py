import xlwt
import copy
import datetime
import os

from logic.ExcelHelper.ResultsHelper import create_results_path


def get_max_col(max_list):
    line_list = []
    # i表示行，j代表列
    for j in range(len(max_list[0])):
        line_num = []
        for i in range(len(max_list)):
            line_num.append(max_list[i][j])  # 将每列的宽度存入line_num
        line_list.append(max(line_num))  # 将每列最大宽度存入line_list
    return line_list


def write_excel(data, results_path):
    print("开始写入Excel...")
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.bold = True
    style.font = font
    border = xlwt.Borders()
    border.top = xlwt.Borders.THIN
    border.bottom = xlwt.Borders.THIN
    border.left = xlwt.Borders.THIN
    border.right = xlwt.Borders.THIN
    style.borders = border
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = 0x01
    style.alignment = alignment

    row_num = 0  # 记录写入行数
    col_list = []  # 记录每行宽度
    # 创建一个workbook对象
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    # 创建一个sheet对象
    sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)
    col_num = [x for x in range(0, len(data[0]))]
    # 写入数据
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            sheet.write(row_num, j, data[i][j])
            col_num[j] = len(data[i][j].encode('gb18030'))  # 计算每列值的大小
        col_list.append(copy.copy(col_num))  # 记录一行每列写入的长度
        row_num += 1
    # # 获取每列最大宽度
    # col_max_num = get_max_col(col_list)
    # # 设置自适应列宽
    # for i in range(0, len(col_max_num)):
    #     # 256*字符数得到excel列宽,为了不显得特别紧凑添加两个字符宽度
    #     sheet.col(i).width = 256 * (col_max_num[i] + 2)

    # 保存excel文件
    start_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    excel_name = 'result_info_' + str(start_time) + '.xls'
    excel_file = os.path.join(results_path, excel_name)
    book.save(excel_file)
    print("写入Excel文件完成...")


if __name__ == '__main__':
    results_lists = []
    result_lists = []
    now_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    with open('../results/2022_06_07_17_31_54_result.txt') as f:
        results_list = f.readlines()
    print(results_list)
    for results in results_list:
        if results != '':
            result_lists.append(results[0:-2].split(';'))

    print(result_lists)
    results_lists.append(results_list)
    path = create_results_path()
    write_excel(result_lists, path)
    print("执行结果保存位置：", path)
