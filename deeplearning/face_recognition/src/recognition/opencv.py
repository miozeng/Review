import cv2
import matplotlib.pyplot as plt
import numpy as np

# 在使用OpenCV的人脸检测之前，需要一个人脸训练模型，格式是xml的，
# 我们这里使用OpenCV提供好的人脸分类模型xml，下载地址：https://github.com/opencv/opencv/tree/master/data/haarcascades 可全部下载到本地
filepath = "D:\\test2\\C360.jpg"
img = cv2.imread(filepath)  # readfile 

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # conver to gray

# OpenCV人脸识别分类器
classifier = cv2.CascadeClassifier(
    "D:\Program Files\python3.6\Lib\site-packages\opencv-master\data\haarcascades\haarcascade_frontalface_default.xml"
)

color = (0, 255, 0)  # 定义绘制颜色
# 调用识别人脸
faceRects = classifier.detectMultiScale(
    gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
if len(faceRects):  # 大于0则检测到人脸
    for faceRect in faceRects:  # 单独框出每一张人脸
        x, y, w, h = faceRect
        # 框出人脸
        cv2.rectangle(img, (x, y), (x + h, y + w), color, 2)
        # 左眼
        cv2.circle(img, (x + w // 4, y + h // 4 + 30), min(w // 8, h // 8),
                   color)
        # 右眼
        cv2.circle(img, (x + 3 * w // 4, y + h // 4 + 30), min(w // 8, h // 8),
                   color)
        # 嘴巴
        cv2.rectangle(img, (x + 3 * w // 8, y + 3 * h // 4),
                      (x + 5 * w // 8, y + 7 * h // 8), color)

cv2.imshow("image", img)  # 显示图像
c = cv2.waitKey(10)

cv2.waitKey(0)
cv2.destroyAllWindows()
