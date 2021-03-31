## PROJECT HALIOTH
## GAME RESOURCE DATABASE (IMAGES,MUSIC,FONTS)

import pygame
import random
from os import path
pygame.init()

### IMAGE DIRECTORY ###
image_dir = path.join(path.dirname(__file__), 'images')

## UI ##
ui_dir = path.join(image_dir,'UI')

dashboard_dir = path.join(ui_dir,'dashboard')
dashboard = {}
dashColor = ['blue','green','red']
for color in dashColor:
    filename = 'd_{}'.format(color)+'.png'
    image2import = path.join(dashboard_dir,filename)
    dashboard[color] = pygame.image.load(image2import)

scoreBoard = pygame.image.load(path.join(ui_dir,'scoreBoard.png'))
scoreName = pygame.image.load(path.join(ui_dir,'scoreName.png'))
titleImage = pygame.image.load(path.join(ui_dir,'title.png'))

howto = []
for page in range(3):
    filename = 'how_'+str(page+1)+'.png'
    image2import = path.join(ui_dir,filename)
    howto.append(pygame.image.load(image2import))

gameCredits = pygame.image.load(path.join(ui_dir,'credits.png'))

leftArrow = pygame.image.load(path.join(ui_dir,'leftarrow.png'))
leftArrow_hover = pygame.image.load(path.join(ui_dir,'leftarrow_hover.png'))
rightArrow = pygame.image.load(path.join(ui_dir,'rightarrow.png'))
rightArrow_hover = pygame.image.load(path.join(ui_dir,'rightarrow_hover.png'))

bar_dir = path.join(ui_dir,'bar')
bar = {}
barColor = ['blue','green','red']
for barSet in barColor:
    bar[barSet] = []
    for segment in range(3):
        filename = str(barSet+'_{}'.format(segment+1)+'.png')
        image2import = path.join(bar_dir,filename)
        bar[barSet].append(pygame.image.load(image2import))
    
confirm_bg = pygame.image.load(path.join(ui_dir,'confirm_bg.png'))
confirm_button = pygame.image.load(path.join(ui_dir,'confirm_button.png'))

## PLAYER SHIP / LIVES ICON ##
ships_dir = path.join(image_dir,'ships')
icon_dir = path.join(image_dir,'live_icons')

player = {'ship1':{},'ship2':{}}
player_color = ['blue','green','red']
player_type = list(player.keys())

for ship in player_type:
    typeNumber = str(player_type.index(ship)+1)
    filename = typeNumber+'_shadow.png'
    image2import = path.join(icon_dir,filename)
    player[ship]['shadow'] = pygame.image.load(image2import)
    for color in player_color:
        colorNumber = str(player_color.index(color)+1)
        
        filename = typeNumber+'_'+colorNumber+'.png'
        image2import = path.join(ships_dir,filename)
        player[ship][color] = [pygame.image.load(image2import)]
        
        filename = typeNumber+'_'+colorNumber+'_small.png'
        image2import = path.join(icon_dir,filename)
        player[ship][color].append(pygame.image.load(image2import))

## ENEMIES ##
enemy_dir = path.join(image_dir,'enemies')
enemy = {'enemy1':[],'enemy2':[],'enemy3':[]}
enemy_type = list(enemy.keys())

for ship in enemy_type:
    typeNumber = str(enemy_type.index(ship)+1)
    filename = 'enemy_'+typeNumber+'.png'
    image2import = path.join(enemy_dir,filename)
    enemy[ship].append(pygame.image.load(image2import))
    if ship == 'enemy3':
        enemy[ship].extend((2,200))
    else:
        enemy[ship].extend((1,100))

## ASTEROIDS ##
asteroid_dir = path.join(image_dir,'asteroids')
asteroid = {}
asteroid_size = ['large','medium','small']

for a_type in range(12):
    theme = 't{}'.format(a_type+1)
    asteroid[theme] = {}
    for size in range(3):
        filename = str(a_type+1)+'_'+str(size+1)+'.png'
        image2import = path.join(asteroid_dir,filename)
        asteroid[theme][asteroid_size[size]]=[pygame.image.load(image2import),\
                                              10*(3-size)]

## BACKGROUNDS ##
background_dir = path.join(image_dir,'backgrounds')
background = []

for bg in range(1,7):
    filename = 'bg_'+str(bg)+'.png'
    image2import = path.join(background_dir,filename)
    background.append(pygame.image.load(image2import))
    
background_pref = random.choice(background)

## EXPLOSIONS ##
explosion_dir = path.join(image_dir,'explosions')
explosion_anim = {}
explosion_anim['1_1'],explosion_anim['1_2'] = [],[]
explosion_anim['2_1'],explosion_anim['2_2'] = [],[]

for size in range(1,3):
    for var in range(1,3):
        s_dir = path.join(explosion_dir,('exp_'+str(size)+'_'+str(var)))
        c_entry = str(size)+'_'+str(var)
        for frame in range(1,15):
            filename = 'frame_'+str(frame)+'.png'
            image2import = path.join(s_dir,filename)
            explosion_anim[c_entry].append(pygame.image.load(image2import))

## BULLETS ##
bullet_dir = path.join(image_dir,'bullets')
bullet = {}
bullet_color = ['blue','green','red','enemy']

for color in bullet_color:
    bullet[color] = []
    for size in range(2):
        colorNumber = str(bullet_color.index(color)+1)
        filename = 'b_'+colorNumber+'_'+str(size+1)+'.png'
        image2import = path.join(bullet_dir,filename)
        bullet[color].append(pygame.image.load(image2import))

## POWERUP ##
powerup_dir = path.join(image_dir,'powerups')
powerup = {}
powerup_type = ['fire','speed','life']

for item in powerup_type:
    typeNumber = str(powerup_type.index(item)+1)
    filename = 'power_'+typeNumber+'.png'
    image2import = path.join(powerup_dir,filename)
    powerup[item] = pygame.image.load(image2import)


### FONT DATABASE ###
pygame.font.init()
font_dir = path.join(path.dirname(__file__), 'fonts')
headingFont = pygame.font.Font\
              (path.join(font_dir,'kenvector_future_thin.ttf'),50)
textFont = pygame.font.Font(path.join(font_dir,'kenvector_future.ttf'),9)
warnFont = pygame.font.Font(path.join(font_dir,'kenvector_future.ttf'),8)
numberFont = pygame.font.Font(path.join(font_dir,'digital7mono.ttf'),19)
topScoreFont = pygame.font.Font(path.join(font_dir,'digital7mono.ttf'),24)
letterFont = pygame.font.Font\
             (path.join(font_dir,'kenvector_future_thin.ttf'),20)
levelFont = pygame.font.Font(path.join(font_dir,'digital7mono.ttf'),40)


### MUSIC ###
music_dir = path.join(path.dirname(__file__), 'music')
gameMusic_dir = path.join(music_dir,'game')

titleMusic = path.join(music_dir,'intro.ogg')
endMusic = path.join(music_dir,'end.ogg')

gameMusicList = []
for number in range(11):
    filename = 'm_{}'.format(number)+'.ogg'
    music2import = path.join(gameMusic_dir,filename)
    gameMusicList.append(music2import)


### SOUNDS ###
sounds_dir = path.join(path.dirname(__file__), 'sounds')

playerDeath = pygame.mixer.Sound(path.join(sounds_dir,'playerdeath.ogg'))
playerBullet = pygame.mixer.Sound(path.join(sounds_dir,'playerbullet.ogg'))
enemyBullet = pygame.mixer.Sound(path.join(sounds_dir,'enemybullet.ogg'))
nextLevel = pygame.mixer.Sound(path.join(sounds_dir,'nextlevel.ogg'))
powerupSound = pygame.mixer.Sound(path.join(sounds_dir,'powerup.ogg'))

explosionSound = []
for ex in range(4):
    filename = 'ex_{}'.format(ex+1)+'.ogg'
    sound2import = path.join(sounds_dir,filename)
    explosionSound.append(sound2import)

count = pygame.mixer.Sound(path.join(sounds_dir,'count.ogg'))
countend = pygame.mixer.Sound(path.join(sounds_dir,'countend.ogg'))
gameover = pygame.mixer.Sound(path.join(sounds_dir,'gameover.ogg'))
    
