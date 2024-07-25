import cv2
import time
import os

import handlandmarksmodule as hlm
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,4800)
cap.set(10,300)

folderpath="Resources/FingerImages"
mylist=os.listdir(folderpath)
overlaylist=[]
for impath in mylist:
    image=cv2.imread(f'{folderpath}/{impath}')
    overlaylist.append(image)
    print(f'{folderpath}/{impath}')
ptime=0
detector=hlm.handDetector()
tips=[4,8,12,16,20]
while True:
    _,frame=cap.read()
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    fps=str(int(fps))
    frame=detector.finddetector(frame)
    list=detector.findlocation(frame,False)
    cv2.putText(frame,fps,(500,70),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,0),2)
    if len(list)!=0:
        fingers=[]
        for i in tips:
            if i==4:
                if list[i][1]<list[i-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
               
            else:
                if list[i][2]<list[i-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        count=fingers.count(1)
        img=overlaylist[count-1]
        h,w,c=img.shape
        frame[0:h,0:w]=img
        count=str(count)
        cv2.rectangle(frame,(0,225),(150,425),(0,255,0),-1)
        cv2.putText(frame,count,(25,375),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),25)
    cv2.imshow("frame",frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()