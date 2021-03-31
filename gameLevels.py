## PROJECT HALIOTH
## GAME LEVEL SYSTEM

levels = {}

for level in range(10):
    levelName = 'level_{}'.format(level+1)
    levels[levelName] = {}
    levels[levelName]['ySpeed'] = [1,2]
    levels[levelName]['xSpeed'] = [1,2]
    levels[levelName]['intervalRange'] = [1,1000]
    levels[levelName]['enemyID'] = 50
    levels[levelName]['spawnRange'] = [-1000,-100]
    levels[levelName]['playerRange'] = [175,200]
    levels[levelName]['powerChance'] = 0.9
    
for level in range(10,30):
    levelName = 'level_{}'.format(level+1)
    levels[levelName] = {}
    levels[levelName]['ySpeed'] = [1,4]
    levels[levelName]['xSpeed'] = [1,3]
    levels[levelName]['intervalRange'] = [1,800]
    levels[levelName]['enemyID'] = 50
    levels[levelName]['spawnRange'] = [-4000,-200]
    levels[levelName]['playerRange'] = [160,190]
    levels[levelName]['powerChance'] = 0.8

for level in range(30,50):
    levelName = 'level_{}'.format(level+1)
    levels[levelName] = {}
    levels[levelName]['ySpeed'] = [1,4]
    levels[levelName]['xSpeed'] = [1,5]
    levels[levelName]['intervalRange'] = [1,600]
    levels[levelName]['enemyID'] = 40
    levels[levelName]['spawnRange'] = [-12000,-800]
    levels[levelName]['playerRange'] = [145,170]
    levels[levelName]['powerChance'] = 0.7

for level in range(50,76):
    levelName = 'level_{}'.format(level+1)
    levels[levelName] = {}
    levels[levelName]['ySpeed'] = [1,4]
    levels[levelName]['xSpeed'] = [1,5]
    levels[levelName]['intervalRange'] = [1,500]
    levels[levelName]['enemyID'] = 30
    levels[levelName]['spawnRange'] = [-15000,-900]
    levels[levelName]['playerRange'] = [120,150]
    levels[levelName]['powerChance'] = 0.6

for level in range(76,100):
    levelName = 'level_{}'.format(level+1)
    levels[levelName] = {}
    levels[levelName]['ySpeed'] = [1,5]
    levels[levelName]['xSpeed'] = [1,6]
    levels[levelName]['intervalRange'] = [1,400]
    levels[levelName]['enemyID'] = 30
    levels[levelName]['spawnRange'] = [-18000,-900]
    levels[levelName]['playerRange'] = [100,120]
    levels[levelName]['powerChance'] = 0.5

levels['level_100'] = {}
levels['level_100']['ySpeed'] = [3,6]
levels['level_100']['xSpeed'] = [3,6]
levels['level_100']['intervalRange'] = [1,200]
levels['level_100']['enemyID'] = 20
levels['level_100']['spawnRange'] = [-15000,-500]
levels['level_100']['playerRange'] = [90,110]
levels['level_100']['powerChance'] = 0.4
    
    

