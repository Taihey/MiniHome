import Objects
from System import *
import math

def CreatePC():
    #キーボード
    cube = Objects.Cube(100, 10, 80).setColor(GRAY, AQUA)
    #画面
    cube2 = Objects.Cube(100, 80, 10).setColor(GRAY, AQUA)
    rect = Objects.Rect(80, 64)
    
    cube2.setChild(rect, Vector3([0, 0, -10]), Vector3([0, 0, 15]))  #描画しやすいように少し画面を前に出す
    #cube2.rotate(Vector3([-30, 0, 0]))
    
    cube.setChild(cube2, Vector3([0, -10, 80]), Vector3([0, 80, -10]))
    
    #アニメーション
    class Close:
        def __init__(self):
            return
        
        def play(self):
            if cube2.rotation.vec[0] < 90 * math.pi / 180:  
                cube2.rotate(Vector3([10, 0, 0]))
            else:
                cube2.rotation.vec[0] = 90 * math.pi / 180
    
    cube.setMotion("close", Close())
    
    return cube

def CreatePlayer():
    core = Objects.Object()
    body = Objects.Cube(100, 150, 80).setColor(BLUE, RED)
    head = Objects.Cube(50, 50, 50).setColor(RED, RED)
    armL = Objects.Cube(30, 100, 30).setColor(GRAY, RED)
    armR = Objects.Cube(30, 100, 30).setColor(GRAY, RED)
    legL = Objects.Cube(50, 100, 50).setColor(YELLOW, RED)
    legR = Objects.Cube(50, 100, 50).setColor(YELLOW, RED)
    
    eye1 = Objects.Rect(15, 15)
    eye2 = Objects.Rect(15, 15)
    armL2 = Objects.Cube(20, 100, 20).setColor(GRAY, RED)
    armR2 = Objects.Cube(20, 100, 20).setColor(GRAY, RED)
    legL2 = Objects.Cube(40, 100, 40).setColor(YELLOW, RED)
    legR2 = Objects.Cube(40, 100, 40).setColor(YELLOW, RED)
    
    footL = Objects.Cube(40, 20, 60).setColor(PERPLE, RED)
    footR = Objects.Cube(40, 20, 60).setColor(PERPLE, RED)
    
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
                body.rotate(Vector3([0, -2, 0]))
                head.rotate(Vector3([0, 2, 0]))
                armR.rotate(Vector3([5, 2, 0]))
                armL.rotate(Vector3([-5, 2, 0]))
                legR.rotate(Vector3([-10, 2, 0]))
                legL.rotate(Vector3([10, 2, 0]))
                legL2.rotate(Vector3([10, 0, 0]))
                footL.rotate(Vector3([10, 0, 0]))
                if armR.rotation.vec[0] >= -10*math.pi/180:
                    self.state = 0
                    legR2.setRotation(Vector3([-100, 0, 0]))
                    legL2.setRotation(Vector3([-10, 0, 0]))
                    footR.setRotation(Vector3([-30, 0, 0]))
                    footL.setRotation(Vector3([0, 0, 0]))
            elif self.state == 0:
                body.rotate(Vector3([0, 2, 0]))
                head.rotate(Vector3([0, -2, 0]))
                armR.rotate(Vector3([-5, -2, 0]))
                armL.rotate(Vector3([5, -2, 0]))
                legR.rotate(Vector3([10, -2, 0]))
                legL.rotate(Vector3([-10, -2, 0]))
                legR2.rotate(Vector3([10, 0, 0]))
                footR.rotate(Vector3([10, 0, 0]))
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
    return core