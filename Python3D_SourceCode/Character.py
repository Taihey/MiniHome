#機能を持ったオブジェクトのクラス
import pygame
import math
from System import *

#Objectクラスを指定する
class Character:
    def __init__(self, obj):
        self.object = obj
    
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
    
    def onCollision(self, opponent):
        if opponent.id == "player":
            self.window.createGUI()
            opponent.shift(opponent.velosity * (-1))