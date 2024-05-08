# Data Visualization Script and Preliminary Findings

# import tensorflow as tf
# from tensorflow.keras import datasets, layers, models
import json
import matplotlib.pyplot as plt
# import numpy as np
import pandas as pd

landmark_df = pd.read_csv('landmarks.csv')


wrist_y_diff = landmark_df["right_wrist_y"] - landmark_df["left_wrist_y"]
wrist_x_diff = landmark_df["right_wrist_x"] - landmark_df["left_wrist_x"]
wrist_z_diff = landmark_df["right_wrist_z"] - landmark_df["left_wrist_z"]

#print(landmark_df["right_elbow_y"].min())
#print(landmark_df["right_elbow_y"].max())

#plt.plot(landmark_df["left_elbow_y"],landmark_df["right_elbow_y"])
plt.plot(range(0, len(wrist_y_diff)), wrist_y_diff, label="y")
plt.plot(range(0, len(wrist_x_diff)), wrist_x_diff, label="x")
plt.plot(range(0, len(wrist_z_diff)), wrist_z_diff, label="z")
plt.show()


# Specifically looking at arm raises
# We state to the user to begin at some specified start point (arms low/arms high)
# Note we specify arms low
# Initial Idea:
# Record starting benchmark location for some x number of features
# Once the rep is completed theoretically, those features will come into close proximity
# of the recorded benchmark, we then denote this as 1 rep
# Then we must check the frames in between the then start point and end point
# If the features approach some specfied location somewhere in between the middle
# of those two points, we classify it as a repetition and increment

# define the baseline as all the frames where left wrist is below left hip and right wrist is below right hip
# once it leaves this baseline area, we begin checking if it is approaching top baseline
# top baseline is whenever 
