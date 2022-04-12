# SimplifyWorkLin

## Python

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



### python os

https://zhuanlan.zhihu.com/p/52359623



### python教程

https://www.runoob.com/python3/python3-tutorial.html



## 图像处理实例

贴图思路

https://stackoverflow.com/questions/65046692/how-to-put-an-image-on-a-t-shirt-using-python-opencv



mask、resize实例

https://stackoverflow.com/questions/61383950/altering-the-shape-of-an-image-to-take-the-shape-of-an-enclosed-image-with-pytho



如何在照片上使用纹理叠加（blend mode）

https://we.graphics/blog/how-to-use-texture-overlays-on-photos/



通过改变alpha通道改变车子的颜色

https://stackoverflow.com/questions/66704725/how-to-change-car-body-color-with-opencv-on-python-or-javascript



去除png图片多余透明部分，crop the  object

https://stackoverflow.com/questions/46273309/using-opencv-how-to-remove-non-object-in-transparent-image



## 用到的第三方库

### OpenCV

#### 安装nummy和opencv

```
pip install numpy opencv-python
```

官方教程

https://docs.opencv.org/4.0.0/index.html



创建图像

https://blog.csdn.net/zhy29563/article/details/107382109



【OpenCV】HSV颜色识别-HSV基本颜色分量范围

https://blog.csdn.net/taily_duan/article/details/51506776



消除锯齿（羽化）

https://stackoverflow.com/questions/58097626/how-can-i-soften-just-the-edges-of-this-image



resize

https://www.jianshu.com/p/0deabe02a379



将透明背景png图片贴到另一张背景图片

https://linuxtut.com/en/923aefb052f217f2f3c5/



面向初学者的 OpenCV-Python 教程

http://codec.wang/#/opencv/



### Blend Modes

混合multiply模式，保留了衣服的阴影褶皱

https://github.com/flrs/blend_modes

安装

```bash
pip install blend_modes
```

封装了GIMP的库

https://gitlab.gnome.org/GNOME/gimp/-/blob/master/app/operations/layer-modes-legacy/gimpoperationmultiplylegacy.c

 文档

https://blend-modes.readthedocs.io/en/latest/index.html   

维基百科——混合模式

https://en.wikipedia.org/wiki/Blend_modes



### skimage

```bash
pip install -U scikit-image
```

使用了skimage.exposure.rescale_intensity完成去锯齿

