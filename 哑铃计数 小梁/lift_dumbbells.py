import cv2
import numpy as np
import time
import PoseModule as pm
# cap = cv2.VideoCapture("AiTrainer/curls.mp4")
cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    # img = cv2.imread("AiTrainer/test.jpg")
    # 找骨骼，False选择不标出骨骼
    img = detector.findPose(img, False)
    # 找关键点，False选择不标出关键点
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        # 右胳膊
        angle = detector.findAngle(img, 12, 14, 16)
        # 左胳膊，False没画出骨骼
        # angle = detector.findAngle(img, 11, 13, 15,False)
        # 线性插值,根据手臂弯曲的角度
        # 百分比数
        per = np.interp(angle, (220, 310), (0, 100))
        # 窗口中的进度条
        bar = np.interp(angle, (220, 310), (650, 100))
        # print(angle, per)
        # 哑铃计数
        color = (255, 0, 255)
        # 手臂弯曲
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        # 手臂伸直
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)
        # 绘制能量条
        # 框
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        # 值
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        # 显示百分比数
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)
        # 显示计数
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 0, 0), 25)
    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, 'FPS  '+str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) in [ord('q'), 27]:  # 按键盘上的q或esc退出（在英文输入法下）
        break
    cv2.waitKey(1)