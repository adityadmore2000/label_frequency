from label_frequency import calculate_yolo_labels,visualize_labelme_labels
import pandas as pd
import os


def label_difference_txt(input_dir):
    results = []
    for directory in ('train', 'test', 'val'):
        results.append(calculate_yolo_labels(os.path.join(input_dir, directory)))

    total = [sum(i) for i in zip(*results)]

    train_expected = [round(i * 0.8) for i in total]
    test_expected = [round(i * 0.1) for i in total]
    val_expected = [round(i * 0.1) for i in total]

    train_diff = [i - j for i, j in zip(results[0], train_expected)]
    test_diff = [i - j for i, j in zip(results[1], test_expected)]
    val_diff = [i - j for i, j in zip(results[2], val_expected)]

    labels = ["basin", "toilet_bowl", "bathtub", "roof_ac", "smoke_detector", "lamp1", "lamp2", "ac_vent", "lamp3",
              "wall_ac", "fire_hydrant", "pump", "generator", "transformer", "pump_stand"]

    df = pd.DataFrame(zip(labels, results[0], results[1], results[2], train_diff, test_diff, val_diff))
    df.columns = ("Labels", "Train count", "Test Count", "Val Count", "Train_diff", "Test_diff", "Val_diff")
    print(df)
    df.to_csv(rf'./label_freq_{data_name}.csv', index=False)
    return df

def label_difference_json(data_name,input_dir):
    labels = []
    if data_name == 'ARCH':
        labels = ["window", "door", "doorframe", "staircase", "ladder", "curtain_wall", "ramp"]
    else:
        labels = ['ICH_Steel','Rect_Steel']

    results = []
    train_actual = visualize_labelme_labels(os.path.join(input_dir, 'train'))
    test_actual = visualize_labelme_labels(os.path.join(input_dir, 'test'))
    val_actual = visualize_labelme_labels(os.path.join(input_dir, 'val'))

    # print(results)
    sum_dict = {}

    # Iterate through each dictionary in the list
    for key in train_actual.keys():
        # Add the corresponding values from all dictionaries
        sum_dict[key] = train_actual[key] + test_actual.get(key, 0) + val_actual.get(key, 0)

    print(sum_dict)

    train_exp = dict()
    test_exp = dict()
    val_exp = dict()

    for key, value in sum_dict.items():
        # Calculate the values for train, test, and validation sets
        train_value = value * 0.8
        test_value = value * 0.1
        val_value = value * 0.1
        # Add the calculated values to the respective dictionaries
        train_exp[key] = round(train_value)
        test_exp[key] = round(test_value)
        val_exp[key] = round(val_value)

    # print('train_exp', train_exp)
    # print('test_exp', test_exp)
    # print('val_exp', val_exp)

    train_diff = {}
    test_diff = {}
    val_diff = {}

    # Iterate through each key in train_actual
    for key in train_actual.keys():
        # Calculate the differences
        train_diff[key] = train_actual[key] - train_exp[key]
        test_diff[key] = test_actual[key] - test_exp[key]
        val_diff[key] = val_actual[key] - val_exp[key]
    # df = pd.DataFrame.from_records([train_actual,test_actual,val_actual,train_exp,test_exp,val_exp,train_diff,test_diff,val_diff],index=['train_actual','test_actual','val_actual','train_exp','test_exp','val_exp','train_diff','test_diff','val_diff'])

    data = [train_actual,test_actual,val_actual,train_exp,test_exp,val_exp,train_diff,test_diff,val_diff]
    df = pd.DataFrame(data)
    df = df.T

    # df['door']
    # Print the DataFrame
    df.columns = ['train_actual','test_actual','val_actual','train_exp','test_exp','val_exp','train_diff','test_diff','val_diff']

    df.to_csv(rf'./label_freq_{data_name}.csv')
    return df

input_dir = input("Enter input directory path ")


data_name = input("Enter name of dataset: (ARCH|MEP|STR) ")

if data_name == 'ARCH' or data_name=='STR':
    label_difference_json(data_name,input_dir)
elif data_name == 'MEP':
    label_difference_txt(input_dir)
else:
    print("Invalid dataset name!!!")