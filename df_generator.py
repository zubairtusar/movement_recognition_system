from mpu9250_manual_lib import *
import numpy as np
import pandas as pd


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
    return features


time.sleep(1)  # delay necessary to allow mpu9250 to settle

counter = 0
window = []
while counter < 200:
    start_time = time.time()
    seconds = 8
    #window = []
    print('recording data')

    while True:
        try:
            ax, ay, az, wx, wy, wz = mpu6050_conv()
            window.append([time.time(), ax, ay, az, 1])
            time.sleep(0.024)
        except:
            continue
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > seconds:
            counter = counter + 1
            print(len(window))
            break
df = pd.DataFrame(window, columns=[
                  'Timestamp UTC', 'Accelerometer X', 'Accelerometer Y', 'Accelerometer Z', 'Label'])
df.to_csv('generated_walk.csv')
