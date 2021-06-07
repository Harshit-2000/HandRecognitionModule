import cv2 as cv
import mediapipe as mp
import time

capture = cv.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    isTrue, img = capture.read()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    result = hands.process(imgRGB)

    if result.multi_hand_landmarks:
        for handlms in result.multi_hand_landmarks:
            for id, lm in enumerate(handlms.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(h*lm.x), int(w*lm.y)
                print(id, cx, cy)

            mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, str(int(fps)), (10, 70), cv.FONT_ITALIC, 2, (0,0,0),3)

    cv.imshow('WebCam', img)
    cv.waitKey(1)
