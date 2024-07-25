import cv2
import numpy as np
import time
import handdetectormodule as hdm

import autopy
##################
wcam=640
hcam=480
wscr,hscr=autopy.screen.size()
frameR=100
px,py=0,0
cx,cy=0,0
smoothing=7
##################

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)

detector = hdm.handDetector()

ptime = 0

while True:
    _, frame = cap.read()
    ctime = time.time()

    fps = 1 / (ctime - ptime)
    ptime = ctime
    fps = str(int(fps))
    frame = detector.finddetector(frame, True)
    list, bbox = detector.findlocation(frame)
    if len(list) != 0:
        x1,y1=list[8][1:]
        x2,y2=list[12][1:]
        fingers = detector.finger()
        cv2.rectangle(frame,(frameR-20,frameR-10),(wcam-frameR+20,hcam-frameR+10),(0,255,0),3)
        if fingers[1]==1 and fingers[2]==0:
            x3=np.interp(x1,(frameR,wcam-frameR),(0,wscr))
            y3=np.interp(y1,(frameR,hcam-frameR),(0,hscr))
            cx=px+(x3-px)/smoothing
            cy=py+(y3-py)/smoothing
            cv2.circle(frame,(x1,y1),10,(255,255,0),-1)
            autopy.mouse.move(cx,cy)
            px,py=cx,cy
        if fingers[1]==1 and fingers[2]==1:
            length,frame,mid=detector.finddistance(8,12,True)
            if length<30:
                cv2.circle(frame,(mid[4],mid[5]),20,(0,255,0),-1)
                autopy.mouse.click()


    cv2.putText(frame, fps, (20, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255,0, 0), 2)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()