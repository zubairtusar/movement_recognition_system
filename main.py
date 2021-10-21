from mpu9250_manual_lib import *
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
from scipy import stats
loaded_model = pickle.load(
    open("model_relax_vs_walking_fast", 'rb'))


def get_features(x_data):
    # Set features list
    features = []

    # Calculate features (STD, Average, Max, Min) for each data columns X Y Z
    for k in range(0, 3):
        # std
        mean = np.average(x_data[k])
        features.append(sum([((x - mean) ** 2) for x in x_data[k]]) ** 0.5)
        # avg
        features.append(mean)
        # max
        features.append(np.max(x_data[k]))
        # min
        features.append(np.min(x_data[k]))
        # median
        features.append(np.median(x_data[k]))
        # mode
        features.append(stats.mode(x_data[k])[0][0])
    return features


time.sleep(1)  # delay necessary to allow mpu9250 to settle

while True:
    start_time = time.time()
    seconds = 8
    window = []
    print('recording data')

    while True:
        try:
            ax, ay, az, wx, wy, wz = mpu6050_conv()  # read and convert mpu6050 data
            window.append([ax, ay, az])
            # print('{}'.format('-'*30))
            # print(
            #     'accel [g]: x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(ax, ay, az))
            time.sleep(0.024)
        except:
            continue
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > seconds:
            #print("Finished iterating in: " + str(int(elapsed_time)))

            # df = pd.DataFrame(window, columns=[
            #     'Accelerometer X', 'Accelerometer Y', 'Accelerometer Z'])

            # print(df.head(10))
            # print(df.shape)

            features_list = []
            features_list.append(get_features(window))
            #print("features: ", features_list)

            pred = loaded_model.predict(features_list)
            print(pred)
            # if pred[0] == 1 :
            #     print("Doing other activities")
            # else:
            #     print("Walking fast")
            break
