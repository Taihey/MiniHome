import pygame
from System import *

def fieldOperation(camera, PC, Player):
    key = pygame.key.get_pressed()
    
    #カメラの操作
    if key[pygame.K_c]:
        if key[pygame.K_DOWN]:
            camera.rotate(Vector3([1, 0, 0]))
            
        if key[pygame.K_RIGHT]:
            camera.rotate(Vector3([0, 1, 0]))
        elif key[pygame.K_LEFT]:
            camera.rotate(Vector3([0, -1, 0]))
            
        if key[pygame.K_UP]:
            camera.rotate(Vector3([-1, 0, 0]))
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
            Player.object.play("stay")
    else:    
        if key[pygame.K_p]:
            PC.play("close")
        
        if key[pygame.K_UP]:
            Player.walkz(camera, 1)
        elif key[pygame.K_DOWN]:
            Player.walkz(camera, -1)
        elif key[pygame.K_RIGHT]:
            Player.walkx(camera, 1)
        elif key[pygame.K_LEFT]:
            Player.walkx(camera, -1)
        else:
            Player.object.play("stay")