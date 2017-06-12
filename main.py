import numpy as np
import cv2
import math
import time
import DobotDllType as dType
import speech_recognition as sr
import pygame
import copy

def Cam():
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
    # cv2.waitKey()

    return (circles[0,mi][0], -circles[0,mi][1])

def Voice() :
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return r.recognize_google(audio)

# 원(처음)위치로 이동
def Mov_StartingPoint(x,y,z) :
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, x-50, y, z, 0, 0)
    time.sleep(3)

# 볼트로 이동
# X,Y : 영상 처리로 얻은 이동 대상 좌표 값
# x,y,z : GetPose로 얻은 x,y,z 좌표값
def Mov_Target(X, Y, x, y) :
    newX = -0.0394 * X + 1.1523 * Y + x - 224 # (x - (처음 x)) plus 처리 해주기
    newY = 0.3878 * X - 0.6521 * Y # y값 리셋

    theta = math.atan(0.0033441 * newX)
    OQ = math.sqrt(1836.18 * (1-math.cos(theta)))
    R_X = OQ * math.sin(theta/2)
    R_Y = R_X * math.tan(theta)

    newXX = newX + R_X
    newYY = newY + R_Y

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x-50, y, 40, 0, 0)  # z 위로 이동
    time.sleep(5)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, newXX, y, 40, 0, 0)  # x이동
    time.sleep(5)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, newXX, newYY, 40, 0, 0)  # y이동
    time.sleep(5)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, newXX, newYY, 13, 0, 0)  # z 아래로 이동
    time.sleep(5)

# 너트 조이기
# X,Y : 영상 처리로 얻은 이동 대상 좌표 값
# x,y,z : GetPose로 얻은 x,y,z 좌표값
def Fasten(X, Y, x, y) :
    # 너트 감기 -120 ~ 120 => 그립ing이랑 싱크를 맞춰 줘야해
    # '-' 회전방향이 너트 돌리는 방향?
    newX = -0.0394 * X + 1.1523 * Y + x - 224 # 처음 x 값 세팅
    newY = 0.3878 * X - 0.6521 * Y # y값 리셋

    theta = math.atan(0.0033441 * newX)
    OQ = math.sqrt(1836.18 * (1-math.cos(theta)))
    R_X = OQ * math.sin(theta/2)
    R_Y = R_X * math.tan(theta)

    newXX = newX + R_X
    newYY = newY + R_Y

    # 잡아 돌리기 싱크 왔다갔다 함... 2, 3 반복 또는 1, 2 반복으로 맞추어 볼것
    for i in range(0, 3):
        dType.SetEndEffectorGripper(api, 1, 1, 0)
        time.sleep(2)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, newXX, newYY, 13, -120, 0)  # grip on, 나사 감기
        time.sleep(3)
        dType.SetEndEffectorGripper(api, 1, 0, 0)
        time.sleep(2)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, newXX, newYY, 13, 120, 0)  # grip off, 돌리기
        time.sleep(3)
    dType.SetEndEffectorGripper(api, 1, 1, 0)
    time.sleep(2)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, newXX, newYY, 13, -120, 0)  # grip on, 나사 감기
    time.sleep(3)
    dType.SetEndEffectorGripper(api, 1, 0, 0)
    time.sleep(2)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, newXX, newYY, 13, 0, 0)
    time.sleep(2)
    dType.SetEndEffectorGripper(api, 0, 0, 0)  # Disable gripper
    time.sleep(2)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, newXX, newYY, 30, 0, 0)
    time.sleep(2)

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll
api = dType.load()

#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):

    #Clean Command Queued
    dType.SetQueuedCmdClear(api)

    #Async Motion Params Setting
    dType.SetPTPJointParams(api, 50, 50, 50, 50, 50, 50, 200, 200)
    dType.SetPTPCoordinateParams(api, 50, 50, 50, 200)
    dType.SetPTPJumpParams(api, 10, 100)
    dType.SetPTPCommonParams(api, 50, 50)

    pos = dType.GetPose(api)
    x = pos[0]
    y = pos[1]
    z = pos[2]
    rHead = pos[3]

    dType.Mov_StartingPoint(x, y, z)

    #Call Cam function
    Val_Cam = Cam()

    #Call Voice function
    while True :
        Val_Voice = Voice()
        #Voice 값은 첫글자 대문자로 들어온다.
        if Voice != None :
            # 볼트로 이동 및 조이기
            Mov_Target(Val_Cam[0], Val_Cam[1], x, y)
            Fasten(Val_Cam[0], Val_Cam[1], x, y)
            break
        else :
            print("인식을 못했습니다. 다시 말씀해주세요")
            continue
    dType.Mov_StartingPoint(x, y, z)

#Disconnect Dobot
dType.DisconnectDobot(api)

