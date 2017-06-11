import main as Main
import numpy as np
import cv2
import math
import time
import DobotDllType as dType
import speech_recognition as sr

#M.Fasten(val[0], val[1])
#M.Mov_StartingPoint()

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll
api = dType.load()

dType.DisconnectDobot(api)

#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

dType.SetPTPJointParams(api, 50, 50, 50, 50, 50, 50, 200, 200)
dType.SetPTPCoordinateParams(api, 50, 50, 50, 200)
dType.SetPTPJumpParams(api, 10, 100)
dType.SetPTPCommonParams(api, 50, 50)

pos = dType.GetPose(api)
x = pos[0]
y = pos[1]
z = pos[2]
rHead = pos[3]

Main.Mov_StartingPoint(x,y,z)
val = Main.Cam()
Main.Mov_Target(val[0], val[1], x, y)
#Main.Fasten(val[0], val[1], x, y)
Main.Mov_StartingPoint(x,y,z)

dType.DisconnectDobot(api)

