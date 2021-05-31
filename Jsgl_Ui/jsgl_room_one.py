from jsgl_model_room.CommonLib.PrivateLib import PrivateModule
from jsgl_model_room.ScreenCap.Up_Load import upload
from jsgl_model_room.Jsgl_Ui.Oracle_Data import OracleAction
from selenium import webdriver
import time
import os
import threading
import glob
import cv2
from multiprocessing import Process
# from jsgl_model_room.ScreenCap.Up_Load import upload


class ModuleRoom:
    def __init__(self):
        self.oracle_data = OracleAction()
        self.video_file_dir = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\TestResult\\'
        # self.dir_png_app = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\pa'
        # self.dir_png1 = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p1'
        # self.dir_png2 = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p2'
        # self.dir_png3 = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p3'
        self.dir_png4 = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p4'

    def clear_dir(self, path):
        """创建或清空目录"""
        if not os.path.isdir(path):
            os.mkdir(path)  # 创建目录
        else:  # 清空目录
            [os.remove(os.path.join(path, file_name)) for file_name in os.listdir(path)]

    def shot(self, dr, img_dir, start_num):
        """循环截图函数"""
        i = start_num
        self.clear_dir(img_dir)  # 清空目录
        while True:
            img_file = os.path.join(img_dir, f'{i}.png')
            try:
                dr.save_screenshot(img_file)
            except:
                return
            i += 1

    '''app端视频录制'''
    def app_ui(self, dr, wbsid):
        try:
            url = 'http://172.16.9.253:8080/jsgl/pages/str/esm/house/phone.jsp?wbsid={}'.format(wbsid)
            dr.get(url)
        except Exception as e:
            pass


    '''样板房一之 web端工序检查'''
    def start_ui(self, dr):
        p = PrivateModule(dr)
        p.login()
        p.main_frame()
        p.log.info('>>> 进入到 工序检查 页面')
        p.men_choice('工序检查')
        p.log.info('>>> 工序检查 数据查看')
        p.details_read()
        p.log.info('>>> 返回到首页')
        p.back_firstpage()

    def room_two(self, dr, section_data, main_list_report, sub_dict_report):
        try:
            p = PrivateModule(dr)
            p.login()
            p.main_frame()
            p.log.info('>>> 进入到 质检评定 页面')
            p.men_choice('质检评定', '1')
            p.quality_page('检验评定')
            p.log.info('>>> 质检评定 页面选择标段及分项工程')
            p.section_search(section_data['标段'], section_data['分项结构'])       # K73+673-K73+703段V级深埋洞身开挖
            p.log.info('>>> 质检评定 页面添加主表单')
            p.add_main_report(main_list_report)      # 易重构体质
            p.log.info('>>> 质检评定 页面添加子表单')
            p.add_sub_report(sub_dict_report)        # 质检表单添加
            dr.quit()
        except Exception as e:
            dr.quit()

    """样板房一之 现场收方单模块"""

    def room_three(self, dr, section_data, list_data):
        try:
            p = PrivateModule(dr)
            p.login()
            p.main_frame()
            p.log.info('>>> 进入到 现场收方单 页面')
            p.men_choice('工程结构计量', out='null', second_name='现场收方单')
            p.receipt_choice(section_data['标段'], section_data['分项结构'])
            p.receipt_add(list_data)
            p.receipt_upload()                # 上报收方单
            p.windows_handle('0')               # 切换到主窗口
            p.log.info('>>> 返回到首页')
            p.back_firstpage()
            self.oracle_data.update_sfd_state(section_data['分项结构'])      # 更新收方单状态为 审核通过
            p.main_frame()
            p.log.info('>>> 进入到 中间计量 页面')
            p.men_choice('工程结构计量', out='null', second_name='中间计量')
            p.log.info('>>> 中间计量页面标段结构选择')
            p.measure_choice(section_data['标段'], section_data['分项结构'])
            p.log.info('>>> 新增中间计量')
            p.measure_increase()
            p.log.info('>>> 返回到首页')
            p.back_firstpage()
            p.main_frame()
            p.log.info('>>> 进入到 工程结构中期支付证书 页面')
            p.men_choice('工程结构计量', out='null', second_name='中期支付证书')
            p.section_id(section_data['标段'])
            p.log.info('>>> 支付证书新增及上报')
            p.add_certificate_file()
            self.oracle_data.update_zqzs_state(section_data['标段ID'])     # 更新中期证书状态为 审核通过
            dr.quit()
        except Exception as e:
            dr.quit()

    """样板房一之 BIM数据融合模块"""

    def room_four(self, dr, section_data):
        try:
            p = PrivateModule(dr)
            p.login()
            p.main_frame()
            p.log.info('>>> 进入到 WBS结构 页面')
            p.men_choice('基础资料', out='null', second_name='WBS结构')
            p.bim_into(section_data['标段'], section_data['分项结构'])  # K73+643-K73+673段V级浅埋洞身开挖 右幅_8号桥台台帽_第1行_左起第1列_挡块
            p.bim_data_basic()
            p.bim_data_measure()
            p.bim_data_quality()
            p.bim_data_process()
            p.bim_data_change()
            p.bim_data_progress()
            dr.quit()
        except Exception as e:
            dr.quit()

    # 视频合成
    def cor_vd(self, video_file_dir, video_file_name):
        loacl_vedio = r'{}{}.mp4'.format(video_file_dir, video_file_name[0:10])
        print('1111111')
        print(loacl_vedio)
        path_file_APP = len(glob.glob('D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\pa\*.png'))
        path_file_number1 = len(glob.glob('D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p1\*.png'))
        path_file_number2 = len(glob.glob('D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p2\*.png'))
        path_file_number3 = len(glob.glob('D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p3\*.png'))
        path_file_number4 = len(glob.glob('D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p4\*.png'))

        sum_num = path_file_number3 + path_file_number4
        print('sum{}'.format(sum_num))

        video_write = cv2.VideoWriter(loacl_vedio, -1, 5, (2560, 1080))  # 参数3是帧数，参数4是图片尺寸
        img_array = []

        for filename in [r'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\pa\{}.png'.format(i) for i in range(1, 150)]:
            img = cv2.imread(filename)
            if img is None:
                print(filename + " is error!")
                continue
            img_array.append(img)

        for filename in [r'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p1\{}.png'.format(i) for i in range(1, 150)]:
            img = cv2.imread(filename)
            if img is None:
                print(filename + " is error!")
                continue
            img_array.append(img)

        for filename in [r'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p2\{}.png'.format(i) for i in range(1, 150)]:
            img = cv2.imread(filename)
            if img is None:
                print(filename + " is error!")
                continue
            img_array.append(img)

        for filename in [r'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p3\{}.png'.format(i) for i in range(1, 150)]:
            img = cv2.imread(filename)
            if img is None:
                print(filename + " is error!")
                continue
            img_array.append(img)

        for filename in [r'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p4\{}.png'.format(i) for i in range(151, 350)]:
            img = cv2.imread(filename)
            if img is None:
                print(filename + " is error!")
                continue
            img_array.append(img)

        for i in range(1, 300):
            video_write.write(img_array[i])   # 遍历数量需要做处理

    # 指令监控及执行
    def execute_process(self):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument('window-size=2560,1080')
        # dr1 = webdriver.Chrome(chrome_options=option)
        # dr2 = webdriver.Chrome()
        # dr3 = webdriver.Chrome()
        dr4 = webdriver.Chrome()


        # time.sleep(3)
        a = '0'
        while a == '0':
            a = self.oracle_data.order_exe()[1]     # 指令值0 or 1

        es_id = self.oracle_data.order_exe()[2]

        self.oracle_data.call_procedure(es_id)  # 调用建管平台 存储过程
        # self.oracle_data.call_procedure_zj(es_id)  # 调用质检平台 存储过程

        section_data = self.oracle_data.data_to_dict(es_id, item_list='项目标段')  # 项目标段及结构名称
        list_data = self.oracle_data.data_to_dict(es_id, item_list='收方单')  # 现场收方单 清单
        # main_list_report = self.oracle_data.data_to_dict_zj(es_id, request='keys')  # 质检 主表与子表对应关系字典
        # sub_dict_report = self.oracle_data.data_to_dict_zj(es_id, request='sub_list')  # 主表名称列表


        # p1 = threading.Thread(target=self.shot, args=(dr1, self.dir_png1))
        # p2 = threading.Thread(target=self.start_ui, args=(dr1,))
        #
        # p3 = threading.Thread(target=self.shot, args=(dr2, self.dir_png2))
        # p4 = threading.Thread(target=self.room_two, args=(dr2, section_data, main_list_report, sub_dict_report))
        #
        # p5 = threading.Thread(target=self.shot, args=(dr3, self.dir_png3))
        # p6 = threading.Thread(target=self.room_three, args=(dr3, section_data, list_data))

        p7 = threading.Thread(target=self.shot, args=(dr4, self.dir_png4, 5))
        p8 = threading.Thread(target=self.room_four, args=(dr4, section_data))


        # p1.start()
        # p2.start()
        # time.sleep(3)
        # p3.start()
        # p4.start()
        # time.sleep(3)
        # p5.start()
        # p6.start()
        # time.sleep(3)
        p7.start()
        p8.start()
        # time.sleep(3)

        # p2.join()
        # p4.join()
        # p6.join()
        p8.join()

        # # if not p2.is_alive():
        # # p1.terminate()
        self.oracle_data.set_order_value()
        time.sleep(3)
        # self.cor_vd(self.video_file_dir, section_data['分项结构'])  # 生成视频文件，已分项结构前10个字符  作为 视频文件名称
        # time.sleep(3)
        # upload(self.video_file_dir, section_data['分项结构'])
        # self.oracle_data.video_file_into_data(section_data['分项结构'], self.oracle_data.order_exe()[0])
        # self.execute_process()
        # time.sleep(3)

if __name__ == '__main__':
    ModuleRoom().execute_process()















# from jsgl_model_room.CommonLib.PrivateLib import PrivateModule
# # from jsgl_model_room.ScreenCap.Record_Screen import RecordScreen
# from jsgl_model_room.Jsgl_Ui.Oracle_Data import OracleAction
# from selenium import webdriver
# import time
# import os
# import threading
# from multiprocessing import Process
# # from jsgl_model_room.ScreenCap.Up_Load import upload
#
#
# oracle_data = OracleAction()
# # option = webdriver.ChromeOptions()
# # option.add_argument('headless')
# # option.add_argument('window-size=2560,1080')
# # dr = webdriver.Chrome(chrome_options=option)
# dr = webdriver.Chrome()
#
#
# def clear_dir(path):
#     """创建或清空目录"""
#     if not os.path.isdir(path):
#         os.mkdir(path)  # 创建目录
#     else:  # 清空目录
#         [os.remove(os.path.join(path, file_name)) for file_name in os.listdir(path)]
#
#
# def shot():
#     """循环截图函数"""
#     img_dir = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture'
#     i = 0
#     clear_dir(img_dir)  # 清空目录
#     while True:
#         img_file = os.path.join(img_dir, f'{i}.png')
#         try:
#             dr.save_screenshot(img_file)
#         except:
#             return
#         i += 1
#
# '''样板房一之 web端工序检查'''
# def start_ui():
#     # 真实数据存于字典data中
#     data = {'标段':'K1', '分项工程':'K73+950-K74+025段超前小导管'}
#     '''静默运行，设置屏幕大小'''
#
#     '''调用业务模块'''
#     p = PrivateModule(dr)
#     '''工序检查模块'''
#     p.login()
#     p.main_frame()
#     p.log.info('>>> 进入到 工序检查 页面')
#     p.men_choice('工序检查')
#     p.log.info('>>> 工序检查 数据查看')
#     p.details_read()
#     p.log.info('>>> 返回到首页')
#
#     # p.log.info('>>> 进入到 工序检查 页面')
#     # p.men_choice('工序检查')
#     # p.log.info('>>> 工序检查 数据查看')
#     # p.details_read()
#     # p.log.info('>>> 返回到首页')
#     # p.back_firstpage()
#     # p.main_frame()
#     # p.log.info('>>> 进入到 质检评定 页面')
#     # p.men_choice('质检评定', '1')
#     # p.quality_page('检验评定')
#     # p.log.info('>>> 质检评定 页面选择标段及分项工程')
#     # p.section_search(data['标段'], data['分项工程']) # K73+673-K73+703段V级深埋洞身开挖
#     # p.log.info('>>> 质检评定 页面添加主表单')
#     # p.add_main_report(["测表10 全站仪放线记录表(SG)", "监表06 施工放样报验单", "监表04 机械设备报验单", "监表10-1 分项工程开工申请批复单"])  #  易重构体质
#     # p.log.info('>>> 质检评定 页面添加子表单')
#     # p.add_sub_report(['123'])  # 质检表单添加
#     # p.windows_handle('first')
#     # p.log.info('>>> 进入到 现场收方单 页面')
#     # p.men_choice('工程结构计量', out='null', second_name='现场收方单')
#     # # p.men_choice('电子档案', '1')
#     # # a = {'文件题名': '测试题名'}  # 电子档案新增文件信息字典
#     # # p.file_manage('LJ2', '施工记录', a)
#     # p.receipt_choice(data['标段'], data['分项工程'])
#     # p.receipt_add(self.oracle_data.return_receipt())
#     # p.receipt_upload()
#     # p.men_choice('基础资料', out='null', second_name='WBS结构')
#     # p.bim_into('K1', 'K73+643-K73+673段V级浅埋洞身开挖')  # K73+643-K73+673段V级浅埋洞身开挖 右幅_8号桥台台帽_第1行_左起第1列_挡块
#     # p.bim_data_basic()
#     # p.bim_data_measure()
#     # p.bim_data_quality()
#     # p.bim_data_process()
#     # p.bim_data_change()
#     # p.bim_data_progress()
#
#
# # 指令监控及执行
# def execute_process():
#     # p1 = Process(target=start_rs)  # 必须加,号
#     # time.sleep(3)
#     p1 = Process(target=shot)
#     time.sleep(3)
#     a = 0
#     while a == 0:
#         a = oracle_data.order_exe()
#     p2 = Process(target=start_ui)
#
#     p1.start()
#     p2.start()
#     # p2.join()
#     if not p2.is_alive():
#         p1.terminate()
#     oracle_data.set_order_value()
#     execute_process()
#     # time.sleep(3)
#     # upload()
#
# if __name__ == '__main__':
#     execute_process()
#     # # p1 = Process(target=start_rs)  # 必须加,号
#     # # time.sleep(3)
#     # a = 0
#     # while a == 0:
#     #     b = OracleAction()
#     #     a = b.order_exe()
#     # p2 = Process(target=start_ui)
#     # #
#     # # p1.start()
#     # p2.start()
#     # p2.join()
#     # if not p2.is_alive():
#     #     p1.terminate()
#     # time.sleep(3)
#     # upload()
#
#





# from jsgl_model_room.CommonLib.PrivateLib import PrivateModule
# # from jsgl_model_room.ScreenCap.Record_Screen import RecordScreen
# from jsgl_model_room.Jsgl_Ui.Oracle_Data import OracleAction
# from selenium import webdriver
# import time
# import os
# import threading
# from multiprocessing import Process
# # from jsgl_model_room.ScreenCap.Up_Load import upload
#
#
# class ModuleRoom:
#     def __init__(self):
#         self.oracle_data = OracleAction()
#         # option = webdriver.ChromeOptions()
#         # option.add_argument('headless')
#         # option.add_argument('window-size=2560,1080')
#         # self.dr = webdriver.Chrome(chrome_options=option)
#         # self.dr = webdriver.Chrome()
#
#
#     # 视屏录制
#     # def start_rs(self, status=True):
#         # rs = RecordScreen()
#         # if status:
#         #     rs.screen_action()
#         # path = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture'
#
#     def clear_dir(self, path):
#         """创建或清空目录"""
#         if not os.path.isdir(path):
#             os.mkdir(path)  # 创建目录
#         else:  # 清空目录
#             [os.remove(os.path.join(path, file_name)) for file_name in os.listdir(path)]
#
#     def shot(self, dr):
#         """循环截图函数"""
#         img_dir = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture'
#         i = 0
#         self.clear_dir(img_dir)  # 清空目录
#         while True:
#             img_file = os.path.join(img_dir, f'{i}.png')
#             try:
#                 self.dr.save_screenshot(img_file)
#             except:
#                 return
#             i += 1
#
#     '''样板房一之 web端工序检查'''
#     def start_ui(self, dr):
#         # 真实数据存于字典data中
#         data = {'标段':'K1', '分项工程':'K73+950-K74+025段超前小导管'}
#         '''静默运行，设置屏幕大小'''
#
#         '''调用业务模块'''
#         p = PrivateModule(dr)
#         '''工序检查模块'''
#         p.login()
#         p.main_frame()
#         p.log.info('>>> 进入到 工序检查 页面')
#         p.men_choice('工序检查')
#         p.log.info('>>> 工序检查 数据查看')
#         p.details_read()
#         p.log.info('>>> 返回到首页')
#
#         # p.log.info('>>> 进入到 工序检查 页面')
#         # p.men_choice('工序检查')
#         # p.log.info('>>> 工序检查 数据查看')
#         # p.details_read()
#         # p.log.info('>>> 返回到首页')
#         # p.back_firstpage()
#         # p.main_frame()
#         # p.log.info('>>> 进入到 质检评定 页面')
#         # p.men_choice('质检评定', '1')
#         # p.quality_page('检验评定')
#         # p.log.info('>>> 质检评定 页面选择标段及分项工程')
#         # p.section_search(data['标段'], data['分项工程']) # K73+673-K73+703段V级深埋洞身开挖
#         # p.log.info('>>> 质检评定 页面添加主表单')
#         # p.add_main_report(["测表10 全站仪放线记录表(SG)", "监表06 施工放样报验单", "监表04 机械设备报验单", "监表10-1 分项工程开工申请批复单"])  #  易重构体质
#         # p.log.info('>>> 质检评定 页面添加子表单')
#         # p.add_sub_report(['123'])  # 质检表单添加
#         # p.windows_handle('first')
#         # p.log.info('>>> 进入到 现场收方单 页面')
#         # p.men_choice('工程结构计量', out='null', second_name='现场收方单')
#         # # p.men_choice('电子档案', '1')
#         # # a = {'文件题名': '测试题名'}  # 电子档案新增文件信息字典
#         # # p.file_manage('LJ2', '施工记录', a)
#         # p.receipt_choice(data['标段'], data['分项工程'])
#         p.receipt_add(self.oracle_data.return_receipt())
#         # p.receipt_upload()
#         # p.men_choice('基础资料', out='null', second_name='WBS结构')
#         # p.bim_into('K1', 'K73+643-K73+673段V级浅埋洞身开挖')  # K73+643-K73+673段V级浅埋洞身开挖 右幅_8号桥台台帽_第1行_左起第1列_挡块
#         # p.bim_data_basic()
#         # p.bim_data_measure()
#         # p.bim_data_quality()
#         # p.bim_data_process()
#         # p.bim_data_change()
#         # p.bim_data_progress()
#
#     # 指令监控及执行
#     def execute_process(self):
#         dr = webdriver.Chrome()
#         # p1 = Process(target=start_rs)  # 必须加,号
#         # time.sleep(3)
#         # p1 = Process(target=self.shot, args=(dr,))
#         time.sleep(3)
#         a = '0'
#         while a == '0':
#             a = self.oracle_data.order_exe()[0]
#         p2 = threading.Thread(target=self.start_ui, args=(dr,))
#
#         # p1.start()
#         p2.start()
#         p2.join()
#         # if not p2.is_alive():
#         #     p1.terminate()
#         self.oracle_data.set_order_value()
#         self.execute_process()
#         # time.sleep(3)
#         # upload()
#
# if __name__ == '__main__':
#     ModuleRoom().execute_process()
#     # # p1 = Process(target=start_rs)  # 必须加,号
#     # # time.sleep(3)
#     # a = 0
#     # while a == 0:
#     #     b = OracleAction()
#     #     a = b.order_exe()
#     # p2 = Process(target=start_ui)
#     # #
#     # # p1.start()
#     # p2.start()
#     # p2.join()
#     # if not p2.is_alive():
#     #     p1.terminate()
#     # time.sleep(3)
#     # upload()
#
#
#
#
#
# # from jsgl_model_room.CommonLib.PrivateLib import PrivateModule
# # # from jsgl_model_room.ScreenCap.Record_Screen import RecordScreen
# # from jsgl_model_room.Jsgl_Ui.Oracle_Data import OracleAction
# # from selenium import webdriver
# # import time
# # import os
# # import threading
# # from multiprocessing import Process
# # # from jsgl_model_room.ScreenCap.Up_Load import upload
# #
# #
# # oracle_data = OracleAction()
# # # option = webdriver.ChromeOptions()
# # # option.add_argument('headless')
# # # option.add_argument('window-size=2560,1080')
# # # dr = webdriver.Chrome(chrome_options=option)
# # dr = webdriver.Chrome()
# #
# #
# # def clear_dir(path):
# #     """创建或清空目录"""
# #     if not os.path.isdir(path):
# #         os.mkdir(path)  # 创建目录
# #     else:  # 清空目录
# #         [os.remove(os.path.join(path, file_name)) for file_name in os.listdir(path)]
# #
# #
# # def shot():
# #     """循环截图函数"""
# #     img_dir = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture'
# #     i = 0
# #     clear_dir(img_dir)  # 清空目录
# #     while True:
# #         img_file = os.path.join(img_dir, f'{i}.png')
# #         try:
# #             dr.save_screenshot(img_file)
# #         except:
# #             return
# #         i += 1
# #
# # '''样板房一之 web端工序检查'''
# # def start_ui():
# #     # 真实数据存于字典data中
# #     data = {'标段':'K1', '分项工程':'K73+950-K74+025段超前小导管'}
# #     '''静默运行，设置屏幕大小'''
# #
# #     '''调用业务模块'''
# #     p = PrivateModule(dr)
# #     '''工序检查模块'''
# #     p.login()
# #     p.main_frame()
# #     p.log.info('>>> 进入到 工序检查 页面')
# #     p.men_choice('工序检查')
# #     p.log.info('>>> 工序检查 数据查看')
# #     p.details_read()
# #     p.log.info('>>> 返回到首页')
# #
# #     # p.log.info('>>> 进入到 工序检查 页面')
# #     # p.men_choice('工序检查')
# #     # p.log.info('>>> 工序检查 数据查看')
# #     # p.details_read()
# #     # p.log.info('>>> 返回到首页')
# #     # p.back_firstpage()
# #     # p.main_frame()
# #     # p.log.info('>>> 进入到 质检评定 页面')
# #     # p.men_choice('质检评定', '1')
# #     # p.quality_page('检验评定')
# #     # p.log.info('>>> 质检评定 页面选择标段及分项工程')
# #     # p.section_search(data['标段'], data['分项工程']) # K73+673-K73+703段V级深埋洞身开挖
# #     # p.log.info('>>> 质检评定 页面添加主表单')
# #     # p.add_main_report(["测表10 全站仪放线记录表(SG)", "监表06 施工放样报验单", "监表04 机械设备报验单", "监表10-1 分项工程开工申请批复单"])  #  易重构体质
# #     # p.log.info('>>> 质检评定 页面添加子表单')
# #     # p.add_sub_report(['123'])  # 质检表单添加
# #     # p.windows_handle('first')
# #     # p.log.info('>>> 进入到 现场收方单 页面')
# #     # p.men_choice('工程结构计量', out='null', second_name='现场收方单')
# #     # # p.men_choice('电子档案', '1')
# #     # # a = {'文件题名': '测试题名'}  # 电子档案新增文件信息字典
# #     # # p.file_manage('LJ2', '施工记录', a)
# #     # p.receipt_choice(data['标段'], data['分项工程'])
# #     # p.receipt_add(self.oracle_data.return_receipt())
# #     # p.receipt_upload()
# #     # p.men_choice('基础资料', out='null', second_name='WBS结构')
# #     # p.bim_into('K1', 'K73+643-K73+673段V级浅埋洞身开挖')  # K73+643-K73+673段V级浅埋洞身开挖 右幅_8号桥台台帽_第1行_左起第1列_挡块
# #     # p.bim_data_basic()
# #     # p.bim_data_measure()
# #     # p.bim_data_quality()
# #     # p.bim_data_process()
# #     # p.bim_data_change()
# #     # p.bim_data_progress()
# #
# #
# # # 指令监控及执行
# # def execute_process():
# #     # p1 = Process(target=start_rs)  # 必须加,号
# #     # time.sleep(3)
# #     p1 = Process(target=shot)
# #     time.sleep(3)
# #     a = 0
# #     while a == 0:
# #         a = oracle_data.order_exe()
# #     p2 = Process(target=start_ui)
# #
# #     p1.start()
# #     p2.start()
# #     # p2.join()
# #     if not p2.is_alive():
# #         p1.terminate()
# #     oracle_data.set_order_value()
# #     execute_process()
# #     # time.sleep(3)
# #     # upload()
# #
# # if __name__ == '__main__':
# #     execute_process()
# #     # # p1 = Process(target=start_rs)  # 必须加,号
# #     # # time.sleep(3)
# #     # a = 0
# #     # while a == 0:
# #     #     b = OracleAction()
# #     #     a = b.order_exe()
# #     # p2 = Process(target=start_ui)
# #     # #
# #     # # p1.start()
# #     # p2.start()
# #     # p2.join()
# #     # if not p2.is_alive():
# #     #     p1.terminate()
# #     # time.sleep(3)
# #     # upload()
# #
# #
