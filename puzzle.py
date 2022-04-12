import img
import cv2
import numpy as np
import os
import re


# 缩放图片
def resize(im, scale):
    im_resized = cv2.resize(im, dsize=(0, 0), fx=scale, fy=scale)
    return im_resized


# 粘贴图片
def paste_png(im_png, im_bg, y1, x1):
    # Setting the paste destination coordinates. For the time being, in the upper left
    x2, y2 = im_png.shape[1], im_png.shape[0]

    result = im_bg.copy()
    # Synthetic!
    result[y1:y1+y2, x1:x1+x2] = im_bg[y1:y1+y2, x1:x1+x2] * (1 - im_png[:, :, 3:] / 255) + \
                          im_png[:, :, :3] * (im_png[:, :, 3:] / 255)
    return result


# 计算缩放因子，背景图片（bg）设定为方形
def compute_scale(im):
    # 背景为分辨率1560*1560
    bg_hw = 1560

    im_h, im_w = im.shape[:2]
    maxhw = max(im_h, im_w)
    minhw = min(im_h, im_w)

    # 长边的一排放2个，一个图留100空隙作为缓冲
    scale1 = (bg_hw // 2 - 100) / maxhw

    # 短边的一排放3个，一个图留100空隙作为缓冲
    scale2 = (bg_hw // 3 - 100) / minhw

    scale = min(scale1, scale2)

    return scale


def compute_single_scale(im):
    # 背景为分辨率1560*1560
    bg_hw = 1560

    im_h, im_w = im.shape[:2]
    maxhw = max(im_h, im_w)
    minhw = min(im_h, im_w)

    # 留300像素空隙
    scale = (bg_hw - 300) / maxhw

    return scale

# 有正反面的，特殊计算，因为行列都放2个
def compute_scale_fb(im):
    # 背景为分辨率1560*1560
    bg_hw = 1560

    im_h, im_w = im.shape[:2]
    maxhw = max(im_h, im_w)

    # 长边的一排放2个，一个图留100空隙作为缓冲
    scale = (bg_hw // 2 - 100) / maxhw

    return scale


# 计算图片间的空隙，以确定位置
def compute_step_mode(im_pa, im_bg):
    pa_h, pa_w = im_pa.shape[:2]
    bg_h, bg_w = im_bg.shape[:2]

    if pa_h <= pa_w:  # 横向2个，竖向3个
        # 两张图之间3个空隙（step）
        step_x = (bg_w - 2 * pa_w) // 3
        # 三张图之间4个空隙（step）
        step_y = (bg_h - 3 * pa_h) // 4

        mode = 0
    else:  # 横向3个，竖向2个
        # 两张图之间3个空隙（step）
        step_x = (bg_w - 3 * pa_w) // 4
        # 三张图之间4个空隙（step）
        step_y = (bg_h - 2 * pa_h) // 3

        mode = 1
    return step_y, step_x, mode


# 计算图片间的空隙，以确定位置（正反面版本）
def compute_step_fb(im_pa, im_bg):
    pa_h, pa_w = im_pa.shape[:2]
    bg_h, bg_w = im_bg.shape[:2]

    # 两张图之间3个空隙（step）
    step_x = (bg_w - 2 * pa_w) // 3
    # 两张图之间3个空隙（step）
    step_y = (bg_h - 2 * pa_h) // 3
    return step_y, step_x


# 创建一张高为h，宽为w的白色背景图
def create_white_bg(h, w):
    im_ones = np.ones((h, w, 3), np.uint8)
    im_white = im_ones * 255
    return im_white

# 单张图，分辨率1560*1560
def create_single(img):
    bg = create_white_bg(1560, 1560)

    sc = compute_single_scale(img)
    img = resize(img, sc)

    # 放中心
    cy = (bg.shape[0] - img.shape[0]) // 2
    cx = (bg.shape[1] - img.shape[1]) // 2
    result = paste_png(img, bg, cy, cx)
    return result


# 模式0，横向2个，竖向3个
def mode0_puzzle(im_png, im_bg, step_y, step_x, cnt):
    py = im_png.shape[0]
    px = im_png.shape[1]
    y = 0
    x = 0
    subcnt = cnt % 5
    if subcnt == 1:
        y = step_y
        x = step_x + px + step_x
    elif subcnt == 2:
        y = step_y + py + step_y
        x = step_x
    elif subcnt == 3:
        y = step_y + py + step_y
        x = step_x + px + step_x
    elif subcnt == 4:
        y = step_y + py + step_y + py + step_y
        x = step_x
    elif subcnt == 0:
        y = step_y + py + step_y + py + step_y
        x = step_x + px + step_x
    result = paste_png(im_png, im_bg, y, x)
    # 方便编号
    if subcnt == 0:
        subcnt = 5
    return result, subcnt


# 模式1，横向3个，竖向2个
def mode1_puzzle(im_png, im_bg, step_y, step_x, cnt):
    py = im_png.shape[0]
    px = im_png.shape[1]
    y = 0
    x = 0
    subcnt = cnt % 5
    if subcnt == 1:
        y = step_y
        x = step_x + px + step_x
    elif subcnt == 2:
        y = step_y
        x = step_x + px + step_x + px + step_x
    elif subcnt == 3:
        y = step_y + py + step_y
        x = step_x
    elif subcnt == 4:
        y = step_y + py + step_y
        x = step_x + px + step_x
    elif subcnt == 0:
        y = step_y + py + step_y
        x = step_x + px + step_x + px + step_x
    result = paste_png(im_png, im_bg, y, x)
    # 方便编号
    if subcnt == 0:
        subcnt = 5
    return result, subcnt


# 加入正面图到组图(front)
def puzzle_f(im_f, im_bg, step_y, step_x):
    # resize
    t_scale = compute_scale_fb(im_f)
    im_f = resize(im_f, t_scale)

    py = im_f.shape[0]

    y = step_y + py + step_y
    x = step_x

    result = paste_png(im_f, im_bg, y, x)
    return result


# 加入反面图到组图(back)
def puzzle_b(im_b, im_bg, step_y, step_x):
    # resize
    t_scale = compute_scale_fb(im_b)
    im_b = resize(im_b, t_scale)

    py = im_b.shape[0]
    px = im_b.shape[1]

    y = step_y + py + step_y
    x = step_x + px + step_x

    result = paste_png(im_b, im_bg, y, x)
    return result


# 加入正面白色原图到组图(original front)
def puzzle_of(im_f, im_bg, step_y, step_x):
    # resize
    t_scale = compute_scale_fb(im_f)
    im_f = resize(im_f, t_scale)

    y = step_y
    x = step_x

    result = paste_png(im_f, im_bg, y, x)
    return result


# 加入反面白色原图到组图(original back)
def puzzle_ob(im_b, im_bg, step_y, step_x):
    # resize
    t_scale = compute_scale_fb(im_b)
    im_b = resize(im_b, t_scale)

    px = im_b.shape[1]

    y = step_y
    x = step_x + px + step_x

    result = paste_png(im_b, im_bg, y, x)
    return result


def select_mode_puzzle(im_png, im_bg, step_y, step_x, cnt, mode):
    if mode == 0:
        result, subcnt = mode0_puzzle(im_png, im_bg, step_y, step_x, cnt)
    elif mode == 1:
        result, subcnt = mode1_puzzle(im_png, im_bg, step_y, step_x, cnt)
    return result, subcnt


# 拼图
# dir_input 输入文件夹
# dir_output 输出文件夹
def do_puzzle(dir_input, dir_output):
    imgs = os.listdir(dir_input)
    # 根据名字中的数字由小到大排序，如res8_0，res8_1，根据末尾的0和1排序
    imgs.sort(key=lambda x: int(re.search(r'(\d+)', x).group(0)))
    # 读入第一张白色原图
    img_pa = cv2.imread(dir_input + r'/' + imgs[0], cv2.IMREAD_UNCHANGED)
    # resize
    t_scale = compute_scale(img_pa)
    img_pa = resize(img_pa, t_scale)
    # create bg
    img_bg = create_white_bg(1560, 1560)
    # 计算间隔和拼图模式
    stp_y, stp_x, mode = compute_step_mode(img_pa, img_bg)
    # 先将白色原图贴到背景上
    img_pa_bg = paste_png(img_pa, img_bg, stp_y, stp_x)

    res = img_pa_bg
    i = 1
    group_cnt = 1
    newdir = dir_output + r'/' + 'res_' + str(group_cnt)
    if not os.path.exists(newdir):
        os.mkdir(newdir)
    imgs.pop(0)  # 去除第一张白色原图
    for img in imgs:
        # 读入其他图
        img_png = cv2.imread(dir_input + r'/' + img, cv2.IMREAD_UNCHANGED)
        # resize
        resized_img_png = resize(img_png, t_scale)
        # puzzle
        res, s_cnt = select_mode_puzzle(resized_img_png, res, stp_y, stp_x, i, mode)
        # 生成单个图
        res_single = create_single(img_png)
        res_single_name = 'res' + str(group_cnt) + '_' + str(s_cnt) + '.png'
        cv2.imwrite(newdir + r'/' + res_single_name, res_single)

        # 凑满一张图，生成组图（puzzle图）
        if i % 5 == 0:
            res_name = 'res' + str(group_cnt) + '_0' + '.png'
            cv2.imwrite(newdir + r'/' + res_name, res)
            print(newdir + r'/' + res_name, '   finished')

            res = img_pa_bg  # 重置res
            group_cnt += 1

            # 建立新文件夹
            newdir = dir_output + r'/' + 'res_' + str(group_cnt)
            if not os.path.exists(newdir):
                os.mkdir(newdir)
        i += 1

    # 若最后没有凑满一张图，仍然组图
    if i % 5 != 1:
        res_name = 'res' + str(group_cnt) + '_0' + '.png'
        cv2.imwrite(newdir + r'/' + res_name, res)
        print(newdir + r'/' + res_name, '   finished')
    return


# 拼图
# 有正面反面的，一行2个，正面和反面
# 放原图2个，和贴图的2个
def do_puzzle_fb(dir_input, dir_output):
    imgs_f = os.listdir(dir_input + r'/front')
    imgs_b = os.listdir(dir_input + r'/back')

    # 根据名字中的数字由小到大排序，如res8_0，res8_1，根据末尾的0和1排序
    imgs_f.sort(key=lambda x: int(re.search(r'(\d+)', x).group(0)))
    imgs_b.sort(key=lambda x: int(re.search(r'(\d+)', x).group(0)))

    # 读入第一张白色原图
    img_pa_f = cv2.imread(dir_input + r'/front/' + imgs_f[0], cv2.IMREAD_UNCHANGED)
    img_pa_b = cv2.imread(dir_input + r'/back/' + imgs_b[0], cv2.IMREAD_UNCHANGED)

    # create bg
    img_bg = create_white_bg(1560, 1560)

    # resize
    t_scale = compute_scale_fb(img_pa_f)
    img_pa_f = resize(img_pa_f, t_scale)

    # 计算间隔和拼图模式
    stp_y, stp_x = compute_step_fb(img_pa_f, img_bg)

    # 原图正反面加到组图
    img_pa_bg = puzzle_of(img_pa_f, img_bg, stp_y, stp_x)
    img_pa_bg = puzzle_ob(img_pa_b, img_pa_bg, stp_y, stp_x)


    res = img_pa_bg
    size = len(imgs_f)
    i = 1
    group_cnt = 1
    while i < size:
        # 贴图正反面加到主图
        img_f = cv2.imread(dir_input + r'/front/' + imgs_f[i], cv2.IMREAD_UNCHANGED)
        res = puzzle_f(img_f, res, stp_y, stp_x)
        img_b = cv2.imread(dir_input + r'/back/' + imgs_b[i], cv2.IMREAD_UNCHANGED)
        res = puzzle_b(img_b, res, stp_y, stp_x)

        # 每6个分一组
        if (i - 1) % 6 == 0:
            newdir = dir_output + r'/' + 'res_' + str(group_cnt)
            os.mkdir(newdir)
            group_cnt += 1

        # 生成组图
        res_name = 'res' + '_' + str(i) + '.png'
        cv2.imwrite(newdir + r'/' + res_name, res)
        print(newdir + r'/' + res_name, '   finished')

        res = img_pa_bg  # 重置res
        i += 1
    return

if __name__ == '__main__':
    path_dir_input = r'C:\Users\yeternity\Desktop\clothsticker\processing'
    path_dir_output = r'C:\Users\yeternity\Desktop\clothsticker\output'

    if not os.path.exists(path_dir_output):
        os.mkdir(path_dir_output)

    # 遍历输入文件夹
    dirs = os.listdir(path_dir_input)
    for dir in dirs:
        # 进入子文件夹
        new_dir_input = path_dir_input + r'/' + dir

        # 建立新的输出子文件夹
        new_dir_output = path_dir_output + r'/' + dir
        if not os.path.exists(new_dir_output):
            os.mkdir(new_dir_output)

        # 根据名字内容判定是否有正反面
        foo = os.listdir(new_dir_input)
        if foo[0] == 'back' or foo[0] == 'front':
            do_puzzle_fb(new_dir_input, new_dir_output)
        else:
            do_puzzle(new_dir_input, new_dir_output)

