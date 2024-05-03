import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib as plt
import numpy as np
import pandas as pd
import os
import json

curr_path = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(curr_path, 'data.json')

with open(json_path) as json_file:
    data = json.load(json_file)
    df_images = pd.DataFrame(data['images']) #line 144
    df_annotations = pd.DataFrame(data['annotations']) # line 4192
    #print(df_images.head)
    #print(df_annotations.head)
    print(df_annotations.shape[0])
    print(df_images.shape[0])