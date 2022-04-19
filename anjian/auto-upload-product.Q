[General]
SyntaxVersion=2
BeginHotkey=121
BeginHotkeyMod=0
PauseHotkey=0
PauseHotkeyMod=0
StopHotkey=123
StopHotkeyMod=0
RunOnce=1
EnableWindow=
MacroID=47563407-d5c4-484f-bd76-44773d064b9e
Description=auto-upload-product
Enable=1
AutoRun=0
[Repeat]
Type=0
Number=1
[SetupUI]
Type=2
QUI=
[Relative]
SetupOCXFile=
[Comment]

[Script]
' auto upload product
'environment:
'os: Windows 10 home edition
'rte:anjian 2014.06.19549
'display resolution:1920*1080
'Encoding:GB 2312
'end of line sequence:CRLF(to upload giuthub, convert to LF)



'最小延迟，一般用于鼠标点击，键盘按键之后
Function delay_min()
	Delay 1000
End Function

'中等延迟
Function delay_mid()
	Delay 3000
End Function

'最大延迟，一般用于有网络请求的操作用，如打开新的网页
Function delay_max()
	Delay 15000
End Function



'打开浏览器，打开网站并登录
Function open_web()
	'打开谷歌
	MoveTo 218, 1054
	LeftClick 1
	Call delay_mid()
	
	'打开ali
	MoveTo 962, 782
	LeftClick 1
	Call delay_max()
	
	'登录
	MoveTo 1349, 576
	LeftClick 1
	Call delay_max()
End Function


'打开到发布类似界面
Function publish_similar_product()
	
	'产品管理
	MoveTo 136, 478
	LeftClick 1
	Call delay_max()
	
	'编辑
	MoveTo 1709, 962
	LeftClick 1
	Call delay_mid()
	
	'打开类似产品
	MoveTo 1731, 595
	LeftClick 1
	Call delay_max()

End Function

'获取产品信息
Function get_product_info(e_cnt)
	'打开excel
	Call Plugin.Office.OpenXls("D:\test\产品标题及关键词.xlsx")
	
	'产品型号（第2个表单，第i行第1列）
	product_model_number = Plugin.Office.ReadXls(excel_sheet_cnt, e_cnt, 1)
	
	'产品类别（第2个表单，第i行第2列）
	product_kind = Plugin.Office.ReadXls(excel_sheet_cnt, e_cnt, 2)
	
	'产品名称（第2个表单，第i行第3列）
    product_name = Plugin.Office.ReadXls(excel_sheet_cnt, e_cnt, 3)
    
    '产品关键字（第2个表单，第i行第4-6列）
    product_keyword_1 = Plugin.Office.ReadXls(excel_sheet_cnt, e_cnt, 4)
    product_keyword_2 = Plugin.Office.ReadXls(excel_sheet_cnt, e_cnt, 5)
    product_keyword_3 = Plugin.Office.ReadXls(excel_sheet_cnt, e_cnt, 6)
    
    '产品图片路径（第2个表单，第i行第7列）
    product_image_path = Plugin.Office.ReadXls(excel_sheet_cnt, e_cnt, 7)
    
    '关闭excel
	Plugin.Office.CloseXls
End Function


'清空当前选框中的内容
Function clear_content()
	'ctrl+a 选中框中全部
	KeyDown 17, 1
	KeyPress 65, 1
	KeyUp 17, 1
	Call delay_min()
	
	'删除
	KeyPress "BackSpace", 1
	Call delay_min()
End Function



'修改产品名称（基本信息）
Function modify_product_name()
	'鼠标点击“产品名称”的选框
	MoveTo 613, 589
	LeftClick 1
	Call delay_min()
	
	'清空当前选框中的内容
	Call clear_content()
	
	'输入产品名称
	SayString product_name
	Call delay_min()
End Function


'修改产品关键字（基本信息）
Function modify_product_keyword()
	'修改第一个关键词
	MoveTo 529, 652
	LeftClick 1
	Call delay_min()
	
	Call clear_content()
	
	SayString product_keyword_1
	Call delay_min()
	
	'单机空白区域，去除（偶然出现的）下拉框
	MoveTo 193, 641
	LeftClick 1
	Call delay_min()
	
	
	'修改第二个关键词
	MoveTo 458, 705
	LeftClick 1
	Call delay_min()
	
	Call clear_content()
	
	SayString product_keyword_2
	Call delay_min()
	
	'单机空白区域，去除（偶然出现的）下拉框
	MoveTo 193, 641
	LeftClick 1
	Call delay_min()
	
	
	'修改第三个关键词
	MoveTo 495, 758
	LeftClick 1
	Call delay_min()
	
	Call clear_content()
	
	SayString product_keyword_3
	Call delay_min()
	
	'单机空白区域，去除（偶然出现的）下拉框
	MoveTo 193, 641
	LeftClick 1
	Call delay_min()
	
End Function


'修改产品型号（基本信息）
Function modify_product_model_number()
	'向下滑动到适合位置
	MouseWheel -12 
	Call delay_min()
	
	'修改产品型号
	MoveTo 416, 528
	LeftClick 1
	Call delay_min()
	
	Call clear_content()
	
	SayString product_model_number
	Call delay_min()
	
	'恢复默认位置
	MouseWheel 12 
	Call delay_min()
End Function


'修改产品名称（自定义属性）
Function modify_customized_product_name()
	'向下滑动到适合位置
	MouseWheel -12 
	Call delay_min()

	'修改自定义产品名称
	MoveTo 686, 899
	LeftClick 1
	Call delay_min()
	
	Call clear_content()
	
	SayString product_name
	Call delay_min()
	
	'恢复默认位置
	MouseWheel 12 
	Call delay_min()
End Function


'在弹出的窗口添加图片
Function add_product_image()
	'点击路径
	MoveTo 867, 190
	LeftClick 1
	Call delay_min()
	
	'删除原本路径
	KeyPress "BackSpace", 1
	Call delay_min()
	
	'输入新路径
	SayString product_image_path
	Call delay_min()
	
	'回车确认路径
	KeyPress "Enter", 1
	Call delay_min()
	
	'点击产品图片位置（方便后面全部选中）
	MoveTo 903, 551
	LeftClick 1
	Call delay_min()
	
	
	'ctrl+a 选中全部图片
	KeyDown 17, 1
	KeyPress 65, 1
	KeyUp 17, 1
	Call delay_min()
	
	'点击打开（上传全部图片）
	MoveTo 1061, 855
	LeftClick 1
	Call delay_max()
End Function


'添加产品图片和守护
Function add_product_image_and_daemon()
	'向下滑动到适合位置
	MouseWheel -24 
	Call delay_min()
	
	'点击浏览
	MoveTo 348, 538
	LeftClick 1
	Call delay_min()
	
	'在弹出的窗口添加图片
	Call add_product_image()
	
	'添加守护（6个图片）
	'第1个
	MoveTo 355, 855
	LeftClick 1
	Call delay_min()
	
	'第2个
	MoveTo 525, 830
	LeftClick 1
	Call delay_min()
	
	'第3个
	MoveTo 665, 832
	LeftClick 1
	Call delay_min()
	
	'第4个
	MoveTo 808, 830
	LeftClick 1
	Call delay_min()
	
	'第5个
	MoveTo 951, 829
	LeftClick 1
	Call delay_min()
	
	'第6个
	MoveTo 1084, 827
	LeftClick 1
	Call delay_min()
	
	
	'恢复默认位置
	MouseWheel 24
	Call delay_min()
End Function


'修改产品名称（specification）
Function modify_product_name_spec()
	'鼠标点击“产品名称”的选框
	MoveTo 1076, 262
	LeftDoubleClick 1
	Call delay_min()
	
	'清空当前选框中的内容
	Call clear_content()
	
	'输入产品名称
	SayString product_name
	Call delay_min()
End Function


'修改产品型号（specification）
Function modify_product_model_number_spec()
	'修改产品型号
	MoveTo 1006, 340
	LeftDoubleClick 1
	Call delay_min()
	
	Call clear_content()
	
	SayString product_model_number
	Call delay_min()
End Function


'修改产品描述
Function modify_product_description_spec()
	'点击图片描述的位置
	MoveTo 948, 1004
	LeftClick 1
	Call delay_min()
	
	'删除第1张图片
	MoveTo 1825, 380
	LeftClick 1
	Call delay_min()
	
	'删除后5张图片
	MoveTo 1852, 349
	LeftClick 1
	Call delay_min()
	LeftClick 1
	Call delay_min()
	LeftClick 1
	Call delay_min()
	LeftClick 1
	Call delay_min()
	LeftClick 1
	Call delay_min()

	'点击本地上传
	MoveTo 1650, 423
	LeftClick 1
	Call delay_mid()
	
	'点击上传图片
	MoveTo 440, 490
	LeftClick 1
	Call delay_min()
	
	'在弹出的窗口添加图片
	Call add_product_image()
	Call delay_max()
	
	'点击确认上传
	MoveTo 405, 757
	LeftClick 1
	Call delay_mid()
End Function


Function search_highlight(search_content)
	'ctrl+f，谷歌搜索快捷键
	KeyDown 17, 1
	KeyPress 70, 1
	KeyUp 17, 1
	Call delay_min()
	
	SayString search_content
	Call delay_min()
	
	// KeyPress "Enter", 1
	// Call delay_min()
End Function


'点击谷歌浏览器搜索文字后高亮的区域
Function click_highlighted_area()
	FindColor 8,92,1892,1020,"3296FF",intX,intY
	If intX > 0 And intY > 0 Then 
		MoveTo intX + 5, intY + 5
		LeftClick 1
		Call delay_min()
	End If
End Function


'为图片添加店内类目商品列表页"
Function add_kind_tag()
	'点击"店内类目商品列表页"
	Call search_highlight("店内类目商品列表页")
	Call click_highlighted_area()
	
	'选择店铺分组
	MoveTo 686, 320
	LeftClick 1
	Call delay_min()
	
	
	'点击"店内类目商品列表页"
	Call search_highlight(product_kind)
	Call click_highlighted_area()
	
	'点击确认（选择店铺分组）
	MoveTo 1450, 883
	LeftClick 1
	Call delay_min()
	
	'点击预览链接
	MoveTo 496, 419
	LeftClick 1
	Call delay_min()
	
	'点击确认（店内类目商品列表页）
	MoveTo 1444, 888
	LeftClick 1
	Call delay_mid()
End Function



'添加图片链接
Function add_image_attach()
	'点击第1个图片添加链接
	MoveTo 1782, 447
	LeftClick 1
	Call delay_min()
	Call add_kind_tag()

	'点击第2个图片添加链接
	MoveTo 1783, 568
	LeftClick 1
	Call delay_min()
	Call add_kind_tag()
	
	'点击第3个图片添加链接
	MoveTo 1780, 697
	LeftClick 1
	Call delay_min()
	Call add_kind_tag()
	
	
	'点击第4个图片添加链接
	MoveTo 1783, 821
	LeftClick 1
	Call delay_min()
	'点击跳出的小框，方便滚轮拖下去
	MoveTo 1635, 885
	LeftClick 1
	Delay 1000
	'拖到底部，露出“店内类目商品列表页”
	MouseWheel - 50 
	Delay 1000
	Call add_kind_tag()
	
	
	'点击第5个图片添加链接
	MoveTo 1781, 944
	LeftClick 1
	Call delay_min()
	'点击跳出的小框，方便滚轮拖下去
	MoveTo 1637, 1005
	LeftClick 1
	Delay 1000
	'拖到底部，露出“店内类目商品列表页”
	MouseWheel - 50 
	Delay 1000
	Call add_kind_tag()	
	
	
	'点击多图模块的滚动条
	MoveTo 1864, 283
	LeftClick 1
	Delay 1000
	'滚动到底部，从下往上再添加一遍链接
	MouseWheel - 50 
	Call delay_min()
	
	'点击第倒数第1个图片添加链接
	MoveTo 1786, 949
	LeftClick 1
	Call delay_min()
	'点击跳出的小框，方便滚轮拖下去
	MoveTo 1648, 1008
	LeftClick 1
	Delay 1000
	'拖到底部，露出“店内类目商品列表页”
	MouseWheel - 50 
	Delay 1000
	Call add_kind_tag()
	
	'点击第倒数第2个图片添加链接
	MoveTo 1782, 824
	LeftClick 1
	Call delay_min()
	'点击跳出的小框，方便滚轮拖下去
	MoveTo 1673, 881
	LeftClick 1
	Delay 1000
	'拖到底部，露出“店内类目商品列表页”
	MouseWheel - 50 
	Delay 1000
	Call add_kind_tag()
	
	'点击第倒数第3个图片添加链接
	MoveTo 1783, 704
	LeftClick 1
	Call delay_min()
	Call add_kind_tag()
	
	'点击第倒数第4个图片添加链接
	//MoveTo 1780, 574
	//LeftClick 1
	//Call delay_min()
	//Call add_kind_tag()
	
	'点击第倒数第5个图片添加链接
	//MoveTo 1788, 451
	//LeftClick 1
	//Call delay_min()
	//Call add_kind_tag()
	
	'点击第倒数第6个图片添加链接
	//MoveTo 1778, 324
	//LeftClick 1
	//Call delay_min()
	//Call add_kind_tag()
	
	'关闭谷歌浏览器的搜索栏
	MoveTo 1756, 112
	LeftClick 1
	Call delay_min()
	
	'点击保存
	MoveTo 1682, 122
	LeftClick 1
	Call delay_mid()
	
	'点击编辑完成
	MoveTo 1807, 124
	LeftClick 1
	Call delay_mid()
	
	'点击确定同步
	MoveTo 1317, 615
	LeftClick 1
	Call delay_mid()
End Function


'修改产品详细说明
Function modify_specification()
	'向下滑动到适合位置
	MouseWheel -34 
	Call delay_min()
	
	'点击我要编辑
	MoveTo 1166, 559
	LeftDoubleClick 1
	Call delay_max()
	
	'修改产品名称（specification）
	Call modify_product_name_spec()
	
	'修改产品型号（specification）
	Call modify_product_model_number_spec()
	
	'修改产品描述
	Call modify_product_description_spec()
	
	'添加图片链接
	Call add_image_attach()
	
	
	'恢复默认位置
	MouseWheel 34
	Call delay_min()
End Function


Function save_submit_comeback()
	'滚动到页面底部
	MouseWheel -100
	Call delay_min()

	'点击保存
	MoveTo 636, 770
	LeftClick 1
	Call delay_max()
	
	'回到主页面（点击My Alibaba）
	MoveTo 376, 119
	LeftClick 1
	Call delay_mid()
	
	'点击离开
	MoveTo 1090, 203
	LeftClick 1
	Call delay_max()
End Function



Function submit()
	'滚动到页面底部
	MouseWheel -100
	Call delay_min()
	
	'点击提交
	MoveTo 852, 773
	LeftClick 1
	Call delay_max()
End Function




'==========配置项==========
' 要遍历的excel的首行
excel_rcnt_start = 18
' 要遍历的excel的尾行
excel_rcnt_end = 19
' 要遍历的excel的第几个表单
excel_sheet_cnt = 2
'==========配置项==========







product_model_number = 0
product_name = ""
product_kind = ""
product_keyword_1 = ""
product_keyword_2 = ""
product_keyword_3 = ""
product_image_path = ""

excel_rcnt_now = excel_rcnt_start
loop_cnt = excel_rcnt_end - excel_rcnt_start + 1
// Call open_web()
For loop_cnt
	Call publish_similar_product()
	Call get_product_info(excel_rcnt_now)
	Call modify_product_name()
	Call modify_product_keyword()
	Call modify_product_model_number()
	Call modify_customized_product_name()
	Call add_product_image_and_daemon()
	Call modify_specification()
	Call save_submit_comeback()
	
	excel_rcnt_now = excel_rcnt_now + 1
Next



