import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    # Read the frame from the video capture object
    ret, frame = cap.read()

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe hands
    with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5) as hands:
        results = hands.process(frame_rgb)

        # Get the zoom level
        zoom_level = 1  # Default zoom level

        # Calculate zoom level if hands detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get the coordinates of the thumb tip and index finger tip
                thumb_tip = np.array([hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x,
                                      hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y])
                index_finger_tip = np.array([hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x,
                                             hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y])

                # Calculate the distance between the thumb tip and index finger tip
                distance = np.linalg.norm(thumb_tip - index_finger_tip)

                # Use the distance to control the zoom level
                zoom_level = int(distance * 20)  # Adjust the multiplier as needed

    # Draw zoom level indicator
    cv2.rectangle(frame, (10, 10), (10 + zoom_level, 20), (0, 255, 0), -1)

    # Display the frame
    cv2.imshow('Hand Tracking with Zoom Level', frame)

    # Print the zoom level to the console
    print("Zoom Level:", zoom_level)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()
