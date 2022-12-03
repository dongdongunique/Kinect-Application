
import numpy as np
import time
import cv2
import PoseModule as pm
import siot


siot.init(client_id="SyWH2Af2sV" ,server="iot.dfrobot.com.cn" ,port=1883 ,user="X8jykxFnR" ,password="u8jskbFngz")
siot.connect()
siot.loop()

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
success =True

countpre =0

while success:
    success, img = cap.read()
    if success:
        img = cv2.resize(img, (640, 480))

        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
            # 身体弯曲角度
            angle2 =detector.findAngle(img, 12, 24, 26)
            angle3 =detector.findAngle(img, 24, 26, 28)
            if angle3 >270:
                if angle2 >130:

                    if dir == 0:
                        count += 0.5
                        dir = 1
                if angle2 < 80:

                    if dir == 1:
                        count += 0.5
                        dir = 0
                if countpre != int(count):
                    countpre = int(count)
                    siot.publish(topic="5n92uqBMg", data=str(int(count)))
                    print(int(count))
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(count)), (50, 450), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
        cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 0), 5)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
