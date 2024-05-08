import cv2
import mediapipe as mp


class CountReps:
    def __init__(self):
        self.rep_count = 0
        self.vector = []
        self.going_up = True

    def update_vector(self, x, y, x1, y1):
        """function to add latest coordinates to self.vector
        hand0 - x, y; hand1 - x1, y1
        calls count_reps() to check if updated self.vector increments self.rep_count
        returns rep count
        """
        self.vector.append((x, y, x1, y1))
        self.count_reps()
        return self.rep_count

    def count_reps(self):
        """function to increment self.rep_count when necessary
        currently increments by 0.5 when going up and both y values are less than 100
        also increments by 0.5 when going down and both y values are over 500
        """
        if self.going_up and self.vector[-1][1] < 100 and self.vector[-1][3] < 100:
            self.going_up = False
            self.rep_count += 0.5
        elif not self.going_up and self.vector[-1][1] > 500 and self.vector[-1][3] > 500:
            self.going_up = True
            self.rep_count += 0.5
    # 500 - 100


# only for hand landmarks, will need to use different model for body pose
class HandTracker:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, modelComplexity=1, trackCon=0.5):
        self.results = None
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def hands_finder(self, img, draw=True):
        imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def position_finder(self, img, handNo=0, draw=True):
        landmark_list = []
        if self.results.multi_hand_landmarks:
            cx = None
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmark_list.append([id, cx, cy])
            h, w, c = img.shape
            cx, cy = int(Hand.landmark[8].x * w), int(Hand.landmark[8].y * h)
            if draw:
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                return cx, cy
        return landmark_list


def check_vid():
    """
    display video with rep-count, hand0 position, hand1 position
    calls CountReps.update_vector() every time both hands are on camera, updating rep_count when needed
    """
    countReps = CountReps()
    cap = cv2.VideoCapture(1)
    tracker = HandTracker()
    rep_count = 0
    while True:
        success, image = cap.read()
        image = tracker.hands_finder(image)
        cv2.putText(image, "counting " + "arm raises", (50, 200), 0, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(image, "rep_count: " + str(rep_count), (50, 150), 0, 1, (0, 0, 255), 1, cv2.LINE_AA)

        try:
            hand0 = tracker.position_finder(image, handNo=0)  # hand0 position (x, y)
            hand1 = tracker.position_finder(image, handNo=1)  # hand1 position
        except Exception as e:
            cv2.putText(image, "hand not detected", (50, 100), 0, 1, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imshow("Video", image)
            cv2.waitKey(1)
            continue
        if hand0 == [] or hand1 == []:
            cv2.putText(image, "hand not detected", (50, 100), 0, 1, (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imshow("Video", image)
            cv2.waitKey(1)
            continue
        cv2.putText(image, "hand0:", (50, 65), 0, 1, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(image, str(hand0), (50, 100), 0, 1, (0, 0, 255), 1, cv2.LINE_AA)

        cv2.putText(image, "hand1", (250, 65), 0, 1, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(image, str(hand1), (250, 100), 0, 1, (0, 0, 255), 1, cv2.LINE_AA)

        rep_count = countReps.update_vector(hand0[0], hand0[1], hand1[0], hand1[1])

        cv2.imshow("Video", image)
        cv2.waitKey(1)


check_vid()
