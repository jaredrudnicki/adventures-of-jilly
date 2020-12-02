#! /usr/bin/env python

import pygame, sys, math
WHITE = [255,255,255]
RED = [255, 0, 0]

class Home:
    def __init__(self):
        self.screen = pygame.display.set_mode((512,352))
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Courier', 20)
        self.count = 1
        
        self.LEVEL1= ([["tl-wall", "t-wall", "t-wall", "tr-wall", "t-wall", "t-wall", "t-wall", "t-wall", "t-wall", "t-wall", "t-wall", "t-wall", "t-wall", "t-wall", "t-wall", "tr-wall"],
                       ["l-wall", "floor", "key", "r-wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "r-wall"],
                       ["l-wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "r-wall"],
                       ["wall", "wall", "wall", "wall", "floor", "floor", "floor", "empty-shlf", "cos-shlf", "cos-shlf", "cos-shlf", "empty-shlf", "cos-shlf", "floor", "floor", "r-wall"],
                       ["wall", "l-wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "knife", "floor", "floor", "floor", "floor", "r-wall"],
                       ["wall", "l-door", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "r-wall"],
                       ["wall", "l-wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "r-wall"],
                       ["tl-wall", "t-wall", "t-wall", "tr-wall", "floor", "floor", "floor", "tool-shlf", "empty-shlf", "tool-shlf", "food-shlf", "empty-shlf", "empty-shlf", "floor", "floor", "r-wall"],
                       ["l-wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "r-wall"],
                       ["l-wall", "floor", "ladder", "r-wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "r-wall"],
                       ["wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall"]])
        self.SPIDER1 = ([[9,5],[8,5],[7,5],[6,5],[5,5],[4,5],[3,5],[2,5],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],[7,5],[8,5]])
        self.PLAYER1 = [1,1]

        self.LEVEL2 = ([["wall", "wall", "wall", "wall", "wall"],
                        ["wall", "floor", "floor", "floor", "wall"],
                        ["wall", "wall", "wall", "wall", "wall"]])
        self.SPIDER2 = ([[1,3]])
        self.PLAYER2 = [1,1]

    def next_level(self):
        if(self.count == 1):
            self.count += 1
            self.level_two()
        elif(self.count == 2):
            self.count += 1
            self.level_three()
    
    def level_one(self):
        g = Game(self.LEVEL1, self.SPIDER1, self.PLAYER1, 100, self)
        g.run()

    def level_two(self):
        g = Game(self.LEVEL2, self.SPIDER2, self.PLAYER2, 100, self)
        g.run()
        
    def level_three(self):
        print('not_used')
        
    def draw(self):
        ts1 = self.myfont.render('Welcome', True, RED)
        ts2 = self.myfont.render('Press SPACE to play', True, RED)
        self.screen.blit(ts1, (20,20))
        self.screen.blit(ts2, (20,200))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                        self.level_one()
            self.screen.fill(WHITE)
            self.draw()
            pygame.display.update()
        

class Player(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, game):
        pygame.sprite.Sprite.__init__(self)
        #set boardering tiles
        self.game = game
        self.current_tile = self.game.levelArr[ypos][xpos]
        self.up_tile = self.game.levelArr[ypos-1][xpos]
        self.left_tile = self.game.levelArr[ypos][xpos-1]
        self.right_tile = self.game.levelArr[ypos][xpos+1]
        self.down_tile = self.game.levelArr[ypos+1][xpos]
        
        self.image = pygame.image.load("down-jilly.png")
        self.rect = self.image.get_rect()
        self.ypos = ypos
        self.xpos = xpos
        self.rect.x = xpos*32
        self.rect.y = ypos*32
        self.items = []

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if (self.up_tile != "wall" and self.up_tile != "t-wall" and self.up_tile != "tr-wall" and self.up_tile != "r-wall" and self.up_tile != "l-wall" and
            self.up_tile != "tl-wall" and self.up_tile != "empty-shlf" and self.up_tile != "cos-shlf" and self.up_tile != "food-shlf" and self.up_tile != "tool-shlf"):
                self.ypos -= 1
                self.rect.y -= 32
                self.image = pygame.image.load("up-jilly.png")
        elif keys[pygame.K_s]:
            if (self.down_tile != "wall" and self.down_tile != "t-wall" and self.down_tile != "tr-wall" and self.down_tile != "r-wall" and self.down_tile != "l-wall" and self.down_tile != "tl-wall"
             and self.down_tile != "empty-shlf" and self.down_tile != "cos-shlf" and self.down_tile != "food-shlf" and self.down_tile != "tool-shlf"):
                self.ypos +=1
                self.rect.y += 32
                self.image = pygame.image.load("down-jilly.png")
        elif keys[pygame.K_a]:
            if (self.left_tile != "wall" and self.left_tile != "t-wall" and self.left_tile != "tr-wall" and self.left_tile != "r-wall" and self.left_tile != "l-wall" and self.left_tile != "tl-wall"
             and self.left_tile != "empty-shlf" and self.left_tile != "cos-shlf" and self.left_tile != "food-shlf" and self.left_tile != "tool-shlf"):
                self.xpos -= 1
                self.rect.x -= 32
                self.image = pygame.image.load("left-jilly.png")
        elif keys[pygame.K_d]:
            if (self.right_tile != "wall" and self.right_tile != "t-wall" and self.right_tile != "tr-wall" and self.right_tile != "r-wall" and self.right_tile != "l-wall" and self.right_tile != "tl-wall"
             and self.right_tile != "empty-shlf" and self.right_tile != "cos-shlf" and self.right_tile != "food-shlf" and self.right_tile != "tool-shlf"):
                self.xpos += 1
                self.rect.x += 32
                self.image = pygame.image.load("right-jilly.png")

        self.current_tile = self.game.levelArr[self.ypos][self.xpos]
        self.up_tile = self.game.levelArr[self.ypos-1][self.xpos]
        self.left_tile = self.game.levelArr[self.ypos][self.xpos-1]
        self.right_tile = self.game.levelArr[self.ypos][self.xpos+1]
        self.down_tile = self.game.levelArr[self.ypos+1][self.xpos]

        #pick-up
        if(self.current_tile == "key" or self.current_tile == "knife"):
            self.items.append(self.current_tile)
            #edit the tile group in game
            self.game.levelArr[self.ypos][self.xpos] = "floor"
            self.game.setBoard(self.game.levelArr)

        #check at door
        elif(self.current_tile == "l-door" or self.current_tile == "r-door" or self.current_tile == "t-door"):
            if("key" in self.items and "knife" in self.items):
                print("won")
                self.game.running = False
                if(self.game.levelNum < 2):
                    self.game.home.next_level()
                else:
                    g = GameOver()
                    g.run()

class Spider(pygame.sprite.Sprite):
    def __init__(self, path, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.image.load("up-spider.png")
        self.rect = self.image.get_rect()
        
        self.count = 0
        self.path = path

        self.xpos = self.path[self.count][1]
        self.ypos = self.path[self.count][0]
        
        self.rect.x = self.xpos*32
        self.rect.y = self.ypos*32
        
        
    def update(self):
        self.count += 1
        if(self.count == len(self.path)):
            self.count = 0
        
        self.xpos = self.path[self.count][1]
        self.ypos = self.path[self.count][0]
        self.rect.x = self.xpos*32
        self.rect.y = self.ypos*32

        if self.ypos == 1:
            self.vel = 1
        elif self.ypos == 9:
            self.vel = -1

        if(((self.game.player.xpos >= self.xpos -1) and (self.game.player.xpos <= self.xpos+1)) and
           ((self.game.player.ypos >= self.ypos -1) and (self.game.player.ypos <= self.ypos+1))):
            self.game.running = False
            g = GameOver()
            g.run()
        

class Tile(pygame.sprite.Sprite):
    def __init__(self, identifier, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        #either wall, floor, key, etc.
        self.identifier = identifier
        if identifier == "t-wall":
            self.image = pygame.image.load("top-wall.png")
        elif identifier == "l-wall":
            self.image = pygame.image.load("left-wall.png")
        elif identifier == "r-wall":
            self.image = pygame.image.load("right-wall.png")
        elif identifier == "wall":
            self.image = pygame.image.load("full-wall.png")
        elif identifier == "tl-wall":
            self.image = pygame.image.load("top-left-wall.png")
        elif identifier == "tr-wall":
            self.image = pygame.image.load("top-right-wall.png")

            
        elif identifier == "key":
            self.image = pygame.image.load("key.png")
        elif identifier == "knife":
            self.image = pygame.image.load("knife.png")
        elif identifier == "keycard":
            self.image = pygame.image.load("keycard.png")
        elif identifier == "ladder":
            self.image = pygame.image.load("ladder.png")

        elif identifier == "cos-shlf":
            self.image = pygame.image.load("cosmetics-shelf.png")
        elif identifier == "empty-shlf":
            self.image = pygame.image.load("placeholder-shelf.png")
        elif identifier == "food-shlf":
            self.image = pygame.image.load("food-shelf.png")
        elif identifier == "tool-shlf":
            self.image = pygame.image.load("tool-shelf.png")

        elif identifier == "l-door":
            self.image = pygame.image.load("left-wall-door.png")
        elif identifier == "r-door":
            self.image = pygame.image.load("right-wall-door.png")
        elif identifier == "t-door":
            self.image = pygame.image.load("top-wall-door.png")
        
        elif identifier == "empty":
            self.image = pygame.image.load("full-wall.png")
        else:
            self.image = pygame.image.load("basic-floor-tile.png")
        self.rect = self.image.get_rect()
        self.rect.x = xpos*32
        self.rect.y = ypos*32
        #self.rect = pygame.Rect(8,8,xpos*8,ypos*8)




class Game:
    def __init__(self, levelArr, spiderPath, playerPos, time, home):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('empty.mp3')
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Courier', 20)
        self.clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode((512, 352))

        self.home = home
        self.levelArr = levelArr
        self.spiderPath = spiderPath
        self.levelNum = self.home.count
        
        self.tiles = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.spider_group = pygame.sprite.Group()
        
        self.time = time
        self.init_time = time
        self.running = True

        self.spider_group.add(Spider(self.spiderPath, self))
        self.player = Player(playerPos[0], playerPos[1], self)
        self.player_group.add(self.player)

    def setBoard(self, levelArr):
        for col in range (len(levelArr)):
            for row in range (len(levelArr[col])):
                identifier = levelArr[col][row]
                self.tiles.add(Tile(identifier, row, col))
                #print(row,",",col,": ",identifier)

    def draw(self):
        self.screen.fill(WHITE)
        self.tiles.draw(self.screen)
        self.player_group.draw(self.screen)
        self.spider_group.draw(self.screen)
        timer_surface = self.myfont.render(str(self.time), True, RED)
        self.screen.blit(timer_surface, (4,4))
        pygame.display.update()

    def update(self):
        self.player_group.update()

    def run(self):
        self.setBoard(self.levelArr)
        pygame.mixer.music.play(2)
        start_ticks=pygame.time.get_ticks()
        while self.running:
            self.clock.tick(10)
            difference=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
            self.time = math.floor(self.init_time - difference)
            
            if (self.time<=0): # if more than 10 seconds close the game
                self.running = False
                print("game over")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.update()
            self.spider_group.update()
            self.draw()


class GameOver:
    def __init__(self):
        self.screen = pygame.display.set_mode((512,352))
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Courier', 20)

    def draw(self):
        ts1 = self.myfont.render('Game Over', True, RED)
        ts2 = self.myfont.render('Press SPACE to restart', True, RED)
        self.screen.blit(ts1, (20,20))
        self.screen.blit(ts2, (20,200))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                        h = Home()
                        h.run()
            self.screen.fill(WHITE)
            self.draw()
            pygame.display.update()




g = Home()
g.run()
        
        
            
