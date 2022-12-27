import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets = ['train', 'test', 'val']

Imgpath = 'C:/Users/xy/Desktop/Work/XDUAV-dataset2/images'  # 图片文件夹
xmlfilepath = 'C:/Users/xy/Desktop/Work/XDUAV-dataset2/Annotations/'  # xml文件存放地址
ImageSets_path = 'C:/Users/xy/Desktop/Work/XDUAV-dataset2/ImageSets/Main/'
Label_path = 'C:/Users/xy/Desktop/Work/XDUAV-dataset2/'
classes = ['1', '2', '3', '4', '5', '6']


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id):
    in_file = open(xmlfilepath + '%s.xml' % (image_id))
    out_file = open(Label_path + 'labels/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


wd = getcwd()
# print(wd)

for image_set in sets:
    if not os.path.exists(Label_path + 'labels/'):
        os.makedirs(Label_path + 'labels/')
    image_ids = open(ImageSets_path + '%s.txt' % (image_set)).read().strip().split()
    list_file = open(Label_path + '%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        # print(image_id)  # DJI_0013_00360
        list_file.write(Imgpath + '/%s.jpg\n' % (image_id))
        convert_annotation(image_id)
    list_file.close()

# if __name__ == '__main__':
#     os.makedirs('temp/')
#     list_file = open('%emp.txt', 'w')
#     list_file.write('12325')
#     list_file.close()
