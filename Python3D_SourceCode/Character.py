#機能を持ったオブジェクトのクラス
import pygame
import math
from System import *

#Objectクラスを指定する
class Character:
    def __init__(self, obj):
        self.object = obj
        obj.character = self
    
    #当たり判定の外までずらす(水平方向)
    def moveOut(self, opponent):
        if opponent.collider.tag == "box":
            #colliderの位置
            colPos = self.object.position + self.object.collider.position
            oppColPos = opponent.position + opponent.collider.position
            
            deltaXR = (colPos + self.object.collider.size
                    ).vec[0] - (oppColPos - opponent.collider.size).vec[0] + 10
            deltaXL = (oppColPos + opponent.collider.size
                    ).vec[0] - (colPos - self.object.collider.size).vec[0] + 10
            deltaZB = (colPos + self.object.collider.size
                    ).vec[2] - (oppColPos - opponent.collider.size).vec[2] + 10
            deltaZF = (oppColPos + opponent.collider.size
                    ).vec[2] - (colPos - self.object.collider.size).vec[2] + 10
            
            #この中で最小のものを求める
            deltaDists = [deltaXR, deltaXL, deltaZB, deltaZF]
            vectors = [
                Vector3([1, 0, 0]), Vector3([-1, 0, 0]), Vector3([0, 0, 1]), Vector3([0, 0, -1])
                ]
            dist = deltaXR
            ind = 0
            for i in range(len(deltaDists)):
                if deltaDists[i] < dist:
                    dist = deltaDists[i]
                    ind = i
            
            opponent.shift(vectors[ind] * dist)
    
    def onCollision(self, opponent):
        return

class Player(Character):
    def __init__(self, player):
        self.object = player
        player.character = self
        self.walkV = 5
        self.dashV = 15
    
    def setVelocity(self, walkV, dashV):
        self.walkV = walkV
        self.dashV = dashV
        return self
    
    #歩くアニメーションと移動
    #画面上のx, z方向に進む
    def walkz(self, camera, orient):
        self.object.play("walk")
        
        #y方向だけに回転させる
        if orient == 1:
            self.object.setRotation(camera.rotation.y() * (180/math.pi))
        elif orient == -1:
            self.object.setRotation(
                (camera.rotation.y() + Vector3([0, math.pi, 0])) * (180/math.pi)
                )
        self.object.velosity = camera.unitVectorz.zx().normalize() * self.walkV * orient
    
    def walkx(self, camera, orient):
        self.object.play("walk")
        
        self.object.setRotation(
            (camera.rotation.y() + (Vector3([0, math.pi/2, 0]) * orient)) * (180/math.pi)
            )
        #object.move()で動かす大きさ
        self.object.velosity = camera.unitVectorx.zx().normalize() * self.walkV * orient
        
    def runz(self, camera, orient):
        self.object.play("run")
        
        if orient == 1:
            self.object.setRotation(camera.rotation.y() * (180/math.pi))
        elif orient == -1:
            self.object.setRotation(
                (camera.rotation.y() + Vector3([0, math.pi, 0])) * (180/math.pi)
                )
        self.object.velosity = camera.unitVectorz.zx().normalize() * self.dashV * orient
        
    def runx(self, camera, orient):
        self.object.play("run")
        
        self.object.setRotation(
            (camera.rotation.y() + (Vector3([0, math.pi/2, 0]) * orient)) * (180/math.pi)
            )
        self.object.velosity = camera.unitVectorx.zx().normalize() * self.dashV * orient
    
    #移動していないときは速度を0にする
    def stay(self):
        self.object.play("stay")
        self.object.velosity = Vector3([0, 0 ,0])
    
    def onCollision(self, opponent):
        return

#当たったらWindowを表示する
class PC(Character):
    def __init__(self, pc, window):
        self.object = pc
        pc.character = self
        self.window = window
    
    def close(self):
        self.object.play("close")
    
    def open(self):
        self.object.play("open")
    
    def onCollision(self, opponent):
        if opponent.id == "player":
            self.open()
            #開ききっていたらGUIを開く
            if self.object.state == "opening":
                #windowを開いているというUIを表示
                SceneManager().moveScene(2)
                self.object.state = "opened"
                #playerを止める
                opponent.play("stay")
                
            elif self.object.state == "opened":
                self.window.createGUI()
                #表示が終わったときの処理
                SceneManager().moveScene(1)
                self.object.state = "default"
                opponent.state = "default"
                #当たり判定の外に行くまでずらす
                self.moveOut(opponent)
                self.close()

class Door(Character):
    def __init__(self, door):
        super().__init__(door)
    
    def close(self):
        self.object.play("close")
    
    def open(self):
        self.object.play("open")
    
    def onCollision(self, opponent):
        if opponent.id == "player":
            self.open()
            if self.object.state == "opening":
                SceneManager().moveScene(-1)
                #一度だけ移動したら、moveSceneは実行しない
                self.object.state = "opened"