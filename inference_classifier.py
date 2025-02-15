import pickle
import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import time

# Load the trained model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Alphabet labels
to_labels = {i: chr(65 + i) for i in range(26)}  # 0 -> 'A', 1 -> 'B', ..., 25 -> 'Z'
current_word = ""
last_recognition_time = time.time()  # Track last recognition time
interval = 4  # Interval in seconds

while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()
    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks and (time.time() - last_recognition_time >= interval):
        last_recognition_time = time.time()  # Reset timer
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        prediction = model.predict([np.asarray(data_aux)])
        predicted_character = to_labels[int(prediction[0])]

        print(f"Recognized Letter: {predicted_character}")
        current_word += predicted_character
        print(f"Current Word: {current_word}")

    cv2.putText(frame, f"Word: {current_word}", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 0, 0), 3, cv2.LINE_AA)
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('c'):  # Clear word
        current_word = ""
        print("Word cleared")
    
    if key == ord('b'):  # Backspace to remove last character
        current_word = current_word[:-1]
        print("Last character removed")
    
    if key == ord(' '):  # Space for separating words
        current_word += " "
        print("Space added")
    
    if key == ord('s'):  # Speak the word
        engine.say(current_word)
        engine.runAndWait()
    
    if key == ord('q'):  # Quit
        break

cap.release()
cv2.destroyAllWindows()
