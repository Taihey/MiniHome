from System import *

class BoxCollider:
    def __init__(self, belonging):
        self.belonging = belonging
        self.position = Vector3([0, 0, 0]) #所属先とのずれ
        self.size = belonging.size
        self.tag = "box"
        self.unitVectorx = belonging.unitVectorx
        self.unitVectory = belonging.unitVectory
        self.unitVectorz = belonging.unitVectorz
    
    def judge(self, opponent):
        if opponent.tag == "box":
            