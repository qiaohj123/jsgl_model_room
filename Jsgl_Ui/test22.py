# # from moviepy.editor import *
# # # import os
# # #
# # video = VideoFileClip('ModuleRoom.flv')
# # audio = AudioFileClip('新录音.m4a')
# # video2 = video.set_audio(CompositeAudioClip([video.audio, audio]))
# # video2.write_videofile('test.flv')
# # # print(video)
# # # audio_clip = CompositeVideoClip([video])
# # # print(audio_clip)
# # # audio_clip.write_videofile('te334t.avi')
# # #
# # #
# # # # # # video.write_videofile('new.avi')
# # # # def convert_avi_to_mp4():
# # # #     os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}.mp4'".format(input = 'ModuleRoom.avi', output = 'tstw'))
# # # #
# # # # convert_avi_to_mp4()
#
# import subprocess
#
#
# # 给视频添加背景声音
# def get_image():
#     video_path = 'aaaa.avi'
#     image_path = 'mama.m4a'
#     out_path = 'out2.avi'
#
#     cmd_str = f'ffmpeg -i {video_path} -i {image_path} -t 7.1 -c copy {out_path}'
#     subprocess.run(cmd_str, encoding="utf-8" , shell=True)
#
#
# get_image()
# test1 = ['a', 'b', 'c']
# test2 = [['1', '2'], ['3', '4'], ['5', '6'], ['7', '8'], ['9', '10'], ['11', '12']]
# test1_num = len(test1)+1
# for i in range(1, test1_num):
#     test2[i * 2 - 2].append(test1[i - 1])
#     test2[i * 2 - 1].append(test1[i - 1])
# print(test2)
# 如果 a+b+c=1000，且 a^2 + b^2 = c^2（a,b,c 为自然数），如何求出所有a、b、c可能的组合?

#
def funA(fn):
    # 定义一个嵌套函数
    print("Python:")

    def say(arc):
        print("Python:", arc)

    return say


def funB():
    print("funB()11111:")


fund = funA(funB)
fund("http://c.biancheng.net/python")