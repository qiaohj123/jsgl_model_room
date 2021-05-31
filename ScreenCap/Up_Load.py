from ftplib import FTP
import os
from time import sleep
# from jsgl_model_room.ScreenCap.Record_Screen import RecordScreen

host = '172.16.9.107'
port = 21
username = 'jg'
password = 'cgjgftpPro@2020'


def upload(file_dir, file_name):
    # file_path = '{}{}.mp4'.format(file_dir, file_name[0:10])   # 本地文件路径
    # file_name = 'video02.avi'
    file_path = 'D:\PycharmProjects\MyPoroject\jsgl_model_room\TestResult\K73+830-K7.mp4'
    print(file_path)
    ftp = FTP()
    # ftp.set_debuglevel(2)   # 开启2级调试模式，显示详细信息
    ftp.connect(host, port)
    ftp.login(username, password)
    ftp.cwd('./product/HOUSE')
    # ftp.delete('K73+830-K7.mp4')   # 删除已存在的文件
    print(ftp.dir())
    sleep(10)
    f = open(file_path, 'rb')
    # ftp.storbinary('STOR %s' % RecordScreen().file_name, f, 4096)  # 将本地文件上传到服务器，4096为缓冲区大小
    ftp.storbinary('STOR {}.mp4'.format(file_name), f, 4096)  # 将本地文件上传到服务器，4096为缓冲区大小
    f.close()
    print(ftp.dir())
    # ftp.set_debuglevel(0)   # 关闭调试模式
    ftp.quit()
#
# #
# upload('1', 'K73+830-K7')