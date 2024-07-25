import cv2 
import mediapipe as mp
import time
import math

class handDetector:
    def __init__(self):
        self.mphands=mp.solutions.hands
        self.hands=self.mphands.Hands()
        self.mpdraw=mp.solutions.drawing_utils
        self.tips=[4,8,12,16,20]
    def finddetector(self,frame,draw=True):
        self.frame=cv2.flip(frame,1)
        self.img=cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
        self.result=self.hands.process(self.img)
        if self.result.multi_hand_landmarks:
            for handlms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(self.frame,handlms,self.mphands.HAND_CONNECTIONS,landmark_drawing_spec=self.mpdraw.DrawingSpec(color=(0,0,255)),connection_drawing_spec=self.mpdraw.DrawingSpec(color=(0,255,0)))
        return  self.frame
    def findlocation(self,img,draw=True):
        self.list=[]
        xlist=[]
        ylist=[]
        bbox=[]
        if self.result.multi_hand_landmarks:
            for handlms in self.result.multi_hand_landmarks:
                for id,lm in enumerate(handlms.landmark):
                    h,w,c=img.shape
                    cx,cy=int(lm.x*w),int(lm.y*h)
                    self.list.append([id,cx,cy])
                    xlist.append(cx)
                    ylist.append(cy)
                x1,x2=min(xlist),max(xlist)
                y1,y2=min(ylist),max(ylist)
                bbox=[x1,y1,x2,y2]
                if draw:
                    cv2.rectangle(img,(x1-20,y1-20),(x2+20,y2+20),(255,0,255),2)
        return self.list,bbox
                        
        
    def finger(self):
        fingers=[]
        
        if len(self.list)!=0:
            for i in self.tips:
                if i==4:
                    if self.list[i][1]<self.list[i-1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
               
                else:
                    if self.list[i][2]<self.list[i-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)          
        return fingers    
    
    def finddistance(self,p1,p2,draw=True,r=20,t=3):
        length=0
        if len(self.list)!=0:
            x1,y1=self.list[p1][1:]
            x2,y2=self.list[p2][1:]
            cx,cy=(x1+x2)//2,(y1+y2)//2
            length=math.hypot((x2-x1),(y2-y1))
            if draw:
                cv2.line(self.frame,(x1,y1),(x2,y2),(255,0,0),t)
                cv2.circle(self.frame,(x1,y1),r,(0,255,255),-1)
                cv2.circle(self.frame,(x2,y2),r,(0,255,255),-1)
                cv2.circle(self.frame,(cx,cy),r,(255,0,255),-1)
        return length,self.frame,[x1,y1,x2,y2,cx,cy]
def  main():
    ctime=0
    ptime=0
    cap=cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)
    cap.set(10,100)
    detector=handDetector()
    while True:
   
     _,frame=cap.read()
     ctime=time.time()
     
     fps=1/(ctime-ptime)
     ptime=ctime
     fps=str(int(fps))
     frame=detector.finddetector(frame,True)
     cv2.putText(frame,fps,(20,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
     list,bbox=detector.findlocation(frame)
     if len(list)!=0:
        print(list[4])
        fingers=detector.finger()
        #length,frame,=detector.finddistance(4,8)
        #print(length)
        
     cv2.imshow("frame",frame)
     if cv2.waitKey(1)&0xFF==ord('q'):
        break
    cap.release()
    cv2.destroyAllWindows()  
    
if __name__=="__main__":
    main()
    
    
    
