# import tensorflow as tf
# from tensorflow.keras import datasets, layers, models
import json

# import matplotlib as plt
# import numpy as np
import pandas as pd


with open('data/InfinityAI_InfiniteRep_armraise_v1.0/data/000000.json') as json_data:
    data = json.load(json_data)
    df = pd.DataFrame(data['annotations'])
    quaternions = df['quaternions']
    created = False
    for landmark_dict in quaternions:
        new_dict = {}
        if type(landmark_dict) != dict:
            continue
        for landmark in landmark_dict:
            new_dict[landmark + "_x"] = landmark_dict[landmark][0]
            new_dict[landmark + "_y"] = landmark_dict[landmark][1]
            new_dict[landmark + "_v"] = landmark_dict[landmark][2]
            new_dict[landmark + "_z"] = landmark_dict[landmark][3]
        if created:
            new_df = pd.DataFrame([new_dict])
            df_new = df_new.append(new_df, ignore_index=True)
        else:
            df_new = pd.DataFrame([new_dict])
            created = True
    print(df_new)
    df_new.to_csv("landmarks.csv")
