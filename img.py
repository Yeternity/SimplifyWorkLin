# 在这里模式图（白色衣服图）称为pattern（pa），pa中白色衣服称为zone（zo），其余成为background（bg）
# zone中需要贴图的称为accessible zone（azo）
# zone中不需要贴图的成为forbidden zone（fzo）
# 贴图称为sticker
# select zone(szo)图为区域选择图，分为蓝色（贴图部分）和红色（不贴图部分）
import cv2
import numpy as np
from blend_modes import multiply
import skimage.exposure


# 羽化，消除锯齿
def feather(img):
    a = img[:, :, 3]

    # blur alpha channel
    ab = cv2.GaussianBlur(a, (0, 0), sigmaX=2, sigmaY=2, borderType=cv2.BORDER_DEFAULT)

    # stretch so that 255 -> 255 and 127.5 -> 0
    aa = skimage.exposure.rescale_intensity(ab, in_range=(127.5, 255), out_range=(0, 255))
    return aa


def get_mask_not_red(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    return mask


def get_mask_not_blue(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([100, 43, 46])
    upper_red = np.array([124, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    return mask


# 改变sticker图的大小以适应pa，自动将pa放在sticker正中间
def resize_sticker(pa, sticker):
    # get pa's max dimension
    hh, ww = pa.shape[:2]
    maxwh = max(hh, ww)

    # get sticker's size and minimum dimension
    ht, wd = sticker.shape[:2]
    minwh = min(ht, wd)

    # resize pattern so minimum dimension is size of largest dimension of tshirt image
    scale = maxwh / minwh
    sticker_enlarge = cv2.resize(sticker, dsize=(0, 0), fx=scale, fy=scale)
    nht, nwd = sticker_enlarge.shape[:2]

    # limit resized sticker to size of pa， put pa in the center of sticker
    hc = int((nht - hh) // 2)
    wc = int((nwd - ww) // 2)
    sticker_enlarge = sticker_enlarge[hc:hc + hh, wc:wc + ww]
    return sticker_enlarge


def stick_complex(path_pa, path_szo, path_sticker):
    img_pa = cv2.imread(path_pa, cv2.IMREAD_UNCHANGED)
    img_szo = cv2.imread(path_szo, cv2.IMREAD_COLOR)
    img_sticker = cv2.imread(path_sticker, cv2.IMREAD_UNCHANGED)

    # 图片大小调整
    resized_img_sticker = resize_sticker(img_pa, img_sticker)

    # multiply blend mode（混合图片，贴图同时保留衣服阴影）
    if resized_img_sticker.shape[2] != 4:
        resized_img_sticker = cv2.cvtColor(resized_img_sticker, cv2.COLOR_BGR2BGRA)
    img_blend = multiply(img_pa.astype(float), resized_img_sticker.astype(float), 1.0).astype(np.uint8)

    # # 根据bg白色和衣服灰色的微小差别，取bg mask（遮掩bg，露出zo）
    # gray = cv2.cvtColor(img_pa, cv2.COLOR_BGRA2GRAY)
    # # 大于245的点，置0（黑），否则置255（白），用于白色背景图
    # mask_bg = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY_INV)[1]

    # 蓝色区域（贴图部分），取fzo mask（遮掩不贴图的区域）
    mask_not_azo = get_mask_not_blue(img_szo)
    mask_azo = cv2.bitwise_not(mask_not_azo)

    # 红色区域（不贴图部分），取fzo mask（遮掩不贴图的区域）
    mask_not_fzo = get_mask_not_red(img_szo)
    mask_fzo = cv2.bitwise_not(mask_not_fzo)

    # 抠出蓝色区域（贴图部分）
    azo = cv2.bitwise_and(img_blend, img_blend, mask=mask_not_azo)
    # # 抠出红色区域（不贴图部分）
    fzo = cv2.bitwise_and(img_pa, img_pa, mask=mask_not_fzo)

    # 羽化（消除贴图部分边缘锯齿）
    azo[:, :, 3] = feather(azo)

    # # 由于羽化改变了部分像素点，因此根据羽化结果重新取mask
    # # 大于0的点，置0（黑），否则置255（白），用于白色背景图
    # alpha = azo[:, :, 3]
    # mask_azo = cv2.threshold(alpha, 0, 255, cv2.THRESH_BINARY_INV)[1]
    # fzo = cv2.bitwise_and(fzo, fzo, mask=mask_azo)

    # 合并贴图部分和不贴图部分
    zo_blend = cv2.add(azo, fzo)

    # 将透明部分变成白色
    trans_mask = zo_blend[:, :, 3] == 0
    result = zo_blend.copy()
    result[trans_mask] = [255, 255, 255, 255]

    # result = cv2.GaussianBlur(result, (5, 5), sigmaX=2, sigmaY=2, borderType=cv2.BORDER_WRAP)  # 高斯滤波

    return result


def stick_simple(path_pa, path_szo, path_sticker):
    img_pa = cv2.imread(path_pa, cv2.IMREAD_UNCHANGED)
    img_szo = cv2.imread(path_szo, cv2.IMREAD_UNCHANGED)
    img_sticker = cv2.imread(path_sticker, cv2.IMREAD_UNCHANGED)

    # 图片大小调整
    resized_img_sticker = resize_sticker(img_pa, img_sticker)

    # # 根据bg白色和衣服灰色的微小差别，取bg mask（遮掩bg，露出zo）
    # gray = cv2.cvtColor(img_pa, cv2.COLOR_BGRA2GRAY)
    # # 大于245的点，置0（黑），否则置255（白），用于白色背景图
    # mask_bg = cv2.threshold(gray, 253, 255, cv2.THRESH_BINARY_INV)[1]

    mask_bg = get_mask_not_blue(img_szo)

    # multiply blend mode（混合图片，贴图同时保留衣服阴影）
    if resized_img_sticker.shape[2] != 4:
        resized_img_sticker = cv2.cvtColor(resized_img_sticker, cv2.COLOR_BGR2BGRA)
    img_blend = multiply(img_pa.astype(float), resized_img_sticker.astype(float), 1.0).astype(np.uint8)

    # 抠出贴图后的衣服(混合后)
    zo_blend = cv2.bitwise_and(img_blend, img_blend, mask=mask_bg)

    # 羽化（消除贴图部分边缘锯齿）
    zo_blend[:, :, 3] = feather(zo_blend)

    # 将透明部分变成白色
    trans_mask = zo_blend[:, :, 3] == 255
    result = zo_blend.copy()
    result[trans_mask] = [255, 255, 255, 255]

    return result


if __name__ == '__main__':
    tpath_pa = r'C:\Users\yeternity\Desktop\imgprocess/pa.png'
    tpath_szo = r'C:\Users\yeternity\Desktop\imgprocess/pa_szo.png'
    tpath_pa2 = r'C:\Users\yeternity\Desktop\imgprocess/pa2.png'
    tpath_szo2 = r'C:\Users\yeternity\Desktop\imgprocess/pa2_szo.png'
    tpath_sticker = r'C:\Users\yeternity\Desktop\imgprocess/bg2.jpg'
    res = stick_complex(tpath_pa2, tpath_szo2, tpath_sticker)
    # res = stick_simple(tpath_pa, tpath_szo, tpath_sticker)
    # cv2.imshow('result', res)
    cv2.imwrite(r'C:\Users\yeternity\Desktop\imgprocess/result1.png', res)
    cv2.waitKey()
