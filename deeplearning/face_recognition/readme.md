## 人脸识别相关
突发奇想想给陈先生做一组表情包，但是不会P图的我就想到了写代码呀

首先我利用网上一些包写了一些人脸识别的代码，以方便后期我需要获取人脸特征点
dlibface.py   使用dlib进行人脸识别

opencv.py     利用opencv 进行人脸识别

face_detection.py   利用开源包face_recognition人脸识别

face_recog.py  利用开源包face_recognition人脸验证

face_video.py  视频人脸验证

### Procrustes analysis
人脸识别之后我看了下Procrustes analysis
   普氏分析法是一种用来分析形状分布的方法。数学上来讲，就是不断迭代，寻找标准形状(canonical shape)，并利用最小二乘法寻找每个样本形状到这个标准形状的仿射变化方式。（可参照维基百科的GPA算法）
   具体可以参考如下链接：https://blog.csdn.net/tinyzhao/article/details/53169818
https://github.com/mattzheng/Face_Swapping
http://python.jobbole.com/82546/
实现换脸主要是以下几个步骤
1借助 dlib 库检测出图像中的脸部特征
2计算将第二张图像脸部特征对齐到一张图像脸部特征的变换矩阵
3综合考虑两张照片的面部特征获得合适的面部特征掩码
4根据第一张图像人脸的肤色修正第二张图像
5通过面部特征掩码拼接这两张图像
6保存图像

