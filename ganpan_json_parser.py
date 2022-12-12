import json
import os

dir = 'C:/Users/jsk/Desktop/라벨샘플'
from collections import OrderedDict

"""
영역이 겹치는지 보는 함수
"""
def getInnerTextRegionRatio(objectBbox, textBbox):
    textBbox_area = (textBbox[2] - textBbox[0] + 1) * (textBbox[3] - textBbox[1] + 1)

    x1 = max(objectBbox[0], textBbox[0])
    y1 = max(objectBbox[1], textBbox[1])
    x2 = min(objectBbox[2], textBbox[2])
    y2 = min(objectBbox[3], textBbox[3])

    w = max(0, x2 - x1 + 1)
    h = max(0, y2 - y1 + 1)

    inter = w * h

    text_ratio = inter / textBbox_area
    return text_ratio

"""
ganpan_object == True인 것의 label을 roi_name으로
ganpan_text == Trud인 것들을 한데 모아 words에 각각 넣어줘야됨
"""
for filename in os.listdir(dir):
    with open(os.path.join(dir, filename), encoding= 'UTF-8') as f:
        text = json.load(f)
        shapes = text["shapes"]

        # object== True인 것과 text인 것, telephone, noise를 각각 찾는다.
        ganpantext = []
        ganpanname = []
        ganpanphone = []
        ganpannoise = []


        """
        각각의 flag가 True라면, 그것을 각 list에 append시킴.
        """
        for i in range(len(shapes)):
            if shapes[i]["flags"]["ganpan_object"] == True :
                ganpanname.append(shapes[i])
            elif shapes[i]["flags"]["ganpan_text"] == True :
                ganpantext.append(shapes[i])
            elif shapes[i]["flags"]["telephone"] == True :
                ganpanphone.append(shapes[i])
            elif shapes[i]["flags"]["noise"] == True :
                ganpannoise.append(shapes[i])

        # print(len(ganpanname), ganpanname)
        # print(len(ganpantext),ganpantext)
        # print(len(ganpanphone),ganpanphone)
        # print(len(ganpannoise),ganpannoise)

        # 새로 구축할 img
        file_data = OrderedDict()
        img_name = text["imagePath"][:-4]
        # 최상단 : 메타
        file_data["meta"] = {'version' : 0, 'image_id' : img_name[9:], "image_path" : img_name,
                                  'image_height' : text["imageHeight"], 'image_width' : text["imageWidth"]}
        # file_data["roi"] = {}
        file_data["roi"] = [0 for i in range(len(ganpanname))] # 임시

        # 간판 1개 이상이면 roi에 points와 roi_name 넣는다. 각 간판마다
        for i in range(len(ganpanname)):
            tmp_data = OrderedDict()
            tmp_data["points"] = ganpanname[i]["points"]
            roi_name = ganpanname[i]["label"].split('_')  # 단어를 _기준으로 스플릿

            # 해당 간판의 좌표의 xy의 최소 최대
            points_arr, points_arrx, points_arry = [], [], []
            # print(ganpanname[i]["points"])
            for j in range(4):
                points_arrx.append(ganpanname[i]["points"][j][0])
                points_arry.append(ganpanname[i]["points"][j][1])
            points_arr.append(min(points_arrx))
            points_arr.append(min(points_arry))
            points_arr.append(max(points_arrx))
            points_arr.append(max(points_arry))
            print(points_arr)

            # 각 단어 별로 처리
            tmp_data["words"] = []
            for j in range(len(ganpantext)):
                if ganpantext[j]['label'] not in roi_name:
                    # print('text now is ', ganpantext[j]['label'])
                    continue
                txttmp = {}
                txttmp["points"] = ganpantext[j]["points"]
                txttmp["is_vertical"] = ganpantext[j]["flags"]["vertical"]
                txttmp["is_occlusion"] = ganpantext[j]["flags"]["occlusion"]
                txttmp["category"] = 'store_name'
                txttmp["text"] = ganpantext[j]["label"]
                tmp_data["words"].append(txttmp)

            # 전번 처리
            """
            points 획득, 그중 xmin ymin xmax ymax 획득
            일반적 간판 roi의 ximin ymin xmax ymax 획득 인자로 넘김
            """
            for j in range(len(ganpanphone)):
                numpoint_arr, numpoint_arrx, numpoint_arry = [], [], []
                # print(ganpanphone[j]["points"])
                for k in range(4):
                    # print("now phone ", ganpanphone[j]["points"][k])
                    numpoint_arrx.append(ganpanphone[j]["points"][k][0])
                    numpoint_arry.append(ganpanphone[j]["points"][k][1])
                numpoint_arr.append(min(numpoint_arrx))
                numpoint_arr.append(min(numpoint_arry))
                numpoint_arr.append(max(numpoint_arrx))
                numpoint_arr.append(max(numpoint_arry))
                print('ganpanmaxmin ', numpoint_arr)

                """
                간판 영역과 특정 flag의 영역이 겹치는 부분이 0.9를 넘는다면
                그 flag는 해당 간판의 일부분이므로, 이 간판 내부의 문구로 취급
                """
                ratio = getInnerTextRegionRatio(points_arr, numpoint_arr)
                if ratio > 0.9:
                    txttmp = {}
                    txttmp["points"] = ganpanphone[j]["points"]
                    txttmp["is_vertical"] = ganpanphone[j]["flags"]["vertical"]
                    txttmp["is_occlusion"] = ganpanphone[j]["flags"]["occlusion"]
                    txttmp["category"] = 'telephone'
                    txttmp["text"] = ganpanphone[j]["label"]
                    tmp_data["words"].append(txttmp)
                    break

            # noise 처리
            """
            points 획득, 그중 xmin ymin xmax ymax 획득
            일반적 간판 roi의 ximin ymin xmax ymax 획득 인자로 넘김
            """
            for j in range(len(ganpannoise)):
                numpoint_arr, numpoint_arrx, numpoint_arry = [], [], []
                # print(ganpanphone[j]["points"])
                for k in range(4):
                    # print("now phone ", ganpanphone[j]["points"][k])
                    numpoint_arrx.append(ganpannoise[j]["points"][k][0])
                    numpoint_arry.append(ganpannoise[j]["points"][k][1])
                numpoint_arr.append(min(numpoint_arrx))
                numpoint_arr.append(min(numpoint_arry))
                numpoint_arr.append(max(numpoint_arrx))
                numpoint_arr.append(max(numpoint_arry))
                print('ganpanmaxmin ', numpoint_arr)

                ratio = getInnerTextRegionRatio(points_arr, numpoint_arr)
                if ratio > 0.9:
                    txttmp = {}
                    txttmp["points"] = ganpannoise[j]["points"]
                    txttmp["is_vertical"] = ganpannoise[j]["flags"]["vertical"]
                    txttmp["is_occlusion"] = ganpannoise[j]["flags"]["occlusion"]
                    txttmp["category"] = 'noise'
                    txttmp["text"] = ganpannoise[j]["label"]
                    tmp_data["words"].append(txttmp)
            # ----------------- 노이즈 처리 끝 ----------------------------

            """
            roi_name과 occlusion, vertical 여부 정리
            """
            tmp_data["roi_name"] = ganpanname[i]["label"]
            # tmp_data["category"] = 'store_name'
            tmp_data["occlusion"] = ganpanname[i]["flags"]["occlusion"]
            tmp_data["vertical"] = ganpanname[i]["flags"]["vertical"]
            file_data["roi"][i] = tmp_data


        print(json.dumps(file_data, ensure_ascii=False, indent = "\t"))

        #with open('new' + img_name + '.json', 'w', encoding = "utf-8") as make_file:
        #    json.dump(file_data, make_file, ensure_ascii = False, indent = "\t")
        with open('tmp.json', 'w', encoding = "utf-8") as make_file:
            json.dump(file_data, make_file, ensure_ascii = False, indent = "\t")
        break


"""
# file_data["roi"]["points"] = ganpanname[i]["points"]
            # roi_name = ganpanname[i]["label"].split('_')
            # print(roi_name)
            # file_data["roi"]["words"] = []
            # for j in range(len(ganpantext)):
            #     if ganpantext[j]['label'] not in roi_name:
            #         print('text now is ' , ganpantext[j]['label'])
            #         continue
            #     txttmp = {}
            #     txttmp["points"] = ganpantext[j]["points"]
            #     txttmp["is_vertical"] = ganpantext[j]["flags"]["vertical"]
            #     txttmp["is_occlusion"] = ganpantext[j]["flags"]["occlusion"]
            #     # txttmp["category"] = ganpantext[j]["flags"]["vertical"]
            #     txttmp["text"] = ganpantext[j]["label"]
            #     file_data["roi"]["words"].append(txttmp)
            #
            #
            # file_data["roi"]["roi_name"] = ganpanname[i]["label"]
            # file_data["roi"]["occlusion"] = ganpanname[i]["flags"]["occlusion"]
            # file_data["roi"]["vertical"] = ganpanname[i]["flags"]["vertical"]
"""
