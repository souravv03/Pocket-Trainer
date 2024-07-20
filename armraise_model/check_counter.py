class CountArmRaiseReps:
    def __init__(self):
        self.rep_count = 0
        self.vector = []
        self.going_up = True

    def update_vector(self, right_wrist, left_wrist, right_shoulder, left_shoulder, right_hip, left_hip):
        """function to add latest coordinates to self.vector
        hand0 - x, y; hand1 - x1, y1
        calls count_reps() to check if updated self.vector increments self.rep_count
        returns rep count
        """
        self.count_reps(right_wrist, left_wrist, right_shoulder, left_shoulder, right_hip, left_hip)
        return self.rep_count

    def count_reps(self, right_wrist, left_wrist, right_shoulder, left_shoulder, right_hip, left_hip):
        """function to increment self.rep_count when necessary
        currently increments by 0.5 when going up and both y values are less than 100
        also increments by 0.5 when going down and both y values are over 500
        """
        if self.going_up and (right_wrist <= right_shoulder or left_wrist <= left_shoulder):
            self.going_up = False
        elif not self.going_up and (right_wrist >= right_hip or left_wrist >= left_hip):
            self.going_up = True
            self.rep_count += 1
