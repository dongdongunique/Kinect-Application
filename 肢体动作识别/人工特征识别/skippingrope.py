
import cv2
import numpy as np
import time
from module import HandTrackingModule as htm
import PoseModule as pm


# 计算判定点
def max_min(a):
    h = []
    l = []

    for i in range(1, len(a ) -1):
        if(a[ i -1] < a[i] and a[ i +1] < a[i]):
            h.append(a[i])
        elif(a[ i -1] > a[i] and a[ i +1] > a[i]):
            l.append(a[i])
    if(len(h) == 0):
        h.append(max(a))
    if(len(l) == 0):
        l.append(min(a[a.index(max(a)):]))
    mid =(np.mean(h ) +np.mean(l) ) /2
    print(int(mid) ,int(np.mean(h ) -np.mean(l)))
    return(int(mid) ,int(np.mean(h ) -np.mean(l)))
#######################
brushThickness = 25
eraserThickness = 100
########################
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)

detector_hand = htm.handDetector(detectionCon=0.65 ,maxHands=1)
detector_pose = pm.poseDetector()
imgCanvas = np.zeros((480, 640, 3), np.uint8)
rect =[(20, 20), (120, 120)]
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.rectangle(imgCanvas, rect[0], rect[1] ,(0, 255, 0), 2)
cv2.putText(imgCanvas, "SET", (45 ,85), font, 1, drawColor, 2)
bs =0
bs2 =0
bs3 =0
point =[]
count =0
pTime = 0
dire =0
while True:
    success, img = cap.read()
    if success:
        img = cv2.flip(img, 1)
        if bs==1 and bs2==0:
            if bs3==1:
                if time.time( )-time_start <4:
                    cv2.putText(img, str( 3 -int(time.time( ) -time_start)), (300, 240), cv2.FONT_HERSHEY_PLAIN, 10
                                ,(255, 255, 0), 5)
                else:
                    bs3 =0
                    time_start =time.time()
            else:
                if time.time( ) -time_start <11:
                    img = detector_pose.findPose(img, False)
                    lmList = detector_pose.findPosition(img, False)

                    if len(lmList) != 0:
                        point_tem =detector_pose.midpoint(img, 24, 23)
                        point.append(point_tem['y'])
                        cv2.putText(img, str(point_tem['y']), (45, 460), cv2.FONT_HERSHEY_PLAIN, 7 ,(255, 0, 0), 8)
                    cv2.putText(img, str(10 -int(time.time( ) -time_start)), (500, 460), cv2.FONT_HERSHEY_PLAIN, 10
                                ,(255, 255, 0), 5)
                else:
                    point_sd , l =max_min(point)
                    bs =2
                    cv2.rectangle(imgCanvas, rect[0], rect[1] ,(0, 255, 0), 2)
                    cv2.putText(imgCanvas, "START", (30 ,85), font, 1, drawColor, 2)

        if bs==3 and bs2==0:
            if bs3==1:
                if time.time( ) -time_start <4:
                    cv2.putText(img, str( 3 -int(time.time( ) -time_start)), (300, 240), cv2.FONT_HERSHEY_PLAIN, 10
                                ,(255, 255, 0), 5)
                else:
                    bs3 =0
                    time_start =time.time()
            else:
                img = detector_pose.findPose(img, False)
                lmList = detector_pose.findPosition(img, False)

                if len(lmList) != 0:
                    point = detector_pose.midpoint(img, 24, 23)
                    if point["y" ]> point_sd + l /4:

                        if dire == 0:
                            count += 0.5
                            dire = 1
                    if point["y" ] <point_sd - l /4:

                        if dire == 1:
                            count += 0.5
                            dire = 0

                    cv2.putText(img, str(int(count)), (45, 460), cv2.FONT_HERSHEY_PLAIN, 7 ,(255, 0, 0), 8)



        if bs2==1  :  # 等待三秒
            if time.time( ) -time_start >4:
                bs2 =0
                time_start =time.time()

        else:
            # 手势操作
            img = detector_hand.findHands(img)
            lmList = detector_hand.findPosition(img, draw=False)
            if len(lmList)!=0:
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]
                fingers = detector_hand.fingersUp()
                # 出示食指
                if fingers[1] and fingers[2] == False:
                    cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                    if x1 >rect[0][0] and x1 <rect[1][0] and y1 >rect[0][1] and y1 <rect[1][1]  :  # 食指进入按钮区域
                        if bs==0:
                            print("OK")
                            imgCanvas = np.zeros((480, 640, 3), np.uint8)

                            bs =1
                            bs2 =1
                            bs3 =1
                            time_start =time.time()
                        elif bs==1:
                            imgCanvas = np.zeros((480, 640, 3), np.uint8)
                            bs2 =1
                            bs3 =1
                            time_start =time.time()
                        elif bs==2:
                            imgCanvas = np.zeros((480, 640, 3), np.uint8)
                            cv2.rectangle(imgCanvas, rect[0], rect[1] ,(0, 255, 0), 2)
                            cv2.putText(imgCanvas, "STOP", (30 ,85), font, 1, drawColor, 2)
                            bs =3
                            bs2 =1
                            bs3 =1
                            time_start =time.time()
                        elif bs==3:
                            imgCanvas = np.zeros((480, 640, 3), np.uint8)
                            cv2.rectangle(imgCanvas, rect[0], rect[1] ,(0, 255, 0), 2)
                            cv2.putText(imgCanvas, "START", (30 ,85), font, 1, drawColor, 2)
                            bs =2
                            bs2 =1
                            bs3 =1
                            time_start =time.time()

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (500, 100), cv2.FONT_HERSHEY_PLAIN, 5 ,(255, 0, 0), 5)
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        img = cv2.bitwise_or(img ,imgCanvas)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()