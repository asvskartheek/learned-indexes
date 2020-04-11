import pandas as pd
from sklearn.model_selection import train_test_split
import datetime

def hybrid_training(threshold, use_threshold, stage_nums, core_nums, train_step_nums, batch_size_nums, learning_rate_nums,
                    keep_ratio_nums, train_data_x, train_data_y, test_data_x, test_data_y):
    stage_length = len(stage_nums)
    col_num = stage_nums[1]

    tmp_inputs = [[[] for i in range(col_num)] for i in range(stage_length)]
    tmp_labels = [[[] for i in range(col_num)] for i in range(stage_length)]
    index = [[None for i in range(col_num)] for i in range(stage_length)]
    tmp_inputs[0][0] = train_data_x
    tmp_labels[0][0] = train_data_y
    test_inputs = test_data_x
    for i in range(0, stage_length):
        for j in range(0, stage_nums[i]):
            if len(tmp_labels[i][j]) == 0:
                continue
            inputs = tmp_inputs[i][j]
            labels = []
            test_labels = []
            if i == 0:
                divisor = stage_nums[i + 1] // (TOTAL_NUMBER // BLOCK_SIZE)
                for k in tmp_labels[i][j]:
                    labels.append(int(k * divisor))
                for k in test_data_y:
                    test_labels.append(int(k * divisor))
            else:
                labels = tmp_labels[i][j]
                test_labels = test_data_y              
            tmp_index = TrainedNN(threshold[i], use_threshold[i], core_nums[i], train_step_nums[i], batch_size_nums[i],
                                    learning_rate_nums[i], keep_ratio_nums[i], inputs, labels, test_inputs, test_labels)            
            tmp_index.train()      
            index[i][j] = AbstractNN(tmp_index.get_weights(), tmp_index.get_bias(), core_nums[i], tmp_index.cal_err())
            del tmp_index
            gc.collect()
            if i < stage_length - 1:
                for ind in range(len(tmp_inputs[i][j])):
                    p = index[i][j].predict(tmp_inputs[i][j][ind])                    

                    if p > stage_nums[i + 1] - 1:
                        p = stage_nums[i + 1] - 1
                    tmp_inputs[i + 1][p].append(tmp_inputs[i][j][ind])
                    tmp_labels[i + 1][p].append(tmp_labels[i][j][ind])

    for i in range(stage_nums[stage_length - 1]):
        if index[stage_length - 1][i] is None:
            continue
        mean_abs_err = index[stage_length - 1][i].mean_err
        print("mean abs err:", mean_abs_err)
        if mean_abs_err > threshold[stage_length - 1]:
            print("Using BTree")
            index[stage_length - 1][i] = BTree(32)
            index[stage_length - 1][i].build(tmp_inputs[stage_length - 1][i], tmp_labels[stage_length - 1][i])
    return index

data = pd.read_csv('data/exponential.csv')
X = data['key'].values
y = data['value'].values

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.1,random_state=42)

threshold = [55, 10000]
use_threshold = [True,False]

print("Start Train")
start_time = datetime.datetime.now()
trained_index = hybrid_training(threshold, use_threshold, stage_set, core_set, train_step_set, batch_size_set, learning_rate_set, keep_ratio_set, X_train, y_train, [], [])
learn_time = datetime.datetime.now() - start_time
print("Build Learned NN time ", learn_time)