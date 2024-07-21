# Pocket-Trainer

Pocket-Trainer is an app designed to help monitor exercise form in real-time using your phone. It provides posture feedback, counts reps out loud, and stores workout data for future analysis.
<br><br>

### Features

- **Real-time Posture Feedback:** Uses machine learning algorithms to check your form and give immediate feedback.
- **Rep Counting:** Automatically counts your reps out loud.
- **Workout Data Storage:** Keeps track of your workout data for future review.
  <br><br>

### Technologies Used

- **Posture Checking Algorithms:** Random Forests, K-Nearest Neighbors (KNN), Logistic Regression
- **Video Analysis:** Toeplitz Inverse Covariance-Based Clustering
- **Video Parsing:** OpenCV, MediaPipe
  <br><br>

### Development Stage

Pocket-Trainer is currently being developed. The React Native app will be available soon.
<br><br>

### Setting Up Python Environment

1. **Clone repository:**

   ```sh
   git clone https://github.com/souravv03/Pocket-Trainer.git
   ```

2. **Create virtual environment:**

   ```sh
   virtualenv venv
   ```

3. **Activate virtual environment:**

   - Windows:
     ```sh
     venv\Scripts\activate
     ```
   - MacOS and Linux:
     ```sh
     source venv/bin/activate
     ```

4. **Install required packages:**
   ```sh
   pip install -r requirements.txt
   ```
   <br><br>

### Running the Scripts

1. **Prepare data:**

   ```sh
   python armraise_model/data.py
   ```

2. **Train models:**

   ```sh
   python armraise_model/train.py
   ```

3. **Make predictions:**
   ```sh
   python armraise_model/predict.py
   ```
   <br><br>

### Contributing

We welcome your ideas and suggestions to improve Pocket-Trainer. If you want to contribute, please contact us.
