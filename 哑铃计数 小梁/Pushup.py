from PoseModule import poseDetector
import mediapipe as mp
import math
import time
import cv2
import numpy as np
direction=0
count=0
def pushup(img,detector:poseDetector,width,height):
    img=detector.findPose(img,False)
    lmlist=detector.findPosition(img,False)
    global count
    global direction
    if(len(lmlist)!=0):
        elbow=detector.findAngle(img,11,13,15)
        shoulder=detector.findAngle(img,13,11,23)
        hip=detector.findAngle(img,11,23,25)
        per=np.interp(elbow,(90,160),(0,100))
        bar=np.interp(elbow,(90,160),(380,50))
        check_ok=0
        feedback="Fix form"
        current_status="Unsure"
        if elbow > 160 and shoulder > 40 and hip > 160:
            check_ok = 1
        if check_ok == 1:
            if per == 0:
                if elbow <= 90 and hip > 160:
                    feedback = "Up"
                    if direction == 0:
                        count += 0.5
                        direction = 1
                else:
                    feedback = "Fix Form"
                    
            if per == 100:
                if elbow > 160 and shoulder > 40 and hip > 160:
                    feedback = "Down"
                    if direction == 1:
                        count += 0.5
                        direction = 0
                else:
                    feedback = "Fix Form"
                        # form = 0
        if check_ok==1:
            cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(img,(580,int(bar)),(600,380),(0,255,0),cv2.FILLED)
            cv2.putText(img,f'{int(per)}',(565,430),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
        cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)
        
        #Feedback 
        cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)
        cv2.imshow("Pushup counter",img)

def main():
    cap=cv2.VideoCapture(0)
    detector=poseDetector()
    while(cap.isOpened()):
        ret,img=cap.read()
        width=cap.get(3)
        height=cap.get(4)
        pushup(img,detector,width,height)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
if __name__=="__main__":
    main()
        
