# coding:utf-8
from xml.dom import minidom
import xml_parser as xp
import hashlib
import cv2


if __name__ == '__main__':
    # # xml_doc = minidom.parse(xml_full_path)
    # # # xmlDoc = minidom.loadXMLDoc("books.xml")
    # #
    # # x = xml_doc.getElementsByTagName("title")[0]
    # # parent = x.parentNode
    # #
    # # document.write("Parent node: " + parent.nodeName)


    # xml_dom_url = json_dict['dom_tree_url']
    # shot_img_url = json_dict['screen_shot_url']


    xml_parser = xp.XmlParser()
    xml_dom_url1 = '/root/workspace/devicepass-ai/devicepassai/devicepassai/ImageDiffer/1_1.xml'
    xml_dom_url2 = '/root/workspace/devicepass-ai/devicepassai/devicepassai/ImageDiffer/1_2.xml'
    shot_img_url = '/root/workspace/devicepass-ai/devicepassai/devicepassai/ImageDiffer/1_2.jpg'
    img_shot = cv2.imread(shot_img_url, cv2.IMREAD_COLOR)

    node_list1 = xml_parser.get_xml_data(xml_dom_url1)
    if node_list1 is None:
        print " Read xml file FAILURE!!!"

    leaf_node_list1 = []
    for n in node_list1:
        children_node = n.getchildren()
        if len(children_node) == 0:
            leaf_node_list1.append(n)

    node_list2 = xml_parser.get_xml_data(xml_dom_url2)
    if node_list2 is None:
        print " Read xml file FAILURE!!!"

    leaf_node_list2 = []
    for n in node_list2:
        children_node = n.getchildren()
        if len(children_node) == 0:
            leaf_node_list2.append(n)

    # for i in range(1, len(node_list)-1):
    #     print node_list[i].tag

    # mystring = "Any string you want"
    # print hashlib.md5(mystring).hexdigest()


    # xml_str = xml_parser.xml2str('/root/workspace/devicepass-ai/devicepassai/devicepassai/ImageDiffer/150.xml')
    # hash_object = hashlib.md5(xml_str)
    # print(hash_object.hexdigest())
    #
    # xml_str = xml_parser.xml2str('/root/workspace/devicepass-ai/devicepassai/devicepassai/ImageDiffer/151.xml')
    # hash_object = hashlib.md5(xml_str)
    # print(hash_object.hexdigest())

    nodes_md5_map1 = {}
    map1 = {}
    for n1 in leaf_node_list1:
        print n1
        print n1.attrib

        text_value = n1.get('text')
        class_value = n1.get('class')
        rc_id_value = n1.get('resource-id')
        package_value = n1.get('package')
        content_desc_value = n1.get('content-desc')

        if not text_value.strip():
            text_value = 'None'
        if not class_value.strip():
            class_value = 'None'
        if not rc_id_value.strip():
            rc_id_value = 'None'
        if not package_value.strip():
            package_value = 'None'
        if not content_desc_value.strip():
            content_desc_value = 'None'

        hash_str = text_value + ',' + class_value + ',' + rc_id_value + ',' + package_value + ',' + content_desc_value
        hash_node = hashlib.md5(hash_str.encode('utf-8'))
        nodes_md5_map1[hash_node.hexdigest()] = hash_str

        map1[hash_node.hexdigest()] = n1.attrib

    nodes_md5_map2 = {}
    map2 = {}
    for n2 in leaf_node_list2:
        text_value = n2.get('text')
        class_value = n2.get('class')
        rc_id_value = n2.get('resource-id')
        package_value = n2.get('package')
        content_desc_value = n2.get('content-desc')

        if  not text_value.strip():
            text_value = 'None'
        if not class_value.strip():
            class_value = 'None'
        if not rc_id_value.strip():
            rc_id_value = 'None'
        if not package_value.strip():
            package_value = 'None'
        if not content_desc_value.strip():
            content_desc_value = 'None'

        hash_str = text_value + ',' + class_value + ',' + rc_id_value + ',' + package_value + ',' + content_desc_value
        hash_node = hashlib.md5(hash_str.encode('utf-8'))
        nodes_md5_map2[hash_node.hexdigest()] = hash_str
        map2[hash_node.hexdigest()] = n2.attrib

    differ_map = xml_parser.differ(nodes_md5_map1, nodes_md5_map2)

    for k, v in differ_map.items():
        print k

        found = False
        for k2, v2 in map2.items():
            if k == k2:
                found = True
                bound_value = v2['bounds']
                print bound_value
                l, u, r, d = xml_parser.coord_transform(bound_value)
                cv2.rectangle(img_shot, (l, u), (r, d), (0, 0, 255), 2, 8)
                cv2.imwrite('differ.jpg', img_shot)