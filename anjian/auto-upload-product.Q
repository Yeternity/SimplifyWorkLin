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
'end of line sequence:CRLF  (to upload giuthub, convert to LF)



'��С�ӳ٣�һ����������������̰���֮��
Function delay_min()
	Delay 1000
End Function

'�е��ӳ�
Function delay_mid()
	Delay 3000
End Function

'����ӳ٣�һ����������������Ĳ����ã�����µ���ҳ
Function delay_max()
	Delay 15000
End Function



'�������������վ����¼
Function open_web()
	'�򿪹ȸ�
	MoveTo 218, 1054
	LeftClick 1
	Call delay_mid()
	
	'��ali
	MoveTo 962, 782
	LeftClick 1
	Call delay_max()
	
	'��¼
	MoveTo 1349, 576
	LeftClick 1
	Call delay_max()
End Function


'�򿪵��������ƽ���
Function publish_similar_product()
	
	'��Ʒ����
	MoveTo 136, 478
	LeftClick 1
	Call delay_max()
	
	'�༭
	MoveTo 1709, 962
	LeftClick 1
	Call delay_mid()
	
	'�����Ʋ�Ʒ
	MoveTo 1731, 595
	LeftClick 1
	Call delay_max()

End Function

'��ȡ��Ʒ��Ϣ
Function get_product_info(e_cnt)
	'��excel
	Call Plugin.Office.OpenXls("D:\test\��Ʒ���⼰�ؼ���.xlsx")
	
	'��Ʒ�ͺţ���2����������i�е�1�У�
	product_model_number = Plugin.Office.ReadXls(excel_sheet_cnt, e_cnt, 1)
	
	'��Ʒ��𣨵�2����������i�е�2�У�
	product_kind = Plugin.Office.ReadXls(excel_sheet_cnt, e_cnt, 2)
	
	'��Ʒ���ƣ���2����������i�е�3�У�
    product_name = Plugin.Office.ReadXls(excel_sheet_cnt, e_cnt, 3)
    
    '��Ʒ�ؼ��֣���2����������i�е�4-6�У�
    product_keyword_1 = Plugin.Office.ReadXls(excel_sheet_cnt, e_cnt, 4)
    product_keyword_2 = Plugin.Office.ReadXls(excel_sheet_cnt, e_cnt, 5)
    product_keyword_3 = Plugin.Office.ReadXls(excel_sheet_cnt, e_cnt, 6)
    
    '��ƷͼƬ·������2����������i�е�7�У�
    product_image_path = Plugin.Office.ReadXls(excel_sheet_cnt, e_cnt, 7)
    
    '�ر�excel
	Plugin.Office.CloseXls
End Function


'��յ�ǰѡ���е�����
Function clear_content()
	'ctrl+a ѡ�п���ȫ��
	KeyDown 17, 1
	KeyPress 65, 1
	KeyUp 17, 1
	Call delay_min()
	
	'ɾ��
	KeyPress "BackSpace", 1
	Call delay_min()
End Function



'�޸Ĳ�Ʒ���ƣ�������Ϣ��
Function modify_product_name()
	'���������Ʒ���ơ���ѡ��
	MoveTo 613, 589
	LeftClick 1
	Call delay_min()
	
	'��յ�ǰѡ���е�����
	Call clear_content()
	
	'�����Ʒ����
	SayString product_name
	Call delay_min()
End Function


'�޸Ĳ�Ʒ�ؼ��֣�������Ϣ��
Function modify_product_keyword()
	'�޸ĵ�һ���ؼ���
	MoveTo 529, 652
	LeftClick 1
	Call delay_min()
	
	Call clear_content()
	
	SayString product_keyword_1
	Call delay_min()
	
	'�����հ�����ȥ����żȻ���ֵģ�������
	MoveTo 193, 641
	LeftClick 1
	Call delay_min()
	
	
	'�޸ĵڶ����ؼ���
	MoveTo 458, 705
	LeftClick 1
	Call delay_min()
	
	Call clear_content()
	
	SayString product_keyword_2
	Call delay_min()
	
	'�����հ�����ȥ����żȻ���ֵģ�������
	MoveTo 193, 641
	LeftClick 1
	Call delay_min()
	
	
	'�޸ĵ������ؼ���
	MoveTo 495, 758
	LeftClick 1
	Call delay_min()
	
	Call clear_content()
	
	SayString product_keyword_3
	Call delay_min()
	
	'�����հ�����ȥ����żȻ���ֵģ�������
	MoveTo 193, 641
	LeftClick 1
	Call delay_min()
	
End Function


'�޸Ĳ�Ʒ�ͺţ�������Ϣ��
Function modify_product_model_number()
	'���»������ʺ�λ��
	MouseWheel -12 
	Call delay_min()
	
	'�޸Ĳ�Ʒ�ͺ�
	MoveTo 416, 528
	LeftClick 1
	Call delay_min()
	
	Call clear_content()
	
	SayString product_model_number
	Call delay_min()
	
	'�ָ�Ĭ��λ��
	MouseWheel 12 
	Call delay_min()
End Function


'�޸Ĳ�Ʒ���ƣ��Զ������ԣ�
Function modify_customized_product_name()
	'���»������ʺ�λ��
	MouseWheel -12 
	Call delay_min()

	'�޸��Զ����Ʒ����
	MoveTo 686, 899
	LeftClick 1
	Call delay_min()
	
	Call clear_content()
	
	SayString product_name
	Call delay_min()
	
	'�ָ�Ĭ��λ��
	MouseWheel 12 
	Call delay_min()
End Function


'�ڵ����Ĵ�������ͼƬ
Function add_product_image()
	'���·��
	MoveTo 867, 190
	LeftClick 1
	Call delay_min()
	
	'ɾ��ԭ��·��
	KeyPress "BackSpace", 1
	Call delay_min()
	
	'������·��
	SayString product_image_path
	Call delay_min()
	
	'�س�ȷ��·��
	KeyPress "Enter", 1
	Call delay_min()
	
	'�����ƷͼƬλ�ã��������ȫ��ѡ�У�
	MoveTo 903, 551
	LeftClick 1
	Call delay_min()
	
	
	'ctrl+a ѡ��ȫ��ͼƬ
	KeyDown 17, 1
	KeyPress 65, 1
	KeyUp 17, 1
	Call delay_min()
	
	'����򿪣��ϴ�ȫ��ͼƬ��
	MoveTo 1061, 855
	LeftClick 1
	Call delay_max()
End Function


'���Ӳ�ƷͼƬ���ػ�
Function add_product_image_and_daemon()
	'���»������ʺ�λ��
	MouseWheel -24 
	Call delay_min()
	
	'������
	MoveTo 348, 538
	LeftClick 1
	Call delay_min()
	
	'�ڵ����Ĵ�������ͼƬ
	Call add_product_image()
	
	'�����ػ���6��ͼƬ��
	'��1��
	MoveTo 355, 855
	LeftClick 1
	Call delay_min()
	
	'��2��
	MoveTo 525, 830
	LeftClick 1
	Call delay_min()
	
	'��3��
	MoveTo 665, 832
	LeftClick 1
	Call delay_min()
	
	'��4��
	MoveTo 808, 830
	LeftClick 1
	Call delay_min()
	
	'��5��
	MoveTo 951, 829
	LeftClick 1
	Call delay_min()
	
	'��6��
	MoveTo 1084, 827
	LeftClick 1
	Call delay_min()
	
	
	'�ָ�Ĭ��λ��
	MouseWheel 24
	Call delay_min()
End Function


'�޸Ĳ�Ʒ���ƣ�specification��
Function modify_product_name_spec()
	'���������Ʒ���ơ���ѡ��
	MoveTo 1076, 262
	LeftDoubleClick 1
	Call delay_min()
	
	'��յ�ǰѡ���е�����
	Call clear_content()
	
	'�����Ʒ����
	SayString product_name
	Call delay_min()
End Function


'�޸Ĳ�Ʒ�ͺţ�specification��
Function modify_product_model_number_spec()
	'�޸Ĳ�Ʒ�ͺ�
	MoveTo 1006, 340
	LeftDoubleClick 1
	Call delay_min()
	
	Call clear_content()
	
	SayString product_model_number
	Call delay_min()
End Function


'�޸Ĳ�Ʒ����
Function modify_product_description_spec()
	'���ͼƬ������λ��
	MoveTo 948, 1004
	LeftClick 1
	Call delay_min()
	
	'ɾ����1��ͼƬ
	MoveTo 1825, 380
	LeftClick 1
	Call delay_min()
	
	'ɾ����5��ͼƬ
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

	'��������ϴ�
	MoveTo 1650, 423
	LeftClick 1
	Call delay_mid()
	
	'����ϴ�ͼƬ
	MoveTo 440, 490
	LeftClick 1
	Call delay_min()
	
	'�ڵ����Ĵ�������ͼƬ
	Call add_product_image()
	Call delay_max()
	
	'���ȷ���ϴ�
	MoveTo 405, 757
	LeftClick 1
	Call delay_mid()
End Function


Function search_highlight(search_content)
	'ctrl+f���ȸ�������ݼ�
	KeyDown 17, 1
	KeyPress 70, 1
	KeyUp 17, 1
	Call delay_min()
	
	SayString search_content
	Call delay_min()
	
	// KeyPress "Enter", 1
	// Call delay_min()
End Function


'����ȸ�������������ֺ����������
Function click_highlighted_area()
	FindColor 8,92,1892,1020,"3296FF",intX,intY
	If intX > 0 And intY > 0 Then 
		MoveTo intX + 5, intY + 5
		LeftClick 1
		Call delay_min()
	End If
End Function


'ΪͼƬ���ӵ�����Ŀ��Ʒ�б�ҳ"
Function add_kind_tag()
	'���"������Ŀ��Ʒ�б�ҳ"
	Call search_highlight("������Ŀ��Ʒ�б�ҳ")
	Call click_highlighted_area()
	
	'ѡ����̷���
	MoveTo 686, 320
	LeftClick 1
	Call delay_min()
	
	
	'���"������Ŀ��Ʒ�б�ҳ"
	Call search_highlight(product_kind)
	Call click_highlighted_area()
	
	'���ȷ�ϣ�ѡ����̷��飩
	MoveTo 1450, 883
	LeftClick 1
	Call delay_min()
	
	'���Ԥ������
	MoveTo 496, 419
	LeftClick 1
	Call delay_min()
	
	'���ȷ�ϣ�������Ŀ��Ʒ�б�ҳ��
	MoveTo 1444, 888
	LeftClick 1
	Call delay_mid()
End Function



'����ͼƬ����
Function add_image_attach()
	'�����1��ͼƬ��������
	MoveTo 1782, 447
	LeftClick 1
	Call delay_min()
	Call add_kind_tag()

	'�����2��ͼƬ��������
	MoveTo 1783, 568
	LeftClick 1
	Call delay_min()
	Call add_kind_tag()
	
	'�����3��ͼƬ��������
	MoveTo 1780, 697
	LeftClick 1
	Call delay_min()
	Call add_kind_tag()
	
	
	'�����4��ͼƬ��������
	MoveTo 1783, 821
	LeftClick 1
	Call delay_min()
	'���������С�򣬷����������ȥ
	MoveTo 1635, 885
	LeftClick 1
	Delay 1000
	'�ϵ��ײ���¶����������Ŀ��Ʒ�б�ҳ��
	MouseWheel - 50 
	Delay 1000
	Call add_kind_tag()
	
	
	'�����5��ͼƬ��������
	MoveTo 1781, 944
	LeftClick 1
	Call delay_min()
	'���������С�򣬷����������ȥ
	MoveTo 1637, 1005
	LeftClick 1
	Delay 1000
	'�ϵ��ײ���¶����������Ŀ��Ʒ�б�ҳ��
	MouseWheel - 50 
	Delay 1000
	Call add_kind_tag()	
	
	
	'�����ͼģ��Ĺ�����
	MoveTo 1864, 283
	LeftClick 1
	Delay 1000
	'�������ײ�����������������һ������
	MouseWheel - 50 
	Call delay_min()
	
	'����ڵ�����1��ͼƬ��������
	MoveTo 1786, 949
	LeftClick 1
	Call delay_min()
	'���������С�򣬷����������ȥ
	MoveTo 1648, 1008
	LeftClick 1
	Delay 1000
	'�ϵ��ײ���¶����������Ŀ��Ʒ�б�ҳ��
	MouseWheel - 50 
	Delay 1000
	Call add_kind_tag()
	
	'����ڵ�����2��ͼƬ��������
	MoveTo 1782, 824
	LeftClick 1
	Call delay_min()
	'���������С�򣬷����������ȥ
	MoveTo 1673, 881
	LeftClick 1
	Delay 1000
	'�ϵ��ײ���¶����������Ŀ��Ʒ�б�ҳ��
	MouseWheel - 50 
	Delay 1000
	Call add_kind_tag()
	
	'����ڵ�����3��ͼƬ��������
	MoveTo 1783, 704
	LeftClick 1
	Call delay_min()
	Call add_kind_tag()
	
	'����ڵ�����4��ͼƬ��������
	//MoveTo 1780, 574
	//LeftClick 1
	//Call delay_min()
	//Call add_kind_tag()
	
	'����ڵ�����5��ͼƬ��������
	//MoveTo 1788, 451
	//LeftClick 1
	//Call delay_min()
	//Call add_kind_tag()
	
	'����ڵ�����6��ͼƬ��������
	//MoveTo 1778, 324
	//LeftClick 1
	//Call delay_min()
	//Call add_kind_tag()
	
	'�رչȸ��������������
	MoveTo 1756, 112
	LeftClick 1
	Call delay_min()
	
	'�������
	MoveTo 1682, 122
	LeftClick 1
	Call delay_mid()
	
	'����༭���
	MoveTo 1807, 124
	LeftClick 1
	Call delay_mid()
	
	'���ȷ��ͬ��
	MoveTo 1317, 615
	LeftClick 1
	Call delay_mid()
End Function


'�޸Ĳ�Ʒ��ϸ˵��
Function modify_specification()
	'���»������ʺ�λ��
	MouseWheel -34 
	Call delay_min()
	
	'�����Ҫ�༭
	MoveTo 1166, 559
	LeftDoubleClick 1
	Call delay_max()
	
	'�޸Ĳ�Ʒ���ƣ�specification��
	Call modify_product_name_spec()
	
	'�޸Ĳ�Ʒ�ͺţ�specification��
	Call modify_product_model_number_spec()
	
	'�޸Ĳ�Ʒ����
	Call modify_product_description_spec()
	
	'����ͼƬ����
	Call add_image_attach()
	
	
	'�ָ�Ĭ��λ��
	MouseWheel 34
	Call delay_min()
End Function


Function save_submit_comeback()
	'������ҳ��ײ�
	MouseWheel -100
	Call delay_min()

	'�������
	MoveTo 636, 770
	LeftClick 1
	Call delay_max()
	
	'�ص���ҳ�棨���My Alibaba��
	MoveTo 376, 119
	LeftClick 1
	Call delay_mid()
	
	'����뿪
	MoveTo 1090, 203
	LeftClick 1
	Call delay_max()
End Function



Function submit()
	'������ҳ��ײ�
	MouseWheel -100
	Call delay_min()
	
	'����ύ
	MoveTo 852, 773
	LeftClick 1
	Call delay_max()
End Function




'==========������==========
' Ҫ������excel������
excel_rcnt_start = 18
' Ҫ������excel��β��
excel_rcnt_end = 19
' Ҫ������excel�ĵڼ�������
excel_sheet_cnt = 2
'==========������==========







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



