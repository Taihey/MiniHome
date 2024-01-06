import pygame
import System
windowx = System.windowx
windowy = System.windowy

BG = pygame.image.load("./GameFile/BG.png")
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
    
    elif System.index == -1:
        bg.blit(screen, [0, 0])
        System.Text("Have a nice day!").putCenter(bg, 120, System.BLACK)
    
    elif System.index == 0:
        System.Text("Mini Home").putHeight(bg, 140, System.BLACK, 300)
        System.Text("Push [S] to Start!").putHeight(bg, 80, System.BLACK, 700)
        System.Text("Push [Q] to Quit Game").putHeight(bg, 60, System.RED, 800)
    
    elif System.index == 1:
        System.Text("Move: [RIGHT], [LEFT], [UP], [DOWN]"
                    ).putFlex(bg, 40, System.BLACK, 380, 20)
        System.Text("Run: [D] + [RIGHT], [LEFT], [UP], [DOWN]"
                    ).putFlex(bg, 40, System.BLACK, 380, 70)
        System.Text("Move Camera: [C] + [RIGHT], [LEFT]"
                    ).putFlex(bg, 40, System.BLACK, 380, 120)
        System.Text("Pause: [P]"
                    ).putFlex(bg, 40, System.BLACK, 380, 170)
        
        pygame.draw.rect(bg, System.YELLOW, [30, 50, 300, 100])
        pygame.draw.rect(bg, System.AQUA, [27, 47, 306, 106], width=6, border_radius=10)
        System.Text("Get Closer to PC").putFlex(bg, 40, System.BLACK, x = 50, y = 60)
        System.Text("to Open a Window").putFlex(bg, 40, System.BLACK, x = 50, y = 110)
    
    elif System.index == 2:
        bg.blit(pauseScreen, [0, 0])
        
        pygame.draw.rect(bg, System.YELLOW, [100, 400, 800, 200])
        pygame.draw.rect(bg, System.AQUA, [97, 397, 806, 206], width=6, border_radius=10)
        
        System.Text("Window is Open").putCenter(bg, 120, System.BLUE)
        
    if System.pause:
        bg.blit(pauseScreen, [0, 0])
        pygame.draw.rect(bg, System.YELLOW, [200, 155, 600, 90])
        pygame.draw.rect(bg, System.AQUA, [197, 152, 606, 96], width=6, border_radius=10)
        System.Text("Pause Menu").putHeight(bg, 100, System.BLACK, y = 200)
        
        pygame.draw.rect(bg, System.YELLOW, [100, 550, 800, 200])
        pygame.draw.rect(bg, System.AQUA, [97, 547, 806, 206], width=6, border_radius=10)
        System.Text("Push [P] to Restart").putHeight(bg, 80, System.BLACK, 600)
        System.Text("Push [B] to Back to Title").putHeight(bg, 60, System.RED, 700)