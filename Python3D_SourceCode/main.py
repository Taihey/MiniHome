import pygame
import sys
import Objects
import Character
import CreateObject
from System import *
import Operation
import Window

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
YELLOW = (255, 255,  0)

def main():
    pygame.init()
    pygame.display.set_caption("pygameでの3D描画")
    screen = pygame.display.set_mode((windowx, windowy))
    
    #オブジェクトを作成--------------
    clock = pygame.time.Clock()
    #font = pygame.font.Font(None, 80)
    tridim = Tridim(Vector3([windowx/2, windowy/2, -500]))
    
    Camera = Objects.Camera()
    
    pc = CreateObject.CreatePC().shift(Vector3([windowx/2, windowy/2-100, 500]))
    PC = Character.PC(pc, Window.InputRecord())
    
    player = CreateObject.CreatePlayer().shift(
        Vector3([-100, 500, 400])).rotate(
        Vector3([0, 90, 0]))
    Player = Character.Player(player).setVelocity(10, 100)
    
    Floor = CreateObject.CreateFloor(1000).shift(Vector3([300, 2500, 400]))
    
    Desk = CreateObject.CreateDesk().shift(Vector3([windowx/2, windowy/2 + 50, 500]))
    #-------------------------------
    Hierarchy = [pc, player, Floor, Desk]
    Camera.setHierarchy(Hierarchy)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(BLACK)       #黒で、スクリーンをクリアする
        
        #操作による移動
        Operation.fieldOperation(Camera, PC, Player)
        
        #重力による自由落下
        for obj in Hierarchy:
            obj.move()
        
        judgeCollision(Hierarchy)
        
        Camera.chase(player, 800)
        Camera.display(screen, tridim)
        
        pygame.display.update()
        clock.tick(15)

if __name__ == '__main__':
    main() 
