## PROJECT HALIOTH
## LUCAS ZHOU ~ HAOMING MENG
## ICS3U1-01 SUMMATIVE
## JUNE 1 2018
## MR. SALEEM

import math
import os
import pygame
import random
import gameResources
import gameLevels
from pygame.locals import *
from os import path

def mainProgram():
    ## MAIN PROGRAM STRUCTURE ##
    pygame.init()

    ### SETUP ###
    width,height = 600,800
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Project Halioth - Lucas Z. & Haoming M.")
    clock = pygame.time.Clock()
    fps = 60
    enemies_fire_event = USEREVENT + 1

    ### COLORS ###
    white = (255,255,255)
    black = (0,0,0)
    green = (89,171,53)
    grey = (136,136,136)
    red = (250,129,50)
    blue = (30,167,225)
    yellow = (198,157,0)

    ### SPRITE CLASSES ###
    class Explosion(pygame.sprite.Sprite):
        ## EXPLOSION ##
        def __init__(self,center,sizeType):
            super().__init__()
            ''' PHYSICAL PROPERTIES '''
            self.type = sizeType
            self.series = gameResources.explosion_anim[self.type]
            self.image = self.series[0]
            self.last_frame = len(self.series)
            self.rect = self.image.get_rect()
            self.rect.center = center
            ''' ANIMATION PROPERTIES '''
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.framerate = 50
        ## ANIMATION ##
        def update(self):
            ''' STREAM FRAMES AT SET FREQUENCY '''
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update > self.framerate:
                self.last_update = current_time
                self.frame += 1
                if self.frame == self.last_frame:
                    self.kill()
                else:
                    center = self.rect.center
                    self.image = self.series[self.frame]
                    self.rect = self.image.get_rect()
                    self.rect.center = center

    class Bullet(pygame.sprite.Sprite):
        ## BULLET SPRITE ##
        def __init__(self,x,y,direction,color,size=1):
            super().__init__()
            ''' PHYSICAL PROPERTIES '''
            self.image = gameResources.bullet[color][size-1]
            self.rect = self.image.get_rect()
            self.rect.centerx = x    
            self.mask = pygame.mask.from_surface(self.image)
            if direction == 'enemy':
                self.ySpeed = -10
                self.rect.bottom = y
            elif direction == 'player':
                self.ySpeed = 10
                self.rect.top = y
        ## MOVEMENT ##
        def update(self):
            self.rect.y += self.ySpeed
            ''' BOUNDARIES '''
            if self.rect.bottom < 0 or self.rect.top > height + 10:
                self.kill()
                
    class Player(pygame.sprite.Sprite):
        ## PLAYER SPRITE ##
        def __init__(self,player_image,player_color,player_lives,shootFreq):
            super().__init__()
            ''' PHYSICAL PROPERTIES '''
            self.image = player_image
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.color = player_color
            self.rect.center = (width//2,height-175)
            ''' GAME PROPERTIES '''
            self.actionCounter = 1
            self.speed = 5
            self.health = 100
            self.lives = player_lives
            self.levelStatus = 'not complete'
            ''' GUN PROPERTIES '''
            self.turrets = 1
            self.shoot_delay = 400
            self.last_shot = pygame.time.get_ticks()
            ''' POWERUP PROPERTIES '''
            self.power_time = 0
            self.power_type = 'none'
            ''' WHEN LIFE IS LOST '''
            self.killed = False
            self.hidden = False
            self.hide_timer = pygame.time.get_ticks()
            self.flash_timer = pygame.time.get_ticks()
            ''' TO CALCULATE ENEMY MOVEMENT '''
            global player_position
            player_position = self.rect.centerx
        ## RESET DEFAULT GAME PROPERTIES ##
        def reset(self):
            self.speed = 5
            self.turrets = 1
            self.shoot_delay = 400
            self.power_type = 'none'
        ## MOVEMENT ##
        def update(self):
            ''' KEY CONTROLS '''
            keyPress = pygame.key.get_pressed()
            if keyPress[pygame.K_LEFT]:
                self.rect.centerx -= self.speed
            if keyPress[pygame.K_RIGHT]:
                self.rect.centerx += self.speed
            if keyPress[pygame.K_SPACE]:
                if self.levelStatus == 'not complete':
                    self.shoot()
            ''' BOUNDARIES '''
            if self.rect.right > width-5:
                self.rect.right = width-5
            if self.rect.left < 5:
                self.rect.left = 5
            ''' POWERUP TIMING '''
            if pygame.time.get_ticks()-self.power_time > 10000:
                self.reset()
            ''' TO CALCULATE ENEMY MOVEMENT '''
            global player_position
            player_position = self.rect.centerx
            ''' LIFE IS LOST AND 1 SECOND PASSED, RESET PLAYER FLASHING'''
            if self.killed:
                if self.actionCounter == 1:
                    self.destroyed()
                    gameResources.playerDeath.play()
                    self.actionCounter -= 1
                if pygame.time.get_ticks()-self.flash_timer>100:
                    self.hidden = not self.hidden
                    if self.hidden:
                        self.rect.centery -= 300
                    else:
                        self.rect.centery += 300
                    self.flash_timer = pygame.time.get_ticks()
                ''' PLAYER BECOMES SOLID AFTER 5 SECONDS'''
                if self.hidden and \
                   pygame.time.get_ticks()-self.hide_timer>5000:
                    self.hidden = False
                    self.killed = False
                    self.rect.centery = height-175
                    self.actionCounter += 1
                ''' PLAYER OUT OF LIVES '''
                if self.lives == 0:
                    self.levelStatus = 'end'
                    self.rect.centery += 300
        ## SHOOTING MECHANISM ##
        def shoot(self):
            ''' SHOOTING FREQUENCY CONTROL '''
            if not self.killed:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_shot > self.shoot_delay:
                    gameResources.playerBullet.play()
                    self.last_shot = current_time
                    if self.turrets == 1:
                        bullet = Bullet(self.rect.centerx,\
                                        self.rect.top,'enemy',self.color,2)
                        playerBullets.add(bullet)
                        all_sprites.add(bullet)
                    elif self.turrets == 2:
                        turret_pos = int((1/6)*self.rect.width)
                        bullet_1 = Bullet(self.rect.centerx+turret_pos,\
                                          self.rect.top,'enemy',self.color)
                        bullet_2 = Bullet(self.rect.centerx-turret_pos,\
                                          self.rect.top,'enemy',self.color)
                        playerBullets.add(bullet_1,bullet_2)
                        all_sprites.add(bullet_1,bullet_2)
        ## POWERUP MECHANISM ##
        def powerup(self,power_type,shootFreq):
            if power_type == 'fire':
                self.reset()
                self.power_type = 'fire'
                self.turrets = 2
                self.shoot_delay /= 2
                self.power_time = pygame.time.get_ticks()
            elif power_type == 'speed':
                self.reset()
                self.power_type = 'speed'
                self.speed = 10
                self.power_time = pygame.time.get_ticks()
            elif power_type == 'life':
                self.health = 100
        ## UPON LOSING A LIFE, HIDE THE PLAYER ##
        def destroyed(self):
            self.hidden = True
            self.hide_timer = pygame.time.get_ticks()
            self.flash_timer = pygame.time.get_ticks()
            self.rect.centerx = width//2
            self.reset()
    
    class Enemy(pygame.sprite.Sprite):
        ## ENEMY SPRITE ##
        def __init__(self,ySRange,xSRange,spawnRange,playerRange,enemyID):
            super().__init__()
            ''' RANDOMLY GENERATE ENEMY, CALCULATE PROPERTIES'''
            self.type = random.choice(['enemy1','enemy2','enemy3'])
            self.series = gameResources.enemy[self.type]
            self.image = self.series[0]
            self.b_size = self.series[1]
            self.points = self.series[2]
            self.pRange = playerRange
            self.killed = False
            self.kill_time = 0
            self.actionCounter = 1
            ''' PHYSICAL PROPERTIES '''
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.centerx = random.randrange(50,width-50)
            self.rect.centery = random.randrange(spawnRange[0],spawnRange[1])
            ''' GAME PROPERTIES '''
            self.ySpeed = random.randrange(ySRange[0],ySRange[1])
            self.xSpeed = random.randrange(xSRange[0],xSRange[1])
            ''' DETERMINES WHEN ENEMY CAN FIRE '''
            self.identifier = random.randint(1,enemyID)
        ## MOVEMENT ##
        def update(self):
            ''' CHANGE SPEED RANDOMLY AND FOLLOW PLAYER '''
            currentRange = random.randint(self.pRange[0],self.pRange[1])
            if (player_position > self.rect.left+currentRange and \
                self.xSpeed < 0) or \
                (player_position < self.rect.right-currentRange and \
                 self.xSpeed > 0):
                if self.xSpeed > 10:
                    self.xSpeed = 10
                else:
                    self.xSpeed *= -random.uniform(0.75,1.25)
            self.rect.x += self.xSpeed
            self.rect.y += self.ySpeed
            ''' BOUNDARIES '''
            if self.rect.top > height+20:
                global score,player
                ''' PENALTY IF OBJECT REACHES BOTTOM '''
                if player.levelStatus == 'not complete':
                    score -= self.points
                self.kill()
            if (self.rect.left <= 5 and \
                self.rect.left+self.xSpeed < 5) or \
                (self.rect.right >= width-5 and \
                 self.rect.right+self.xSpeed > width-5):
                self.xSpeed *= -1
            ''' WHEN KILLED '''
            if self.killed:
                if self.actionCounter == 1:
                    self.kill_time = pygame.time.get_ticks()
                    self.xSpeed,self.ySpeed = 0,0
                    eSound = pygame.mixer.Sound(random.choice\
                                                (gameResources.explosionSound))
                    eSound.play()
                    self.actionCounter -= 1
                if pygame.time.get_ticks()-self.kill_time>100:
                    self.kill()
        ## SHOOTING MECHANISM ##
        def shoot(self,enemies_fire_interval):
            ''' RANDOM TIMING OF ENEMY FIRE '''
            if enemies_fire_interval % self.identifier == 0:
                if self.rect.centery > 0:
                    gameResources.enemyBullet.play()
                if self.type == 'enemy3':
                    turret_pos = int((1/6)*self.rect.width)
                    bullet_1 = Bullet(self.rect.centerx+turret_pos,\
                                      self.rect.bottom,'player',\
                                      'enemy',self.b_size-1)
                    bullet_2 = Bullet(self.rect.centerx-turret_pos,\
                                      self.rect.bottom,'player',\
                                      'enemy',self.b_size-1)
                    enemyBullets.add(bullet_1,bullet_2)
                    all_sprites.add(bullet_1,bullet_2)
                else:
                    bullet = Bullet(self.rect.centerx,\
                                    self.rect.bottom,'player',\
                                    'enemy',self.b_size-1)
                    all_sprites.add(bullet)
                    enemyBullets.add(bullet)
            

    class Asteroid(pygame.sprite.Sprite):
        ## ASTEROID SPRITE ##
        def __init__(self,a_type,ySRange,xSRange,spawnRange):
            super().__init__()
            ''' RANDOMLY CREATE ASTEROID AND ITS PROPERTIES '''
            self.size = random.choice(['small','medium','large'])
            self.points = gameResources.asteroid\
                          ['t{}'.format(a_type)][self.size][1]
            self.image_ref = gameResources.asteroid\
                             ['t{}'.format(a_type)][self.size][0]
            self.image = self.image_ref.copy()
            ''' PHYSICAL PROPERTIES '''
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.centerx = random.randrange(50,width-50)
            self.rect.centery = random.randrange(spawnRange[0],spawnRange[1])
            ''' GAME PROPERTIES '''
            self.ySpeed = random.randrange(ySRange[0],ySRange[1])
            self.xSpeed = random.randrange(xSRange[0],xSRange[1])
            self.killed = False
            self.kill_time = 0
            self.actionCounter = 1
            ''' ROTATIONAL PROPERTIES '''
            self.r_angle = 0
            self.r_speed = random.randrange(-8,8)
            self.last_update = pygame.time.get_ticks()
        ## MOVEMENT ##
        def update(self):
            self.rect.x += self.xSpeed
            self.rect.y += self.ySpeed
            ''' BOUNDARIES '''
            if self.rect.top > height+20:
                global score,player
                ''' PENALTY IF OBJECT REACHES BOTTOM '''
                if player.levelStatus == 'not complete':
                    score -= self.points
                self.kill()
            if (self.rect.left <= 5 and \
                self.rect.left+self.xSpeed < 5) or \
               (self.rect.right >= width-5 and \
                self.rect.right+self.xSpeed > width-5):
                self.xSpeed *= -1
            ''' ROTATE '''
            self.rotate()
            ''' WHEN KILLED '''
            if self.killed:
                if self.actionCounter == 1:
                    self.kill_time = pygame.time.get_ticks()
                    self.xSpeed,self.ySpeed = 0,0
                    eSound = pygame.mixer.Sound(random.choice\
                                                (gameResources.explosionSound))
                    eSound.play()
                    self.actionCounter -= 1
                if pygame.time.get_ticks()-self.kill_time>100:
                    self.kill()
        ## ROTATIONAL MOVEMENT ##
        def rotate(self):
            ''' ROTATE AT AN INTERVAL '''
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update > 50:
                self.last_update = current_time
                self.r_angle = (self.r_angle + self.r_speed) % 360
                new_image = pygame.transform.rotate(self.image_ref,self.r_angle)
                old_center = self.rect.center
                self.image = new_image
                self.rect = self.image.get_rect()
                self.rect.center = old_center
                
    class Powerup(pygame.sprite.Sprite):
        ## POWERUP SPRITE ##
        def __init__(self,center,ySpeed):
            super().__init__()
            ''' RANDOMLY GENERATE PROPERTIES OF POWERUP '''
            self.type = random.choice(gameResources.powerup_type)
            self.image = gameResources.powerup[self.type]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.ySpeed = ySpeed
        ## MOVEMENT ##
        def update(self):
            self.rect.y += self.ySpeed
            ''' BOUNDARIES '''
            if self.rect.top > height+10:
                self.kill()

    class Background(pygame.sprite.Sprite):
        ## BACKGROUND ##
        def __init__(self,image,y):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.ySpeed = 3
            self.rect.x = 0
            self.rect.bottom = y
        def update(self):
            self.rect.y += self.ySpeed
            ''' RESET BACKGROUND POSITION AFTER DISAPPEARING '''
            if self.rect.top > height:
                self.rect.bottom = height-self.rect.height+1

    class AddScore(pygame.sprite.Sprite):
        ## FLOATING SCORE ADD INDICATOR ##
        def __init__(self,points,x,y):
            super().__init__()
            self.points = '+{}'.format(points)
            self.image = gameResources.textFont.render(self.points,True,white)
            self.rect = self.image.get_rect()
            self.ySpeed = -1
            self.rect.center = (x,y)
            self.visible_time = pygame.time.get_ticks()
        def update(self):
            ''' PRINT TO DASHBOARD '''
            self.rect.y += self.ySpeed
            textRender(self.points,\
                       gameResources.textFont,green,[width-200,height-37],True)
            if pygame.time.get_ticks()-self.visible_time > 450:
                self.kill()

    class Button(pygame.sprite.Sprite):
        ## BUTTON ##
        def __init__(self,message,color,coordinates):
            super().__init__()
            self.color = color
            self.message = message
            self.image = gameResources.letterFont.render(message,True,color)
            self.rect = self.image.get_rect()
            self.rect.center = coordinates
        def update(self):
            pass
        def switch(self):
            self.image = gameResources.letterFont.render\
                         (self.message,True,blue)
        def reset(self):
            self.image = gameResources.letterFont.render\
                         (self.message,True,self.color)

    class Arrow(pygame.sprite.Sprite):
        ## ARROW ##
        def __init__(self,direction,coordinates):
            super().__init__()
            if direction == 'left':
                self.image = gameResources.leftArrow
            elif direction == 'right':
                self.image = gameResources.rightArrow
            self.message = direction
            self.rect = self.image.get_rect()
            self.rect.center = coordinates
        def update(self):
            pass
        def switch(self):
            if self.message == 'left':
                self.image = gameResources.leftArrow_hover
            if self.message == 'right':
                self.image = gameResources.rightArrow_hover
        def reset(self):
            if self.message == 'left':
                self.image = gameResources.leftArrow
            if self.message == 'right':
                self.image = gameResources.rightArrow 

                
    ''' FUNCTIONS '''
    def textRender(text,font,color,coordinates,antialias):
        ## UNIFIED TEXT RENDERER / screen BLIT ##
        txt2bmp = font.render(text,antialias,color)
        txtRect = txt2bmp.get_rect()
        ''' SIMPLIFIED ALIGNMENT METHOD '''
        xAlignKey = ['center','right','left']
        xAlignList = [(width-txtRect.width)//2,\
                      width-5-txtRect.width,\
                      5]
        yAlignKey = ['middle','top','bottom']
        yAlignList = [(height-txtRect.height)//2,\
                      5,\
                      height-5-txtRect.height]
        ''' REPLACE KEYWORD WITH CALCULATED COORDINATE '''
        if coordinates[0] in xAlignKey:
            coordinates[0] = xAlignList[xAlignKey.index(coordinates[0])]
        if coordinates[1] in yAlignKey:
            coordinates[1] = yAlignList[yAlignKey.index(coordinates[1])]       
        return screen.blit(txt2bmp,coordinates)

    def drawHealth(surface,x,y,health):
        ## HEALTH BAR ##
        textRender('HEALTH',\
                       gameResources.textFont,grey,[107,height-27],True)
        if health < 0:
            health = 0
            return
        if health < 20:
            segmentImage = gameResources.bar['red']
            textRender('CRITICAL',\
                       gameResources.warnFont,red,[107,height-17],True)
        else:
            segmentImage = gameResources.bar['green']
        barLength = int(health*0.87)
        barHeight = 18
        midSegmentNum = barLength-10
        if midSegmentNum < 0:
                midSegmentNum = 0
        surface.blit(segmentImage[0],[x,y])
        for segment in range(midSegmentNum):
            surface.blit(segmentImage[1],[x+segment+5,y])
        surface.blit(segmentImage[2],[x+midSegmentNum+5,y])

    def drawPower(surface,x,y,time):
        ## POWER TIMER BAR ##
        colorList = {'fire':red,'speed':blue}
        if player.power_type != 'none':
            textRender(player.power_type,\
                   gameResources.textFont,colorList[player.power_type],\
                       [107,height-50],True)
            segmentImage = gameResources.bar['blue']
            timeLeft = (10000-pygame.time.get_ticks()+player.power_time)//100
            textRender(str((10000-pygame.time.get_ticks()+\
                            player.power_time)//1000),\
                       gameResources.textFont,\
                       colorList[player.power_type],[110,height-41],True)
            barLength = int(timeLeft*0.87)
            barHeight = 18
            midSegmentNum = barLength-10
            if midSegmentNum < 0:
                midSegmentNum = 0
            surface.blit(segmentImage[0],[x,y])
            for segment in range(midSegmentNum):
                surface.blit(segmentImage[1],[x+segment+5,y])
            surface.blit(segmentImage[2],[x+midSegmentNum+5,y])

    def drawLives(surface,x,y,lives,image):
        ## LIVES INDICATOR ##
        for i in range(lives):
            imageRect = image.get_rect()
            imageRect.x = x + 22 * i
            imageRect.y = y
            surface.blit(image, imageRect)
            
    def drawSlot(surface,x,y,image):
        ## LIVES SLOT ##
        for i in range(6):
            imageRect = image.get_rect()
            imageRect.x = x - 22 * i
            imageRect.y = y
            surface.blit(image, imageRect)

    def generateMob(sprite,spriteGroup):
        ## GENERATE ENEMIES / ASTEROIDS ##
        m = sprite
        spriteGroup.add(m)
        all_sprites.add(m)

    def confirm(message):
        ## CONFIRM SCREEN ##
        ''' BUTTON SPRITES '''
        button_group = pygame.sprite.Group()
        button1 = Button('yes',white,(width//2-50,440))
        screen.blit(gameResources.confirm_button,[width//2-90,420])
        button2 = Button('no',white,(width//2+50,440))
        screen.blit(gameResources.confirm_button,[width//2+10,420])
        button_group.add(button1,button2)
        ''' DRAW TEXT ONE TIME ONLY '''
        screen.blit(gameResources.confirm_bg,[width//2-155,300])
        textRender('are you sure',gameResources.letterFont,\
                   white,['center',330],True)
        textRender(message,gameResources.letterFont,\
                   white,['center',360],True)
        button_group.draw(screen)
        ''' MAIN LOOP '''
        confirm = True
        while confirm:
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return 'yes'
                for button in button_group.sprites():
                    if button.rect.collidepoint(mouse_pos):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            action = button.message
                            confirm = False
                        else:
                            button.switch()
                    else:
                        button.reset()
            button_group.update()
            button_group.draw(screen)
            pygame.display.flip()
            clock.tick(fps)
        button1.kill()
        button2.kill()
        return action



    ### GAME FUNCTIONS / LOOPS ###
    def gameTitleScreen(name,score):
        ## TITLE SCREEN ##
        ''' DRAW ON SCREEN '''
        all_sprites = pygame.sprite.Group()
        buttons = pygame.sprite.Group()
        currentBackground = random.choice(gameResources.background)
        bg_1 = Background(currentBackground,height+1)
        bg_2 = Background(currentBackground,height+1-bg_1.rect.height)
        all_sprites.add(bg_1,bg_2)
        play = Button('play',white,[300,460])
        how2Play = Button('how to play',white,[300,530])
        dispCreds = Button('credits',white,[300,560])
        l_arrow = Arrow('left',[215,390])
        r_arrow = Arrow('right',[width-215,390])
        buttons.add(play,how2Play,dispCreds,l_arrow,r_arrow)
        ''' SELECTION '''
        shipIndex = 0
        ''' MAIN LOOP '''
        screenRunning = True
        while screenRunning:
            ''' DRAW BOARD '''
            screen.fill(black)
            all_sprites.update()
            all_sprites.draw(screen)
            buttons.update()
            buttons.draw(screen)
            screen.blit(playerList[shipIndex],[268,340])
            ''' TEXT TO DISPLAY '''
            screen.blit(gameResources.titleImage,[30,50])
            textRender('hunt big. explore bigger.',\
                       gameResources.letterFont,white,['center',170],True)
            textRender('highscore: {} - {}'.format(name,score),\
                       gameResources.letterFont,red,['center',220],True)
            textRender('choose your ship:',\
                       gameResources.letterFont,white,['center',300],True)
            ''' KEYBOARD CONTROLS '''
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    return 'quit'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 'quit'
                    if event.key == pygame.K_RIGHT:
                        if shipIndex+1 > len(playerList)-1:
                            shipIndex = 0
                        else:
                            shipIndex += 1
                    if event.key == pygame.K_LEFT:
                        shipIndex -= 1
                        if shipIndex < 0:
                            shipIndex = len(playerList)-1
                                                   
                for button in buttons.sprites():
                    if button.rect.collidepoint(mouse_pos):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if button.message == 'right':
                                if shipIndex+1 > len(playerList)-1:
                                    shipIndex = 0
                                else:
                                    shipIndex += 1
                            elif button.message == 'left':
                                shipIndex -= 1
                                if shipIndex < 0:
                                    shipIndex = len(playerList)-1
                            else:
                                action = button.message
                                screenRunning = False
                        else:
                            button.switch()
                    else:
                        button.reset()
            pygame.display.flip()
            clock.tick(fps)
        return action,shipIndex
            
    def gameScreen(level,lives,startingScore,\
                   ship_pref,color_pref,icon_pref,icon_shadow):
        ## MAIN GAMEPLAY SCREEN / UNIVERSAL LEVEL SYSTEM ##
        ''' LEVEL SETUP '''
        global score
        score = startingScore
        enemiesLeft = 10+level
        ySpeed = gameLevels.levels['level_{}'.format(level)]\
                 ['ySpeed']
        xSpeed = gameLevels.levels['level_{}'.format(level)]\
                 ['xSpeed']
        intervalRange = gameLevels.levels['level_{}'.format(level)]\
                        ['intervalRange']
        enemyID = gameLevels.levels['level_{}'.format(level)]\
                  ['enemyID']
        spawnRange = gameLevels.levels['level_{}'.format(level)]\
                     ['spawnRange']
        playerRange = gameLevels.levels['level_{}'.format(level)]\
                      ['playerRange']
        powerChance = gameLevels.levels['level_{}'.format(level)]\
                      ['powerChance']
        playerShootFreq = 400
        nextLevelDelay = 0
        a_theme = random.randint(1,12)
        ''' SPRITE GROUPS '''
        global all_sprites,playerBullets,enemyBullets
        backgrounds = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        playerBullets = pygame.sprite.Group()
        enemyBullets = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        messages = pygame.sprite.Group()
        ''' LOAD SCROLLING BACKGROUNDS '''
        currentBackground = random.choice(gameResources.background)
        bg_1 = Background(currentBackground,height+1)
        bg_2 = Background(currentBackground,height+1-bg_1.rect.height)
        backgrounds.add(bg_1,bg_2)
        ''' LOAD PLAYER '''
        global player
        player = Player(ship_pref,color_pref,lives,playerShootFreq)
        all_sprites.add(player)
        ''' LOAD ENEMIES AND ASTEROIDS '''
        for i in range(enemiesLeft):
            generateMob(Enemy(ySpeed,xSpeed,spawnRange,playerRange,enemyID),\
                        enemies)
            generateMob(Asteroid(a_theme,ySpeed,xSpeed,spawnRange),asteroids)
        ''' SET ENEMY FIRE INTERVAL '''
        enemies_fire_interval = random.randint(intervalRange[0],\
                                               intervalRange[1])
        pygame.time.set_timer(enemies_fire_event, enemies_fire_interval)
        ''' MAIN LOOP '''
        global beginning
        levelOver = False
        beginning = True
        changeNum = pygame.time.get_ticks()
        counter = 3
        gameRunning = True
        gameResources.nextLevel.play()
        pygame.mixer.music.load(random.choice(gameResources.gameMusicList))
        while gameRunning:
            if not beginning:
                ### KEYBOARD CONTROLS ###
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        player.levelStatus = 'quit'
                        gameRunning = False
                    if event.type == enemies_fire_event:
                        for enemy in enemies.sprites():
                            enemy.shoot(enemies_fire_interval)
                            enemies_fire_interval = random.randint\
                                                    (intervalRange[0],\
                                                     intervalRange[1])
                            pygame.time.set_timer(enemies_fire_event,\
                                                  enemies_fire_interval)
                    if event.type == pygame.KEYDOWN:
                        cheats = pygame.key.get_pressed()
                        ''' PAUSE '''
                        if event.key == pygame.K_p:
                            gamePaused = pauseScreen()
                            if gamePaused == 'continue':
                                pygame.mixer.music.unpause()
                                continue
                            elif gamePaused == 'quit':
                                player.levelStatus = 'quit'
                                gameRunning = False
                            elif gamePaused == 'restart':
                                player.levelStatus = 'restart'
                                gameRunning = False
                        ''' CHEAT CODES '''
                        if cheats[K_9] and cheats[K_r] and level < 99:
                            return ['99',player.lives,score]
                        elif cheats[K_0] and cheats[K_r] and level < 99:
                            return ['00',player.lives,score]
                        ''' RESET ENEMY FIRE INTERVAL '''
                        enemies_fire_interval = random.randint\
                                                (intervalRange[0],\
                                                 intervalRange[1])
                        pygame.time.set_timer(enemies_fire_event,\
                                              enemies_fire_interval)   
                ### COLLISIONS ###
                all_sprites.update()
                for enemy in enemies.sprites():
                    if enemy.rect.x > height:
                        generateMob(Enemy(ySpeed,xSpeed,spawnRange,\
                                          playerRange,enemyID),enemies)
                for asteroid in asteroids.sprites():
                    if asteroid.rect.x > height:
                        generateMob(Asteroid(a_theme,ySpeed,xSpeed,\
                                             spawnRange),asteroids)
                ''' PLAYER BULLET AND ENEMY COLLISIONS '''
                bullet2enemy = dict.items(pygame.sprite.groupcollide\
                                          (enemies,playerBullets, False, False))
                for hitList in bullet2enemy:
                    ## COLLISION ACCURACY USING MASKS / MARK EXPLOSION ##
                    if pygame.sprite.collide_mask(hitList[0],hitList[1][0]):
                        if hitList[0].type == 'enemy3':
                            expl = Explosion(hitList[0].rect.center,'1_1')
                        else:
                            expl = Explosion(hitList[0].rect.center,'2_1')
                        all_sprites.add(expl)
                        ## DISPLAY POINTS ADDED ##
                        pointScored = AddScore(hitList[0].points,\
                                               hitList[0].rect.centerx,\
                                               hitList[0].rect.top)
                        all_sprites.add(pointScored)
                        messages.add(pointScored)
                        ## DESTROY ENEMY AND GENERATE NEW ##
                        for bulletHit in hitList[1]:
                            bulletHit.kill()
                        score += hitList[0].points
                        enemiesLeft -= 1
                        hitList[0].killed = True
                        if enemiesLeft > 0:
                            generateMob(Enemy(ySpeed,xSpeed,spawnRange,\
                                              playerRange,enemyID),enemies)
                ''' PLAYER BULLET AND ASTEROID COLLISIONS '''          
                bullet2asteroid = dict.items(pygame.sprite.groupcollide\
                                             (asteroids, playerBullets,\
                                              False,False))
                for hitList in bullet2asteroid:
                    ## MARK EXPLOSION AND POWERUP ##
                    if pygame.sprite.collide_mask(hitList[0],hitList[1][0]):
                        if hitList[0].size == 'large':
                            expl = Explosion(hitList[0].rect.center,'1_1')
                            if random.random() > powerChance:
                                powr = Powerup(hitList[0].rect.center,2)
                                powerups.add(powr)
                                all_sprites.add(powr)
                        else:
                            expl = Explosion(hitList[0].rect.center,'2_1')
                        all_sprites.add(expl)
                        ## DISPLAY POINTS ADDED ##
                        pointScored = AddScore(hitList[0].points,\
                                               hitList[0].rect.centerx,\
                                               hitList[0].rect.top)
                        all_sprites.add(pointScored)
                        messages.add(pointScored)
                        ## DESTROY ASTEROID AND GENERATE NEW ##
                        for bulletHit in hitList[1]:
                            bulletHit.kill()
                        score += hitList[0].points
                        hitList[0].killed = True
                        generateMob(Asteroid\
                                    (a_theme,ySpeed,xSpeed,spawnRange),\
                                    asteroids)
                ''' PLAYER SPECIFIC COLLISIONS'''
                if player.levelStatus == 'not complete':        
                    if not player.killed:
                        ''' ENEMY BULLET AND PLAYER COLLISIONS '''
                        bullet2player = pygame.sprite.spritecollide\
                                        (player,enemyBullets, False)
                        for hitList in bullet2player:
                            ## MARK EXPLOSION ##
                            if pygame.sprite.collide_mask(player,hitList):
                                expl = Explosion(hitList.rect.center,'2_2')
                                all_sprites.add(expl)
                                hitList.kill()
                                ## PENALTY TO HEALTH ##
                                player.health -= 10
                        ''' PLAYER AND ASTEROID COLLISIONS '''
                        player2asteroid = pygame.sprite.spritecollide\
                                          (player,asteroids,False)
                        for hitList in player2asteroid:
                            ## MARK EXPLOSION ##
                            if pygame.sprite.collide_mask(player,hitList):
                                expl = Explosion(hitList.rect.center,'2_2')
                                all_sprites.add(expl)
                                hitList.kill()
                                ## PENALTY TO HEALTH / GENERATE NEW ASTEROID ##
                                player.health -= 25
                                generateMob(Asteroid\
                                            (a_theme,ySpeed,xSpeed,spawnRange),\
                                            asteroids)
                        ''' ENEMY AND PLAYER COLLISIONS '''
                        enemy2player = pygame.sprite.spritecollide\
                                       (player,enemies,False)
                        for hitList in enemy2player:
                            ## MARK EXPLOSION ##
                            if pygame.sprite.collide_mask(player,hitList):
                                expl = Explosion(hitList.rect.center,'1_2')
                                all_sprites.add(expl)
                                hitList.kill()
                                ## PENALTY TO HEALTH / GENERATE NEW ENEMY ##
                                player.health -= 25
                                enemiesLeft -= 1
                                generateMob(Enemy\
                                            (ySpeed,xSpeed,spawnRange,\
                                             playerRange,enemyID),enemies)
                        ''' PLAYER AND POWERUP COLLISIONS '''
                        player2power = pygame.sprite.spritecollide\
                                       (player,powerups,False)  
                        for hitList in player2power:
                            ## TRIGGER POWERUP METHOD ##
                            if pygame.sprite.collide_mask(player,hitList):
                                gameResources.powerupSound.play()
                                player.powerup(hitList.type,playerShootFreq)
                                hitList.kill()                          
                ### GAME SPECIFIC CONDITIONS ###
                if score < 0:
                    score = 0
                ''' PLAYER HEALTH IS ZERO '''
                if player.health <= 0:
                    expl = Explosion(player.rect.center,'1_2')
                    all_sprites.add(expl)
                    player.killed = True
                    player.lives -= 1
                    player.health = 100
                ''' PLAYER LIVES IS ZERO '''
                if player.lives == 0 and not levelOver:
                    pygame.mixer.music.pause()
                    nextLevelDelay = pygame.time.get_ticks()
                    player.levelStatus = 'end'
                    levelOver = True
                ''' NO MORE ENEMIES '''
                if enemiesLeft <= 0 and not levelOver:
                    pygame.mixer.music.pause()
                    nextLevelDelay = pygame.time.get_ticks()
                    player.levelStatus = 'next'
                    levelOver = True
                if enemiesLeft <= 0:
                    enemiesLeft = 0
                ''' ONCE LEVEL IS FINISHED / RETURN WITH STATUS '''
                if pygame.time.get_ticks()-nextLevelDelay>4000 and \
                   (enemiesLeft == 0 or player.lives == 0):
                    return [player.levelStatus,player.lives,score]
            ### DRAW ELEMENTS ###
            screen.fill(white)
            backgrounds.update()
            backgrounds.draw(screen)
            all_sprites.draw(screen)
            ''' DRAW DASHBOARD '''
            screen.blit(gameResources.dashboard[color_pref],(100,height-85))
            drawSlot(screen,width-135,height-81,icon_shadow)
            drawLives(screen,width-244,height-80,player.lives,icon_pref)
            drawHealth(screen,158,height-26,player.health)
            drawPower(screen,158,height-51,player.power_time)
            textRender('ENEMIES LEFT',\
                       gameResources.textFont,grey,[width-240,height-52],True)
            textRender(str(enemiesLeft).rjust(3,'0'),\
                       gameResources.numberFont,\
                       white,[width-150,height-50],True)
            textRender('SCORE',\
                       gameResources.textFont,grey,[width-240,height-37],True)
            textRender(str(score).rjust(13,'0'),\
                       gameResources.numberFont,\
                       white,[width-240,height-25],True)
            textRender('LEVEL',\
                       gameResources.textFont,white,['center',height-70],True)
            textRender(str(level).rjust(3,'0'),\
                       gameResources.levelFont,white,['center',height-47],True)
            ''' HUD MESSAGES '''
            if player.levelStatus == 'next':
                textRender('LEVEL COMPLETED',\
                           gameResources.headingFont,\
                           white,['center','middle'],True)
            elif player.levelStatus == 'end':
                textRender('SHIP DESTROYED',\
                           gameResources.headingFont,\
                           white,['center','middle'],True)
            messages.update()
            ### COUNTDOWN INITIATE (ONE TIME ONLY) ###
            if beginning:
                counter,changeNum = countdown(counter,changeNum,level)
            pygame.display.flip()
            clock.tick(fps)
        return [player.levelStatus,player.lives,score]
            
    def countdown(counter,changeNum,level):
        ## COUNTDOWN SCREEN ##
        if counter != 0:
            textRender('Level {}'.format(level),gameResources.headingFont,\
                       white,['center',320],True)
            textRender('Get Ready!',gameResources.letterFont,\
                       white,['center','middle'],True)
            ''' MAIN LOOP '''
            textRender('{}'.format(counter),gameResources.headingFont,\
                       white,['center',430],True)
        ''' CHANGE NUMBER '''
        if pygame.time.get_ticks()-changeNum > 1000:
            if counter-1 != 0:
                gameResources.count.play()
            changeNumNew = pygame.time.get_ticks()
            counterNew = counter - 1
            return counterNew,changeNumNew
        if counter <= 0:
            global beginning
            beginning = False
            gameResources.countend.play()
            pygame.mixer.music.play(-1)
            return 0,0
        return counter,changeNum

    def pauseScreen():
        ## PAUSE SCREEN ##
        ''' BUTTON SPRITES '''
        button_group = pygame.sprite.Group()
        continueButton = Button('continue',white,(width-80,height-300))
        restartButton = Button('restart',white,(width//2,height-300))
        quitButton = Button('quit',white,(80,height-300))
        button_group.add(continueButton,restartButton,quitButton)
        pygame.image.save(screen, 'pauseShot.png')
        bg = pygame.image.load('pauseShot.png')
        ''' MAIN LOOP '''
        pause = True
        pygame.mixer.music.pause()
        while pause:
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        screen.blit(bg,[0,0])
                        confirmTrue = confirm\
                                      ('you want to continue?')
                        if confirmTrue == 'yes':
                            return 'continue'
                    if event.key == pygame.K_r:
                        screen.blit(bg,[0,0])
                        confirmTrue = confirm\
                                      ('you want to restart?')
                        if confirmTrue == 'yes':
                            return 'restart'
                    if event.key == pygame.K_ESCAPE:
                        screen.blit(bg,[0,0])
                        confirmTrue = confirm\
                                      ('you want to quit?')
                        if confirmTrue == 'yes':
                            return 'quit'
                for button in button_group.sprites():
                    if button.rect.collidepoint(mouse_pos):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            screen.blit(bg,[0,0])
                            confirmTrue = confirm\
                                          ('you want to {}?'.format\
                                           (button.message))
                            if confirmTrue == 'yes':
                                action = button.message
                                return action
                            else:
                                continue
                        else:
                            button.switch()
                    else:
                        button.reset()
            ''' DRAW TEXT ONE TIME ONLY '''
            screen.blit(bg,[0,0])
            textRender('TIME FREEZE!',gameResources.headingFont,\
                       white,['center',300],True)
            textRender('GAME PAUSED',gameResources.letterFont,\
                       white,['center',350],True)
            button_group.update()
            button_group.draw(screen)
            pygame.display.flip()
            clock.tick(fps)
        
    def gameOverScreen(score,highScores,highScoreNames):
        ## GAME OVER SCREEN ##
        newScore = None
        ''' CHECK IF HIGH SCORE '''
        for topScore in highScores:
            if score > topScore:
                place = highScores.index(topScore)
                highScores.insert(place,score)
                highScoreNames.insert(place,' ')
                newScore,keyboardActive = True,True
                name = ""
                break
        if len(highScores) < 10 and newScore == None:
            place = len(highScores)
            highScores.append(score)
            highScoreNames.insert(place,' ')
            newScore,keyboardActive = True,True
            name = ""
        elif newScore == None:
            newScore,keyboardActive = False,False
            place = 11
        if len(highScores) > 10:
            highScores.pop()
            highScoreNames.pop()
        if score == 0:
            newScore,keyboardActive = False,False
        ''' DRAW ON SCREEN (ONE TIME) '''
        all_sprites = pygame.sprite.Group()
        button_sprites = pygame.sprite.Group()
        currentBackground = random.choice(gameResources.background)
        bg_1 = Background(currentBackground,height+1)
        bg_2 = Background(currentBackground,height+1-bg_1.rect.height)
        all_sprites.add(bg_1,bg_2)
        ''' FILL EMPTY SPOTS '''
        if len(highScores) < 10:
            for line in range(10,len(highScores),-1):
                textRender(' '.rjust(14,'0'),\
                           gameResources.topScoreFont,\
                           white,[width//2+112,150+35*(line-1)],True)
                textRender("{}. ".format(line),\
                           gameResources.letterFont,\
                           grey,[50,150+35*(line-1)],True)
        ''' MAIN LOOP '''
        screenRunning = True
        gameResources.gameover.play()
        pygame.mixer.music.load(gameResources.endMusic)
        pygame.mixer.music.play(-1)
        while screenRunning:
            ''' DRAW BOARD '''
            all_sprites.update()
            all_sprites.draw(screen)
            button_sprites.update()
            button_sprites.draw(screen)
            screen.blit(gameResources.scoreBoard,[19,104])
            ''' TEXT TO DISPLAY '''
            textRender('game over',\
               gameResources.headingFont,white,['center',23],True)
            if newScore:
                textRender('you earned a new record!',\
                           gameResources.letterFont,white,['center',73],True)            
            textRender('high scores',\
                       gameResources.textFont,\
                       white,[screen.get_rect().centerx-220,113],True)
            textRender('final score',\
                       gameResources.letterFont,\
                       white,['center',height-250],True)
            textRender(str(score),\
                       gameResources.headingFont,\
                       white,['center',height-200],True)
            if not keyboardActive:
                restartButton = Button('restart',white,(100,height-100))
                quitButton = Button('quit',white,(width-80,height-100))
                button_sprites.add(restartButton,quitButton)
            ''' SCOREBOARD '''
            for line in range(len(highScores)):
                textRender(str(highScores[line]).rjust(13,'0'),\
                           gameResources.topScoreFont,\
                           white,[width//2+112,150+35*line],True)
                textRender('{}.'.format(line+1),\
                           gameResources.letterFont,grey,[50,150+35*line],True)
                if line != place:
                    textRender(highScoreNames[line],\
                               gameResources.letterFont,\
                               grey,[90,150+35*line],True)
                else:
                    textRender(highScoreNames[line],\
                               gameResources.letterFont,\
                               yellow,[90,150+35*line],True)
                    if keyboardActive:
                        screen.blit(gameResources.scoreName,\
                                    [screen.get_rect().centerx-220,\
                                     150+35*line-3])
                        block = gameResources.letterFont.render\
                                (name,True,yellow)
                        rect = block.get_rect()
                        rect.x = screen.get_rect().centerx-210
                        rect.y = 150+35*line
                        screen.blit(block, rect)
            ''' KEYBOARD CONTROLS '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if newScore and keyboardActive:
                    if event.type == pygame.KEYDOWN:
                        if (event.unicode.isalpha() or event.unicode.isdigit()) and len(name) < 14:
                            name += event.unicode
                        elif event.key == K_BACKSPACE:
                            name = name[:-1]
                        elif event.key == K_RETURN:
                            highScoreNames[place] = name
                            keyboardActive = False
                            record = open("highScores.txt","w",newline='\n')
                            for line in range(len(highScores)):
                                record.write(highScoreNames[line]+\
                                             '-'+str(highScores[line])+'\n')
                            record.close()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        confirmTrue = confirm\
                                      ('you want to restart?')
                        if confirmTrue == 'yes':
                            return 'restart'
                    if event.key == pygame.K_ESCAPE:
                        confirmTrue = confirm\
                                      ('you want to quit?')
                        if confirmTrue == 'yes':
                            return 'quit'
                if not keyboardActive:
                    for button in button_sprites.sprites():
                        mouse_pos = pygame.mouse.get_pos()
                        if button.rect.collidepoint(mouse_pos):
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pygame.image.save(screen, 'pauseShot.png')
                                bg = pygame.image.load('pauseShot.png')
                                screen.blit(bg,[0,0])
                                confirmTrue = confirm\
                                              ('you want to {}?'.format\
                                               (button.message))
                                if confirmTrue == 'yes':
                                    action = button.message
                                    screenRunning = False
                                else:
                                    continue
                            else:
                                button.switch()
                        else:
                            button.reset()
                            
            pygame.display.flip()
            clock.tick(fps)
        return action

    def gameHowTo():
        pageIndex = 0
        screen.fill(black)
        screen.blit(gameResources.howto[pageIndex],[0,0])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN or \
                   event.type == pygame.MOUSEBUTTONDOWN:
                    if pageIndex+1 > 2:
                        return 'back'
                    else:
                        pageIndex += 1
                        screen.blit(gameResources.howto[pageIndex],[0,0])
            pygame.display.flip()
            clock.tick(fps)

    def gameCredits():
        screen.fill(black)
        screen.blit(gameResources.gameCredits,[0,0])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN or \
                   event.type == pygame.MOUSEBUTTONDOWN:
                    return 'back'
            pygame.display.flip()
            clock.tick(fps)
                    
    ### GAME STRUCTURE ###
    ''' LOAD HIGHSCORES FROM FILE '''
    highScores = []
    highScoreNames = []
    file2read = open("highScores.txt","r")
    scores = file2read.readlines()
    for line in scores:
        indiv = line.split('-')
        highScoreNames.append(indiv[0])
        highScores.append(int(indiv[1]))
    if highScores:
        topScorer = highScoreNames[0]
        topScore = highScores[0]
    else:
        topScorer = ''
        topScore = ''
    ''' LOAD PLAYER CHOICES '''
    playerList = []
    typeList = list(gameResources.player.keys())
    for s_type in typeList:
        for color in ['blue','green','red']:
            playerList.append(gameResources.player[s_type][color][0])
    ''' INITIALIZE MAIN MENU '''
    menuRunning = True
    pygame.mixer.music.load(gameResources.titleMusic)
    pygame.mixer.music.play(-1)
    while menuRunning:
        playerChoice = gameTitleScreen(topScorer,topScore)
        if playerChoice == 'quit':
            menuRunning = False
            programRunning = False
            continue
        elif playerChoice == 'back':
            continue
        if playerChoice[0] == 'how to play':
            playerChoice = gameHowTo()
        if playerChoice[0] == 'credits':
            playerChoice = gameCredits()
        if playerChoice[0] == 'play':
            programRunning = True
            menuRunning = False
    ''' INITIALIZE GAME PREFS AND LEVELS'''
    if programRunning:
        ship_pref = playerList[playerChoice[1]]
        for s_type in typeList:
            for color in ['blue','green','red']:
                if gameResources.player[s_type][color][0] == ship_pref:
                    type_pref = s_type
                    color_pref = color
        icon_pref = gameResources.player[type_pref][color_pref][1]
        icon_shadow = gameResources.player[type_pref]['shadow']
        dash_color = gameResources.dashboard[color_pref]
        playerLevel = 1
        playerLives = 3
        playerScore = 0
        programRunning = True
        ''' GAME LOOP '''
        while programRunning:
            levelResults = gameScreen(playerLevel,playerLives,playerScore,\
                                      ship_pref,color_pref,icon_pref,icon_shadow)
            if levelResults[0] == '99':
                playerLevel = 99
                playerLives = 6
                playerScore = levelResults[2]
                continue
            if levelResults[0] == '00':
                playerLevel = 100
                playerLives = 6
                playerScore = levelResults[2]
                continue
            if levelResults[0] == 'next':
                playerLevel += 1
                playerLives = levelResults[1]+1
                if playerLives > 6:
                    playerLives = 6
                playerScore = levelResults[2]
            elif levelResults[0] == 'end' or (levelResults[0] == 'next' and \
                                              playerLevel == 100):
                playerScore = levelResults[2]
                playerChoice = gameOverScreen(playerScore,highScores,highScoreNames)
                if playerChoice == 'restart':
                    playerLevel = 1
                    playerLives = 3
                    playerScore = 0
                    continue
                elif playerChoice == 'quit':
                    programRunning = False
            elif levelResults[0] == 'restart':
                playerLevel = 1
                playerLives = 3
                playerScore = 0
                continue
            elif levelResults[0] == 'quit':
                programRunning = False

mainProgram()

pygame.quit()
