import cv2
import numpy as np
import os
import time
import handlandmarksmodule as hlm


folderpath="Resources/paint"
mylist=os.listdir(folderpath)

overlaylist=[]
for path in mylist:
    img=cv2.imread(f"{folderpath}/{path}")
    overlaylist.append(img)

#######################
xp,yp=0,0
brushthickness=15
eraserthickness=100
#######################

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
cap.set(10,300)

header=overlaylist[0]
img=np.zeros((720,1280,3),np.uint8)

ptime=0

detector=hlm.handDetector()

color=(255,0,0)

while True:
    _,frame=cap.read()
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    fps=str(int(fps))
    
    
    
    
    
    frame=detector.finddetector(frame)
    list=detector.findlocation(frame,False)
    if len(list)!=0:
        fingers=detector.finger()
        x1,y1=list[8][1:]
        x2,y2=list[12][1:]
        count=fingers.count(1)
        if fingers[1]==0:
            xp,yp=0,0
        if fingers[1]&fingers[2]&(not(fingers[0]|fingers[3]|fingers[4])):
            
            if y1<180:
                if 185<x1<345:
                    header=overlaylist[0]
                    color=(255,0,0)
                elif 405<x1<550:
                    header=overlaylist[1]
                    color=(0,255,0)
                elif 650<x1<750:
                    header=overlaylist[2]
                    color=(0,255,255)
                elif 840<x1<950:
                    header=overlaylist[3]
                    color=(0,0,255)
                elif 1055<x1<1200:
                    header=overlaylist[4]
                    color=(0,0,0)
            cv2.rectangle(frame,(x1-10,y1-10),(x2+25,y2+10),color,-1)
            
        if fingers[1]&(fingers[2]==False):
            cv2.circle(frame,(x1,y1),25,color,-1)
            if xp==0 and yp==0:
                xp,yp=x1,y1
            if color==(0,0,0):
                cv2.line(frame,(xp,yp),(x1,y1),color,eraserthickness)
                cv2.line(img,(xp,yp),(x1,y1),color,eraserthickness)
            else:
                cv2.line(frame,(xp,yp),(x1,y1),color,brushthickness)
                cv2.line(img,(xp,yp),(x1,y1),color,brushthickness)
            xp,yp=x1,y1
        if count==5:
            img=np.zeros((720,1280,3),np.uint8)
    imggray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,imginv=cv2.threshold(imggray,10,255,cv2.THRESH_BINARY_INV)        
    imginv=cv2.cvtColor(imginv,cv2.COLOR_GRAY2BGR)
    frame=cv2.bitwise_and(frame,imginv)   
    frame=cv2.bitwise_or(frame,img)
        

        
        
        
        
    frame[0:125,0:1280]=header    
    cv2.putText(frame,fps,(1200,200),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),6)
    cv2.imshow("frame",frame)
    
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


