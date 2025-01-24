"""Script that collects the images used for training"""
import os
import cv2

DATA_DIR = ".\\data\\"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

numberOfClasses = 3
numberOfImages = 100

cap = cv2.VideoCapture(0)

for j in range(numberOfClasses):
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    print("Collecting images for class {}".format(j))

    while True:
        ret, frame = cap.read()
        cv2.putText(frame, "Press 'Q' to start: {}".format(j), (100, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.3, (255, 0, 0), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

    counter = 0
    while counter < numberOfImages:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        print(os.path.join(DATA_DIR, str(j), "{}.jpg".format(counter)))
        cv2.imwrite(os.path.join(DATA_DIR, str(j), "{}.jpg".format(counter)), frame)
        counter += 1

cap.release()
cv2.destroyAllWindows()