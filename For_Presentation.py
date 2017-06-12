import Functions as func

CON_STR = {
    func.dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    func.dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    func.dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll
api = func.dType.load()

func.dType.DisconnectDobot(api)

#Connect Dobot
state = func.dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

#Dobt 축별 속도 지정
dType.SetPTPJointParams(api, 50, 50, 50, 50, 50, 50, 200, 200)
dType.SetPTPCoordinateParams(api, 50, 50, 50, 200)
dType.SetPTPJumpParams(api, 10, 100)
dType.SetPTPCommonParams(api, 50, 50)

# 처음에 hand teaching으로 x, y, z 좌표 가져오기
pos = func.dType.GetPose(api)
x = pos[0]
y = pos[1]
z = pos[2]
rHead = pos[3]

func.Mov_StartingPoint(x,y,z) # 웹캠 가리지 않도록 위치 조정
val = func.Cam() # 캠 시작, 영상 인식, ESC 키 입력에 좌표 반환
func.Robot_Work(val[1], val[2], x, y, z)
func.Mov_StartingPoint(x,y,z) # 작업 완료 후 원위치로 이동

func.dType.DisconnectDobot(api)
