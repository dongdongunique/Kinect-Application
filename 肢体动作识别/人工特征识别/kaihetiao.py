import numpy as np
import time
import cv2
import PoseModule as pm
from pathlib import Path
import sys

my_file = Path("module/data.txt")
if not my_file.is_file():
    print("没有标准数据文件")
    sys.exit()
else:
    f = open("module/data.txt", encoding="utf-8")
    data = f.read()
    data = data.split(",")
    f.close()
# from pinpong.board import Board,Pin,NeoPixel
# NEOPIXEL_PIN = Pin.P0
# PIXELS_NUM = 120 #灯数
# Board("microbit").begin()  #初始化
# npX = NeoPixel(Pin(NEOPIXEL_PIN), PIXELS_NUM)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(3, 640)
cap.set(4, 480)
detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
success = True

while success:
    success, img = cap.read()
    if success:
        img = cv2.resize(img, (640, 480))

        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
            # 双腿夹角
            angle1 = detector.findAngle(img, 28, 23, 27)
            # 双臂与躯干夹角
            angle2 = detector.findAngle(img, 15, 11, 23)
            angle3 = detector.findAngle(img, 16, 12, 24)
            # print(angle1,angle2,angle3)
            per1 = np.interp(angle1, (int(data[1]), int(data[0])), (0, 100))
            per2 = np.interp(angle2, (int(data[3]), int(data[2])), (100, 0))
            per3 = np.interp(angle3, (int(data[5]), int(data[4])), (0, 100))

            # print(angle, per)
            # 计算个数
            per = per1 + per2 + per3
            # print(per1,per2,per3)
            if per == 300:

                if dir == 0:
                    count += 0.5
                    dir = 1
            if per == 0:

                if dir == 1:
                    count += 0.5
                    dir = 0
            # print(count)
            # light = int(np.interp(int(count)), (0, 120), (0, 120)))
            # npX.rainbow(0, light, 0, 0x0000FF)
            cv2.putText(img, str(int(count)), (45, 460), cv2.FONT_HERSHEY_PLAIN, 7, (255, 0, 0), 8)
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()
