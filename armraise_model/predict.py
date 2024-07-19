import mediapipe as mp
import cv2
import numpy as np
import pickle

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

    with open("rf_classifier", "rb") as handler:
        rf = pickle.load(handler)

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
        landmarks = results.pose_landmarks.landmark
        keypoints = []
        for lm in IMPORTANT_LMS:
            keypoint = landmarks[mp_pose.PoseLandmark[lm].value]
            keypoints.append([keypoint.x, keypoint.y, keypoint.z, keypoint.visibility])
        
        keypoints = list(np.array(keypoints).flatten())
        prediction = rf.predict([keypoints])[0]

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        colors = (114, 219, 140)
        text = 'correct'
        if prediction == 3:
            colors = (0, 0, 255)
            text = 'too high'
        if prediction == 2:
            colors = (255, 0, 255)
            text = 'too wide'
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                                  mp_drawing.DrawingSpec(color=colors, thickness=1, circle_radius=1), 
                                  mp_drawing.DrawingSpec(color=colors, thickness=1, circle_radius=1))
        
        font = cv2.FONT_HERSHEY_SIMPLEX 
  
        fontScale = 0.5
        thickness = 1
        image = cv2.putText(image, text, (10, 20), font,
                        fontScale, colors, thickness, cv2.LINE_AA)

        cv2.imshow("CV2", image)  # display the frame
        k = cv2.waitKey(0) & 0xFF  # delay set to 0, so will wait indefinitely for key press
        count = 0
                
    cap.release()
    cv2.destroyAllWindows()
        
capture_vid("/Users/rohan/GaTech Dropbox/Rohan Modi/Pocket-Trainer/data/InfinityAI_InfiniteRep_armraise_v1.0/data/000010.mp4")
