import random
import sys
import pygame
import time
from pygame.locals import *

pygame.init()


FPS = 32
SCREENWIDTH = 287
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT)) #SCREEN DISPLAY
GROUNDY = SCREENHEIGHT * 0.8  #BASE KA SIZE KYA HOGA
GAME_SPRITES = {} #IMAGE DISPLAY
GAME_SOUNDS = {} #IMAGE SOUND
PLAYER = 'gallery/sprites/bird.png' #FULL PATH PLAYER IMAGE
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'
gamedisplay = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
pygame.display.set_caption("FLAPPY")
clock = pygame.time.Clock()

 #ab game spirit or sound mae image or sound dalege jo use krege 
def welcomeScreen():
    playerx = int(SCREENWIDTH/5) 
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_height())/3.5)
    messagey = int(SCREENHEIGHT * 0.25)
    basex = 0
    while True:
        for event in pygame.event.get():  #user in button
            #IF USER CROSS THE BUTTON
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #if space or up key start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))#screen dikhaa do bs
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update() #jbtk yeh nhi hoga tbtk screen change nnhi hogi chahe blit() kitne krle
                FPSCLOCK.tick(FPS)

def random_pipe():
    pipeheight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3.5
    y2 = offset + random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeheight - y2 + offset
    pipe = [
        {'x':pipex,'y': -y1}, #upper pipe
        {'x':pipex , 'y':y2} #lower pipe
    ]
    return pipe

def text_objects(text1,text2):
    textsurface = text2.render(text1,True,(0,0,0))
    return textsurface, textsurface.get_rect()

def message_display(text):
    largetext = pygame.font.Font(None,50)
    textsurf , textrect = text_objects(text,largetext)
    textrect.center = ((SCREENWIDTH/2),(SCREENHEIGHT/1.125))
    gamedisplay.blit(textsurf,textrect)
    pygame.display.update()
    time.sleep(10)
    
def mainGame():
    score_value = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0
    #create random pipes

    newpipe1 = random_pipe()
    newpipe2 = random_pipe()


    #list of upper nad lower pipes

    upperpipes = [
        {'x':SCREENWIDTH+200 , 'y':newpipe1[0]['y']},
        
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2) , 'y':newpipe2[0]['y']},
        ]
    lowerpipes = [
        {'x':SCREENWIDTH+200 , 'y':newpipe1[1]['y']},
        
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2) , 'y':newpipe2[1]['y']},
        ]

    pipevelx = -2  #pipe move krega ulta

    playervely = -9 #placer nicher ko girega
    playermaxvely = 15 
    playerminvely = -5
    playeraccy = 1.2

    playerFlapvel = -8 #velocity while flap
    playerFlapped = False #true while flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or K_UP):
                if playery>0:
                    playervely =  playerFlapvel
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos + 4:
                score_value+= 1
                print(f"Score: {score_value}")
                GAME_SOUNDS['point'].play()

        crashTest = isCollide(playerx , playery, upperpipes , lowerpipes)
        if crashTest:
            message_display("CRASHED")
            return

        if playervely < playermaxvely and not playerFlapped:
            playervely+= playeraccy

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playervely , GROUNDY - playery - playerHeight)

        #move pipes to left

        for upperpipe , lowerpipe in zip(upperpipes , lowerpipes):
            upperpipe['x']+= pipevelx
            lowerpipe['x']+= pipevelx

        #add new pipe
        if 0<upperpipes[0]['x']<5:
            newpipe = random_pipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])
        #if the pipe is out screen remove it

        if upperpipes[0]['x']< -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperpipe , lowerpipe in zip(upperpipes , lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'] , upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'] , lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['player'],(playerx , playery))
        SCREEN.blit(GAME_SPRITES['base'],(basex , GROUNDY))
        myDigits = [int(x) for x in list(str(score_value))]
        width = 0
        for digit in myDigits:
            width+= GAME_SPRITES['numbers'][digit].get_width()

        xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(xoffset , SCREENHEIGHT*0.12))
            xoffset+= GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


    
    
    

def isCollide(playerx , playery, upperpipes, lowerpipes):
    if playery> GROUNDY - 25 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperpipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x'] - 16) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
            
        

    for pipe in lowerpipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x'] - 10 ) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
            
        
    
    return False
                    
                
                 
        
    
    
    
                
                
            

if __name__ == "__main__":
     #thus will be main fun game start
     pygame.init() #initalize pygame k saaare modules
     FPSCLOCK = pygame.time.Clock()  #game k fps ko control krta hai 
     pygame.display.set_caption("Flappy Bird")
     GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
     ) #tuple jisme 0-9 image dedi
     GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
     GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
     GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
     )

    #GAME SOUND
     GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
     GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
     GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
     GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
     GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')
    
     GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
     GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

     while True:
        welcomeScreen()  #SHOW THE WELCOME SCREEN TO USER
        mainGame()  #THIS IS MAIN GAME FUNC
