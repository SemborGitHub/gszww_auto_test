# coding=utf-8

import time
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import time
import re
from selenium.webdriver.common.action_chains import ActionChains
from logic.UI.ChromeHelper import ChromeHelper
from common.LoggerHelper import logger

from config import conf


def user_login(chrome=ChromeHelper()):
    # chrome = ChromeHelper()
    chrome.open_chrome("https://zwfw.gansu.gov.cn/")
    logger.info(chrome.driver.current_window_handle)
    chrome.click_element('xpath', conf.GSZWW.login_element.login_href)
    time.sleep(2)

    image_verify_xpath = conf.GSZWW.login_element.image_verify
    image_verify_element = chrome.find_element('xpath', image_verify_xpath)
    image_verify_element_style = image_verify_element.get_attribute('style')

    link = re.compile('background-position: (.*?)px (.*?)px;')
    b = link.search(image_verify_element_style)
    # print b.group(1)
    distance = int(float(b.group(1)))
    sliding_block_element = chrome.find_element('xpath', conf.GSZWW.login_element.sliding_block)
    action = ActionChains(chrome.driver)
    action.click_and_hold(sliding_block_element)
    action.move_by_offset(-distance, 0)
    action.release()
    action.perform()
    chrome.input_keys('id', conf.GSZWW.login_element.username, conf.GSZWW.account_pwd.account)
    chrome.input_keys('id', conf.GSZWW.login_element.password, conf.GSZWW.account_pwd.pwd)
    chrome.click_element('xpath', conf.GSZWW.login_element.login_button)

    return chrome

user_login()