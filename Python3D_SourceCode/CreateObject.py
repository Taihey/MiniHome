import Objects
from System import *
import math

def CreatePC():
    #キーボード
    cube = Objects.Cube(Vector3([100, 10, 80])).setColor(GRAY, AQUA)
    #画面
    cube2 = Objects.Cube(Vector3([100, 80, 10])).setColor(GRAY, AQUA)
    rect = Objects.Rect(80, 64)
    
    #描画しやすいように少し画面を前に出す
    cube2.setChild(rect, Vector3([0, 0, -10]), Vector3([0, 0, 15]))  
    
    cube.setChild(cube2, Vector3([0, -10, 80]), Vector3([0, 80, -10]))
    
    #アニメーション
    class Close:
        def __init__(self):
            return
        
        def play(self):
            cube.state = "default"
            if cube2.rotation.vec[0] < 90 * math.pi / 180:  
                cube2.rotate(Vector3([10, 0, 0]))
            else:
                cube2.rotation.vec[0] = 90 * math.pi / 180
    
    #close()に加えてopen()が実行される -> 多めの角度にする
    class Open:
        def __init__(self):
            return
        
        def play(self):
            if cube2.rotation.vec[0] > -10 * math.pi / 180:
                cube2.rotate(Vector3([-20, 0, 0]))
                if cube2.rotation.vec[0] < -10 * math.pi / 180:
                    cube2.rotation.vec[0] = -10 * math.pi / 180
                    cube.state = "opening"
            #close()の後にopen()が来るのでこうはならない
            else:
                cube2.rotation.vec[0] = -10 * math.pi / 180
                #開ききっている状態
                cube.state = "opening"
    
    cube.setMotion("close", Close())
    cube.setMotion("open", Open())
    
    #Playerが近づいているかを判定
    cube.setCollider("box"
        ).setColliderSize(Vector3([200, 10, 200]))
    
    cube.activeRigid()
    
    return cube

def CreatePlayer():
    core = Objects.Object()
    body = Objects.Cube(Vector3([100, 150, 80])).setColor(BLUE, RED)
    head = Objects.Cube(Vector3([50, 50, 50])).setColor(RED, RED)
    armL = Objects.Cube(Vector3([30, 100, 30])).setColor(GRAY, RED)
    armR = Objects.Cube(Vector3([30, 100, 30])).setColor(GRAY, RED)
    legL = Objects.Cube(Vector3([50, 100, 50])).setColor(YELLOW, RED)
    legR = Objects.Cube(Vector3([50, 100, 50])).setColor(YELLOW, RED)
    
    eye1 = Objects.Rect(15, 15)
    eye2 = Objects.Rect(15, 15)
    armL2 = Objects.Cube(Vector3([20, 100, 20])).setColor(GRAY, RED)
    armR2 = Objects.Cube(Vector3([20, 100, 20])).setColor(GRAY, RED)
    legL2 = Objects.Cube(Vector3([40, 100, 40])).setColor(YELLOW, RED)
    legR2 = Objects.Cube(Vector3([40, 100, 40])).setColor(YELLOW, RED)
    
    footL = Objects.Cube(Vector3([40, 20, 60])).setColor(PERPLE, RED)
    footR = Objects.Cube(Vector3([40, 20, 60])).setColor(PERPLE, RED)
    
    core.setChild(body, Vector3([0, 0, 0]), Vector3([0, 0, 0]))
    body.setChild(head, Vector3([0, -150, 0]), Vector3([0, 50, 0]))
    body.setChild(armL, Vector3([-100, -110, 0]), Vector3([20, -60, 0]))
    body.setChild(armR, Vector3([100, -110, 0]), Vector3([-20, -60, 0]))
    body.setChild(legL, Vector3([-60, 150, 0]), Vector3([0, -100, 0]))
    body.setChild(legR, Vector3([60, 150, 0]), Vector3([0, -100, 0]))
    
    head.setChild(eye1, Vector3([-25, -25, 50]), Vector3([0, 0, -15]))
    head.setChild(eye2, Vector3([25, -25, 50]), Vector3([0, 0, -15]))
    armL.setChild(armL2, Vector3([0, 80, 0]), Vector3([0, -80, 0]))
    armR.setChild(armR2, Vector3([0, 80, 0]), Vector3([0, -80, 0]))
    legL.setChild(legL2, Vector3([0, 100, 0]), Vector3([0, -100, 0]))
    legR.setChild(legR2, Vector3([0, 100, 0]), Vector3([0, -100, 0]))
    
    legL2.setChild(footL, Vector3([0, 100, 0]), Vector3([0, -20, -20]))
    legR2.setChild(footR, Vector3([0, 100, 0]), Vector3([0, -20, -20]))
    
    class Stay:
        def __init__(self):
            return
        
        def play(self):
            #他のアニメーションを初期化する
            core.motion["run"].__init__()         
            core.motion["walk"].__init__()
            
            body.setRotation(Vector3([0, 0, 0]))
            head.setRotation(Vector3([0, 0, 0]))
            armL.setRotation(Vector3([0, 0, 0]))
            armR.setRotation(Vector3([0, 0, 0]))
            legL.setRotation(Vector3([0, 0, 0]))
            legR.setRotation(Vector3([0, 0, 0]))
            armL2.setRotation(Vector3([0, 0, 0]))
            armR2.setRotation(Vector3([0, 0, 0]))
            legL2.setRotation(Vector3([0, 0, 0]))
            legR2.setRotation(Vector3([0, 0, 0]))
            footL.setRotation(Vector3([0, 0, 0]))
            footR.setRotation(Vector3([0, 0, 0]))
    
    class Walk:
        def __init__(self):
            self.playing = 0
            self.state = 1      #右手を前に出すか左手を前に出すか
            return
        
        def play(self):
            core.motion["run"].__init__()  
            
            if self.playing == 0:
                self.playing = 1
                armR2.setRotation(Vector3([10, 0, 0]))
                armL2.setRotation(Vector3([10, 0, 0]))
                legR2.setRotation(Vector3([-10, 0, 0]))
                legL2.setRotation(Vector3([-10, 0, 0]))
            if self.state == 1: #右手を前に出す
                armR.rotate(Vector3([5, 0, 0]))
                armL.rotate(Vector3([-5, 0, 0]))
                legR.rotate(Vector3([-5, 0, 0]))
                legL.rotate(Vector3([5, 0, 0]))
                legL2.rotate(Vector3([2, 0, 0]))
                footL.rotate(Vector3([5, 0, 0]))
                if armR.rotation.vec[0] >= 30*math.pi/180:
                    self.state = 0
                    legR2.setRotation(Vector3([-20, 0, 0]))
                    legL2.setRotation(Vector3([-5, 0, 0]))
                    footR.setRotation(Vector3([-30, 0, 0]))
                    footL.setRotation(Vector3([0, 0, 0]))
            elif self.state == 0:
                armR.rotate(Vector3([-5, 0, 0]))
                armL.rotate(Vector3([5, 0, 0]))
                legR.rotate(Vector3([5, 0, 0]))
                legL.rotate(Vector3([-5, 0, 0]))
                legR2.rotate(Vector3([2, 0, 0]))
                footR.rotate(Vector3([5, 0, 0]))
                if armR.rotation.vec[0] <= -30*math.pi/180:
                    self.state = 1
                    legL2.setRotation(Vector3([-20, 0, 0]))
                    legR2.setRotation(Vector3([-5, 0, 0]))
                    footL.setRotation(Vector3([-30, 0, 0]))
                    footR.setRotation(Vector3([0, 0, 0]))
        
    class Run:
        def __init__(self):
            self.state = 1      #右手を前に出すか左手を前に出すか
            self.playing = 0
            return
        
        def play(self):
            core.motion["walk"].__init__()
            
            if self.playing == 0:
                self.playing = 1
                body.rotate(Vector3([-10, 0, 0]))
                legR.rotate(Vector3([10, 0, 0]))
                legL.rotate(Vector3([10, 0, 0]))
                armR.rotate(Vector3([-30, 0, -10]))
                armL.rotate(Vector3([-30, 0, 10]))
                armR2.rotate(Vector3([120, 0, 0]))
                armL2.rotate(Vector3([120, 0, 0]))
                legL2.setRotation(Vector3([-100, 0, 0]))
                
            if self.state == 1: #右手を前に出す 右足は伸ばして左足は曲げる
                body.rotate(Vector3([0, -3, 0]))
                head.rotate(Vector3([0, 3, 0]))
                armR.rotate(Vector3([7, 3, 0]))
                armL.rotate(Vector3([-7, 3, 0]))
                legR.rotate(Vector3([-14, 3, 0]))
                legL.rotate(Vector3([14, 3, 0]))
                legL2.rotate(Vector3([14, 0, 0]))
                footL.rotate(Vector3([14, 0, 0]))
                if armR.rotation.vec[0] >= -10*math.pi/180:
                    self.state = 0
                    legR2.setRotation(Vector3([-100, 0, 0]))
                    legL2.setRotation(Vector3([-10, 0, 0]))
                    footR.setRotation(Vector3([-30, 0, 0]))
                    footL.setRotation(Vector3([0, 0, 0]))
            elif self.state == 0:
                body.rotate(Vector3([0, 3, 0]))
                head.rotate(Vector3([0, -3, 0]))
                armR.rotate(Vector3([-7, -3, 0]))
                armL.rotate(Vector3([7, -3, 0]))
                legR.rotate(Vector3([14, -3, 0]))
                legL.rotate(Vector3([-14, -3, 0]))
                legR2.rotate(Vector3([14, 0, 0]))
                footR.rotate(Vector3([14, 0, 0]))
                if legR2.rotation.vec[0] >= 0:
                    legR2.rotation = Vector3([0, 0, 0])
                if armR.rotation.vec[0] <= -50*math.pi/180:
                    self.state = 1
                    legL2.setRotation(Vector3([-100, 0, 0]))
                    legR2.setRotation(Vector3([-10, 0, 0]))
                    footL.setRotation(Vector3([-30, 0, 0]))
                    footR.setRotation(Vector3([0, 0, 0]))
    
    core.setMotion("stay", Stay())
    core.setMotion("walk", Walk())
    core.setMotion("run", Run())    
    
    core.setCollider("box"
        ).setColliderSize(Vector3([100, 420, 100])
        ).shiftCollider(Vector3([0, 170, 0]))
        
    core.activeRigid()
    core.setID("player")
    
    return core

#cubeをつなげた床を作る
#一辺の長さの半分を指定する 重くなる
def CreateFloor(l):
    core = Objects.Object()
    
    #10X10の床
    floors = []
    xlen = 10
    zlen = 10
    for i in range(xlen):
        floors.append([])
        for j in range(zlen):
            floors[i].append(Objects.Cube(Vector3([l, l, l])).setColor(AQUA, BLUE))
            
            #coreから見たそのcubeの位置
            distx = None
            distz = None
            
            if xlen % 2 == 0:
                distx = (-2*l * (xlen/2) + l) + 2*l * i
            else:
                distx = (-2*l * int(xlen/2)) + 2*l * i
            
            if zlen % 2 == 0:
                distz = (-2*l * (zlen/2) + l) + 2*l * j
            else:
                distz = (-2*l * int(zlen/2)) + 2*l * j
                
            core.setChild(floors[i][j], Vector3([distx, 0, distz]), Vector3([0, 0, 0]))
            
    core.setCollider("box").setColliderSize(Vector3([l * xlen, l, l * zlen]))
    
    core.setID("floor")
    
    return core

#一つの直方体 軽い 描画順を調整できない
def CreateFloorVer2(l):
    floor = Objects.Cube(Vector3([l * 100, l, l * 100])).setColor(AQUA, BLUE)
    floor.setCollider("box").setColliderSize(Vector3([l * 100, l, l * 100]))
    floor.setID("floor")
    
    return floor

#平面をつなげた地面 重くなる
def CreateFloorPlane(l):
    core = Objects.Object()
    
    #10X10の床
    floors = []
    xlen = 10
    zlen = 10
    for i in range(xlen):
        floors.append([])
        for j in range(zlen):
            floors[i].append(
                Objects.Rect(l, l).setColor(AQUA, BLUE).rotate(Vector3([90, 0, 0]))
                )
            
            #coreから見たそのcubeの位置
            distx = None
            distz = None
            
            if xlen % 2 == 0:
                distx = (-2*l * (xlen/2) + l) + 2*l * i
            else:
                distx = (-2*l * int(xlen/2)) + 2*l * i
            
            if zlen % 2 == 0:
                distz = (-2*l * (zlen/2) + l) + 2*l * j
            else:
                distz = (-2*l * int(zlen/2)) + 2*l * j
                
            core.setChild(floors[i][j], Vector3([distx, 0, distz]), Vector3([0, 0, 0]))
            
    core.setCollider("box").setColliderSize(Vector3([l * xlen, l, l * zlen]))
    
    core.setID("floor")
    
    return core

def CreateDesk():
    core = Objects.Object()
    board = Objects.Cube(Vector3([150, 20, 150])).setColor(YELLOW, PERPLE)
    col1 = Objects.Cube(Vector3([10, 130, 10])).setColor(YELLOW, PERPLE)
    col2 = Objects.Cube(Vector3([10, 130, 10])).setColor(YELLOW, PERPLE)
    col3 = Objects.Cube(Vector3([10, 130, 10])).setColor(YELLOW, PERPLE)
    col4 = Objects.Cube(Vector3([10, 130, 10])).setColor(YELLOW, PERPLE)
    
    core.setChild(board, Vector3([0, 0, 0]), Vector3([0, 0, 0]))
    board.setChild(col1, Vector3([-130, 20, -130]), Vector3([0, -130, 0]))
    board.setChild(col2, Vector3([130, 20, -130]), Vector3([0, -130, 0]))
    board.setChild(col3, Vector3([130, 20, 130]), Vector3([0, -130, 0]))
    board.setChild(col4, Vector3([-130, 20, 130]), Vector3([0, -130, 0]))
    
    core.setCollider("box"
        ).setColliderSize(Vector3([150, 150, 150])
        ).shiftCollider(Vector3([0, 130, 0]))
    
    core.activeRigid()
    
    core.setID("floor")
    
    return core

def CreateDoor():
    core = Objects.Object()
    gateL = Objects.Cube(Vector3([20, 600, 20])).setColor(YELLOW, BLUE)
    gateR = Objects.Cube(Vector3([20, 600, 20])).setColor(YELLOW, BLUE)
    gateU = Objects.Cube(Vector3([400, 20, 20])).setColor(YELLOW, BLUE)
    doorL = Objects.Rect(200, 600).setColor(WHITE, BLACK)
    doorR = Objects.Rect(200, 600).setColor(WHITE, BLACK)
    
    core.setChild(gateL, Vector3([-420, 0, 0]), Vector3([0, 0, 0]))
    core.setChild(gateR, Vector3([420, 0, 0]), Vector3([0, 0, 0]))
    core.setChild(gateU, Vector3([0, -620, 0]), Vector3([0, 0, 0]))
    gateL.setChild(doorL, Vector3([20, 0, 0]), Vector3([-200, 0, 0]))
    gateR.setChild(doorR, Vector3([-20, 0, 0]), Vector3([200, 0, 0]))
    
    class Open:
        def __init__(self):
            return
        
        def play(self):
            doorL.rotate(Vector3([0, -20, 0]))
            doorR.rotate(Vector3([0, 20, 0]))
            if doorR.rotation.vec[1] > 100 * math.pi / 180:
                doorR.rotation.vec[1] = 100 * math.pi / 180
                doorL.rotation.vec[1] = -100 * math.pi / 180
                if core.state != "opened":
                    core.state = "opening"
    
    class Close:
        def __init__(self):
            return
        
        def play(self):
            if core.state != "opened":
                core.state = "default"
            if doorR.rotation.vec[1] <= 0:
                doorR.rotation.vec[1] = 0
                doorL.rotation.vec[1] = 0
            else:
                doorL.rotate(Vector3([0, 10, 0]))
                doorR.rotate(Vector3([0, -10, 0]))
    
    core.setMotion("close", Close())
    core.setMotion("open", Open())
    
    core.setCollider("box"
        ).setColliderSize(Vector3([400, 600, 500])
        ).shiftCollider(Vector3([0, 0, 500]))
    
    core.activeRigid()
    
    core.setID("door")
    
    return core

#x方向の柵
def CreateFenseH(l):
    core = Objects.Object()
    lineU = Objects.Cube(Vector3([l/2, 20, 20])).setColor(RED, BLACK)
    lineU2 = Objects.Cube(Vector3([l/2, 20, 20])).setColor(RED, BLACK)
    lineD = Objects.Cube(Vector3([l/2, 20, 20])).setColor(RED, BLACK)
    lineD2 = Objects.Cube(Vector3([l/2, 20, 20])).setColor(RED, BLACK)
    colL = Objects.Cube(Vector3([20, 200, 20])).setColor(RED, BLACK)
    colR = Objects.Cube(Vector3([20, 200, 20])).setColor(RED, BLACK)
    
    core.setChild(lineU, Vector3([0, 0, 0]), Vector3([-l/2, 0, 0]))
    core.setChild(lineU2, Vector3([0, 0, 0]), Vector3([l/2, 0, 0]))
    core.setChild(lineD, Vector3([0, 150, 0]), Vector3([-l/2, 0, 0]))
    core.setChild(lineD2, Vector3([0, 150, 0]), Vector3([l/2, 0, 0]))
    core.setChild(colL, Vector3([-l, 0, 0]), Vector3([20, -200, 0]))
    core.setChild(colR, Vector3([l, 0, 0]), Vector3([-20, -200, 0]))
    
    core.setCollider("box"
        ).setColliderSize(Vector3([l, 200, 300])
        ).shiftCollider(Vector3([0, 200, 0]))
    
    core.activeRigid()
    
    core.setID("floor")
    
    return core

def CreateFenseV(l):
    core = CreateFenseH(l)
    
    core.rotate(Vector3([0, 90, 0]))
    core.setColliderSize(Vector3([300, 200, l]))
    
    return core