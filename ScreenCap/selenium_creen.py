# from selenium import webdriver
# import threading
# import os
# import cv2
# import time
# from PIL import Image
# from jsgl_model_room.CommonLib.PrivateLib import PrivateModule
# from selenium import webdriver
# import glob
#
#
# path = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture'
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
# def shot(dr, img_dir):
#     """循环截图函数"""
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
#
# # Selenium操作
# img_dir = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture'  # 临时图片目录
#
#
# option = webdriver.ChromeOptions()
# option.add_argument('headless')
# option.add_argument('window-size=2560,1080')
# dr = webdriver.Chrome(chrome_options=option)
#
#
# t = threading.Thread(target=shot, args=(dr, img_dir))  # 新建线程
# t.start()  # 启动截图线程
#
# try:
#     data = {'标段':'K1', '分项工程':'K73+950-K74+025段超前小导管'}
#     p = PrivateModule(dr)
#     # 样板房流程-A
#     p.login()
#     p.main_frame()
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
#     p.log.info('>>> 进入到 现场收方单 页面')
#     p.men_choice('工程结构计量', out='null', second_name='现场收方单')
#     # p.men_choice('电子档案', '1')
#     # a = {'文件题名': '测试题名'}  # 电子档案新增文件信息字典
#     # p.file_manage('LJ2', '施工记录', a)
#     p.receipt_choice(data['标段'], data['分项工程'])
#     # p.receipt_add(self.oracle_data.return_receipt())
#     # p.receipt_upload()
# except Exception as e:
#     pass
#
# # # 图片拼接成gif
# # img_list = os.listdir(img_dir)  # 列出目录所有图片
# # img_list.sort(key=lambda x: int(x[:-4]))  # 排序
# #
# # first_img = Image.open(os.path.join(img_dir, img_list[0]))  # 第一张图片对象
# # else_imgs = [Image.open(os.path.join(img_dir, img)) for img in img_list[1:]]  # 剩余图片对象
# #
# # first_img.save("record.gif", append_images=else_imgs,
# #                duration=100,  # 每张图片的过渡时间
# #                save_all=True,) # 拼接保存，如果想要循环播放可以加上loop=0
#
# path_file_number = len(glob.glob('D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\*.png'))
# path_file_number2 = len(glob.glob('D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\img\*.png'))
# video_write = cv2.VideoWriter(r'D:\PycharmProjects\MyPoroject\test.mp4', -1, 5, (2560, 1080))  # 参数3是帧数，参数4是图片尺寸
# img_array = []
#
# for filename in [r'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\{0}.png'.format(i) for i in range(50)]:
#     img = cv2.imread(filename)
#     if img is None:
#         print(filename + " is error!")
#         continue
#     img_array.append(img)
#
# for filename2 in [r'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\img\{0}.png'.format(i) for i in range(47, 149)]:
#     img2 = cv2.imread(filename2)
#     if img2 is None:
#         print(filename2 + " is error!")
#         continue
#     img_array.append(img2)
#
#
# for i in range(150):
#     video_write.write(img_array[i])
#
#
#
from selenium import webdriver
import threading
from multiprocessing import Process
import os
import cv2
import time
import random
from PIL import Image
from jsgl_model_room.CommonLib.PrivateLib import PrivateModule
from jsgl_model_room.Jsgl_Ui.Oracle_Data import OracleAction
from selenium import webdriver
import glob
import inspect
import ctypes


def clear_dir(path):
    """创建或清空目录"""
    if not os.path.isdir(path):
        os.mkdir(path)  # 创建目录
    else:  # 清空目录
        [os.remove(os.path.join(path, file_name)) for file_name in os.listdir(path)]


def shot(dr, img_dir, start_num):
    """循环截图函数"""
    i = 0
    clear_dir(img_dir)  # 清空目录
    while True:
        img_file = os.path.join(img_dir, f'{start_num}.png')
        try:
            dr.save_screenshot(img_file)
        except:
            return
        start_num += 1


# Selenium操作
img_dir1 = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p1'  # 临时图片目录
img_dir2 = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p2'
img_dir3 = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p3'
img_dir4 = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p4'
img_dir5 = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p5'

option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_argument('window-size=2560,1080')
# dr = webdriver.Chrome(chrome_options=option)
data = {'标段':'K1', '分项工程':'K73+950-K74+025段超前小导管'}
# dr1 = webdriver.Chrome(chrome_options=option)
# dr2 = webdriver.Chrome(chrome_options=option)
# dr3 = webdriver.Chrome(chrome_options=option)
# dr4 = webdriver.Chrome(chrome_options=option)
# dr5 = webdriver.Chrome(chrome_options=option)

dr1 = webdriver.Chrome()
# dr2 = webdriver.Chrome()
# dr3 = webdriver.Chrome()
# dr4 = webdriver.Chrome()
# dr5 = webdriver.Chrome()




"""样板房一之 web端工序检查"""


def room_one():
    try:
        p = PrivateModule(dr1)
        p.login()
        p.main_frame()
        p.log.info('>>> 进入到 工序检查 页面')
        p.men_choice('工序检查')
        p.log.info('>>> 工序检查 数据查看')
        p.details_read()
        p.log.info('>>> 返回到首页')
        p.back_firstpage()
    except Exception as e:
        dr1.quit()


"""样板房一之 质检评定模块"""


def room_two():
    try:

        p = PrivateModule(dr2)
        p.login()
        p.main_frame()
        p.log.info('>>> 进入到 质检评定 页面')
        p.men_choice('质检评定', '1')
        p.quality_page('检验评定')
        p.log.info('>>> 质检评定 页面选择标段及分项工程')
        p.section_search(data['标段'], data['分项工程'])  # K73+673-K73+703段V级深埋洞身开挖
        p.log.info('>>> 质检评定 页面添加主表单')
        p.add_main_report(["测表10 全站仪放线记录表(SG)", "监表06 施工放样报验单", "监表04 机械设备报验单", "监表10-1 分项工程开工申请批复单"])  #  易重构体质
        p.log.info('>>> 质检评定 页面添加子表单')
        p.add_sub_report(['123'])  # 质检表单添加
        # 还差一个关闭窗口功能
    except Exception as e:
        dr2.quit()

"""样板房一之 现场收方单模块"""


# def room_three(section_data, list_data):
#     p = PrivateModule(dr3)
#     p.login()
#     p.main_frame()
#     p.log.info('>>> 进入到 现场收方单 页面')
#     p.men_choice('工程结构计量', out='null', second_name='现场收方单')
#     p.receipt_choice(section_data['标段'], section_data['分项结构'])
#     p.receipt_add(list_data)
#     p.receipt_upload()
#
#
# """样板房一之 中间计量&中期支付证书模块"""
#
#
# def room_four(section_data):
#     try:
#         p = PrivateModule(dr4)
#         p.login()
#         p.main_frame()
#         p.log.info('>>> 进入到 中间计量 页面')
#         p.men_choice('工程结构计量', out='null', second_name='中间计量')
#         p.log.info('>>> 中间计量页面标段结构选择')
#         p.measure_choice(section_data['标段'], section_data['分项结构'])
#         p.log.info('>>> 新增中间计量')
#         p.measure_increase()
#         p.log.info('>>> 返回到首页')
#         p.back_firstpage()
#         p.main_frame()
#         p.log.info('>>> 进入到 工程结构中期支付证书 页面')
#         p.men_choice('工程结构计量', out='null', second_name='中期支付证书')
#         p.section_id(section_data['标段'])
#         p.log.info('>>> 支付证书上报')
#         p.upload_certificate_file()
#     except Exception as e:
#         dr4.quit()
#
#
# """样板房一之 BIM数据融合模块"""
#
#
# def room_five(section_data):
#     try:
#
#         p = PrivateModule(dr5)
#         p.login()
#         p.main_frame()
#         p.log.info('>>> 进入到 WBS结构 页面')
#         p.men_choice('基础资料', out='null', second_name='WBS结构')
#         p.bim_into(section_data['标段'], section_data['分项结构'])  # K73+643-K73+673段V级浅埋洞身开挖 右幅_8号桥台台帽_第1行_左起第1列_挡块
#         p.bim_data_basic()
#         p.bim_data_measure()
#         p.bim_data_quality()
#         p.bim_data_process()
#         p.bim_data_change()
#         p.bim_data_progress()
#     except Exception as e:
#         dr5.quit()
#

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    print('tid%s'%(tid))
    print(type(tid))
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    print('res%s'%(res))
    print(type(res))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def get_thread(thread):
    t = thread
    pid = os.getpid()
    print(t.name, t.ident, t.is_alive())
    print('22222')
    time.sleep(5)
    # ts = threading.enumerate()
    # print('ts%s'%(ts))
    # print('------- Running threads On Pid: %d -------' %(pid))
    # for t in ts:
    #     print(t.name, t.ident, t.is_alive())
    #     if t.name == 'test1':
    #         print('I am go dying! Please take care of yourself and drink more hot water!')
    #         stop_thread(t)



def execute_process():
    oracle_data = OracleAction()
    section_data = oracle_data.data_to_dict(item_list='项目标段')
    list_data = oracle_data.data_to_dict(item_list='收方单')
    a = '0'
    while a == '0':
        a = oracle_data.order_exe()[0]  # ['1', '9582F0F1-9687-41FD-A030-E12F43F0E04E']
        print(a)
# ------------------------------------------------------------------------------------
    time.sleep(3)
    t1 = threading.Thread(daemon=True, name='test1', target=shot, args=(dr1, img_dir1, 1))  # 新建线程
    t2 = threading.Thread(daemon=True, name='test2', target=room_one)  # 新建业务线程

    t1.start()  # 启动截图线程1
    t2.start()  # 启动业务线程1
# ------------------------------------------------------------------------------------
#     t3 = threading.Thread(daemon=True, name='test3', target=shot, args=(dr2, img_dir2, 60))  # 新建线程
#     t3.start()  # 启动截图线程2
#
#     t4 = threading.Thread(daemon=True, name='test4', target=room_two)  # 新建业务线程
#     t4.start()  # 启动业务线程2

    t2.join()
    # t3.join()
    # t4.join()
# # ------------------------------------------------------------------------------------
#
#     t5 = threading.Thread(target=shot, args=(dr3, img_dir3, 200))  # 新建线程
#     t5.start()  # 启动截图线程2
#
#     t6 = threading.Thread(target=room_three, args=(section_data, list_data))  # 新建业务线程
#     t6.start()  # 启动业务线程2
# # ------------------------------------------------------------------------------------
#
#     t7 = threading.Thread(target=shot, args=(dr4, img_dir4, 350))  # 新建线程
#     t7.start()  # 启动截图线程2
#
#     t8 = threading.Thread(target=room_four, args=(section_data,))  # 新建业务线程
#     t8.start()  # 启动业务线程2
# # ------------------------------------------------------------------------------------
#
#     t9 = threading.Thread(target=shot, args=(dr5, img_dir5, 500))  # 新建线程
#     t9.start()  # 启动截图线程2
#
#     t10 = threading.Thread(target=room_five, args=(section_data,))  # 新建业务线程
#     t10.start()  # 启动业务线程2
# # ------------------------------------------------------------------------------------ n

    # get_thread(t1)
    # get_thread(t2)
    oracle_data.set_order_value()
    execute_process()



if __name__ == '__main__':
    execute_process()


'''合成视频并上传文件'''

# path_file_number1 = len(glob.glob('D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p1\*.png'))
# path_file_number2 = len(glob.glob('D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p2\*.png'))
# path_file_number3 = len(glob.glob('D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p3\*.png'))
# path_file_number4 = len(glob.glob('D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p4\*.png'))
# path_file_number5 = len(glob.glob('D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p5\*.png'))
#
# video_write = cv2.VideoWriter(r'D:\PycharmProjects\MyPoroject\test.mp4', -1, 5, (2560, 1080))  # 参数3是帧数，参数4是图片尺寸
# img_array = []
#
# for filename in [r'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p1\{0}.png'.format(i) for i in range(path_file_number1)]:
#     img = cv2.imread(filename)
#     if img is None:
#         print(filename + " is error!")
#         continue
#     img_array.append(img)
#
# for filename2 in [r'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p2\{0}.png'.format(i) for i in range(47, 149)]:
#     img2 = cv2.imread(filename2)
#     if img2 is None:
#         print(filename2 + " is error!")
#         continue
#     img_array.append(img2)
#
# for filename in [r'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p3\{0}.png'.format(i) for i in range(50)]:
#     img = cv2.imread(filename)
#     if img is None:
#         print(filename + " is error!")
#         continue
#     img_array.append(img)
#
# for filename in [r'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p4\{0}.png'.format(i) for i in range(50)]:
#     img = cv2.imread(filename)
#     if img is None:
#         print(filename + " is error!")
#         continue
#     img_array.append(img)
#
# for filename in [r'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\p5\{0}.png'.format(i) for i in range(50)]:
#     img = cv2.imread(filename)
#     if img is None:
#         print(filename + " is error!")
#         continue
#     img_array.append(img)
#
# for i in range(150):
#     video_write.write(img_array[i])
#


