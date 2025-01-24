"""Script for creating the dataset needed for training"""
import os
import pickle

import mediapipe as mp
import cv2

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
mpDrawingStyle = mp.solutions.drawing_styles

hands = mpHands.Hands(static_image_mode=True, min_detection_confidence=0.3, max_num_hands=1)

DATA_DIR = "./data"

data = []
labels = []

for directory in os.listdir(DATA_DIR):
    for imagePath in os.listdir(os.path.join(DATA_DIR, directory)):
        dataAux = []
        xValues = []
        yValues = []

        image = cv2.imread(os.path.join(DATA_DIR, directory, imagePath))
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = hands.process(imageRGB)

        if results.multi_hand_landmarks:
            for handLandmark in results.multi_hand_landmarks:
                for i in range(len(handLandmark.landmark)):
                    x = handLandmark.landmark[i].x
                    y = handLandmark.landmark[i].y

                    xValues.append(x)
                    yValues.append(y)

                for i in range(len(handLandmark.landmark)):
                    x = handLandmark.landmark[i].x
                    y = handLandmark.landmark[i].y

                    dataAux.append(x - min(xValues))
                    dataAux.append(y - min(yValues))

            data.append(dataAux)
            labels.append(directory)

f = open('data.pickle', 'wb')
pickle.dump({"data": data, "labels": labels}, f)
f.close()

