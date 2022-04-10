import os
import re
import sys

def rename(file, newname):
    try:
        os.rename(file, newname)
    except FileExistsError:
        print('FileExistsError: 无法命名已经存在的文件，如文件夹中已经有test2.png，就无法再将test1.png命名成test2.png')
        print('解决方法：')
        print('这种错误一般是因为重新编号产生，由于两次编号太过于相近\n'
              '所以可以先设置差距大一些的序号如5000，编好后，再重新设置期望的编号即可避免重复')
        return False
    return True

# 根据文件名中的数字由小到大排序
def sort(obj):
    try:
        obj.sort(key=lambda x: int(re.search(r'\d+', x).group(0)))
    except AttributeError:
        return False
        # print('*************************************************************************')
        # print('AttributeError: 存在名字中没有数字的文件或文件夹，故这一组无法按数字排序，顺序将会随机')
        # print('*************************************************************************')
    return True

def dothetask(imgcnt, dircnt, mainpath):
    # 分三层循环，分别遍历外文件夹（商品种类名字）、子文件夹（任意名字）、图片文件（任意名字）

    print('start')

    subdir_attribute = '数字排序'
    file_attribute = '数字排序'

    # 外文件夹
    exdirs = os.listdir(mainpath)
    for exdir in exdirs:
        print(exdir + '随机排序')

        # 取出外文件夹名的字母和空格，作为后面改名的核心标志（如boxer、shorts、dog tank）
        kindname = re.search(r'[ a-zA-Z]+', exdir).group(0)
        # 记录子文件夹的第一个排序，方便后面标识外文件夹的数字范围
        startdircnt = dircnt

        # 子文件夹
        exdirpath = mainpath + r'/' + exdir
        subdirs = os.listdir(exdirpath)
        if not (sort(subdirs)): subdir_attribute = '随机排序'
        for subdir in subdirs:
            print('    ' + subdir + subdir_attribute)

            # 图片文件
            subdirpath = exdirpath + r'/' + subdir
            files = os.listdir(subdirpath)
            if not(sort(files)): file_attribute = '随机排序'
            os.chdir(subdirpath)  # os也要转换目录，否则rename找不到文件，或者rename用绝对路径的话，可以不加这句话
            for file in files:
                print('        ' + file + file_attribute)

                portion = os.path.splitext(file)  # 拆分文件名，portion[1]为后缀
                new = 'sublimation ' + kindname + ' C' + str(imgcnt)
                newname = new + portion[1]
                if not(rename(file, newname)): return
                imgcnt = imgcnt + 1

            # 改倒数第一层文件夹名字
            newname = 'sublimation ' + kindname + ' C' + str(dircnt)
            os.chdir(exdirpath)
            if not(rename(subdir, newname)): return
            dircnt = dircnt + 1

        # 改倒数第二层文件夹名字
        newname = '[' + str(startdircnt) + '-' + str(dircnt - 1) + ']' + kindname
        os.chdir(mainpath)
        if not(rename(exdir, newname)): return

    print('finished')
    return


if __name__ == '__main__':

    while 1:
        # 初始化
        dircnttmp = 1
        imgcnttmp = 1
        mainpathtmp = None

        print('**********************')
        print('1: 帮助说明\n'
              '2: 开始操作\n'
              '3: 结束程序')
        print('**********************')
        step = input('请输入需要操作的数字: ')

        if step == '1':
            step = 0
            print('=========================================================================================')
            print('该程序依次遍历文件夹并改名，example：')
            print(r'假设路径D:\testfilename目录结构如下')
            print('├──boxer  共三层，第一层我们称为外文件夹\n'
                  '|  ├──文件夹1   第二层子文件夹\n'
                  '|  |  ├──图片1.jpg   第三层图片\n'
                  '|  |  └──图片2.jpg\n'
                  '|  └──文件夹1\n'
                  '|     ├──图片1.png\n'
                  '|     └──图片2.png\n'
                  '└──underwear\n'
                  '   ├──文件夹1\n'
                  '   |  ├──图片1.png\n'
                  '   └──文件夹1\n'
                  '      ├──图片1.png\n'
                  '      └──图片2.png\n')
            print('在程序中输入路径' + r'D:\testfilename' + '\n'
                  '输入子文件夹开始的序号：20\n'
                  '输入图片开始的序号：30\n')
            print('程序处理后的结果处如下所示：')
            print('├──[20-21]boxer   外文件夹会带上子文件夹的序号范围\n'
                  '|  ├──sublimation boxer C20   子文件夹会根据外文件夹boxer的名字命名，并且编号\n'
                  '|  |  ├──sublimation boxer C30.jpg  图片也会根据外文件夹boxer的名字命名，并且编号\n'
                  '|  |  └──sublimation boxer C31.jpg\n'
                  '|  └──sublimation boxer C21\n'
                  '|     ├──sublimation boxer C32.png\n'
                  '|     └──sublimation boxer C33.png\n'
                  '└──[22-23]underwear\n'
                  '   ├──sublimation underwear C22\n'
                  '   |  ├──sublimation underwear C34.png\n'
                  '   └──sublimation underwear C23\n'
                  '      ├──sublimation underwear C35.png\n'
                  '      └──sublimation underwear C36.png\n')
            print('需注意：\n'
                  '1.程序扫描外文件夹时没有设定顺序，因此boxer和underwear谁编号在前是随机的\n'
                  '2.程序对子文件夹和图片会根据它们名字中的数字进行由小到大的排序，如果名字中没有数字，程序会报错\n'
                  '3.以上两点可以根据需求再更改\n'
                  '4.每次重新出现这段话，输入的序号和路径会重置，重新输入即可\n'
                  '5.程序运行完毕出现finished说明成功，否则需要查看对应的错误'
                  )
            print('=====================================================================================')

        elif step == '2':
            step = 0

            # 输入要操作的文件夹路径
            mainpathtmp = input('输入要操作的文件夹路径: ')

            # 判断路径是否错误，正确的话查找路径下的文件并列出
            try:
                directories = os.listdir(mainpathtmp)
            except IOError:
                print('Error: 没有找到该路径', mainpathtmp)
                continue
            else:
                print(mainpathtmp, '扫描到该路径下有: ')
                for directory in directories:
                    print(directory)

            # 确认路径
            isyes = input('请确认这是正确的路径，错误路径可能会导致您的其他文件名被修改（y/n）：')
            if isyes != 'y':
                continue

            # 输入子文件夹开始的序号
            while(1):
                dircnttmp = input('请输入子文件夹开始的序号：')
                if not(dircnttmp.isdecimal()):
                    print('ERROR: 输入的不是纯数字，请重新输入')
                    continue
                break

            # 输入图片开始的序号
            while (1):
                imgcnttmp = input('请输入图片开始的序号：')
                if not (imgcnttmp.isdecimal()):
                    print('ERROR: 输入的不是纯数字，请重新输入')
                    continue
                break

            # 确认执行
            todo = input('是否开始执行（y/n）：')
            if todo != 'y':
                continue
            dothetask(int(imgcnttmp), int(dircnttmp), mainpathtmp)

        elif step == '3':
            sys.exit()
        else:
            print('ERROR: 错误命令，请输入1-3的数字')
            continue
