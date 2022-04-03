while(1):
    dircnttmp = input('请输入子文件夹开始的序号：')
    if not(dircnttmp.isdecimal()):
        print('ERROR: 输入的不是纯数字，请重新输入')
        continue
    break