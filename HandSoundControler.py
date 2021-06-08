import cv2 as cv
import numpy as np
import time
import HandRecognitionModule as hrm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

xCam, yCam = 640, 480

capture = cv.VideoCapture(0)
capture.set(3, xCam)
capture.set(4, yCam)

pTime = 0

detector = hrm.handDetector(decetion_conf=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

maxVol = volRange[1]
minVol = volRange[0]

volBar = 400
while True:
    isTrue, img = capture.read()
    img = detector.findHands(img)
    lmList = detector.getPosition(img, draw = False)

    if len(lmList) != 0:
        indexFinger, thumb= lmList[8], lmList[4]
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx , cy = (x2 + x1) // 2, (y2 + y1) // 2

        cv.circle(img, (x1, y1), 10, (255, 0, 255), -1)
        cv.circle(img, (x2, y2), 10, (255, 0, 255), -1)
        cv.circle(img, (cx, cy), 10, (255, 0, 255), -1)
        cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

        length = math.hypot(x2 - x1, y2 - y1)
        vol = np.interp(length, [50, 200], [minVol, maxVol])
        volBar = np.interp(length, [50, 200], [400, 150 ])

        volume.SetMasterVolumeLevel(vol, None)

        if length <= 50:
            cv.circle(img, (cx, cy), 10, (0, 255, 0), -1)
        print(length)

    cv.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv.putText(img, str(int(fps)), (10, 70), cv.FONT_ITALIC, 2, (0, 0, 0), 2)
    cv.imshow('WebCam', img)
    cv.waitKey(1)
