# 在这里模式图（白色衣服图）称为pattern（pa），pa中白色衣服称为zone（zo），其余成为background（bg）
# zone中需要贴图的称为accessible zone（azo）
# zone中不需要贴图的成为forbidden zone（fzo）
# 贴图称为sticker
# select zone(szo)图为区域选择图，分为蓝色（贴图部分）和红色（不贴图部分）
import cv2
import numpy as np
from blend_modes import multiply
import skimage.exposure
import os


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

    lower_red1 = np.array([0, 43, 46])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([156, 43, 46])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 + mask2
    return mask


def get_mask_not_blue_purple(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 43, 46])
    upper_blue = np.array([124, 255, 255])
    upper_purple = np.array([155, 255, 255])  # 有时涂色边缘会混有紫色，这里包括到贴图范围
    mask = cv2.inRange(hsv, lower_blue, upper_purple)
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


# 将png图片透明部分变为白色
def trans2white(png):
    trans_mask = png[:, :, 3] == 0
    result = png.copy()
    result[trans_mask] = [255, 255, 255, 255]
    return result


# 剪裁png图片，去除多余的透明部分
def crop(im):
    # axis 0 is the row(y) and axis(x) 1 is the column
    y, x = im[:, :, 3].nonzero()  # get the nonzero alpha coordinates
    minx = np.min(x)
    miny = np.min(y)
    maxx = np.max(x)
    maxy = np.max(y)
    cropImg = im[miny:maxy, minx:maxx]
    return cropImg


# 将pa和sticker以multiply模式混合
def blend_multiply(pa, sticker):
    if sticker.shape[2] != 4:
        sticker = cv2.cvtColor(sticker, cv2.COLOR_BGR2BGRA)
    if pa.shape[2] != 4:
        pa = cv2.cvtColor(pa, cv2.COLOR_BGR2BGRA)
    result = multiply(pa.astype(float), sticker.astype(float), 1.0).astype(np.uint8)
    return result


# 部分贴图（蓝色），部分不贴图（红色）
# 可代替stick_simple，不过会多做一些运算
def stick_complex(path_pa, path_szo, path_sticker):
    img_pa = cv2.imread(path_pa, cv2.IMREAD_UNCHANGED)
    img_szo = cv2.imread(path_szo, cv2.IMREAD_COLOR)
    img_sticker = cv2.imread(path_sticker, cv2.IMREAD_UNCHANGED)

    # 图片大小调整
    resized_img_sticker = resize_sticker(img_pa, img_sticker)

    # multiply blend mode（混合图片，贴图同时保留衣服阴影）
    img_blend = blend_multiply(img_pa, resized_img_sticker)

    # 蓝色区域（贴图部分），取mask_not_azo（遮掩非azo的区域）
    mask_not_azo = get_mask_not_blue_purple(img_szo)
    # 红色区域（不贴图部分），取mask_not_fzo（遮掩非fzo的区域）
    # 当没有红色区域时，遮盖全部
    mask_not_fzo = get_mask_not_red(img_szo)

    # 抠出蓝色区域（贴图部分）
    azo = cv2.bitwise_and(img_blend, img_blend, mask=mask_not_azo)
    # # 抠出红色区域（不贴图部分），没有红色区域时，fzo为全透明
    fzo = cv2.bitwise_and(img_pa, img_pa, mask=mask_not_fzo)

    # 羽化（消除贴图部分边缘锯齿）
    # azo[:, :, 3] = feather(azo)

    # 合并贴图部分和不贴图部分
    zo_blend = cv2.add(azo, fzo)

    # 羽化（消除贴图部分边缘锯齿）
    zo_blend[:, :, 3] = feather(zo_blend)

    return zo_blend


# 全部都贴图
def stick_simple(path_pa, path_szo, path_sticker):
    img_pa = cv2.imread(path_pa, cv2.IMREAD_UNCHANGED)
    img_szo = cv2.imread(path_szo, cv2.IMREAD_UNCHANGED)
    img_sticker = cv2.imread(path_sticker, cv2.IMREAD_UNCHANGED)

    # 图片大小调整
    resized_img_sticker = resize_sticker(img_pa, img_sticker)

    # multiply blend mode（混合图片，贴图同时保留衣服阴影）
    img_blend = blend_multiply(img_pa, resized_img_sticker)

    # 蓝色区域（贴图部分），取mask_bg（遮掩bg）
    mask_bg = get_mask_not_blue_purple(img_szo)

    # 抠出贴图后的衣服(混合后)
    zo_blend = cv2.bitwise_and(img_blend, img_blend, mask=mask_bg)

    # 羽化（消除贴图部分边缘锯齿）
    zo_blend[:, :, 3] = feather(zo_blend)

    return zo_blend

# 抠出原图，作为拼图的一部分
def get_prototype(path_pa, path_szo):
    img_pa = cv2.imread(path_pa, cv2.IMREAD_UNCHANGED)
    img_szo = cv2.imread(path_szo, cv2.IMREAD_UNCHANGED)

    # 蓝色区域（贴图部分），取mask_not_azo（遮掩非azo的区域）
    mask_not_azo = get_mask_not_blue_purple(img_szo)
    # 红色区域（不贴图部分），取mask_not_fzo（遮掩非fzo的区域）
    # 当没有红色区域时，遮盖全部
    mask_not_fzo = get_mask_not_red(img_szo)

    # 抠出蓝色区域（贴图部分）
    azo = cv2.bitwise_and(img_pa, img_pa, mask=mask_not_azo)
    # # 抠出红色区域（不贴图部分），没有红色区域时，fzo为全透明
    fzo = cv2.bitwise_and(img_pa, img_pa, mask=mask_not_fzo)

    # 合并贴图部分和不贴图部分
    result = cv2.add(azo, fzo)

    # 羽化（消除贴图部分边缘锯齿）
    result[:, :, 3] = feather(result)

    return result


# 贴图
def do_clothstick(path_pa, path_szo, path_sticker, dir_output):
    stickers = os.listdir(path_sticker)

    # 得到白色原图的裁剪
    res = get_prototype(path_pa, path_szo)
    res = crop(res)
    res_name = 'res_' + '0' + '.png'
    cv2.imwrite(dir_output + r'/' + res_name, res)
    print(dir_output + r'/' + res_name, '   finished')

    i = 1
    for sk in stickers:
        # 贴图
        res = stick_complex(path_pa, path_szo, path_sticker + r'/' + sk)

        # 根据不透明部分用矩形裁剪，去除多余的透明部分
        res = crop(res)

        res_name = 'res_' + str(i) + '.png'
        cv2.imwrite(dir_output + r'/' + res_name, res)
        print(dir_output + r'/' + res_name, '   finished')
        i += 1

    return

def main(path_zo, tpath_sticker, tdir_output):
    # 若文件夹不存在，创建
    if not os.path.exists(tdir_output):
        os.mkdir(tdir_output)

    # 遍历模板文件夹
    dirs_pa = os.listdir(path_zo)
    for dir_pa in dirs_pa:

        # 创建新的输出文件夹
        new_dir_output = tdir_output + r'/' + dir_pa
        if not os.path.exists(new_dir_output):
            os.mkdir(new_dir_output)

        # 遍历模板
        pas = os.listdir(path_zo + r'/' + dir_pa)
        # 只有正面
        if len(pas) == 2:
            if pas[0].find('szo') == -1:
                tpath_pa = path_zo + r'/' + dir_pa + r'/' + pas[0]
                tpath_szo = path_zo + r'/' + dir_pa + r'/' + pas[1]
            else:
                tpath_pa = path_zo + r'/' + dir_pa + r'/' + pas[1]
                tpath_szo = path_zo + r'/' + dir_pa + r'/' + pas[0]
            do_clothstick(tpath_pa, tpath_szo, tpath_sticker, new_dir_output)
        # 有正面反面
        elif len(pas) == 4:
            tpath_front_pa = ''
            tpath_front_szo = ''
            tpath_back_pa = ''
            tpath_back_szo = ''

            # 根据名字中的字符串对应赋值
            for pa in pas:
                if pa.find('front') != -1:
                    if pa.find('szo') != -1:
                        tpath_front_szo = path_zo + r'/' + dir_pa + r'/' + pa
                    else:
                        tpath_front_pa = path_zo + r'/' + dir_pa + r'/' + pa
                else:
                    if pa.find('szo') != -1:
                        tpath_back_szo = path_zo + r'/' + dir_pa + r'/' + pa
                    else:
                        tpath_back_pa = path_zo + r'/' + dir_pa + r'/' + pa

            # 创建front文件夹
            dir_front = new_dir_output + r'/' + 'front'
            if not os.path.exists(dir_front):
                os.mkdir(dir_front)

            do_clothstick(tpath_front_pa, tpath_front_szo, tpath_sticker, dir_front)

            # 创建back文件夹
            dir_back = new_dir_output + r'/' + 'back'
            if not os.path.exists(dir_back):
                os.mkdir(dir_back)

            do_clothstick(tpath_back_pa, tpath_back_szo, tpath_sticker, dir_back)
    return

if __name__ == '__main__':
    path_zo = r'C:\Users\yeternity\Desktop\clothsticker\a_zo'
    tpath_sticker = r'C:\Users\yeternity\Desktop\clothsticker\a_sticker'
    tdir_output = r'C:\Users\yeternity\Desktop\clothsticker\processing'

    main(path_zo, tpath_sticker, tdir_output)

