import pygame
import sys
import Objects
import Objects2
import CreateObject
from System import *
import Operation

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
    camera = Objects.Camera().shift(Vector3([0, 0, 0]))
    PC = CreateObject.CreatePC().shift(Vector3([windowx/2, windowy/2, 500]))
    player = CreateObject.CreatePlayer().shift(
        Vector3([300, 500, 400])).rotate(
        Vector3([0, 90, 0]))
    Player = Objects2.Player(player).setVelocity(10, 100)
    #-------------------------------
    Hierarchy = [PC, player]
    camera.setHierarchy(Hierarchy)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(BLACK)       #黒で、スクリーンをクリアする
        
        Operation.fieldOperation(camera, PC, Player)
        
        camera.chase(player, 800)
        camera.display(screen, tridim)
        
        pygame.display.update()
        clock.tick(15)

if __name__ == '__main__':
    main() 
