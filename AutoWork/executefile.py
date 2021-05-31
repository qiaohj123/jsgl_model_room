from jsgl_ui_test.CommonLib.PrivateLib import PrivateModule
from jsgl_ui_test.CommonLib.PrivateLib import *
from jsgl_model_room.ScreenCap.Record_Screen import RecordScreen
from selenium import webdriver
import time
import unittest
from multiprocessing import Process
from jsgl_model_room.ScreenCap.Up_Load import upload


class ExecuteFile(unittest.TestCase):
    @classmethod
    def setUp(self):
        # 静默运行
        # self.option = webdriver.ChromeOptions()
        # self.option.add_argument('headless')
        # self.dr = webdriver.Chrome(chrome_options=self.option)
        # 非静默运行
        self.dr = webdriver.Chrome()
        self.dr.maximize_window()
        self.log = Log()
        self.p = PrivateModule(self.dr)

    def tearDown(self):
        # self.dr.quit()
        pass

    # # 中期支付证书上报--上报压测
    # def test_upload_function(self):
    #     self.log.info('>>> 登录系统')
    #     self.p.login()
    #     self.p.main_frame()
    #     self.log.info('>>> 进入到工程结构计量-中期支付证书页面')
    #     self.p.men_choice('工程结构计量', 'null', '中期支付证书')
    #     self.p.section_id('S2-2')
    #     # 点击第7行第8列的元素
    #     self.p.get_report_element(5, 8).click()
    #     self.p.upload_times()  # 上报压测

    def site_receipt(self):
        self.log.info('>>> 登录系统')
        self.p.login()
        self.p.main_frame()
        self.log.info('>>> 进入到工程结构计量-现场收方单页面')
        self.p.men_choice('工程结构计量', 'null', '现场收方单')
        self.p.receipt_choice('S1-1', 'ZK4+170~ZK4+237洞身开挖')
        self.p.add_receipt()
        # self.p.upload_receipt()
        time.sleep(10)


if __name__ == '__main__':
    # # unittest.main()
    suit = unittest.TestSuite()
    suit.addTest(ExecuteFile('site_receipt'))
    runner = unittest.TextTestRunner()
    runner.run(suit)
