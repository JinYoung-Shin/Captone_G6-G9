import numpy as np
import cv2
import math
import time
import pygame
import copy
import DobotDllType as dType

# Video recognition function
def Cam() :
    pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
    bang = pygame.mixer.Sound('voice/ready.wav')
    bang.play()
    time.sleep(bang.get_length())

    webcam = cv2.VideoCapture(0)

    if webcam.isOpened():  # try to get the first frame
        rval, image = webcam.read()
    else:
        rval = False

    # define the list of acceptable colors
    colors = [([0, 133, 77], [255, 173, 127])]

    while rval:
        # loop over the boundaries
        for (lower, upper) in colors:
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")
            imgg = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
            # find the colors within the specified boundaries and apply the mask
            mask = cv2.inRange(imgg, lower, upper)
            output = cv2.bitwise_and(imgg, imgg, mask=mask)  # output = cv2.bitwise_and(imgg, imgg, mask=mask)

        rval, image = webcam.read()
        edges = cv2.Canny(output, 30, 30, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
        image2 = copy.copy(image)
        img = cv2.medianBlur(image, 15)
        imgg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        circles = cv2.HoughCircles(imgg, cv2.HOUGH_GRADIENT, 1, 5,
                                   param1=50, param2=30, minRadius=0, maxRadius=15)
        if circles != None:
            index = 0
            for i in circles[0, :]:
                # draw the outer circle
                if index < 2:
                    cv2.circle(image2, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    print(i[0], i[1])
                    # draw the center of the circle
                    cv2.circle(image2, (i[0], i[1]), 2, (0, 0, 255), 3)
                    index = index + 1

        if lines != None:
            index2 = 0
            for x in range(0, 1):
                if (index2 < 3):
                    for rho, theta in lines[x]:
                        x1 = int(np.cos(theta) * rho + 1000 * (-np.sin(theta)))
                        y1 = int(np.sin(theta) * rho + 1000 * np.cos(theta))
                        x2 = int(np.cos(theta) * rho - 1000 * (-np.sin(theta)))
                        y2 = int(np.sin(theta) * rho - 1000 * np.cos(theta))
                        cv2.line(output, (x1, y1), (x2, y2), (0, 0, 255), 1)
                        cv2.line(image2, (x1, y1), (x2, y2), (0, 0, 255), 1)
                        index2 = index2 + 1

        cv2.imshow("images", np.hstack([image2, output]))  # output
        cv2.imshow("tes ", edges)

        key = cv2.waitKey(20)
        if key in [27, ord('Q'), ord('q')]:  # exit on ESC, q
            if lines != None and circles != None:
                pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
                bang = pygame.mixer.Sound('voice/yes.wav')
                bang.play()
                time.sleep(bang.get_length())
                break;

            if lines != None and circles == None:
                pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
                bang = pygame.mixer.Sound('voice/bolt.wav')
                bang.play()
                time.sleep(bang.get_length())
            if circles != None and lines == None:
                pygame.mixer.init(frequency=16500, size=-16, channels=2, buffer=4096)
                bang = pygame.mixer.Sound('voice/position.wav')
                bang.play()
                time.sleep(bang.get_length())

    for x in range(0, 1):
        for rho, theta in lines[x]:
            x1 = int(np.cos(theta) * rho + 1000 * (-np.sin(theta)))
            y1 = int(np.sin(theta) * rho + 1000 * np.cos(theta))
            x2 = int(np.cos(theta) * rho - 1000 * (-np.sin(theta)))
            y2 = int(np.sin(theta) * rho - 1000 * np.cos(theta))
            cv2.line(output, (x1, y1), (x2, y2), (0, 0, 255), 1)
            
            y1 = -1 * y1
            y2 = -1 * y2
            a = (y2 - y1) / (x2 - x1)

    d = [4000, 4000, 4000, 4000, 4000]
    j = 0

    dex = 0;

    for i in circles[0, :]:
        # draw the outer circle
        if dex < 2:
            cv2.circle(image2, (i[0], i[1]), i[2], (0, 255, 0), 2)
            print(i[0], i[1])
            # draw the center of the circle
            cv2.circle(image2, (i[0], i[1]), 2, (0, 0, 255), 3)
            i[1] = -1 * i[1]
            d[j] = abs(a * (i[0] - x1) + y1 - i[1]) / (math.sqrt(a * a + 1))
            j = j + 1
            dex = dex + 1

    j = 0
    for i in d:
        if min(d) == i:
            mi = j
        j = j + 1
    print(circles[0, mi][0], circles[0, mi][1])

    cv2.imshow('Edges', image2)
    cv2.imshow('Output', output)
    #cv2.waitKey()

    return (circles[0,mi][0], -circles[0,mi][1])

# Move starting point function
# x, y, z는 초기 teaching 위치 x,y,z 값(GetPose로 얻음)
def Mov_StartingPoint(x,y,z) :
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, x-50, y, z, 0, 0)
    time.sleep(3)

# Move to the bolt and fasten the bolt
def Robot_Work(X, Y, x, y, z) : # 캠에서 볼트 인식하여 리턴한 X, Y 값
    # X값 구간별 나눔 코드
    # 상수 들어간 위치 적절한 좌표 값 입력해줄 것 !
    if(X >= 0 and X < 200) :
        # 오른쪽 볼트로 이동
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x-50, y, z+20, 0, 0)  # z 위로 이동
        time.sleep(5)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 227.1407, y, z+20, 0, 0)  # x이동
        time.sleep(5)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 227.1407, -76.9479, z+20, 0, 0)  # y이동
        time.sleep(5)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 227.1407, -76.9479, z, 0, 0)  # z 아래로 이동
        time.sleep(5)
    elif(X >= 200 and X < 400) :
        # 중앙 볼트로 이동
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x-50, y, z+20, 0, 0)  # z 위로 이동
        time.sleep(5)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 227.1407, y, z+20, 0, 0)  # x이동
        time.sleep(5)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 227.1407, -76.9479, z+20, 0, 0)  # y이동
        time.sleep(5)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 227.1407, -76.9479, z, 0, 0)  # z 아래로 이동
        time.sleep(5)
    elif(X >= 400 and X < 600) :
        # 왼쪽 볼트로 이동
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x-50, y, z+20, 0, 0)  # z 위로 이동
        time.sleep(5)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 227.1407, y, z+20, 0, 0)  # x이동
        time.sleep(5)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 227.1407, -76.9479, z+20, 0, 0)  # y이동
        time.sleep(5)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 227.1407, -76.9479, z, 0, 0)  # z 아래로 이동
        time.sleep(5)
    #이동 완료 

    #현재 x,y,z 값 저장
    tempPos = dType.GetPose(api)
    tempX = tempPos[0]
    tempY = tempPos[1]
    tempZ = tempPos[2]

    #너트 회전 코드
    for i in range(0, 5):
        dType.SetEndEffectorGripper(api, 1, 1, 0)
        time.sleep(2)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, tempX, tempY, tempZ, -120, 0)  # grip on, 나사 감기
        time.sleep(3)
        dType.SetEndEffectorGripper(api, 1, 0, 0)
        time.sleep(2)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, tempX, tempY, tempZ, 120, 0)  # grip off, 돌리기
        time.sleep(3)
    dType.SetEndEffectorGripper(api, 1, 1, 0)
    time.sleep(2)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, tempX, tempY, tempZ, -120, 0)  # grip on, 나사 감기
    time.sleep(3)
    dType.SetEndEffectorGripper(api, 1, 0, 0)
    time.sleep(2)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, tempX, tempY, tempZ, 0, 0)
    time.sleep(2)
    dType.SetEndEffectorGripper(api, 0, 0, 0)  # Disable gripper
    time.sleep(2)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, tempX, tempY, tempZ+20, 0, 0)
    time.sleep(2)

