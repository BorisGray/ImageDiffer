# coding:utf-8

# """
# - 使用bottle来动态生成html
#     - https://www.reddit.com/r/learnpython/comments/2sfeg0/using_template_engine_with_python_for_generating/
#
# """
# _author_ = "boris"
# _time_  = "2017.9.13"
#
# from bottle import template
# import webbrowser
#
# #一些我们需要展示的文章题目和内容
# articles = [("Image Difference v1.0 #1","Details #1","http://blog.csdn.net/reallocing1/article/details/51694967"),("Title #2","Details #2","http://music.163.com"),("Title #3","Details #3","http://douban.fm")]
#
# #定义想要生成的Html的基本格式
# #使用%来插入python代码
# template_demo="""
# <html>
# <head><h1>Image Difference v1.0</h1></head>
# <title>Difference</title>
# <body>
#
#
# % for title,detail,link in items:
# <h2>{{title.strip()}}</h2>
# <p>{{detail}}</p>
# <a href={{link}}>Link text</a>
# %end
#
#
# </body
# </html>
# """
#
# html = template(template_demo,items=articles)
#
# with open("test.html",'wb') as f:
#     f.write(html.encode('utf-8'))
#
#
# #使用浏览器打开html
# webbrowser.open("test.html")

import os
import base64
import webbrowser

IMAGE_DIFFER_PATH = '/tmp/image_differ'
# GEN_HTML = "demo_1.html"  #命名生成的html

def encodeImage(img_file_name):
    in_file = open(img_file_name, 'rb')
    encoded = base64.b64encode(in_file.read())
    in_file.close()
    ext_name = os.path.splitext(img_file_name)[1]
        # print ext_name
    if ext_name == ".jpg":
        img_header = "data:image/jpeg;base64,"
    elif ext_name == ".png":
        img_header = "data:image/png;base64,"
    else:
        img_header = "data:image/jpeg;base64,"
    return img_header + encoded

img1_marked_base64 = encodeImage('/tmp/image_differ/widget1_shot/1_1_marked.png')
img2_marked_base64 = encodeImage('/tmp/image_differ/widget2_shot/1_2_marked.png')

html_file_name = '1_1' + '_' + '1_2' + '.html'
html_full_name = IMAGE_DIFFER_PATH + html_file_name

f = open(html_full_name, 'w')

# f = open(GEN_HTML,'w')
message = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8"/>
	<title></title>
	<meta name="generator" content="LibreOffice 5.1.6.2 (Linux)"/>
	<meta name="created" content="2017-09-13T23:03:10.007212361"/>
	<meta name="changed" content="2017-09-13T23:11:26.150466540"/>
	<style type="text/css">
		@page { margin: 0.79in }
		p { margin-bottom: 0.1in; line-height: 120% }
		h1 { margin-bottom: 0.08in }
		h1.western { font-family: "Liberation Serif", serif }
		h1.cjk { font-family: "Noto Sans CJK SC Regular"; font-size: 24pt }
		h1.ctl { font-family: "FreeSans\"; font-size: 24pt }
		a:link { so-language: zxx }
	</style>
</head>
<body lang="en-US" dir="ltr">
<h1 class="western"><span style="font-variant: normal"><font color="#000000"><font face="Times New Roman"><span style="letter-spacing: normal"><span style="font-style: normal">Image
Difference v1.0</span></span></font></font></span></h1>
<p style="margin-bottom: 0in; line-height: 100%"><br/>

</p>
<p style="margin-bottom: 0in; line-height: 100%"><br/>

</p>
<p style="margin-bottom: 0in; line-height: 100%"><font color="#333333">
  <img src="""+ img1_marked_base64 + """ name="Image1" align="left" width="254" height="455" border="1"/>
</font>
<font color="#000000">
  <img src=""" + img2_marked_base64 + """ name="Image2" align="left" width="254" height="456" border="1"/>
</font>
<br/>

</p>
<p style="margin-bottom: 0in; line-height: 100%"><br/>

</p>
<p style="margin-bottom: 0in; line-height: 100%">	</p>
</body>
</html>"""

f.write(message)
f.close()

webbrowser.open(html_full_name,new = 1)