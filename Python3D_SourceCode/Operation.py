import pygame
import System 

keyManager_p = System.keyManager(pygame.K_p)

def fieldOperation(camera, Player, sceneManager):
    key = pygame.key.get_pressed()
    
    #タイトル
    if System.index == 0:
        if key[pygame.K_s]:
            sceneManager.moveScene(1)
        
        elif key[pygame.K_q]:
            sceneManager.moveScene(-2)
    
    #index = 1 or -1の時
    elif (System.index == -1 or System.index == 1) and System.pause == False:
        #カメラの操作
        if key[pygame.K_c]:
            if key[pygame.K_RIGHT]:
                camera.rotate(System.Vector3([0, 5, 0]))
            elif key[pygame.K_LEFT]:
                camera.rotate(System.Vector3([0, -5, 0]))
                
        elif key[pygame.K_d]:
            if key[pygame.K_UP]:
                Player.runz(camera, 1)
            elif key[pygame.K_DOWN]:
                Player.runz(camera, -1)
            elif key[pygame.K_RIGHT]:
                Player.runx(camera, 1)
            elif key[pygame.K_LEFT]:
                Player.runx(camera, -1)
            else:
                Player.stay()
                
        else:    
            if key[pygame.K_UP]:
                Player.walkz(camera, 1)
            elif key[pygame.K_DOWN]:
                Player.walkz(camera, -1)
            elif key[pygame.K_RIGHT]:
                Player.walkx(camera, 1)
            elif key[pygame.K_LEFT]:
                Player.walkx(camera, -1)
            else:
                Player.stay()
    
    if System.index == 1:
        if System.pause == False:
            if keyManager_p.onPress():
                System.pause = True
        
        else:
            if keyManager_p.onPress():
                System.pause = False
            
            elif key[pygame.K_b]:
                sceneManager.moveScene(0)
                System.pause = False