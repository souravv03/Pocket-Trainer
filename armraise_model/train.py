# import IPython
import mediapipe as mp
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import precision_score, accuracy_score, f1_score, recall_score, confusion_matrix, ConfusionMatrixDisplay

from sklearn.tree import export_graphviz
# from IPython.display import Image
import graphviz

import warnings
warnings.filterwarnings('ignore')

# Drawing helpers
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def train():
    train_data = pd.read_csv("/Users/rohan/GaTech Dropbox/Rohan Modi/Pocket-Trainer/data/bicep_model/video_1_to_20.csv")
    train_data['label'] = train_data['label'].map({'BACK_POSTURE_INCORRECT':0, 
                                                'UNSYNCHRONIZED_ARMS':1, 
                                                'WIDE_ARMS':2, 
                                                'HIGH_ARMS':3, 
                                                'CORRECT':4})
    train_landmarks = train_data.drop('label', axis=1)
    X_train, X_test, labels_train, labels_test = train_test_split(train_landmarks, train_data['label'], test_size=0.2, random_state=1234)

    # build random forest classifier for front arm raise data
    rf = RandomForestClassifier()
    rf.fit(X_train, labels_train)

    with open("data/bicep_model/rf_classifier.pkl", "wb") as handler:
        pickle.dump(rf, handler)

    results =  rf.predict(X_test)
    accuracy =  accuracy_score(labels_test, results)

"""confusion_matrix = confusion_matrix(labels_test, results, labels=[0, 1, 2, 3, 4])
cmd = ConfusionMatrixDisplay(confusion_matrix, display_labels=None)
cmd.plot()


for i in range(3):
    tree = rf.estimators_[i]
    dot_data = export_graphviz(tree,
                               feature_names=X_train.columns,  
                               filled=True,  
                               max_depth=2, 
                               impurity=False, 
                               proportion=True)
    graph = graphviz.Source(dot_data)
    #IPython.display.Image.display(graph)
    filename = f'tree_{i}.png'
    graph.render(filename, format='png', cleanup=True)"""
train()