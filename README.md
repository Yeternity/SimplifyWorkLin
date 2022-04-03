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