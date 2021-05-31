# # from appium import webdriver
# # import time
# #
# # desired_caps={}
# #
# # desired_caps["platformName"]="Android"
# # desired_caps["platformVersion"]="10.0"
# # desired_caps["deviceName"]="HuaWeiP30"
# # desired_caps["appPackage"]="com.schdri.cms.lexi"
# # desired_caps["appActivity"]="io.dcloud.PandoraEntryActivity"
# # driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub",desired_caps)
# # #在搜索框输入关键词
# # driver.find_element_by_id("com.taobao.taobao:id/home_searchedit").click()
# # # 等待时间
# # time.sleep(3)
# # driver.find_element_by_id("com.taobao.taobao:id/searchEdit").send_keys("adidas")
# # time.sleep(3)
# # driver.find_element_by_id("com.taobao.taobao:id/searchbtn").click()
# # #截图
# # driver.quit()
#
# a = [2]
#
#
# print(a[0])


from jsgl_ui_test.CommonLib.PrivateLib import PrivateModule
from jsgl_ui_test.CommonLib.PrivateLib import *
from jsgl_model_room.ScreenCap.Record_Screen import RecordScreen
from selenium import webdriver
import time
import unittest
from multiprocessing import Process
from jsgl_model_room.ScreenCap.Up_Load import upload


        # 静默运行
        # self.option = webdriver.ChromeOptions()
        # self.option.add_argument('headless')
        # self.dr = webdriver.Chrome(chrome_options=self.option)
        # 非静默运行


# 中期支付证书上报--上报压测
def test_upload_function01():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    dr = webdriver.Chrome(chrome_options=option)
    dr.maximize_window()
    log = Log()
    p = PrivateModule(dr)
    try:
        log.info('>>> 登录系统')
        p.login()
        p.main_frame()
        log.info('>>> 进入到工程结构计量-中期支付证书页面')
        p.men_choice('工程结构计量', 'null', '中期支付证书')
        p.section_id('S2-2')
        # 点击第7行第8列的元素
        p.get_report_element(1, 8).click()
        p.upload_times()  # 上报压测
    except Exception as e:
        log.info('>>> 进程1执行失败%s' % (e))
        screen_shot(dr, '进程1失败.png')
        raise e


def test_upload_function02():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    dr = webdriver.Chrome(chrome_options=option)
    dr.maximize_window()
    log = Log()
    p = PrivateModule(dr)
    try:
        log.info('>>> 登录系统')
        p.login()
        p.main_frame()
        log.info('>>> 进入到工程结构计量-中期支付证书页面')
        p.men_choice('工程结构计量', 'null', '中期支付证书')
        p.section_id('S2-2')
        # 点击第7行第8列的元素
        p.get_report_element(2, 8).click()
        p.upload_times()  # 上报压测
    except Exception as e:
        log.info('>>> 进程2执行失败%s' % (e))
        screen_shot(dr, '进程2失败.png')
        raise e

def test_upload_function03():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    dr = webdriver.Chrome(chrome_options=option)
    dr.maximize_window()
    log = Log()
    p = PrivateModule(dr)
    try:

        log.info('>>> 登录系统')
        p.login()
        p.main_frame()
        log.info('>>> 进入到工程结构计量-中期支付证书页面')
        p.men_choice('工程结构计量', 'null', '中期支付证书')
        p.section_id('S2-2')
        # 点击第7行第8列的元素
        p.get_report_element(3, 8).click()

        p.upload_times()  # 上报压测
    except Exception as e:
        log.info('>>> 进程3执行失败%s' % (e))
        screen_shot(dr, '进程3失败.png')
        raise e


def test_upload_function04():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    dr = webdriver.Chrome(chrome_options=option)
    dr.maximize_window()
    log = Log()
    p = PrivateModule(dr)
    try:
        log.info('>>> 登录系统')
        p.login()
        p.main_frame()
        log.info('>>> 进入到工程结构计量-中期支付证书页面')
        p.men_choice('工程结构计量', 'null', '中期支付证书')
        p.section_id('S2-2')
        # 点击第7行第8列的元素
        p.get_report_element(4, 8).click()
        p.upload_times()  # 上报压测
    except Exception as e:
        log.info('>>> 进程4执行失败%s' % (e))
        screen_shot(dr, '进程4失败.png')
        raise e


def test_upload_function05():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    dr = webdriver.Chrome(chrome_options=option)
    dr.maximize_window()
    log = Log()
    p = PrivateModule(dr)
    log.info('>>> 登录系统')
    try:
        p.login()
        p.main_frame()
        log.info('>>> 进入到工程结构计量-中期支付证书页面')
        p.men_choice('工程结构计量', 'null', '中期支付证书')
        p.section_id('S2-2')
        # 点击第7行第8列的元素
        p.get_report_element(5, 8).click()
        p.upload_times()  # 上报压测
    except Exception as e:
        log.info('>>> 进程5执行失败%s' % (e))
        screen_shot(dr, '进程5失败.png')
        raise e

if __name__ == '__main__':
    p1 = Process(target=test_upload_function01)
    p2 = Process(target=test_upload_function02)
    p3 = Process(target=test_upload_function03)
    p4 = Process(target=test_upload_function04)
    p5 = Process(target=test_upload_function05)
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
