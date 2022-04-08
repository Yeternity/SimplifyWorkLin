# SimplifyWorkLin

### PyCharm设置默认换行符

Settings-> Code Style->Line separator

> 批量修改项目的换行符：先选中项目文件夹，File-File Properties-Line Separators-LF
>
> pycharm死活改不了.iml文件的换行符，最后用VSCode改的。。。

### .gitattributes

`.gitattributes`文件中`text = auto`

Git自动将文本内容的换行符在签入时标准化为LF

有点像是Git的设置core.autocrlf

### PyCharm将.py打包exe

1. 安装pyinstaller，在Terminal输入

   ```bash
   $ pip install pyinstaller
   ```

2. 打包

   ```
   pyinstaller -F main.py
   ```

   > -F 表示生成单个可执行文件

### s.isdigit、isdecimal 和 s.isnumeric 区别

https://www.runoob.com/note/24624

**isdigit()**

- **True**: Unicode数字，byte数字（单字节），全角数字（双字节）
- **False**: 汉字数字，罗马数字，小数
- **Error**: 无

**isdecimal()**

- **True**: Unicode数字，，全角数字（双字节）
- **False**: 罗马数字，汉字数字，小数
- **Error**: byte数字（单字节）

**isnumeric()**

- **True**: Unicode 数字，全角数字（双字节），汉字数字
- **False**: 小数，罗马数字
- **Error**: byte数字（单字节）



### Python中的boolean类型

**0、None、空、False的布尔值为False，其余的为True。**

```python
# all print False
print(bool(0))
print(bool(None))
print(bool(''))
print(bool([]))
print(bool({}))
print(bool(False))
```

### python中值传递还是引用传递？

https://www.jianshu.com/p/e93b6131a5cb

java只有值传递？   区别？



### python编码规范PEP8

[PEP8官方](https://pep8.org/#block-comments)

[PEP8中文翻译](https://github.com/tedyli/PEP8-Style-Guide-for-Python-Code#8.3.1)

[PEP8原文实例少，不好理解，参考这篇](https://blog.csdn.net/qq_33591055/article/details/99581791)



### if __name__ == '__main__' 如何正确理解?

https://www.zhihu.com/question/49136398

当哪个模块被直接执行时，该模块“__name__”的值就是“__main__”



### Python图像处理

[python 几行代码实现抠图](https://www.cnblogs.com/wsnan/p/13060815.html)

飞桨是一个开源的深度学习平台

GitHub:https://github.com/PaddlePaddle/Paddle



https://stackoverflow.com/questions/61383950/altering-the-shape-of-an-image-to-take-the-shape-of-an-enclosed-image-with-pytho

https://stackoverflow.com/questions/56575563/how-to-fill-a-image-with-pattern-fabric-on-shirt

https://stackoverflow.com/questions/65007530/extract-only-the-t-shirt-from-an-image-and-remove-all-other-noise-using-opencv-i

https://towardsdatascience.com/python-for-art-blending-two-images-using-opencv-d1fdfd584efd



https://we.graphics/blog/how-to-use-texture-overlays-on-photos/



https://blog.csdn.net/qq_42722197/article/details/122019791  色彩阴影调整



https://stackoverflow.com/questions/66704725/how-to-change-car-body-color-with-opencv-on-python-or-javascript

https://stackoverflow.com/questions/69023789/change-range-of-colors-in-an-image-using-python

#### Blend Modes

https://github.com/flrs/blend_modes

安装

```bash
pip install blend_modes
```

封装了GIMP的库

### OpenCV

#### 安装nummy和opencv

```
pip install numpy opencv-python
```

创建图像

https://blog.csdn.net/zhy29563/article/details/107382109



【OpenCV】HSV颜色识别-HSV基本颜色分量范围

https://blog.csdn.net/taily_duan/article/details/51506776



消除锯齿（羽化）

https://stackoverflow.com/questions/58097626/how-can-i-soften-just-the-edges-of-this-image



### skimage

```bash
pip install -U scikit-image
```

