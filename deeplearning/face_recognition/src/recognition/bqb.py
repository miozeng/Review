import cv2
import dlib
import numpy

import sys

PREDICTOR_PATH = "D:\\Program Files\\python3.6\\Lib\\site-packages\\dlib-data\\shape_predictor_68_face_landmarks.dat"

# 图像放缩因子
SCALE_FACTOR = 1 
FEATHER_AMOUNT = 11

FACE_POINTS = list(range(17, 68))# 脸
MOUTH_POINTS = list(range(48, 61))# 嘴巴
RIGHT_BROW_POINTS = list(range(17, 22)) # 右眉毛
LEFT_BROW_POINTS = list(range(22, 27))
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
NOSE_POINTS = list(range(27, 35))
JAW_POINTS = list(range(0, 17))# 下巴

# Points used to line up the images.选取了左右眉毛、眼睛、鼻子和嘴巴位置的特征点索引
ALIGN_POINTS = (LEFT_BROW_POINTS + RIGHT_EYE_POINTS + LEFT_EYE_POINTS +
                               RIGHT_BROW_POINTS + NOSE_POINTS + MOUTH_POINTS)

# 选取用于叠加在第一张脸上的第二张脸的面部特征
# 特征点包括左右眼、眉毛、鼻子和嘴巴
OVERLAY_POINTS = [
    LEFT_EYE_POINTS + RIGHT_EYE_POINTS + LEFT_BROW_POINTS + RIGHT_BROW_POINTS,
    NOSE_POINTS + MOUTH_POINTS,
]

# Amount of blur to use during colour correction, as a fraction of the
# 定义用于颜色校正的模糊量，
COLOUR_CORRECT_BLUR_FRAC = 0.6

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

class TooManyFaces(Exception):
    pass

class NoFaces(Exception):
    pass

#将图片的68个特征点提取出来后，将高度和宽度转换为x，y的二维矩阵
def get_landmarks(im):
    rects = detector(im, 1)

    if len(rects) > 1:
        raise TooManyFaces
    if len(rects) == 0:
        raise NoFaces

    return numpy.matrix([[p.x, p.y] for p in predictor(im, rects[0]).parts()])

# 人脸关键点，画图函数
def annotate_landmarks(im, landmarks):
    im = im.copy()
    for idx, point in enumerate(landmarks):
        pos = (point[0, 0], point[0, 1])
        cv2.putText(im, str(idx), pos,
                    fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                    fontScale=0.4,
                    color=(0, 0, 255))
        cv2.circle(im, pos, 3, color=(0, 255, 255))
    return im
#读取图片并获取关键点
def read_im_and_landmarks(fname):
      # 以 RGB 模式读取图像
    im = cv2.imread(fname, cv2.IMREAD_COLOR)
    #缩放
    im = cv2.resize(im, (im.shape[1] * SCALE_FACTOR,
                         im.shape[0] * SCALE_FACTOR))
    s = get_landmarks(im)

    return im, s



# 绘制凸多边形
def draw_convex_hull(im, points, color):
    points = cv2.convexHull(points)
    cv2.fillConvexPoly(im, points, color=color)
#获取面部特征部分（眉毛、眼睛、鼻子以及嘴巴）的图像掩码
def get_face_mask(im, landmarks):
    im = numpy.zeros(im.shape[:2], dtype=numpy.float64)

    for group in OVERLAY_POINTS:
        draw_convex_hull(im,
                         landmarks[group],
                         color=1)

    im = numpy.array([im, im, im]).transpose((1, 2, 0))
    # 应用高斯模糊
    im = (cv2.GaussianBlur(im, (FEATHER_AMOUNT, FEATHER_AMOUNT), 0) > 0) * 1.0
    im = cv2.GaussianBlur(im, (FEATHER_AMOUNT, FEATHER_AMOUNT), 0)

    return im

#Procrustes analysis
def transformation_from_points(points1, points2):

    points1 = points1.astype(numpy.float64)
    points2 = points2.astype(numpy.float64)

    c1 = numpy.mean(points1, axis=0)
    c2 = numpy.mean(points2, axis=0)
    points1 -= c1
    points2 -= c2

    s1 = numpy.std(points1)
    s2 = numpy.std(points2)
    points1 /= s1
    points2 /= s2

    U, S, Vt = numpy.linalg.svd(points1.T * points2)

    R = (U * Vt).T

    return numpy.vstack([numpy.hstack(((s2 / s1) * R,
                                       c2.T - (s2 / s1) * R * c1.T)),
                         numpy.matrix([0., 0., 1.])])



def warp_im(im, M, dshape):
    output_im = numpy.zeros(dshape, dtype=im.dtype)
      # 仿射函数，能对图像进行几何变换
    # 三个主要参数，第一个输入图像，第二个变换矩阵 np.float32 类型，第三个变换之后图像的宽高
    cv2.warpAffine(im,
                   M[:2],
                   (dshape[1], dshape[0]),
                   dst=output_im,
                   borderMode=cv2.BORDER_TRANSPARENT,
                   flags=cv2.WARP_INVERSE_MAP)
    return output_im
#均匀颜色
def correct_colours(im1, im2, landmarks1):
    blur_amount = COLOUR_CORRECT_BLUR_FRAC * numpy.linalg.norm(
                              numpy.mean(landmarks1[LEFT_EYE_POINTS], axis=0) -
                              numpy.mean(landmarks1[RIGHT_EYE_POINTS], axis=0))
    blur_amount = int(blur_amount)
    if blur_amount % 2 == 0:
        blur_amount += 1
    im1_blur = cv2.GaussianBlur(im1, (blur_amount, blur_amount), 0)
    im2_blur = cv2.GaussianBlur(im2, (blur_amount, blur_amount), 0)

    # Avoid divide-by-zero errors.
    a =128 * (im2_blur <= 1.0)
    print(a.dtype)
    print(im2_blur.dtype)
    data = a.astype('uint8')
    im2_blur += data

    return (im2.astype(numpy.float64) * im1_blur.astype(numpy.float64) /
                                                im2_blur.astype(numpy.float64))
def Switch_face(Base_path,cover_path):
    # 获取图像与特征点
    im1, landmarks1 = read_im_and_landmarks(Base_path)  # 底图
    im2, landmarks2 = read_im_and_landmarks(cover_path)  # 贴上来的图
    
    # 选取两组图像特征矩阵中所需要的面部部位
    # 计算转换信息，返回变换矩阵
    M = transformation_from_points(landmarks1[ALIGN_POINTS],
                                   landmarks2[ALIGN_POINTS])
    # 获取 im2 的面部掩码
    mask = get_face_mask(im2, landmarks2)
    # 将 im2 的掩码进行变化，使之与 im1 相符
    warped_mask = warp_im(mask, M, im1.shape)
    # 将二者的掩码进行连通
    combined_mask = numpy.max([get_face_mask(im1, landmarks1), warped_mask],
                              axis=0)
     # 将第二幅图像调整到与第一幅图像相符
    warped_im2 = warp_im(im2, M, im1.shape)
     # 将 im2 的皮肤颜色进行修正，使其和 im1 的颜色尽量协调
    warped_corrected_im2 = correct_colours(im1, warped_im2, landmarks1)
    # 组合图像，获得结果
    output_im = im1 * (1.0 - combined_mask) + warped_corrected_im2 * combined_mask
    return output_im

Base_path = 'D:\\test2\\bqb\\test.jpg'
cover_path = 'D:\\test2\\mm.jpg'
output_im = Switch_face(Base_path,cover_path)
cv2.imwrite('D:\\test2\\bqb\\output4.jpg', output_im)


