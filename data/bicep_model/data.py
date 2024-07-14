import csv
import cv2
import mediapipe as mp
import numpy as np


DATASET_PATH = "/Users/rohan/GaTech Dropbox/Rohan Modi/Pocket-Trainer/data/bicep_model/train2.csv"
IMPORTANT_LMS = [
    "NOSE",
    "LEFT_SHOULDER",
    "RIGHT_SHOULDER",
    "RIGHT_ELBOW",
    "LEFT_ELBOW",
    "RIGHT_WRIST",
    "LEFT_WRIST",
    "LEFT_HIP",
    "RIGHT_HIP",
]

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def capture_vid(video_path):
    cap = cv2.VideoCapture(video_path)
    
    while cap.isOpened():
        ret, image = cap.read()
        if not ret:
            break
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False  # for mp performance
        results = pose.process(image)
        if not results.pose_landmarks:
            print(f"landmarks not found for {image}")
            continue
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                                  mp_drawing.DrawingSpec(color=(244, 117, 66), thickness=1, circle_radius=1), 
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=1, circle_radius=0.5))
        
        cv2.imshow("CV2", image)  # display the frame
        k = cv2.waitKey(0) & 0xFF  # delay set to 0, so will wait indefinitely for key press
        if k == ord('c'):
            export_landmark_to_csv(DATASET_PATH, results, "CORRECT")
        elif k == ord("h"):
            export_landmark_to_csv(DATASET_PATH, results, "HIGH_ARMS")
        elif k == ord("w"):
            export_landmark_to_csv(DATASET_PATH, results, "WIDE_ARMS")
        elif k == ord("u"):
            export_landmark_to_csv(DATASET_PATH, results, "UNSYNCHRONIZED_ARMS")   
        elif k == ord("b"):
            export_landmark_to_csv(DATASET_PATH, results, "BACK_POSTURE_INCORRECT")  
        elif k == ord('q'):
            break
        else: continue


        
    cap.release()
    cv2.destroyAllWindows()
        

def export_landmark_to_csv(dataset_path: str, results, action: str) -> None:
    '''
    Export Labeled Data from detected landmark to csv
    '''
    landmarks = results.pose_landmarks.landmark
    keypoints = []

    try:
        # Extract coordinate of important landmarks
        for lm in IMPORTANT_LMS:
            keypoint = landmarks[mp_pose.PoseLandmark[lm].value]
            keypoints.append([keypoint.x, keypoint.y, keypoint.z, keypoint.visibility])
        
        keypoints = list(np.array(keypoints).flatten())

        # Insert action as the label (first column)
        keypoints.insert(0, action)
        print("keypoints:", keypoints)
        # Append new row to .csv file
        with open(dataset_path, mode="a", newline="") as f:
            csv_writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(keypoints)
        
    except Exception as e:
        print(e)
        pass

capture_vid("/Users/rohan/GaTech Dropbox/Rohan Modi/Pocket-Trainer/data/InfinityAI_InfiniteRep_armraise_v1.0/data/000000.mp4")

