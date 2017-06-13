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
func.dType.SetPTPJointParams(api, 50, 50, 50, 50, 50, 50, 200, 200)
func.dType.SetPTPCoordinateParams(api, 50, 50, 50, 200)
func.dType.SetPTPJumpParams(api, 10, 100)
func.dType.SetPTPCommonParams(api, 50, 50)

# 처음에 hand teaching으로 x, y, z 좌표 가져오기
pos = func.dType.GetPose(api)
x = pos[0]
y = pos[1]
z = pos[2]
rHead = pos[3]

func.Mov_StartingPoint(api, x, y, z) # 웹캠 가리지 않도록 위치 조정
val = func.Cam() # 캠 시작, 영상 인식, ESC 키 입력에 좌표 반환
func.Robot_Work(api, val[0], val[1], x, y, z)
func.Mov_StartingPoint(api, x, y, z) # 작업 완료 후 원위치로 이동

'''
func.Mov_StartingPoint(api, x, y, z) # 작업 완료 후 원위치로 이동
while True:
    val = func.Cam()  # 캠 시작, 영상 인식, ESC 키 입력에 좌표 반환
    Val_Voice = func.Voice()
    # Voice 값은 첫글자 대문자로 들어온다.
    if func.Voice != None:
        # 볼트로 이동 및 조이기
        func.Robot_Work(api, val[0], val[1], x, y, z)
        break
    else:
        print("인식을 못했습니다. 다시 말씀해주세요")
        continue
func.Mov_StartingPoint(api, x, y, z) # 작업 완료 후 원위치로 이동
'''

func.dType.DisconnectDobot(api)
