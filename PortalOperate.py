# coding=utf-8

import time
import re
from config import conf
from logic.UI.ChromeHelper import ChromeHelper
from common.LoggerHelper import logger
from selenium.webdriver.common.action_chains import ActionChains


def user_login(chrome=ChromeHelper()):
    chrome.open_chrome("https://zwfw.gansu.gov.cn/")
    logger.info(chrome.driver.current_window_handle)
    chrome.click_element('xpath', conf.GSZWW.login_element.login_href)
    time.sleep(2)

    # 获取滑块校验缺失图片的坐标
    image_verify_xpath = conf.GSZWW.login_element.image_verify
    image_verify_element = chrome.find_element('xpath', image_verify_xpath)
    image_verify_element_style = image_verify_element.get_attribute('style')

    link = re.compile('background-position: (.*?)px (.*?)px;')
    b = link.search(image_verify_element_style)
    distance = int(float(b.group(1)))
    # 拖动滑块验证
    sliding_block_element = chrome.find_element('xpath', conf.GSZWW.login_element.sliding_block)
    action = ActionChains(chrome.driver)
    action.click_and_hold(sliding_block_element)
    action.move_by_offset(-distance, 0)
    action.release()
    action.perform()
    # 输入用户名和密码 点击登录
    chrome.click_element(chrome.xpath, "//li[contains(text(),'法人登录')]")
    chrome.input_keys('id', conf.GSZWW.login_element.username, conf.GSZWW.account_pwd.account)
    chrome.input_keys('id', conf.GSZWW.login_element.password, conf.GSZWW.account_pwd.pwd)
    chrome.click_element('xpath', conf.GSZWW.login_element.login_button)

    return chrome


def search_application(chrome, value, locale_name):
    title_name = '甘肃政务服务网'
    second_title_name = '甘肃政务服务网-检索'
    if locale_name == '兰州新区':
        title_name = title_name + '-' + locale_name
        second_title_name = locale_name + '政务服务网-检索'
    if chrome.driver.title == title_name:
        # 输入首页搜索框内容，点击搜索
        chrome.input_keys('id', conf.GSZWW.search_element.search_input, value)
        chrome.click_element('xpath', conf.GSZWW.search_element.search_button)

        # 点击应用服务
        # chrome.click_element('xpath', conf.GSZWW.search_element.service_application)

    elif chrome.driver.title == second_title_name:
        # 输入在检索页面要输入的内容， 点击搜索
        chrome.input_keys('id', conf.GSZWW.search_element.retrieval_search_input, value)
        chrome.click_element('id', conf.GSZWW.search_element.retrieval_search_button)
        time.sleep(1)


def user_login_firm(chrome=ChromeHelper()):
    chrome.open_chrome("https://zwfw.gansu.gov.cn/")
    logger.info(chrome.driver.current_window_handle)
    chrome.click_element('xpath', conf.GSZWW.login_element.login_href)
    time.sleep(2)
    # 切换法人登录
    chrome.click_element(chrome.xpath, conf.GSZWW.firm_login_element.switch_login_button)

    # 获取滑块校验缺失图片的坐标
    image_verify_xpath = conf.GSZWW.firm_login_element.image_verify
    image_verify_element = chrome.find_element('xpath', image_verify_xpath)
    image_verify_element_style = image_verify_element.get_attribute('style')

    link = re.compile('background-position: (.*?)px (.*?)px;')
    b = link.search(image_verify_element_style)
    distance = int(float(b.group(1)))
    # 拖动滑块验证
    sliding_block_element = chrome.find_element('xpath', conf.GSZWW.firm_login_element.sliding_block)
    action = ActionChains(chrome.driver)
    action.click_and_hold(sliding_block_element)
    action.move_by_offset(-distance, 0)
    action.release()
    action.perform()
    # 输入用户名和密码 点击登录
    chrome.input_keys('id', conf.GSZWW.firm_login_element.corpname_id, conf.GSZWW.account_pwd.firm_account)
    chrome.input_keys('id', conf.GSZWW.firm_login_element.corppassword_id, conf.GSZWW.account_pwd.firm_pwd)
    chrome.click_element('xpath', conf.GSZWW.firm_login_element.login_button)

    return chrome


def switch_locale(chrome, locale_name):
    # 点击选择区域
    chrome.click_element('xpath', conf.GSZWW.switch_locale.switch_locale_button)
    # 点击对应的市州
    # chrome.click_element('text', locale_name)
    current_locale_name = chrome.driver.find_element_by_xpath('//*[@id="location-nav"]/span').text
    print(current_locale_name)
    if locale_name == '甘肃省':
        # 点击确定
        chrome.click_element('id', conf.GSZWW.switch_locale.query_button)
    else:
        need_switch_locales = chrome.driver.find_elements_by_xpath('//*[@id="link-info"]/li')
        for need_switch_locale in need_switch_locales:
            if need_switch_locale.text == locale_name:
                need_switch_locale.click()
                break
        time.sleep(1)
        chrome.click_element('id', conf.GSZWW.switch_locale.query_button)
