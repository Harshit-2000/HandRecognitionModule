import cv2 as cv
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode = False, max_hands = 2, decetion_conf = 0.5, tracking_conf = 0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.decetion_conf = decetion_conf
        self.tracking_conf = tracking_conf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hands, self.decetion_conf, self.tracking_conf)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        if self.result.multi_hand_landmarks:
            for handlms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
        return img

    def getPosition(self, img, handNo = 0, draw = True):
        lmList = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(w * lm.x), int(h * lm.y)
                lmList.append([id, cx, cy])
                if draw:
                    cv.circle(img, (cx,cy), 6, (255,255,255), -1)
        return lmList

def main():
    capture = cv.VideoCapture(0)
    pTime = 0
    cTime = 0

    detector = handDetector()
    while True:
        isTrue, img = capture.read()
        img = detector.findHands(img)
        lmList = detector.getPosition(img, draw = False)

        if len(lmList) != 0:
            print(lmList[0])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_ITALIC, 2, (0, 0, 0), 3)

        cv.imshow('WebCam', img)
        cv.waitKey(1)


if __name__ == '__main__':
    main()