from System import *

class BoxCollider:
    def __init__(self, belonging):
        self.belonging = belonging
        self.position = Vector3([0, 0, 0]) #所属先とのずれ
        self.rotation = Vector3([0, 0, 0]) #所属先からの回転
        self.size = belonging.size
        self.tag = "box"
        self.unitVectorx = belonging.unitVectorx
        self.unitVectory = belonging.unitVectory
        self.unitVectorz = belonging.unitVectorz
        #衝突判定用
        self.viewUnitVextorx = None
        self.viewUnitVextory = None
        self.viewUnitVextorz = None
    
    def setUnitVector(self):
        #親オブジェクトの単位ベクトルをさらに回転させる。
            self.unitVectorx = self.belonging.unitVectorx
            self.unitVectory = self.belonging.unitVectory
            self.unitVectorz = self.belonging.unitVectorz
            
            rx = self.rotation.vec[0]
            ry = self.rotation.vec[1]
            rz = self.rotation.vec[2]
            #親オブジェクトと一致させた単位ベクトルに、ローカル角度を加える。
            unitVectorx = (
                self.unitVectorx*math.cos(ry)*math.cos(rz) + 
                self.unitVectory*math.sin(rz) - 
                self.unitVectorz*math.sin(ry)
                )
            unitVectory = (
                self.unitVectorx*math.sin(rz)*(-1) +
                self.unitVectory*math.cos(rx)*math.cos(rz) +
                self.unitVectorz*math.sin(rx)
            )
            unitVectorz = (
                self.unitVectorx*math.sin(ry) -
                self.unitVectory*math.sin(rx) +
                self.unitVectorz*math.cos(rx)*math.cos(ry)
            )
            self.unitVectorx = unitVectorx
            self.unitVectory = unitVectory
            self.unitVectorz = unitVectorz
            return self
    
    def rotate(self, arg):
        arg *= math.pi / 180
        
        self.rotation += arg
        self.setUnitVector()
        return self
    
    def setRotation(self, arg):
        arg *= math.pi / 180
        
        self.rotation = arg
        self.setUnitVector()
        return self
    
    #グローバル座標を、このオブジェクトのローカル座標に変換
    #衝突判定用
    def convertLocal(self, position, string):
        if string == "position":
            position -= self.belonging.position + self.position
        
        ans = [0, 0, 0]
        
        A = [[self.unitVectorx.vec[0], self.unitVectory.vec[0], self.unitVectorz.vec[0]], 
             [self.unitVectorx.vec[1], self.unitVectory.vec[1], self.unitVectorz.vec[1]], 
             [self.unitVectorx.vec[2], self.unitVectory.vec[2], self.unitVectorz.vec[2]]]
        
        X = [[position.vec[0], self.unitVectory.vec[0], self.unitVectorz.vec[0]], 
             [position.vec[1], self.unitVectory.vec[1], self.unitVectorz.vec[1]], 
             [position.vec[2], self.unitVectory.vec[2], self.unitVectorz.vec[2]]]

        Y = [[self.unitVectorx.vec[0], position.vec[0], self.unitVectorz.vec[0]], 
             [self.unitVectorx.vec[1], position.vec[1], self.unitVectorz.vec[1]], 
             [self.unitVectorx.vec[2], position.vec[2], self.unitVectorz.vec[2]]]
        
        Z = [[self.unitVectorx.vec[0], self.unitVectory.vec[0], position.vec[0]], 
             [self.unitVectorx.vec[1], self.unitVectory.vec[1], position.vec[1]], 
             [self.unitVectorx.vec[2], self.unitVectory.vec[2], position.vec[2]]]
        
        #クラーメルの定理
        ans[0] = det(X) / det(A)
        ans[1] = det(Y) / det(A)
        ans[2] = det(Z) / det(A)
        return Vector3(ans)       

    def preJudge(self, opponent):
        if opponent.tag == "box":
            opponent.viewPosition = self.convertLocal(opponent.belonging.position + opponent.position, "position")
            opponent.viewUnitVectorx = self.convertLocal(opponent.unitVectorx, "unitVectorx")
            opponent.viewUnitVectory = self.convertLocal(opponent.unitVectory, "unitVectory")
            opponent.viewUnitVectorz = self.convertLocal(opponent.unitVectorz, "unitVectorz")
            tops = self.getTops(opponent)
            #x, y, z方向から見た時に、相手の頂点を含んでいるか
            def isIn(i):
                return (-self.size.vec[i] <= top.vec[i] and top.vec[i] <= self.size.vec[i])
            X = 0
            Y = 0
            Z = 0
            for top in tops:
                #yz写像
                if isIn(1) and isIn(2):
                    X = 1
                #zx写像
                if isIn(2) and isIn(0):
                    Y = 1
                #xy写像
                if isIn(0) and isIn(1):
                    Z = 1
            return X and Y and Z
    
    def judge(self, opponent):
        return self.preJudge(opponent) and opponent.preJudge(self)
            
    #この判定から見た相手の頂点を求める
    def getTops(self, opponent):
        tops = []
        if opponent.tag == "cube":
            x = opponent.size.vec[0]
            y = opponent.size.vec[1]
            z = opponent.size.vec[2]
            tops = [
                #奥の面
                opponent.viewPosition +(opponent.viewUnitVectorx*(-1)*x - opponent.viewUnitVectory*y + opponent.viewUnitVectorz*z),
                opponent.viewPosition + (opponent.viewUnitVectorx*x - opponent.viewUnitVectory*y + opponent.viewUnitVectorz*z),
                opponent.viewPosition + (opponent.viewUnitVectorx*x + opponent.viewUnitVectory*y + opponent.viewUnitVectorz*z),
                opponent.viewPosition + (opponent.viewUnitVectorx*(-1)*x + opponent.viewUnitVectory*y + opponent.viewUnitVectorz*z),
                #手前の面
                opponent.viewPosition +(opponent.viewUnitVectorx*(-1)*x - opponent.viewUnitVectory*y - opponent.viewUnitVectorz*z),
                opponent.viewPosition + (opponent.viewUnitVectorx*x - opponent.viewUnitVectory*y - opponent.viewUnitVectorz*z),
                opponent.viewPosition + (opponent.viewUnitVectorx*x + opponent.viewUnitVectory*y - opponent.viewUnitVectorz*z),
                opponent.viewPosition + (opponent.viewUnitVectorx*(-1)*x + opponent.viewUnitVectory*y - opponent.viewUnitVectorz*z),
            ]
        
        elif opponent.tag == "rect":
            x = opponent.size.vec[0]
            y = opponent.size.vec[1]
            z = opponent.size.vec[2]
            tops = [
                #奥の面
                opponent.viewPosition +(opponent.viewUnitVectorx*(-1)*x - opponent.viewUnitVectory*y + opponent.viewUnitVectorz*z),
                opponent.viewPosition + (opponent.viewUnitVectorx*x - opponent.viewUnitVectory*y + opponent.viewUnitVectorz*z),
                opponent.viewPosition + (opponent.viewUnitVectorx*x + opponent.viewUnitVectory*y + opponent.viewUnitVectorz*z),
                opponent.viewPosition + (opponent.viewUnitVectorx*(-1)*x + opponent.viewUnitVectory*y + opponent.viewUnitVectorz*z)
            ]
            
        return tops