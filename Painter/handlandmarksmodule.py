import cv2 
import mediapipe as mp
import time


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
        if self.result.multi_hand_landmarks:
            for handlms in self.result.multi_hand_landmarks:
                for id,lm in enumerate(handlms.landmark):
                    h,w,c=img.shape
                    cx,cy=int(lm.x*w),int(lm.y*h)
                    self.list.append([id,cx,cy])
                    if draw:
                        cv2.circle(self.frame,(cx,cy),5,(255,0,255),-1)
        return self.list
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
def  main():
    ctime=0
    ptime=0
    cap=cv2.VideoCapture(0)
    cap.set(3,2000)
    cap.set(4,2000)
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
     list=detector.findlocation(frame)
     if len(list)!=0:
         print(list[4])
         fingers=detector.finger()
         print(fingers)
        
     cv2.imshow("frame",frame)
     if cv2.waitKey(1)&0xFF==ord('q'):
        break
    cap.release()
    cv2.destroyAllWindows()  
    
if __name__=="__main__":
    main()
    
    
    
