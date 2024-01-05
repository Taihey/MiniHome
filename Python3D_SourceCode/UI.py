import pygame
import System
windowx = System.windowx
windowy = System.windowy

BG = pygame.image.load("./picture/BG.png")
#半透明のスクリーン
screen = pygame.Surface((windowx, windowy), flags=pygame.SRCALPHA)
screen.fill((0, 255, 255, 128))
pauseScreen = pygame.Surface((windowx, windowy), flags=pygame.SRCALPHA)
pauseScreen.fill((128, 128, 128, 128))

def drawBG(bg):
    bg.blit(BG, [0, 0])

def drawUI(bg):
    if System.index == -2:
        bg.blit(screen, [0, 0])
        System.Text("Thank you for Playing!").putCenter(bg, 120, System.BLACK)
    
    if System.index == -1:
        bg.blit(screen, [0, 0])
        System.Text("Have a nice day!").putCenter(bg, 120, System.BLACK)
    
    elif System.index == 0:
        System.Text("Mini Home").putHeight(bg, 140, System.BLACK, 300)
        System.Text("Push [S] to Start!").putHeight(bg, 80, System.BLACK, 700)
        System.Text("Push [Q] to Quit Game").putHeight(bg, 60, System.RED, 800)
    
    if System.pause:
        bg.blit(pauseScreen, [0, 0])
        System.Text("Push [B] to Back to Title").putHeight(bg, 60, System.RED, 800)