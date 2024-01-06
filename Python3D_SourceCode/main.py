import pygame
import sys
import Objects
import Character
import CreateObject
import System
import Operation
import Window
import UI

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
YELLOW = (255, 255,  0)

windowx = System.windowx
windowy = System.windowy

def main():
    pygame.init()
    pygame.display.set_caption("pygameでの3D描画")
    screen = pygame.display.set_mode((windowx, windowy))
    
    #オブジェクトを作成--------------
    clock = pygame.time.Clock()
    #font = pygame.font.Font(None, 80)
    tridim = System.Tridim(System.Vector3([windowx/2, windowy/2, -500]))
    
    Camera = Objects.Camera()
    timer = System.Timer()
    sceneManager = System.SceneManager()
    
    pc = CreateObject.CreatePC(WHITE, BLUE).shift(System.Vector3([-800, 600, 1500]))
    PC = Character.PC(pc, Window.InputRecord())
    pc2 = CreateObject.CreatePC(BLACK, BLUE).shift(System.Vector3([-1500, 600, 800]))
    PC2 = Character.PC(pc2, Window.EditRecord())
    pc3 = CreateObject.CreatePC(WHITE, RED).shift(System.Vector3([800, 600, 1500]))
    PC3 = Character.PC(pc3, Window.InputFood())
    pc4 = CreateObject.CreatePC(BLACK, RED).shift(System.Vector3([1500, 600, 800]))
    PC4 = Character.PC(pc4, Window.EditFood())
    
    player = CreateObject.CreatePlayer().shift(
        System.Vector3([0, 500, -1300])).rotate(
        System.Vector3([0, 90, 0]))
    Player = Character.Player(player).setVelocity(30, 100)
    
    Floor = CreateObject.CreateFloor(300).shift(System.Vector3([0, 1500, 0]))
    
    Desk = CreateObject.CreateDesk().shift(System.Vector3([-800, 650, 1500]))
    Desk2 = CreateObject.CreateDesk().shift(System.Vector3([-1500, 650, 800]))
    Desk3 = CreateObject.CreateDesk().shift(System.Vector3([800, 650, 1500]))
    Desk4 = CreateObject.CreateDesk().shift(System.Vector3([1500, 650, 800]))
    
    door = CreateObject.CreateDoor().shift(System.Vector3([0, 500, 2500]))
    Door = Character.Door(door)
    Fense = CreateObject.CreateFenseH(850).shift(System.Vector3([-1350, 600, 2600]))
    Fense2 = CreateObject.CreateFenseH(850).shift(System.Vector3([1350, 600, 2600]))
    Fense3 = CreateObject.CreateFenseH(2500).shift(System.Vector3([0, 600, -2600]))
    Fense4 = CreateObject.CreateFenseV(2500).shift(System.Vector3([-2600, 600, 0]))
    Fense5 = CreateObject.CreateFenseV(2500).shift(System.Vector3([2600, 600, 0]))
    #-------------------------------
    Hierarchy = [
        pc, pc2, pc3, pc4, Floor, player, Desk, Desk2, Desk3, Desk4, door, 
        Fense, Fense2, Fense3, Fense4, Fense5
        ]
    Camera.setHierarchy(Hierarchy)
    
    while True:
        timer.count()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        screen.fill(BLACK)       #黒で、スクリーンをクリアする
        
        #背景を描く
        UI.drawBG(screen)
        
        #終了
        if System.index == -1 or System.index == -2:
            if System.tmr > 15:
                pygame.quit()
                sys.exit()
        
        #タイトル
        elif System.index == 0:
            Camera.zoomOut()
        
        elif System.index == 1:
            Camera.zoom()
            #Playerが近くにいるとopen()が加えて実行される
            PC.close()
            PC2.close()
            PC3.close()
            PC4.close()
            Door.close()
        
        System.judgeCollision(Hierarchy)
        
        #速度の変化など
        Operation.fieldOperation(Camera, Player, sceneManager)
        
        #位置の移動
        if System.pause == False:
            for obj in Hierarchy:
                obj.move()
        
        Camera.chase(player)
        Camera.display(screen, tridim)
        
        UI.drawUI(screen)
        
        pygame.display.update()
        clock.tick(15)

if __name__ == '__main__':
    main() 
