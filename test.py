import numpy as np
import cv2
import math

webcam = cv2.VideoCapture(0)

if webcam.isOpened():  # try to get the first frame
    rval, image = webcam.read()
else:
    rval = False

# define the list of acceptable colors
colors = [([0,133,77], [255, 173, 127])]
#colors = [([110, 100, 100], [130, 255, 255])]



while rval:
    # loop over the boundaries
    for (lower, upper) in colors:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        imgg = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(imgg, lower, upper)
        output = cv2.bitwise_and(imgg, imgg, mask=mask)
        #cv2.circle(output, (100, 100), 50, (0, 255, 0), 2)
       # j =image.getpixel((100, 100))
        # show the images

    rval, image = webcam.read()
    edges = cv2.Canny(output, 30, 30, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

    cv2.imshow("images", np.hstack([image, output]))
    key = cv2.waitKey(20)
    if key in [27, ord('Q'), ord('q')]:  # exit on ESC
        cv2.destroyWindow("images")
        break

img = cv2.medianBlur(image, 15)
imgg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
circles = cv2.HoughCircles(imgg,cv2.HOUGH_GRADIENT,1,150,
                            param1=50,param2=30,minRadius=1,maxRadius=100)
for x in range(0, 1):
    for rho,theta in lines[x]:
        x1 = int(np.cos(theta) * rho + 1000 * (-np.sin(theta)))
        y1 = int(np.sin(theta) * rho + 1000 * np.cos(theta))
        x2 = int(np.cos(theta) * rho - 1000 * (-np.sin(theta)))
        y2 = int(np.sin(theta) * rho - 1000 * np.cos(theta))
        cv2.line(output, (x1, y1), (x2, y2), (0, 0, 255), 1)
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 1)

        y1 = -1 * y1
        y2 = -1 * y2
        a = (y2-y1)/(x2-x1)

        print("1:", x1,y1)
        print("2:", x2,y2)
        print("3:", a)

d   = [100.0,100.0,100.0,100.0,100.0]
j=0

for i in circles[0,:]:
    # draw the outer circle
        cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
        #print(circles[0,0])
        print(i[0],i[1])
    # draw the center of the circle
        cv2.circle(image,(i[0],i[1]),2,(0,0,255),3)
        i[1] = -1 * i[1]
        d[j]= abs(a*(i[0]-x1) + y1 -i[1]) / (math.sqrt(a*a +1))
        j = j+1
# d는 list 형태로 원마다 거리나타냄...
print(d)
print("d = ",min(d))

j =0
for i in d :
    if min(d) == i:
        mi = j
    j = j+1
print("index :",mi)

print(circles[0,mi][0],circles[0,mi][1])

cv2.imshow('Edges', image)
cv2.imshow('Output', output)
cv2.waitKey()

'''
로봇 초기화 코드
import threading
import DobotDllType as dType
import time

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
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200)
    dType.SetPTPCoordinateParams(api, 200, 200, 200, 200)
    dType.SetPTPJumpParams(api, 10, 200)
    dType.SetPTPCommonParams(api, 100, 100)

    pos = dType.GetPose(api)
    x = pos[0]
    y = pos[1]
    z = pos[2]
    rHead = pos[3]

    dType.SetEndEffectorGripper(api, 1, 0, 0)  # 열기
    time.sleep(1)
    dType.SetEndEffectorGripper(api, 1, 1, 0)  # 닫기
    time.sleep(1)
    dType.SetEndEffectorGripper(api, 1, 0, 0)  # 열기
    time.sleep(1)
    dType.SetEndEffectorGripper(api, 0, 0, 0)  # 열기
    time.sleep(1)

#Disconnect Dobot
dType.DisconnectDobot(api)
'''