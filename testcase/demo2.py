# coding=utf-8
import time
import re
from selenium.webdriver.common.action_chains import ActionChains
from logic.UI.ChromeHelper import ChromeHelper
from common.LoggerHelper import logger

chrome = ChromeHelper()
chrome.open_chrome("https://zwfw.gansu.gov.cn/")
logger.info(chrome.driver.current_window_handle)
chrome.click_element('xpath', '//*[@id="barrierfree_container"]/div/div[2]/div/div[1]/div[1]/div[2]/p/a')
time.sleep(2)


image_verify_xpath = '/html/body/div[2]/div/div[2]/div[2]/ul/li[1]/div[3]/div[1]/form/div[3]/div/div[2]/div/div/div'
image_verify_element = chrome.find_element('xpath', image_verify_xpath)
image_verify_element_style = image_verify_element.get_attribute('style')

link = re.compile('background-position: (.*?)px (.*?)px;')
b = link.search(image_verify_element_style)
# print b.group(1)
distance = int(float(b.group(1)))
test_element = chrome.find_element('xpath', '/html/body/div[2]/div/div[2]/div[2]/ul/li[1]/div[3]/div[1]/form/div[3]/div/div[2]/div/div')
action = ActionChains(chrome.driver)
action.click_and_hold(test_element)
action.move_by_offset(-distance, 0)
action.release()
action.perform()
time.sleep(1)
chrome.input_keys('id', 'username', '17316134395')

chrome.input_keys('id', 'password', 'XWH333111##')
time.sleep(1)
chrome.click_element('xpath', '//*[@id="userloginform"]/div[5]/button')
time.sleep(2)
chrome.close_chrome()

