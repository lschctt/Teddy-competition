import cv2
import json


# filepath1: .txt的文件位置   filepath2: 图片的文件位置
def Get_coco(filepath1, filepath2):
    times = 0
    bnd_id = 1

    json_dict = {
        "images": [],
        # "type": "instances",
        "annotations": [],
        "categories": []
    }

    # 这里是你的txt文件的读取
    # with open()as f 用于读文件，‘r’即为只读。readlines() 方法用于读取所有行(直到结束符 EOF)并返回列表
    with open(filepath1, 'r', encoding='UTF-8') as f:
        # 读取f所有数据，存储在一个列表中
        data = f.readlines()

    first = 1  # 用于检测是不是标题行
    t = 0
    for d in data:
        if first == 1:
            first = 0
        else:
            content = d.split(",")
            filename = content[1]

            # 读取图片
            img = cv2.imread(filepath2 + filename)
            try:
                # 记录图片长和高
                height, width = img.shape[0], img.shape[1]
                # 图片id即为int(图片名)
                image_id = int(filename.split(".")[0])

                # 定义image 填充到images里面
                image = {
                    'file_name': filename,  # 文件名
                    'height': height,  # 图片的高
                    'width': width,  # 图片的宽
                    'id': image_id  # 图片的id，和图片名对应的
                }
                json_dict['images'].append(image)

                if content[3] != '无':    # 判断该图片上有没有检测的目标
                    left_x = content[6].replace('"', '')
                    left_y = content[7].replace('"', '')
                    right_x = content[8].replace('"', '')
                    right_y = content[9].replace('"', '')

                    # 计算bbox里的x,y,w,h
                    x = int(left_x)
                    y = int(left_y)
                    w = int(right_x) - int(left_x)
                    h = int(right_y) - int(left_y)
                    area = w * h
                    # 种类id
                    category_id = int(content[2])

                    # 定义annotation
                    annotation = {
                        'area': area,  # 目标区域的面积
                        'iscrowd': 0,
                        'image_id': image_id,  # 图片的id
                        'bbox': [x, y, w, h],
                        'category_id': int(category_id),  # 类别的id 通过这个id去查找category里面的name
                        'id': bnd_id,    # 唯一id ,可以理解为一个框一个id
                        'ignore': 0,
                        'segmentation': [[]]
                    }
                    # print(category_id)

                    json_dict['annotations'].append(annotation)

                    bnd_id += 1  # “框”id + 1

                    supercategory = content[3]

                    category = {
                        'supercategory': supercategory,  # 类别的名称
                        'id': category_id,  # 类别的id ,一个索引，主键作用，和别的字段之间的桥梁
                    }

                    json_dict['categories'].append(category)

            except:
                times += 1
                print('file is error')
            t = t + 1
            print(t)

    json_fp = open("val.json", 'w')
    json_str = json.dumps(json_dict)
    json_fp.write(json_str)
    json_fp.close()
