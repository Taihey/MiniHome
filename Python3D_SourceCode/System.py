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
    
    def x(self):
        return Vector3([self.vec[0], 0, 0])
    
    def y(self):
        return Vector3([0, self.vec[1], 0])
    
    def z(self):
        return Vector3([0, 0, self.vec[2]])
    
    def xz(self):
        return Vector3([self.vec[0], 0, self.vec[2]])
    
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
    
    #二つの位置間の距離の2乗を返す
    def distance(self, vec1):
        return (
            (vec1.vec[0] - self.vec[0])*(vec1.vec[0] - self.vec[0]) +
            (vec1.vec[1] - self.vec[1])*(vec1.vec[1] - self.vec[1]) +
            (vec1.vec[2] - self.vec[2])*(vec1.vec[2] - self.vec[2])
        )
    
    def normalize(self):
        return self * (1/math.sqrt(self.distance(Vector3([0, 0, 0]))))
    
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
#透視投影変換
class Tridim:
    def __init__(self, perspective):
        #視点の座標(画面上)
        self.perspective = perspective
        
    def dim(self, position):            
        ratio =  (0-self.perspective.vec[2]) / (position.vec[2]-self.perspective.vec[2])
        delx = position.vec[0] - self.perspective.vec[0]
        dely = position.vec[1] - self.perspective.vec[1]
        xr = self.perspective.vec[0] + delx * ratio
        yr = self.perspective.vec[1] + dely * ratio
    
        return [xr, yr]



