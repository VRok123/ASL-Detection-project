import os
import cv2

# Define the data directory
DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 26
dataset_size = 100

# Initialize the camera with proper error handling
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access the camera. Check the camera index or permissions.")
    exit()

for j in range(number_of_classes):
    # Create directories for each class if not already existing
    class_dir = os.path.join(DATA_DIR, str(j))
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    print(f'Collecting data for class {j}')

    # Initial prompt loop
    while True:
        ret, frame = cap.read()

        # Validate the captured frame
        if not ret or frame is None:
            print("Warning: Failed to capture frame. Retrying...")
            continue

        cv2.putText(
            frame, 
            'Ready? Press "Q" to start collecting!', 
            (50, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1.0, 
            (0, 255, 0), 
            2, 
            cv2.LINE_AA
        )
        cv2.imshow('frame', frame)

        # Break when 'q' is pressed
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Data collection loop
    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()

        # Validate the captured frame
        if not ret or frame is None:
            print("Warning: Failed to capture frame. Retrying...")
            continue

        # Display the frame and save it
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        file_path = os.path.join(class_dir, f'{counter}.jpg')
        cv2.imwrite(file_path, frame)
        print(f"Saved: {file_path}")

        counter += 1

# Release resources
cap.release()
cv2.destroyAllWindows()