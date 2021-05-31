from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import xlrd
import os
import time
import logging
import configparser
import unittest
#from BeautifulReport import BeautifulReport
from PIL import Image
import pytesseract
'''
公共类库，和产品业务没有联系，代码逻辑相关的类与函数
'''


# 元素定位方法封装
class EleLocate:
    def __init__(self, dr, element, content=""):
        self.dr = dr
        self.element = element
        self.content = content

    # 通过ID元素进行定位操作
    def id_ele(self):
        return self.dr.find_element_by_id(self.element)

    # 通过ID元素进行输入操作
    def id_ele_s(self):
        return self.dr.find_element_by_id(self.element).send_keys(self.content)

    # 通过ID元元素进行点击操作
    def id_ele_c(self):
        return self.dr.find_element_by_id(self.element).click()

    # 通过CLASS-NAME元素进行定位操作
    def class_ele(self):
        return self.dr.find_element_by_class_name(self.element)

    # 通过CLASS-NAME元素进行输入操作
    def class_ele_s(self):
        return self.dr.find_element_by_class_name(self.element).send_keys(self.content)

    # 通过CLASS-NAME元元素进行点击操作
    def class_ele_c(self):
        return self.dr.find_element_by_class_name(self.element).click()

    # 通过NAME元素进行定位操作
    def name_ele(self):
        return self.dr.find_element_by_name(self.element)

    # 通过NAME元素进行输入操作
    def name_ele_s(self):
        return self.dr.find_element_by_name(self.element).send_keys(self.content)

    # 通过NAME元元素进行点击操作
    def name_ele_c(self):
        return self.dr.find_element_by_name(self.element).click()

    # 通过XPATH元素进行定位操作
    def xpath_ele(self):
        return self.dr.find_element_by_xpath(self.element)

    # 通过XPATH元素进行输入操作
    def xpath_ele_s(self):
        return self.dr.find_element_by_xpath(self.element).send_keys(self.content)

    # 通过XPATH元元素进行点击操作
    def xpath_ele_c(self):
        return self.dr.find_element_by_xpath(self.element).click()

    # 通过CSS元素进行定位操作
    def css_ele(self):
        return self.dr.find_element_by_css_selector(self.element)

    # 通过CSS元素进行输入操作
    def css_ele_s(self):
        return self.dr.find_element_by_css_selector(self.element).send_keys(self.content)

    # 通过CSS元素进行点击操作
    def css_ele_c(self):
        return self.dr.find_element_by_css_selector(self.element).click()


# 元素等待，可见性/存在性判断
class VisibleElement:
    def __init__(self, dr):
        self.dr = dr
        self.log = Log()
        self.locate = EleLocate

    # 元素By类封装，判断元素定位方法
    def way_ele(self, way, element):
        if way == "id":
            locator = (By.ID, element)
            return locator
        elif way == "name":
            locator = (By.NAME, element)
            return locator
        elif way == "class":
            locator = (By.CLASS_NAME, element)
            return locator
        elif way == "css":
            locator = (By.CSS_SELECTOR, element)
            return locator
        elif way == "xpath":
            locator = (By.XPATH, element)
            return locator
        else:
            self.log.info('>>> 元素方法不存在')

    # 检查元素是否可见，并返回相应结果
    def find_ele(self, way, element, timeout=10):
        try:
            WebDriverWait(self.dr, timeout, 0.5).until(ec.visibility_of_element_located(self.way_ele(way, element)))
            if way == 'id':
                return self.locate(self.dr, element).id_ele()
            elif way == 'name':
                return self.locate(self.dr, element).name_ele()
            elif way == 'class':
                return self.locate(self.dr, element).class_ele()
            elif way == 'xpath':
                return self.locate(self.dr, element).xpath_ele()
            elif way == 'css':
                return self.locate(self.dr, element).css_ele()
        except Exception as NoSuchElement:
            self.log.error('>>> 元素{}不可见,定位失败'.format(element))
            raise NoSuchElement


# 读取配置文件数据
class GetConfig:
    def __init__(self, item, pathname):
        self.item = item
        self.pathname = pathname

    def getpath(self):
        # 指定配置文件路径-顶目录-'cgjgxt'
        pro_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        # 读取配置文件中的数据
        cf = configparser.ConfigParser()
        os.chdir(pro_path)
        cf.read(pro_path + '/jsgl_model_room/GlobalConfig.ini', encoding='utf-8')
        items = cf.options(self.item)
        # 返回配置文件中对应字段的值
        for i in items:
            if i == self.pathname:
                data = cf.get(self.item, self.pathname)
                return data
            else:
                pass


# Excel表数据读写
class ExcelReadWrite:
    def __init__(self, sheet, row, col):
        self.conf = GetConfig('globalconf', 'case_excel_file')  # 读取配置文件下globalconf中的case_excel_fil字段
        self.path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + self.conf.getpath()
        self.sheet = sheet
        self.row = row
        self.col = col

    def read_excel(self):
        book = xlrd.open_workbook(self.path)
        sheets = book.sheet_by_name(self.sheet)
        # 读取指定单元格的值
        cell_value = sheets.cell_value(self.row, self.col)
        return cell_value


# 生成测试报告
class ResultTest:
    def __init__(self):
        # 测试报告存放路径
        self.reports = GetConfig('globalconf', 'test_report_path')
        self.path_report = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + self.reports.getpath()
        # 测试用例路径
        self.top_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.test_case_path = self.top_path + '/jsgl_ui_test/TestCase'

    def create_report(self):
        suit_tests = unittest.defaultTestLoader.discover(self.test_case_path, pattern='*test.py', top_level_dir=None)
        BeautifulReport(suit_tests).report(filename='测试报告', description='测试', log_path=self.path_report)


# 日志封装及结果生成
class Log:
    def __init__(self):
        self.logs = GetConfig('globalconf', 'test_log_path')
        self.log_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + self.logs.getpath()  # 日志生成路径
        self.logname = os.path.join(self.log_path, '%s.log' % time.strftime('%Y_%m_%d'))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s[line:%(lineno)d] - fuc:%(funcName)s- '
                                           '%(levelname)s: %(message)s')

    def __console(self, level, message):
        fh = logging.FileHandler(self.logname, 'a')  # 追加模式
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)


# 页面截图
def screen_shot(dr, filename):
    screen_dir = GetConfig('globalconf', 'screen_path')
    picture_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + screen_dir.getpath()
    os.chdir(picture_path)
    isexist = os.path.exists(time.strftime('%Y%m%d'))

    if not isexist:
        os.makedirs(time.strftime('%Y%m%d'))
        full_path = os.path.join(picture_path, time.strftime('%Y%m%d'))
        os.chdir(full_path)
        dr.get_screenshot_as_file(time.strftime('%H%M%S') + filename)
    else:
        full_path = os.path.join(picture_path, time.strftime('%Y%m%d'))
        os.chdir(full_path)
        dr.get_screenshot_as_file(time.strftime('%H%M%S') + filename)


# table表格数据——获取单元格数据（工程结构中期证书表格）
def getdata(dr, row_s, clu_s):
    try:
        table = dr.find_element(By.ID, 'tableId')
        # 获取列表表格的行数
        table_rows = table.find_elements_by_tag_name('tr')
        # 获取列表单元格数据
        data = table_rows[row_s].find_elements_by_tag_name('td')[clu_s]
        return data
    except Exception as e:
        Log().warning("获取单元格数据失败%s"%(e))
        raise e


# table表格数据——获取单元格数据（工程结构中期证书表格）
def getdatak(dr, row_s, clu_s):
    try:
        table = dr.find_element(By.XPATH, '//div[@id="tableBody"]/table')
        # 获取列表表格的行数
        table_rows = table.find_elements_by_tag_name('tr')
        # 获取列表单元格数据
        data = table_rows[row_s].find_elements_by_tag_name('td')[clu_s]
        return data
    except Exception as e:
        Log().warning("获取单元格数据失败%s" % (e))
        raise e


# 获取表格行数
def getrows(dr):
    try:
        table = dr.find_element(By.ID, 'tableId')
        # 获取列表表格的行数
        table_rows = table.find_elements_by_tag_name('tr')
        return len(table_rows)
    except Exception as e:
        Log().warning("获取表格行数失败%s" % (e))


# table表格数据——获取单元格元素定位信息
def getelement(dr, row_s, clu_s):
    try:
        table = dr.find_element(By.ID, 'tableId')
        # 获取列表表格的行数
        table_rows = table.find_elements_by_tag_name('tr')
        # 获取列表单元格元素信息
        element = table_rows[row_s].find_elements_by_tag_name('td')[clu_s]
        return element
    except Exception as e:
        Log().warning("获取表格单元格元素信息失败%s"%(e))
        raise e































