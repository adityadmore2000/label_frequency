#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import matplotlib.pyplot as plt


def calculate_yolo_labels(folder):
    if os.path.exists(os.path.join(folder, 'classes.txt')):
        with open(os.path.join(folder, 'classes.txt'), 'r') as file:
            labels_count = len(file.readlines())
            # print(f"total labels found in classes file: {labels_count}")
        labels_counter = [0] * labels_count
        # files_with_error = set()
        for file_name in os.listdir(folder):
            if file_name.endswith('txt') and file_name != 'classes.txt':
                file_path = os.path.join(folder, file_name)
                with open(file_path, "r") as f:
                    for line in f:
                        if line[0].isdigit():
                            label = int(line[0:2])
                            if 0 <= label < labels_count:
                                # files_with_error.add(file_name)
                                label = int(line[0:2])
                                labels_counter[label] += 1
                        else:
                            pass
        return labels_counter
    else:
        return -1


def visualize_yolo_labels(folder):
    labels_counter = calculate_yolo_labels(folder)
    if labels_counter != -1:
        labels_count = len(labels_counter)

        plt.bar(range(labels_count), labels_counter)
        plt.xlabel(os.path.join(os.path.basename(os.path.dirname(folder)), os.path.basename(folder)))
        plt.ylabel("Frequency")
        plt.xticks(range(labels_count))
        plt.show()
        print(f"{os.path.basename(folder)}: {labels_counter}")
    else:
        print("Can't plot the frequency, no classes file found")
    # indicating no classes file present
    return labels_counter

# input_folder_path = input("Enter path of labels folder: ")
# labels_count = int(input("Enter the number of labels: "))
# visualize_yolo_labels(input_folder_path, labels_count)


# In[ ]:


import shutil
import os


def printFileWiseLabels(folder, labels_count, target, target_dir):
    count = 0
    for file in os.listdir(folder):

        labels = [0] * labels_count
        f = open(os.path.join(folder, file), "r")
        for line in f:
            try:
                label = line[0]
                labels[int(label)] += 1
            except Exception as E:
                print(label, file)
        max_val = max(labels)
        if labels.index(max_val) == target:
            print(file)
            # shutil.move(os.path.join(folder,file),os.path.join(target_dir,'labels'))

# In[ ]:


import os
import json
import matplotlib.pyplot as plt


def calculate_coco_labels(dataset_path):
    ann_dir = os.path.join(dataset_path, 'annotations')
    annotations = dict()
    total_classes = 0
    for file in os.listdir(ann_dir):
        file_path = os.path.join(ann_dir, file)
        f = open(file_path, 'r')
        data = json.load(f)
        start_id = data["categories"][0]["id"]

        labels_count = len(data['categories'])
        total_classes = labels_count
        labels_counter = [0] * labels_count if start_id==0 else [0]*(labels_count+1)
        for annotation in data['annotations']:
            # annotation starts from 0
            label = annotation['category_id']
            # print(label)
            if start_id==0:
                if 0 <= label < labels_count:
                    labels_counter[label] += 1
            elif start_id==1:
                if 1<=label<=labels_count:
                    labels_counter[label]+=1
        annotations[file.split('.')[0]] = labels_counter

    all_counts = [0]*total_classes if start_id == 0 else [0]*(total_classes+1)
    for _,values in annotations.items():
        for index,value in enumerate(values):
            all_counts[index]+=value
    print(f"per class total count is: {all_counts}")
    # return annotations
    return all_counts

def addlabels_coco(x,y):
    for i in range(len(x)):
        plt.text(i,y[i],y[i])

def visualize_coco_labels(dataset_path):
    # files_with_error = set()
    # for file, labels_counter in calculate_coco_labels(dataset_path).items():
    #     file_path = os.path.join(dataset_path, 'annotations', file)
    #     #labels_counter = calculate_coco_labels(dataset_path)
    #     labels_count = len(labels_counter)
    #     plt.bar(range(labels_count), labels_counter)
    #     plt.xlabel(os.path.basename(file_path))
    #     plt.ylabel("Frequency")
    #     plt.xticks(range(labels_count))
    #     plt.show()
    #     print(f"{os.path.basename(dataset_path)}: {labels_counter}")
    # addlabels_coco(range(labels_count),labels_counter)
    all_anns = calculate_coco_labels(dataset_path)
    labels_count = len(all_anns)
    plt.bar(range(labels_count),all_anns)
    addlabels_coco(range(labels_count),all_anns)
    plt.xlabel(os.path.basename(dataset_path))
    plt.ylabel("Instances")
    plt.xticks(range(labels_count))
    plt.show()


# dataset_path = input("Enter path to coco dataset directory: ")
# ann_dir = os.path.join(dataset_path,'annotations')
# if os.path.exists(ann_dir):
#     for file in os.listdir(ann_dir):
#         visualize_coco_labels(os.path.join(ann_dir,file))


# In[ ]:


import os
import json
import matplotlib.pyplot as plt


def return_class_set(folder_path):
    class_names = set()
    for file in os.listdir(folder_path):
        if file.split('.')[1] == 'json':
            label_file = open(os.path.join(folder_path, file), 'r')
            data = json.load(label_file)
            for shape in data['shapes']:
                class_names.add(shape['label'])
    return class_names

def calculate_labelme_labels(class_names,folder_path):
    labels_dict = {key: 0 for key in class_names}
    # labels_dict = {'window':0,'door':0,'doorframe':0,'staircase':0,'ladder':0,'curtain_wall':0,'ramp':0}    # files_with_error = set()
    for file in os.listdir(folder_path):
        if file.endswith('.json'):
            label_file = open(os.path.join(folder_path, file), 'r')
            data = json.load(label_file)
            for shape in data['shapes']:
                labels_dict[shape['label']] += 1

    return labels_dict


def visualize_labelme_labels(folder_path):
    class_names = return_class_set(folder_path)
    print(f"class names: {class_names}")
    labels_dict = calculate_labelme_labels(class_names, folder_path)

    plt.bar(labels_dict.keys(), labels_dict.values())
    plt.xlabel(os.path.basename(folder_path))
    plt.ylabel("Frequency")
    plt.xticks(list(labels_dict.keys()))
    plt.show()
    print(f"{os.path.basename(folder_path)}: {labels_dict.values()}")
    return labels_dict

# print('train-diff',train_diff)
# print('test-diff',test_diff)
# print('val-diff',val_diff)
# visualize_yolo_labels(r"D:\write\For Rameshwar_sir\Updated_data\YOLOX_DATA_dup_removed\MEP_DATA_27_02_2024\train")
#
# json_labels = input("Enter file path for json annotations: ")
#
visualize_labelme_labels(r"D:\Datasets\Labelme\Data-Steel-STR\val")
