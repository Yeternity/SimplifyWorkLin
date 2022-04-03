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