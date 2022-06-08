# coding=utf-8
import time
import datetime

import xlrd
import requests
from config import conf
from logic.ParticipleHelper.res_count_fun import terms_count_in_html
from logic.ParticipleHelper.res_count_fun import lcut_for_search_fun
from common.PortalOperate import user_login
from common.PortalOperate import search_application
from common.PortalOperate import switch_locale
from logic.ExcelHelper.write_excel import write_excel

result_data = [
    ['应用名称', '原文档中的应用地址', '实际访问的应用地址', '访问状态', '应用在政务网是否存在', '是否通过']
]
now_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
# 读取excel中的内容
data = xlrd.open_workbook('D://code/gszww_auto_test/SeleniumProject/logic/应用信息.xls')
table = data.sheet_by_name('Sheet1')
info_dict = {}
for i in range(table.nrows - 1):
    info_list = []
    application_name = table.cell_value(i + 1, 2)
    application_address = table.cell_value(i + 1, 3)
    if type(application_name) == float:
        application_name = str(int(application_name))
    info_list.append(application_name)
    info_list.append(application_address)
    info_dict[i] = info_list
print(info_dict)
# 用户登录
chrome = user_login()
# 切换地州区域
switch_locale(chrome, conf.GSZWW.locale_name.gansu_locale)
print(chrome.driver.title)
for i in info_dict:
    application_name = info_dict[i][0]
    application_address = info_dict[i][1]
    all_handles = chrome.driver.window_handles
    chrome.driver.switch_to.window(all_handles[-1])
    time.sleep(1)
    search_application(chrome, str(application_name), conf.GSZWW.locale_name.gansu_locale)
    time.sleep(1)
    try:
        no_result = chrome.driver.find_element_by_xpath(
            '//*[@id="search-form"]/div/div/div[3]/div[1]/div[5]/div/div[2]/span')
        if no_result.text == '此分类下没有数据':
            with open('result_' + now_time + '.txt', 'a') as f:
                f.write('应用名称：' + application_name + '，文档中访问地址为：' + application_address + '：没有该应用\n')
            result_data.append([application_name, application_address, '应用不存在', 'error', '没有该应用', '否'])
            continue
    except Exception as e:
        pass
    try:
        result = chrome.driver.find_element_by_link_text(application_name)
        print(result.text)
        result.click()
        time.sleep(2)

    except Exception as e:
        with open('result_' + now_time + '.txt', 'a') as f:
            f.write('应用名称：' + application_name + '，文档中访问地址为：' + application_address + '：应用名称不匹配，请核对\n')
        result_data.append([application_name, application_address, '应用不存在', 'error', '应用名称不匹配', '否'])
        continue
    all_handles = chrome.driver.window_handles
    chrome.driver.switch_to.window(all_handles[-1])
    # 获取应用名称搜索名分词列表
    terms_list = lcut_for_search_fun(application_name)

    try:
        url = chrome.driver.current_url
        r = requests.get(url, allow_redirects=False)
        response_code = r.status_code
        if str(response_code).startswith('2'):
            r.encoding = r.apparent_encoding
            html_text = r.text
            percent = terms_count_in_html(html_text, terms_list)
            if percent > 0.9:
                print('全匹配')
            else:
                print('未匹配')
    except Exception as e:
        response_code = None
        pass

    if str(response_code).startswith('4') or str(response_code).startswith('5'):
        print('重新访问：%s' % url)
        try:
            url = chrome.driver.current_url
            r = requests.get(url, allow_redirects=False)
            response_code = r.status_code
        except Exception as e:
            response_code = None
            url = None
            pass

    with open('result_' + now_time + '.txt', 'a') as f:
        f.write('应用名称：' + application_name + '，文档中访问地址为：' + application_address + '。存在应用且请求该应用响应为：' + str(response_code) + '。当前访问的地址为：' + str(url) + '\n')
    if str(response_code).startswith('2'):
        is_pass = '是'
    else:
        is_pass = '否'
    result_data.append([application_name, application_address, url, str(response_code), '存在', is_pass])
    chrome.driver.close()
write_excel(result_data)
chrome.driver.quit()
