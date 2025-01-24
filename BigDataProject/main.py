import pickle
import cv2

import mediapipe as mp
import numpy as np

modelDict = pickle.load(open('./scripts/model.p', 'rb'))
model = modelDict["model"]

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
mpDrawStyle = mp.solutions.drawing_styles

hands = mpHands.Hands(static_image_mode=True, min_detection_confidence=0.3, max_num_hands=1)

labelsDict = {0: "A", 1: "B", 2: "L"}
while True:
    dataAux = []
    xValues = []
    yValues = []

    ret, frame = cap.read()
    H, W, _ = frame.shape
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frameRGB)

    if results.multi_hand_landmarks:
        for handLandmark in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(
                frame,
                handLandmark,
                mpHands.HAND_CONNECTIONS,
                mpDrawStyle.get_default_hand_landmarks_style(),
                mpDrawStyle.get_default_hand_connections_style())

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

        x1 = int(min(xValues) * W) - 10
        y1 = int(min(yValues) * H) - 30

        x2 = int(max(xValues) * W) + 30
        y2 = int(max(yValues) * H) + 40

        prediction = model.predict([np.asarray(dataAux)])

        predictedCharacter = labelsDict[int(prediction[0])]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        cv2.putText(frame, predictedCharacter, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,
                    1.3, (0, 0, 0), 3, cv2.LINE_AA)

    cv2.imshow("frame", frame)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()