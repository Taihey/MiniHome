import pygame
import math
from System import *

#ローカル座標をいじる
class Object:
    def __init__(self):
        self.tag = "obj"
        self.id = "obj"
        #基準となる位置
        self.position = Vector3([0, 0, 0])
        #親オブジェクトはグローバル、子オブジェクトはローカル
        self.rotation = Vector3([0, 0, 0])
        self.size = Vector3([0, 0, 0])
        
        self.unitVectorx = Vector3([1, 0, 0])
        self.unitVectory = Vector3([0, 1, 0])
        self.unitVectorz = Vector3([0, 0, 1])
        self.tops = []
        #親オブジェクト
        self.parent = None
        self.parConnection = None
        #子オブジェクト
        self.children = []
        self.connection = []
        #カメラのローカル座標での位置
        self.viewPosition = Vector3([0, 0, 0])
        self.viewUnitVectorx = Vector3([1, 0, 0])
        self.viewUnitVectory = Vector3([0, 1, 0])
        self.viewUnitVectorz = Vector3([0, 0, 1])
        #カメラの視点から一番近い点の距離の2乗、描画順を決める。
        #頂点のないオブジェクトは毎回先に描画処理されるが、問題ない
        self.nearestDist = 0  
        
        self.color = GRAY
        self.edgeColor = BLUE
        
        #アニメーション キーと関数をもつオブジェクトを格納
        #その中のplay関数で動きを指定
        self.motion = {}
    
    def setChild(self, child, vec, vec2):
        self.children.append(child)
        child.parent = self
        #接続部のローカル位置を指定
        self.connection.append(vec)
        child.parConnection = vec2
        return self
    
    #子オブジェクトの接続位置を固定
    def setChildPos(self):
        if len(self.children) == 0:
            return
        
        vec = Vector3([self.unitVectorx, self.unitVectory, self.unitVectorz])
        for i in range(len(self.children)):
            vec2 = Vector3([self.children[i].unitVectorx, self.children[i].unitVectory, self.children[i].unitVectorz])
            self.children[i].position = self.position + vec*self.connection[i] - vec2*self.children[i].parConnection
            
            self.children[i].setChildPos()
    
    def setID(self, id):
        self.id = id
    
    def shift(self, vector):          
        if self.parent == None:
            self.position += vector
            self.setChildPos()
            return self
        else:
            self.parent.shift(vector)
    
    def setColor(self, col, edgeCol):
        self.color = col
        self.edgeColor = edgeCol
        return self

    def setMotion(self, string, motion):
        self.motion.setdefault(string, motion)
        return self
        
    #アニメーションの再生
    def play(self, string):
        self.motion[string].play()
        
    #回転-----------------------------------------------------------
    def setUnitVector(self):
        #親オブジェクトなら、回転角から直接求める
        if self.parent == None:
            self.unitVectorx.unitVectorx(self.rotation)
            self.unitVectory.unitVectory(self.rotation)
            self.unitVectorz.unitVectorz(self.rotation)
        #子オブジェクトなら、親オブジェクトの単位ベクトルをさらに回転させる。
        else:
            self.unitVectorx = self.parent.unitVectorx
            self.unitVectory = self.parent.unitVectory
            self.unitVectorz = self.parent.unitVectorz
            
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
    
    #子も同じ角度回転させる。
    def rotateChildren(self, arg):
        if len(self.children) == 0:
            return
        
        for child in self.children:
            #子オブジェクトのローカル回転角で回転させる
            child.setUnitVector()
            child.rotateChildren(arg)
    
    #これ以下の階層のオブジェクトを回転させる
    def rotate(self, arg):
        arg *= math.pi / 180
        
        self.rotation += arg
        self.setUnitVector()
        self.rotateChildren(arg)
        
        #子オブジェクトの場合
        if self.parent != None:
            self.parent.setChildPos()
        else:
            self.setChildPos()
        return self

    def setRotation(self, arg):
        arg *= math.pi / 180
        
        self.rotation = arg
        self.setUnitVector()
        self.rotateChildren(arg)
        
        if self.parent != None:
            self.parent.setChildPos()
        else:
            self.setChildPos()
        return self
    
    def rotatePositionx(self, axis, arg):   #argはint or float
        arg *= math.pi / 180
            
        axisy = axis[0]
        axisz = axis[1] 
        
        #回転軸からの距離
        r = math.sqrt((self.position.vec[1] - axisy)**2 + (self.position.vec[2] - axisz)**2)
        if r == 0:
            return
        
        #始点からの角度
        #+-のどちらか
        theta = math.acos((self.position.vec[1] - axisy)/r)
        #sin(theta) + axisz がz座標と一致しなかったら - を掛ける
        if abs(r*math.sin(theta) + axisz - self.position.vec[2]) > abs(r*math.sin(-theta) + axisz - self.position.vec[2]):
            theta *= -1
            
        #回転後のy, z座標
        posy = axisy + r * math.cos(theta + arg)
        posz = axisz + r * math.sin(theta + arg)
        
        self.position = Vector3([0, posy, posz])
        self.setChildPos()
        
    def rotatePositiony(self, axis, arg):   #argはint or float
        arg *= math.pi / 180
            
        axisz = axis[0]
        axisx = axis[1] 
        
        #回転軸からの距離
        r = math.sqrt((self.position.vec[2] - axisz)**2 + (self.position.vec[0] - axisx)**2)
        if r == 0:
            return
        
        #始点からの角度
        #+-のどちらか
        theta = math.acos((self.position.vec[2] - axisz)/r)
        #sin(theta) + axisx がx座標と一致しなかったら - を掛ける
        if abs(r*math.sin(theta) + axisx - self.position.vec[0]) > abs(r*math.sin(-theta) + axisx - self.position.vec[0]):
            theta *= -1
            
        #回転後のy, z座標
        posz = axisz + r * math.cos(theta + arg)
        posx = axisx + r * math.sin(theta + arg)
        
        self.position = Vector3([posx, 0, posz])
        self.setChildPos()
    
    def rotatePositionz(self, axis, arg):   #argはint or float
        arg *= math.pi / 180
            
        axisx = axis[0]
        axisy = axis[1] 
        
        #回転軸からの距離
        r = math.sqrt((self.position.vec[0] - axisx)**2 + (self.position.vec[1] - axisy)**2)
        if r == 0:
            return
        
        #始点からの角度
        #+-のどちらか
        theta = math.acos((self.position.vec[0] - axisx)/r)
        #sin(theta) + axisz がz座標と一致しなかったら - を掛ける
        if abs(r*math.sin(theta) + axisy - self.position.vec[1]) > abs(r*math.sin(-theta) + axisy - self.position.vec[1]):
            theta *= -1
            
        #回転後のy, z座標
        posx = axisx + r * math.cos(theta + arg)
        posy = axisy + r * math.sin(theta + arg)
        
        self.position = Vector3([posx, posy, 0])
        self.setChildPos()
    
class Rect(Object):
    def __init__(self, lx, ly):
        super().__init__()
        self.tag = "rect"
        
        #xy平面に書く
        self.size = Vector3([lx, ly, 0])                 #中心から端までの距離
        self.color = AQUA
        self.edgeColor = BLUE
    
    def getTops(self):
        self.tops = [
            self.position +(self.unitVectorx*(-1) - self.unitVectory + self.unitVectorz)*self.size,
            self.position + (self.unitVectorx - self.unitVectory + self.unitVectorz)*self.size,
            self.position + (self.unitVectorx + self.unitVectory + self.unitVectorz)*self.size,
            self.position + (self.unitVectorx*(-1) + self.unitVectory + self.unitVectorz)*self.size,
        ]

class Cube(Object):
    def __init__(self, lx, ly, lz):   
        super().__init__()
        self.tag = "cube"
        
        self.size = Vector3([lx, ly, lz])    #重心から端までの距離を指定
        self.color = GRAY
        self.edgeColor = BLUE
        
        #外から見たときに時計回りになるように、面を構成する頂点をまとめる
        self.planes = [
            [1, 0, 3, 2],   #奥 +z
            [0, 1, 5, 4],   #上 -y
            [1, 2, 6, 5],   #右 +x
            [2, 3, 7, 6],   #下 +y
            [3, 0, 4, 7],   #左 -x
            [4, 5, 6, 7]    #前 -z
        ]
        
    def getTops(self):
        self.tops = [
            #奥の面
            self.position + (self.unitVectorx*(-1) - self.unitVectory + self.unitVectorz)*self.size,
            self.position + (self.unitVectorx - self.unitVectory + self.unitVectorz)*self.size,
            self.position + (self.unitVectorx + self.unitVectory + self.unitVectorz)*self.size,
            self.position + (self.unitVectorx*(-1) + self.unitVectory + self.unitVectorz)*self.size,
            #手前の面
            self.position + (self.unitVectorx*(-1) - self.unitVectory - self.unitVectorz)*self.size,
            self.position + (self.unitVectorx - self.unitVectory - self.unitVectorz)*self.size,
            self.position + (self.unitVectorx + self.unitVectory - self.unitVectorz)*self.size,
            self.position + (self.unitVectorx*(-1) + self.unitVectory - self.unitVectorz)*self.size,
        ]
        return self.tops
    
    def put_wire(self, bg, tridim):
        for i in range(4):
            i2 = i + 1
            if i2 == 4:
                i2 = 0
            #奥の面
            pygame.draw.line(bg, self.col,
                            tridim.dim(self.tops[i][0], self.tops[i][1], self.tops[i][2]),
                            tridim.dim(self.tops[i2][0], self.tops[i2][1], self.tops[i2][2]),
                            width = 2)
            #つなぎ目
            pygame.draw.line(bg, self.col,
                            tridim.dim(self.tops[i][0], self.tops[i][1], self.tops[i][2]),
                            tridim.dim(self.tops[i + 4][0], self.tops[i + 4][1], self.tops[i + 4][2]),
                            width = 2)
            #前の面
            pygame.draw.line(bg, self.col,
                            tridim.dim(self.tops[i + 4][0], self.tops[i + 4][1], self.tops[i + 4][2]),
                            tridim.dim(self.tops[i2 + 4][0], self.tops[i2 + 4][1], self.tops[i2 + 4][2]),
                            width = 2)
    
#オブジェクトを描画する
class Camera(Object):
    def __init__(self):
        super().__init__()
        #スクリーンの左上のグローバル座標座標
        self.position = Vector3([0, 0, 0])
        #回転量 いちいちacosとかを使って回転角を求めなくてもいいように
        self.rotation = Vector3([0, 0, 0])
        #ローカル座標の、グローバル座標における座標軸
        self.unitVectorx = Vector3([1, 0, 0])
        self.unitVectory = Vector3([0, 1, 0])
        self.unitVectorz = Vector3([0, 0, 1])
        #映し出すものを格納
        self.hierarchy = []
    
    def setChildHierarchy(self, obj):
        if len(obj.children) == 0:
            return
        
        for child in obj.children:
            self.hierarchy.append(child)
            self.setChildHierarchy(child)
      
    def setHierarchy(self, hierarchy):
        for obj in hierarchy:
            self.hierarchy.append(obj)
            self.setChildHierarchy(obj)
    
    def shift(self, vector):          #Vector3型で指定
        self.position += vector
        return self
    
    
    #グローバル座標をローカル座標に変換する
    def convertAxis(self, position, string):
        relPos = position
        if string == "position":
            relPos = position - self.position
        ans = [0, 0, 0]
        
        A = [[self.unitVectorx.vec[0], self.unitVectory.vec[0], self.unitVectorz.vec[0]], 
             [self.unitVectorx.vec[1], self.unitVectory.vec[1], self.unitVectorz.vec[1]], 
             [self.unitVectorx.vec[2], self.unitVectory.vec[2], self.unitVectorz.vec[2]]]
        
        X = [[relPos.vec[0], self.unitVectory.vec[0], self.unitVectorz.vec[0]], 
             [relPos.vec[1], self.unitVectory.vec[1], self.unitVectorz.vec[1]], 
             [relPos.vec[2], self.unitVectory.vec[2], self.unitVectorz.vec[2]]]

        Y = [[self.unitVectorx.vec[0], relPos.vec[0], self.unitVectorz.vec[0]], 
             [self.unitVectorx.vec[1], relPos.vec[1], self.unitVectorz.vec[1]], 
             [self.unitVectorx.vec[2], relPos.vec[2], self.unitVectorz.vec[2]]]
        
        Z = [[self.unitVectorx.vec[0], self.unitVectory.vec[0], relPos.vec[0]], 
             [self.unitVectorx.vec[1], self.unitVectory.vec[1], relPos.vec[1]], 
             [self.unitVectorx.vec[2], self.unitVectory.vec[2], relPos.vec[2]]]
        
        #クラーメルの定理
        ans[0] = det(X) / det(A)
        ans[1] = det(Y) / det(A)
        ans[2] = det(Z) / det(A)
        return Vector3(ans)
    
    def display(self, bg, tridim):
        tops = []
        #すべてのオブジェクトの位置、ローカル座標をカメラのローカル座標に変換
        for obj in self.hierarchy:
            obj.viewPosition = self.convertAxis(obj.position, "position")
            obj.viewUnitVectorx = self.convertAxis(obj.unitVectorx, "unitVectorx")
            obj.viewUnitVectory = self.convertAxis(obj.unitVectory, "unitVectory")
            obj.viewUnitVectorz = self.convertAxis(obj.unitVectorz, "unitVectorz")
        
        #頂点のうち、視点から一番近いzを求める
        for obj in self.hierarchy:
            tops = self.getTops(obj)
            nearestDist = None
            for top in tops:
                if nearestDist == None:
                    nearestDist = top.distance(tridim.perspective)
                elif top.distance(tridim.perspective) < nearestDist:
                    nearestDist = top.distance(tridim.perspective)
            if nearestDist != None:
                obj.nearestDist = nearestDist
        
        #最小のzが大きい順に並べる
        self.sort(self.hierarchy)
        
        #1つずつ描画
        for obj in self.hierarchy:
            if obj.tag == "cube":
                tops = self.getTops(obj)
                #各面に対して、描画するかを判定、描画する
                for plane in obj.planes:
                    if tops[plane[0]].vec[2]>0 and tops[plane[1]].vec[2]>0 and tops[plane[2]].vec[2]>0 and tops[plane[3]].vec[2]>0:
                        #４つの頂点の画面上の座標
                        t1 = tridim.dim(tops[plane[0]])
                        t2 = tridim.dim(tops[plane[1]])
                        t3 = tridim.dim(tops[plane[2]])
                        t4 = tridim.dim(tops[plane[3]])
                        #その面が手前を向いてたら描く
                        if (t3[0] - t2[0]) * (t1[1] - t2[1]) - (t1[0] - t2[0]) * (t3[1] - t2[1]) > 0:
                            pygame.draw.polygon(bg, obj.color, [t1, t2, t3, t4])
                            pygame.draw.polygon(bg, obj.edgeColor, [t1, t2, t3, t4], width = 3)
                        
            elif obj.tag == "rect":
                tops = self.getTops(obj)
                if tops[0].vec[2]>0 and tops[1].vec[2]>0 and tops[2].vec[2]>0 and tops[3].vec[2]>0:
                    t1 = tridim.dim(tops[0])
                    t2 = tridim.dim(tops[1])
                    t3 = tridim.dim(tops[2])
                    t4 = tridim.dim(tops[3])
                    pygame.draw.polygon(bg, obj.color, [t1, t2, t3, t4])
                    pygame.draw.polygon(bg, obj.edgeColor, [t1, t2, t3, t4], width = 3)
    
    #hierarchyをviewPosition.vec とtridim.perspective.vecとの距離が大きい順に並べ替える
    def sort(self, hierarchy):
        def merge_sort(list, start, end):
            if end-1 == start:
                return
            
            mid = int((start + end)/2)
            
            #一つになるまで分割する
            merge_sort(list, start, mid)
            merge_sort(list, mid, end)
            
            merge(list, start, mid, end)
        
        #二つの配列を結合する 
        def merge(list, start, mid, end):
            #分割
            nl = mid - start
            nr = end - mid
            left = []
            right = []
            for i in range(nl):
                left.append(list[start + i])
            for i in range(nr):
                right.append(list[mid + i])
            #マージ
            lIndex = 0
            rIndex = 0
            #そのオブジェクトの透視投影からの距離を比較する
            for i in range(start, end):
                if rIndex == nr:
                    list[i] = left[lIndex]
                    lIndex += 1
                elif lIndex == nl:
                    list[i] = right[rIndex]
                    rIndex += 1
                elif left[lIndex].nearestDist > right[rIndex].nearestDist:
                    list[i] = left[lIndex]
                    lIndex += 1
                elif left[lIndex].nearestDist <= right[rIndex].nearestDist:
                    list[i] = right[rIndex]
                    rIndex += 1
        
        merge_sort(hierarchy, 0, len(hierarchy))
        return hierarchy
    
    #カメラから見た頂点を求める
    def getTops(self, obj):
        tops = []
        if obj.tag == "cube":
            x = obj.size.vec[0]
            y = obj.size.vec[1]
            z = obj.size.vec[2]
            tops = [
                #奥の面
                obj.viewPosition +(obj.viewUnitVectorx*(-1)*x - obj.viewUnitVectory*y + obj.viewUnitVectorz*z),
                obj.viewPosition + (obj.viewUnitVectorx*x - obj.viewUnitVectory*y + obj.viewUnitVectorz*z),
                obj.viewPosition + (obj.viewUnitVectorx*x + obj.viewUnitVectory*y + obj.viewUnitVectorz*z),
                obj.viewPosition + (obj.viewUnitVectorx*(-1)*x + obj.viewUnitVectory*y + obj.viewUnitVectorz*z),
                #手前の面
                obj.viewPosition +(obj.viewUnitVectorx*(-1)*x - obj.viewUnitVectory*y - obj.viewUnitVectorz*z),
                obj.viewPosition + (obj.viewUnitVectorx*x - obj.viewUnitVectory*y - obj.viewUnitVectorz*z),
                obj.viewPosition + (obj.viewUnitVectorx*x + obj.viewUnitVectory*y - obj.viewUnitVectorz*z),
                obj.viewPosition + (obj.viewUnitVectorx*(-1)*x + obj.viewUnitVectory*y - obj.viewUnitVectorz*z),
            ]
        
        elif obj.tag == "rect":
            x = obj.size.vec[0]
            y = obj.size.vec[1]
            z = obj.size.vec[2]
            tops = [
                #奥の面
                obj.viewPosition +(obj.viewUnitVectorx*(-1)*x - obj.viewUnitVectory*y + obj.viewUnitVectorz*z),
                obj.viewPosition + (obj.viewUnitVectorx*x - obj.viewUnitVectory*y + obj.viewUnitVectorz*z),
                obj.viewPosition + (obj.viewUnitVectorx*x + obj.viewUnitVectory*y + obj.viewUnitVectorz*z),
                obj.viewPosition + (obj.viewUnitVectorx*(-1)*x + obj.viewUnitVectory*y + obj.viewUnitVectorz*z)
            ]
            
        return tops