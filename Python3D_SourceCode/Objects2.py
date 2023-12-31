#機能を持ったオブジェクトのクラス
import pygame
import math
from System import *

#Objectクラスを指定する
class Player:
    def __init__(self, player):
        self.object = player
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
        self.object.position += camera.unitVectorz.xz().normalize() * self.walkV * orient
    
    def walkx(self, camera, orient):
        self.object.play("walk")
        
        self.object.setRotation(
            (camera.rotation.y() + (Vector3([0, math.pi/2, 0]) * orient)) * (180/math.pi)
            )
        self.object.position += camera.unitVectorx.xz().normalize() * self.walkV * orient
        
    def runz(self, camera, orient):
        self.object.play("run")
        
        if orient == 1:
            self.object.setRotation(camera.rotation.y() * (180/math.pi))
        elif orient == -1:
            self.object.setRotation(
                (camera.rotation.y() + Vector3([0, math.pi, 0])) * (180/math.pi)
                )
        self.object.position += camera.unitVectorz.xz().normalize() * self.dashV * orient
        
    def runx(self, camera, orient):
        self.object.play("run")
        
        self.object.setRotation(
            (camera.rotation.y() + (Vector3([0, math.pi/2, 0]) * orient)) * (180/math.pi)
            )
        self.object.position += camera.unitVectorx.xz().normalize() * self.dashV * orient