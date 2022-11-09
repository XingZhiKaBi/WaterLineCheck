import os
import cv2
import math
import csv
import shutil

videoName = 'bandicam 2022-06-30 16-14-29-492.mp4'
txtName = 'bandicam 2022-06-30 16-14-29-492_Hongsheng Li.txt'
sysPath = ['./data/time_txt', './data/video', './data/train_csv']
fullPath = "/home/xr/AI/DATA/video"

originName = (txtName.split("_"))[0].replace(' ', '-')
# print(originName)
path = os.path.join(sysPath[0], txtName)
print("读取文件:", txtName)
file = open(path)
line = file.readlines()
numLine = int(len(line) / 2)
print(f'共{numLine}个标注')
i = 0
j = 0
label = [None for i in range(numLine)]
times = [None for i in range(numLine)]
"""
    读出标注和时间段
"""
while i < numLine * 2:
    label[j] = line[i].strip()
    times[j] = line[i + 1]
    j += 1
    i += 2

# print(label, "\n", times)

startTime = [None for i in range(numLine)]
endTime = [None for i in range(numLine)]

for i in range(numLine):
    time = times[i].split(" - ")
    endTime[i] = time[1].strip()
    startTime[i] = time[0]

# print(startTime)
# print(endTime)
file.close()

file = open(os.path.join(sysPath[2], (originName + ".csv")), mode="w", encoding="utf-8")
csvWriter = csv.writer(file)
print(f'创建文件：{originName + ".csv"}')

path = os.path.join(sysPath[1], videoName)
cap = cv2.VideoCapture(path)
print("读取视频:", videoName)

FPS = cap.get(cv2.CAP_PROP_FPS)  # FPS=30.0

size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# 1920*1080

# totalFrame = cap.get(cv2.CAP_PROP_FRAME_COUNT) # 获取总帧数
# print("总帧数为：", totalFrame)

"""将文件夹清空"""
# shutil.rmtree(sysPath[1] + "/positive/")
# os.mkdir(sysPath[1] + "/positive/")
# shutil.rmtree(sysPath[1] + "/negative/")
# os.mkdir(sysPath[1] + "/negative/")
# print("清空文件夹！")

for i in range(40, numLine):
    """
        定义剪切视频所需要的参数
    """
    time = startTime[i].split(":")
    frameStart = int((float(time[0]) * 3600 + float(time[1]) * 60 + float(time[2])) * FPS)
    # print(frameStart)
    time = endTime[i].split(":")
    frameEnd = math.ceil((float(time[0]) * 3600 + float(time[1]) * 60 + float(time[2])) * FPS)
    # print(frameEnd)

    """
        按照标注分类
    """
    if label[i] == "合格":
        videoWriter = cv2.VideoWriter(sysPath[1] + "/positive/" + originName + "-" + str(i + 1) + ".mp4",
                                      cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                                      FPS, (320, 240))
        csvWriter.writerow([fullPath + "/positive/" + originName + "-" + str(i + 1) + ".mp4 1"])
    elif label[i] == "不合格":
        videoWriter = cv2.VideoWriter(sysPath[1] + "/negative/" + originName + "-" + str(i + 1) + ".mp4",
                                      cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                                      FPS, (320, 240))
        csvWriter.writerow([fullPath + "/negative/" + originName + "-" + str(i + 1) + ".mp4 0"])

    """
        开始裁剪
    """
    print(f'正在裁剪[{i + 1}/{numLine}]-----{label[i]}')

    cap.set(cv2.CAP_PROP_POS_FRAMES, frameStart)
    # 设置起始帧
    COUNT = frameStart

    while True:
        success, frame = cap.read()
        # print(COUNT)
        if success:
            COUNT += 1
            if frameEnd >= COUNT > frameStart:
                frame1 = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_LINEAR)
                videoWriter.write(frame1)
        if COUNT > frameEnd:
            print("done...")
            break

    # if i == 39:
    #     # 设置断点，控制运行时间
    #     break

file.close()
