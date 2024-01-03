from System import *

#判定は回転しないようにする
class BoxCollider:
    def __init__(self, belonging):
        self.belonging = belonging
        self.position = Vector3([0, 0, 0]) #所属先とのずれ 
        self.size = belonging.size
        self.tag = "box"
    
    def setSize(self, vec):
        self.size = vec
        return self
    
    def setPosition(self, vec):
        self.position = vec
        return self
    
    def judge(self, opponent):
        pos = self.position + self.belonging.position
        opos = opponent.position + opponent.belonging.position
        if opponent.tag == "box":
            #自分が内側or相手が内側
            def isin(num):
                #自分が内側
                b1_1 = (opos.vec[num] - opponent.size.vec[num] <= pos.vec[num] - self.size.vec[num]
                        ) and (pos.vec[num] - self.size.vec[num] <= opos.vec[num] + opponent.size.vec[num])
                b1_2 = (opos.vec[num] - opponent.size.vec[num] <= pos.vec[num] + self.size.vec[num]
                        ) and (pos.vec[num] + self.size.vec[num] <= opos.vec[num] + opponent.size.vec[num])
                
                #相手が内側
                b2_1 = (pos.vec[num] - self.size.vec[num] <= opos.vec[num] - opponent.size.vec[num]
                        ) and (opos.vec[num] - opponent.size.vec[num] <= pos.vec[num] + self.size.vec[num])
                b2_2 = (pos.vec[num] - self.size.vec[num] <= opos.vec[num] + opponent.size.vec[num]
                        ) and (opos.vec[num] + opponent.size.vec[num] <= pos.vec[num] + self.size.vec[num])
                
                return (b1_1 or b1_2) or (b2_1 or b2_2)
            
            return isin(0) and isin(1) and isin(2)