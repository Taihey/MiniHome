import math
import pygame
import Objects
windowx = 1000
windowy = 1000

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
PERPLE= (125,   0, 125)
GREEN = (  0, 255,   0)
LGREEN= (  0, 125,   0)
BLUE  = (  0,   0, 255)
GRAY  = (125, 125, 125)
AQUA =  (  0, 125, 125)
YELLOW = (255, 255,  0) 

#3次正方行列の行列式
def det(A):
    return (
            A[0][0]*A[1][1]*A[2][2] + A[1][0]*A[2][1]*A[0][2] + A[0][1]*A[1][2]*A[2][0]
        ) - (
            A[0][2]*A[1][1]*A[2][0] + A[0][1]*A[1][0]*A[2][2] + A[0][0]*A[1][2]*A[2][1]
        )

#3次元のベクトルを扱う
class Vector3:
    def __init__(self, vec):
        self.vec = vec
    
    #演算子のオーバーロード
    # +
    def __add__(self, other):
        ans = [0, 0, 0]
        if type(other) == Vector3:
            for i in range(3):
                ans[i] = self.vec[i] + other.vec[i]
            return Vector3(ans)
        raise TypeError()

    # -
    def __sub__(self, other):
        ans = [0, 0, 0]
        if type(other) == Vector3:
            for i in range(3):
                ans[i] = self.vec[i] - other.vec[i]
            return Vector3(ans)
        raise TypeError()
    
    # * 定数との掛け算
    def __mul__(self, other):     
        ans = [0, 0, 0]
        if type(other) in [int, float]:
            for i in range(3):
                ans[i] = self.vec[i] * other
            return Vector3(ans)
        
        #各要素をかけ合わせたもの
        elif type(other) == Vector3:
            for i in range(3):
                ans[i] = self.vec[i] * other.vec[i]
            if type(ans[0]) == Vector3:
                return ans[0] + ans[1] + ans[2]
            else:
                return Vector3(ans)
        raise TypeError()
    
    #回転量から、単位ベクトルを求める。
    def unitVectorx(self, arg):
        unitVectorx = [math.cos(arg.vec[1])*math.cos(arg.vec[2]), 
                        math.sin(arg.vec[2]), 
                        - math.sin(arg.vec[1])]
        self.vec = unitVectorx
        return Vector3(unitVectorx)
    
    def unitVectory(self, arg):
        unitVectory = [- math.sin(arg.vec[2]), 
                        math.cos(arg.vec[0])*math.cos(arg.vec[2]), 
                        math.sin(arg.vec[0])]
        self.vec = unitVectory
        return Vector3(unitVectory)
    
    def unitVectorz(self, arg):
        unitVectorz = [math.sin(arg.vec[1]), 
                        - math.sin(arg.vec[0]), 
                        math.cos(arg.vec[0])*math.cos(arg.vec[1])]
        self.vec = unitVectorz
        return Vector3(unitVectorz)
    
#3次元座標をスクリーン上の2次元座標に変換する
class Tridim:
    def __init__(self, cx, cy):
        #画面上の収束する点
        self.cx = cx
        self.cy = cy
        
    def dim(self, position):            #Vector3型で指定
        #z → ∞で、xr → cx、yr → cy
        #等比級数の和; a(1 - r^n)/(1 - r) ⇒ x + a/(1-r) = cx
        rx = 0.999                           #項比
        ry = 0.999
        ax = (self.cx - position.vec[0]) * (1 - rx)    #初項
        ay = (self.cy - position.vec[1]) * (1 - ry)
        xr = position.vec[0] + ax*(1 - rx**position.vec[2])/(1 - rx)
        yr = position.vec[1] + ay*(1 - ry**position.vec[2])/(1 - ry)
    
        return [xr, yr]



