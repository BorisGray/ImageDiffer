# coding:utf-8
from xml.dom import minidom
import xml_parser as xp
import image_processor as imgproc
import hashlib
import cv2
import numpy as np
import base64
import webbrowser
import os
import uuid
import devicepassai.common.LogUtils as LogUtils

IMAGE_DIFFER_PATH = '/tmp/image_differ/'
WIDGET1_SHOT_FILE_PATH = '/tmp/image_differ/widget1_shot/'
WIDGET2_SHOT_FILE_PATH = '/tmp/image_differ/widget2_shot/'
log = LogUtils.MyLog('/tmp/image_differ/image_differ.log')

def is_widget_exist(widget_shot_path, widget_type):
    widget_path = widget_shot_path + widget_type + '/'
    if not os.path.exists(widget_path):
        os.makedirs(widget_path)
    return widget_path

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

def image_differ(xml_dom_url1, xml_dom_url2, shot_img_url1, shot_img_url2):
    xml_parser = xp.XmlParser()

    (img1_filepath, img1_tempfilename) = os.path.split(shot_img_url1)
    (img1_shortname, img1_extension) = os.path.splitext(img1_tempfilename)

    (img2_filepath, img2_tempfilename) = os.path.split(shot_img_url2)
    (img2_shortname, img2_extension) = os.path.splitext(img2_tempfilename)

    img_shot1 = cv2.imread(shot_img_url1, cv2.IMREAD_COLOR)
    img_shot2 = cv2.imread(shot_img_url2, cv2.IMREAD_COLOR)

    node_list1 = xml_parser.get_xml_data(xml_dom_url1)
    if node_list1 is None:
        log.info('Read xml1 file FAILURE!!!')

    leaf_node_list1 = []
    for n in node_list1:
        children_node = n.getchildren()
        if len(children_node) == 0:
            leaf_node_list1.append(n)

    node_list2 = xml_parser.get_xml_data(xml_dom_url2)
    if node_list2 is None:
        log.info('Read xml2 file FAILURE!!!')

    leaf_node_list2 = []
    for n in node_list2:
        children_node = n.getchildren()
        if len(children_node) == 0:
            leaf_node_list2.append(n)

    # parse xml and capture all elements shot

    # create directory for save elements shot
    if not os.path.exists(WIDGET1_SHOT_FILE_PATH):
        os.makedirs(WIDGET1_SHOT_FILE_PATH)
    if not os.path.exists(WIDGET2_SHOT_FILE_PATH):
        os.makedirs(WIDGET2_SHOT_FILE_PATH)

    nodes_uuid_map1 = {}
    for n1 in leaf_node_list1:
        list_attribute = []
        class_value = n1.get('class')
        bounds_value = n1.get('bounds')
        widget_path = is_widget_exist(WIDGET1_SHOT_FILE_PATH, class_value)

        cropped_color = imgproc.ImageProcessor.crop(img_shot1, bounds_value)
        if cropped_color is not None:
            id = uuid.uuid4()
            color_file_name = str(id) + ".png"
            cv2.imwrite(widget_path + color_file_name, cropped_color)
            cv2.waitKey(100)

            list_attribute.append(class_value)
            list_attribute.append(bounds_value)
            nodes_uuid_map1[id] = list_attribute

    nodes_uuid_map2 = {}
    for n2 in leaf_node_list2:
        list_attribute = []
        class_value = n2.get('class')
        bounds_value = n2.get('bounds')
        widget_path = is_widget_exist(WIDGET2_SHOT_FILE_PATH, class_value)

        cropped_color = imgproc.ImageProcessor.crop(img_shot2, bounds_value)
        if cropped_color is not None:
            id = uuid.uuid4()
            color_file_name = str(id) + ".png"
            cv2.imwrite(widget_path + color_file_name, cropped_color)
            cv2.waitKey(100)

            list_attribute.append(class_value)
            list_attribute.append(bounds_value)
            nodes_uuid_map2[id] = list_attribute

    out_dict = imgproc.ImageProcessor.differ(nodes_uuid_map1, nodes_uuid_map2)
    return out_dict


if __name__ == '__main__':

    xml_dom_url1 = '/root/workspace/devicepass-ai/devicepassai/devicepassai/ImageDiffer/1_1.xml'
    xml_dom_url2 = '/root/workspace/devicepass-ai/devicepassai/devicepassai/ImageDiffer/1_2.xml'
    shot_img_url1 = '/root/workspace/devicepass-ai/devicepassai/devicepassai/ImageDiffer/1_1.jpg'
    shot_img_url2 = '/root/workspace/devicepass-ai/devicepassai/devicepassai/ImageDiffer/1_2.jpg'

    out_dict = image_differ(xml_dom_url1, xml_dom_url2, shot_img_url1, shot_img_url2)

    xml_parser = xp.XmlParser()
#     (img1_filepath, img1_tempfilename) = os.path.split(shot_img_url1)
#     (img1_shortname, img1_extension) = os.path.splitext(img1_tempfilename)
#
#     (img2_filepath, img2_tempfilename) = os.path.split(shot_img_url2)
#     (img2_shortname, img2_extension) = os.path.splitext(img2_tempfilename)
#
#     img_shot1 = cv2.imread(shot_img_url1, cv2.IMREAD_COLOR)
#     img_shot2 = cv2.imread(shot_img_url2, cv2.IMREAD_COLOR)
#
# ###################################################################################
#     node_list1 = xml_parser.get_xml_data(xml_dom_url1)
#     if node_list1 is None:
#         log.info('Read xml1 file FAILURE!!!')
#
#     leaf_node_list1 = []
#     for n in node_list1:
#         children_node = n.getchildren()
#         if len(children_node) == 0:
#             leaf_node_list1.append(n)
#
#     node_list2 = xml_parser.get_xml_data(xml_dom_url2)
#     if node_list2 is None:
#         log.info('Read xml2 file FAILURE!!!')
#
#     leaf_node_list2 = []
#     for n in node_list2:
#         children_node = n.getchildren()
#         if len(children_node) == 0:
#             leaf_node_list2.append(n)
# ###################################################################################
#
#     # parse xml and capture all elements shot
#     #
#     # create directory for save elements shot
#     if not os.path.exists(WIDGET1_SHOT_FILE_PATH):
#         os.makedirs(WIDGET1_SHOT_FILE_PATH)
#     if not os.path.exists(WIDGET2_SHOT_FILE_PATH):
#         os.makedirs(WIDGET2_SHOT_FILE_PATH)
#
#     nodes_uuid_map1 = {}
#     for n1 in leaf_node_list1:
#         list_attribute = []
#         class_value = n1.get('class')
#         bounds_value = n1.get('bounds')
#         widget_path = is_widget_exist(WIDGET1_SHOT_FILE_PATH, class_value)
#
#         cropped_color = imgproc.ImageProcessor.crop(img_shot1, bounds_value)
#         if cropped_color is not None:
#             id = uuid.uuid4()
#             color_file_name = str(id) + ".png"
#             cv2.imwrite(widget_path + color_file_name, cropped_color)
#
#             list_attribute.append(class_value)
#             list_attribute.append(bounds_value)
#             nodes_uuid_map1[id] = list_attribute
#
#     nodes_uuid_map2 = {}
#     for n2 in leaf_node_list2:
#         list_attribute = []
#         class_value = n2.get('class')
#         bounds_value = n2.get('bounds')
#         widget_path = is_widget_exist(WIDGET2_SHOT_FILE_PATH, class_value)
#
#         cropped_color = imgproc.ImageProcessor.crop(img_shot2, bounds_value)
#         if cropped_color is not None:
#             id = uuid.uuid4()
#             color_file_name = str(id) + ".png"
#             cv2.imwrite(widget_path + color_file_name, cropped_color)
#
#             list_attribute.append(class_value)
#             list_attribute.append(bounds_value)
#             nodes_uuid_map2[id] = list_attribute
#
#     out_dict = imgproc.ImageProcessor.differ(nodes_uuid_map1, nodes_uuid_map2)
#
#     # uuid1, type1, coord1, uuid2, type2, coord2, score
#     for n in out_dict:
#         color = np.random.randint(0, 255, (100,3))
#         coord1 = n[2]
#         coord2 = n[5]
#         score = n[6]
#
#         if score < 0.9:
#             l1, u1, r1, d1 = xml_parser.coord_transform(coord1)
#             l2, u2, r2, d2 = xml_parser.coord_transform(coord2)
#             cv2.rectangle(img_shot1, (l1, u1), (r1, d1), color[0], 3, 8)
#             cv2.rectangle(img_shot2, (l2, u2), (r2, d2), color[0], 3, 8)
#             # font = cv2.InitFont(cv2.FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8)
#             cv2.putText(img_shot1, str(score), (l1, u1 - 30), cv2.FONT_ITALIC, 1, color[0], 2)
#             cv2.putText(img_shot2, str(score), (l2, u2 - 30), cv2.FONT_ITALIC, 1, color[0], 2)
#
#     out_img1 = img1_shortname + '_marked' + ".png"
#     result_img1 = WIDGET1_SHOT_FILE_PATH + out_img1
#     cv2.imwrite(result_img1, img_shot1)
#
#     out_img2 = img2_shortname + '_marked' + ".png"
#     result_img2 = WIDGET2_SHOT_FILE_PATH + out_img2
#     cv2.imwrite(result_img2, img_shot2)
#
#     img1_marked_base64 = encodeImage(result_img1)
#     img2_marked_base64 = encodeImage(result_img2)
#
#     html_file_name = img1_shortname + '_' + img2_shortname + '.html'
#     html_full_name = IMAGE_DIFFER_PATH + html_file_name
#
#     f = open(html_full_name, 'w')
#
#     message = """
#     <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
#     <html>
#     <head>
#     	<meta http-equiv="content-type" content="text/html; charset=utf-8"/>
#     	<title></title>
#     	<meta name="generator" content="LibreOffice 5.1.6.2 (Linux)"/>
#     	<meta name="created" content="2017-09-13T23:03:10.007212361"/>
#     	<meta name="changed" content="2017-09-13T23:11:26.150466540"/>
#     	<style type="text/css">
#     		@page { margin: 0.79in }
#     		p { margin-bottom: 0.1in; line-height: 120% }
#     		h1 { margin-bottom: 0.08in }
#     		h1.western { font-family: "Liberation Serif", serif }
#     		h1.cjk { font-family: "Noto Sans CJK SC Regular"; font-size: 24pt }
#     		h1.ctl { font-family: "FreeSans"; font-size: 24pt }
#     		a:link { so-language: zxx }
#     	</style>
#     </head>
#     <body lang="en-US" dir="ltr">
#     <h1 class="western"><span style="font-variant: normal"><font color="#000000"><font face="Times New Roman"><span style="letter-spacing: normal"><span style="font-style: normal">Image
#     Difference v1.0</span></span></font></font></span></h1>
#     <p style="margin-bottom: 0in; line-height: 100%"><br/>
#
#     </p>
#     <p style="margin-bottom: 0in; line-height: 100%"><br/>
#
#     </p>
#     <p style="margin-bottom: 0in; line-height: 100%"><font color="#333333">
#       <img src=""" + img1_marked_base64 + """ name="Image1" align="left" width="254" height="455" border="1"/>
#     </font>
#     <font color="#000000">
#       <img src=""" + img2_marked_base64 + """ name="Image2" align="left" width="254" height="456" border="1"/>
#     </font>
#     <br/>
#
#     </p>
#     <p style="margin-bottom: 0in; line-height: 100%"><br/>
#
#     </p>
#     <p style="margin-bottom: 0in; line-height: 100%">	</p>
#     </body>
#     </html>"""
#
#     f.write(message)
#     f.close()
#
#     webbrowser.open(html_full_name, new=1)
    
###################################################################################

    #
    # nodes_md5_map1 = {}
    # map1 = {}
    # for n1 in leaf_node_list1:
    #     print n1
    #     print n1.attrib
    #
    #     text_value = n1.get('text')
    #     class_value = n1.get('class')
    #     rc_id_value = n1.get('resource-id')
    #     package_value = n1.get('package')
    #     content_desc_value = n1.get('content-desc')
    #
    #     if not text_value.strip():
    #         text_value = 'None'
    #     if not class_value.strip():
    #         class_value = 'None'
    #     if not rc_id_value.strip():
    #         rc_id_value = 'None'
    #     if not package_value.strip():
    #         package_value = 'None'
    #     if not content_desc_value.strip():
    #         content_desc_value = 'None'
    #
    #     hash_str = text_value + ',' + class_value + ',' + rc_id_value + ',' + package_value + ',' + content_desc_value
    #     hash_node = hashlib.md5(hash_str.encode('utf-8'))
    #     nodes_md5_map1[hash_node.hexdigest()] = hash_str
    #
    #     map1[hash_node.hexdigest()] = n1.attrib
    #
    # nodes_md5_map2 = {}
    # map2 = {}
    # for n2 in leaf_node_list2:
    #     text_value = n2.get('text')
    #     class_value = n2.get('class')
    #     rc_id_value = n2.get('resource-id')
    #     package_value = n2.get('package')
    #     content_desc_value = n2.get('content-desc')
    #
    #     if  not text_value.strip():
    #         text_value = 'None'
    #     if not class_value.strip():
    #         class_value = 'None'
    #     if not rc_id_value.strip():
    #         rc_id_value = 'None'
    #     if not package_value.strip():
    #         package_value = 'None'
    #     if not content_desc_value.strip():
    #         content_desc_value = 'None'
    #
    #     hash_str = text_value + ',' + class_value + ',' + rc_id_value + ',' + package_value + ',' + content_desc_value
    #     hash_node = hashlib.md5(hash_str.encode('utf-8'))
    #     nodes_md5_map2[hash_node.hexdigest()] = hash_str
    #     map2[hash_node.hexdigest()] = n2.attrib
    #
    # differ_map = xml_parser.differ(nodes_md5_map1, nodes_md5_map2)
    #
    # for k, v in differ_map.items():
    #     print k
    #
    #     found = False
    #     for k2, v2 in map2.items():
    #         if k == k2:
    #             found = True
    #             bound_value = v2['bounds']
    #             print bound_value
    #             l, u, r, d = xml_parser.coord_transform(bound_value)
    #             cv2.rectangle(img_shot1, (l, u), (r, d), (0, 0, 255), 2, 8)
    #             cv2.imwrite('differ.jpg', img_shot1)