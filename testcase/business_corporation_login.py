# coding=utf-8
import os
import time
import datetime

import requests
from selenium.common.exceptions import NoSuchElementException

from config import conf
from common.PortalOperate import user_login, user_login_firm
from common.PortalOperate import search_application
from common.PortalOperate import switch_locale
from testcase.write_excel import write_excel
from logic.ExcelHelper.ReadExcelHelper import read_excel
from common.LoggerHelper import logger
from res_count_fun import terms_count_in_html
from res_count_fun import lcut_for_search_fun
from logic.UI.ChromeHelper import ChromeHelper


def create_txt_file(start_time):
    project_path = os.path.dirname(os.path.dirname(__file__))
    txt_path = os.path.join(project_path, "../results")
    if not os.path.exists(txt_path):
        os.mkdir(txt_path)
    txt_name = start_time + "_result.txt"
    txt_file = os.path.join(txt_path, txt_name)
    row1 = "应用名称;原文档中的应用地址;实际访问的应用地址;访问地址是否等于文档所给地址;访问状态;应用在政务网是否存在;" \
           "应用名称与页面是否匹配;截图相对路径\n"
    with open(txt_file, "a") as f:
        f.write(row1)
    return txt_file


# def write_txt(txt_file, application_name, application_address, link_url, response_code, msg):
#     txt = "应用名称:" + str(application_name) + ",文档中访问地址:" + str(application_address) + ",实际访问地址:" + \
#           str(link_url) + ",响应状态:" + str(response_code) + ",结果:" + str(msg) + "\n"
#     logger.debug(txt)
#     print(txt)
#     with open(txt_file, "a") as f:
#         f.write(txt)

def write_txt(txt_file, ans_list):
    record = ""
    for ans in ans_list:
        record = record + str(ans) + ";"
    print(record)
    record = record + "\n"
    with open(txt_file, "a") as f:
        f.write(record)


def get_screenshot(chrome, application_name, date):

    path = os.path.dirname(__file__)
    pic_path = os.path.join(path, "pics", str(date))
    if not os.path.exists(pic_path):
        os.mkdir(pic_path)
    file_name = str(application_name) + ".png"
    file_path = os.path.join(pic_path, file_name)
    chrome.driver.save_screenshot(file_path)
    return os.path.relpath(file_path)


def retry(response_code, url):
    if str(response_code).startswith('4') or str(response_code).startswith('5'):
        time.sleep(2)
        logger.info("重新访问： %s", url)
        try:
            r = requests.get(url, allow_redirects=False, timeout=5)
            response_code = r.status_code
        except Exception as e:
            raise e

    return response_code


def main():
    start_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    # 读取excel中的内容 sheet2 为个人登录的应用  sheet1是企业登录的应用
    info_dict = read_excel("甘肃省省级事项明细.xls", "Sheet1", "业务项名称", "网办地址")
    print("读取excel文件成功...")
    print("读取到的excel内容为:")
    print(info_dict)
    # 用户登录
    print("开始执行浏览器操作...")
    # chrome = user_login()
    chrome = user_login_firm()
    chrome.set_retreat_config(False)
    # 切换地州区域
    switch_locale(chrome, conf.GSZWW.locale_name.gansu_locale)
    logger.info("The title is: %s", chrome.driver.title)

    # 定义错误信息：
    msg1 = "无此应用"
    msg2 = "应用存在"
    msg3 = "应用存在，但访问状态异常"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/95.0.4638.69 Safari/537.36'
    }
    # 定义结果列表
    txt_file = create_txt_file(start_time)
    print("记录txt文件：", txt_file)
    result_data = [
        ['应用名称', '原文档中的应用地址', '实际访问的应用地址', '访问地址是否等于文档所给地址', '访问状态',
         '应用在政务网是否存在', '应用名称与页面是否匹配', '截图相对路径']
    ]

    total_num = len(info_dict.keys())
    success_num = 0
    failure_num = 0
    finish_num = 0

    for row in info_dict.keys():
        # 定义结果变量
        response_code = None
        link_url = None
        is_same = None
        img_path = None
        msg = None

        info = "已完成:" + str(finish_num) + "  共计:" + str(total_num) + "  执行进度:" + str(finish_num*100//total_num)\
               + "%  成功:" + str(success_num) + "  失败:" + str(failure_num)
        print("*" * 60 + info + "*" * 60)
        application_name = info_dict.get(row)[0]
        application_address = info_dict.get(row)[1]
        # 获取应用名称搜索名分词列表
        terms_list = lcut_for_search_fun(application_name)

        print("正在处理事项名称:", str(application_name))

        terms_matching_result = None
        # noinspection PyBroadException
        try:
            search_application(chrome, str(application_name), conf.GSZWW.locale_name.gansu_locale)
            time.sleep(1)
            application_elements = chrome.driver.find_elements_by_xpath(
                '//*[@id="search-form"]/div/div/div[3]/div[1]/div[5]/div[1]/div/div/div/div[1]/a')
            if application_elements is []:
                raise NoSuchElementException('应用不存在')
            index = 1
            for application_element in application_elements:
                print(application_element.text)
                if str(application_name) in application_element.text:

                    chrome.click_element(
                        chrome.xpath,
                        '//*[@id="search-form"]/div/div/div[3]/div[1]/div[5]/div[1]/div'
                        '/div[' + str(index) + ']/div/div[2]/a[1]')
                    break
                index += 1

            time.sleep(3)
            url = chrome.driver.current_url
            link_url = url
            if url == application_address:
                is_same = '一致'
            else:
                is_same = '不一致'
            r = requests.get(url, allow_redirects=False, headers=headers, timeout=5)
            response_code = r.status_code
            response_code = retry(response_code, url)

            if str(response_code).startswith('2') or str(response_code).startswith('3'):
                html_text = chrome.driver.page_source
                percent = terms_count_in_html(html_text, terms_list)
                if percent >= 0.8:
                    terms_matching_result = '匹配'
                else:
                    terms_matching_result = '不匹配'

            msg = msg2
            success_num = success_num + 1
            img_path = get_screenshot(chrome, application_name, start_time)
            chrome.close_current_window()
        except NoSuchElementException:
            response_code = "error"
            msg = msg1
            failure_num = failure_num + 1
            img_path = get_screenshot(chrome, application_name, start_time)

        except Exception:
            msg = msg3
            failure_num = failure_num + 1
            img_path = get_screenshot(chrome, application_name, start_time)
            chrome.close_current_window()
        finally:
            ans_list = [
                str(application_name), str(application_address), str(link_url), str(is_same), str(response_code),
                str(msg), str(terms_matching_result), str(img_path)
            ]
            write_txt(txt_file, ans_list)
            result_data.append(ans_list)
            finish_num = finish_num + 1
    info = "已完成:" + str(finish_num) + "  共计:" + str(total_num) + "  执行进度:" + str(finish_num * 100 // total_num) \
           + "%  成功:" + str(success_num) + "  失败:" + str(failure_num)
    print("*" * 60 + info + "*" * 60)

    chrome.close_chrome()
    # noinspection PyBroadException
    write_excel(result_data, start_time)

    print("执行完成.")


if __name__ == "__main__":
    main()
