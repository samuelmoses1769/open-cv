import cv2
import time
import numpy as np

import math

import handlandmarksmodule as hlm
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
Minvol=volRange[0]
Maxvol=volRange[1]



ptime=0

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
cap.set(10,100)
detector=hlm.handDetector()

while cap.isOpened():
    _,frame=cap.read()
    frame=detector.finddetector(frame,True)
    list=detector.findlocation(frame,False)
    if len(list)!=0:
        x1,y1=list[4][1],list[4][2]
        x2,y2=list[8][1],list[8][2]
        cx,cy=(x1+x2)/2,(y1+y2)/2
        cx=int(cx)
        cy=int(cy)
        
        
        cv2.circle(frame,(x1,y1),20,(255,0,255),-1)
        cv2.circle(frame,(x2,y2),20,(255,0,255),-1)
        cv2.line(frame,(x1,y1),(x2,y2),(255,0,255),5)
        length=math.hypot(x1-x2,y1-y2)
        #volrange[-63.5,0]
        #lengthrange [50,340]
        vol=np.interp(length,[50,340],[Minvol,Maxvol])
        volBar=np.interp(length,[50,340],[400,150])
        volPer=np.interp(length,[50,340],[0,100])
        volume.SetMasterVolumeLevel(vol, None)
        
        if length<50:
         cv2.circle(frame,(cx,cy),20,(0,255,0),-1)
        else:
         cv2.circle(frame,(cx,cy),20,(255,0,255),-1)
        cv2.rectangle(frame,(50,150),(85,400),(255,0,0),3)
        cv2.rectangle(frame,(50,int(volBar)),(85,400),(255,0,0),-1)
        cv2.putText(frame,f"{int(volPer)}%",(50,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
        
    ctime=time.time()
    fps=1/(ctime-ptime)
    fps=str(int(fps))
    ptime=ctime
    cv2.putText(frame,fps,(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,0),2)
    cv2.imshow("frame",frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()  