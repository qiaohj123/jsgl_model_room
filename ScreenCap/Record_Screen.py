import numpy as np
import cv2
from PIL import ImageGrab
import glob
import threading
import os


class RecordScreen:
    def __init__(self, fps=10, start=0, end=600):
        self.fps = fps
        self.start = start
        self.end = end
        self.file_name = 'ModuleRoom.flv'

    def screen_action(self):
        cur_screen = ImageGrab.grab()  # 获取屏幕对象
        height, width = cur_screen.size
        video = cv2.VideoWriter(self.file_name, cv2.VideoWriter_fourcc('F', 'L', 'V', '1'), self.fps, (height, width))  # XVID(*'XVID')
        image_num = 0
        while True:
            image_num += 1
            capture_image = ImageGrab.grab()  # 抓取屏幕
            frame = cv2.cvtColor(np.array(capture_image), cv2.COLOR_RGB2BGR)
            # 显示无图像的窗口
            cv2.imshow('capturing', np.zeros((1, 255), np.uint8))
            # 控制窗口显示位置，方便通过按键方式退出
            cv2.moveWindow('capturing', height - 100, width - 100)
            if image_num > self.fps * self.start:
                video.write(frame)
            # 退出条件
            if cv2.waitKey(50) == ord('q') or image_num > self.fps * self.end:
                break
        video.release()
        cv2.destroyAllWindows()


class RecordScreenSet:
    path = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture'

    def clear_dir(self, path):
        """创建或清空目录"""
        if not os.path.isdir(path):
            os.mkdir(path)  # 创建目录
        else:  # 清空目录
            [os.remove(os.path.join(path, file_name)) for file_name in os.listdir(path)]

    def shot(self, dr, img_dir):
        """循环截图函数"""
        i = 0
        self.clear_dir(img_dir)  # 清空目录
        while True:
            img_file = os.path.join(img_dir, f'{i}.png')
            try:
                dr.save_screenshot(img_file)
            except:
                return
            i += 1

    # Selenium操作
    img_dir = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture'  # 临时图片目录

    # option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    # option.add_argument('window-size=2560,1080')
    # dr = webdriver.Chrome(chrome_options=option)



    try:
        pass
    except Exception as e:
        pass
    path_file_number = len(glob.glob('D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\*.png'))
    path_file_number2 = len(glob.glob('D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\img\*.png'))
    video_write = cv2.VideoWriter(r'D:\PycharmProjects\MyPoroject\test.mp4', -1, 5, (2560, 1080))  # 参数3是帧数，参数4是图片尺寸
    img_array = []

    for filename in [r'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\picture\{0}.png'.format(i) for i in
                     range(50)]:
        img = cv2.imread(filename)
        if img is None:
            print(filename + " is error!")
            continue
        img_array.append(img)

    for filename2 in [r'D:\PycharmProjects\MyPoroject\jsgl_model_room\ScreenCap\img\{0}.png'.format(i) for i in
                      range(47, 149)]:
        img2 = cv2.imread(filename2)
        if img2 is None:
            print(filename2 + " is error!")
            continue
        img_array.append(img2)

    for i in range(150):
        video_write.write(img_array[i])


