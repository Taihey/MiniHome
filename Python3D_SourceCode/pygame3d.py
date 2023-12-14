import pygame
import sys
import Objects
import CreateObject
from System import *

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
    tridim = Tridim(Vector3([windowx/2, windowy/2, -1000]))
    camera = Objects.Camera().shift(Vector3([-100, 0, 0]))
    PC = CreateObject.CreatePC().shift(Vector3([windowx/2, windowy/2, 500]))
    Player = CreateObject.CreatePlayer().shift(Vector3([300, 500, 400])).rotate(Vector3([0, 90, 0]))
    #-------------------------------
    Hierarchy = [PC, Player]
    camera.setHierarchy(Hierarchy)
    
    while True:
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(BLACK)       #黒で、スクリーンをクリアする
        
        if key[pygame.K_DOWN]:
            camera.rotate(Vector3([0, 0, 1]))
            #camera.rotatePositionz([windowx/2, windowy/2], 1)
        if key[pygame.K_RIGHT]:
            camera.rotate(Vector3([0, 1, 0]))
        elif key[pygame.K_LEFT]:
            camera.rotate(Vector3([0, -1, 0]))
            #camera.rotatePositiony([windowx/2, 300], 1)
        if key[pygame.K_UP]:
            camera.rotate(Vector3([0, 0, -1]))
        
        if key[pygame.K_c]:
            PC.play("close")
            
        if key[pygame.K_w]:
            Player.play("walk")
        
        elif key[pygame.K_d]:
            Player.play("run")
            
        else:
            Player.play("stay")
        
        camera.display(screen, tridim)
        
        pygame.display.update()
        clock.tick(15)

if __name__ == '__main__':
    main()