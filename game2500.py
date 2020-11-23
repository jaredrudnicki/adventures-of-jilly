import pygame, sys, numpy, math

WHITE = [255,255,255]

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
        
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.ypos = ypos
        self.xpos = xpos
        self.rect.x = xpos*32
        self.rect.y = ypos*32
        self.items = []

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.up_tile != "wall":
                self.ypos -= 1
                self.rect.y -= 32
        elif keys[pygame.K_s]:
            if self.down_tile != "wall":
                self.ypos +=1
                self.rect.y += 32
        elif keys[pygame.K_a]:
            if self.left_tile != "wall":
                self.xpos -= 1
                self.rect.x -= 32
        elif keys[pygame.K_d]:
            if self.right_tile != "wall":
                self.xpos += 1
                self.rect.x += 32

        self.current_tile = self.game.levelArr[self.ypos][self.xpos]
        self.up_tile = self.game.levelArr[self.ypos-1][self.xpos]
        self.left_tile = self.game.levelArr[self.ypos][self.xpos-1]
        self.right_tile = self.game.levelArr[self.ypos][self.xpos+1]
        self.down_tile = self.game.levelArr[self.ypos+1][self.xpos]

        if(self.current_tile == "key" or self.current_tile == "knife"):
            self.items.append(self.current_tile)
            #edit the tile group in game
            self.game.levelArr[self.ypos][self.xpos] = "floor"
            self.game.setBoard(self.game.levelArr)
        elif(self.current_tile == "door"):
            if("key" in self.items and "knife" in self.items):
                print("won")
                self.game.running = False
                #g = GameOver()
                #g.run()

class Spider(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        
        self.vel = -1
        self.xpos = xpos
        self.ypos = ypos

        self.rect.x = xpos*32
        self.rect.y = ypos*32
        

    def update(self):
        
        self.ypos = self.ypos + self.vel
        self.rect.y = self.ypos*32

        if self.ypos == 1:
            self.vel = 1
        elif self.ypos == 9:
            self.vel = -1

        if(((self.game.player.xpos >= self.xpos -1) and (self.game.player.xpos <= self.xpos+1)) and
           ((self.game.player.ypos >= self.ypos -1) and (self.game.player.ypos <= self.ypos+1))):
            self.game.running = False
            print("gameover:spider eat you")
        
class Tile(pygame.sprite.Sprite):
    def __init__(self, identifier, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        #either wall, floor, key, etc.
        self.identifier = identifier
        if identifier == "wall":
            self.image = pygame.image.load("wall.png")
        elif identifier == "key" or identifier == "knife":
            self.image = pygame.image.load("key.png")
        elif identifier == "door":
            self.image = pygame.image.load("door.png")
        elif identifier == "empty":
            self.image = pygame.image.load("empty.png")
        else:
            self.image = pygame.image.load("floor.png")
        self.rect = self.image.get_rect()
        self.rect.x = xpos*32
        self.rect.y = ypos*32
        #self.rect = pygame.Rect(8,8,xpos*8,ypos*8)




class Game:
    def __init__(self, levelArr, time):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('empty.mp3')
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Courier', 20)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((512, 352))
        self.levelArr = levelArr
        self.tiles = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.spider_group = pygame.sprite.Group()
        self.setBoard(levelArr)
        self.time = time
        self.init_time = time
        self.running = True

    def setBoard(self, levelArr):
        for col in range (len(levelArr)):
            for row in range (len(levelArr[col])):
                identifier = levelArr[col][row]
                if identifier == "player":
                    self.player = Player(row, col, self)
                    self.player_group.add(self.player)
                    self.tiles.add(Tile("floor", row, col))
                    self.levelArr[col][row] = "floor"
                elif identifier == "spider":
                    self.spider_group.add(Spider(row, col, self))
                    self.tiles.add(Tile("floor", row, col))
                    self.levelArr[col][row] = "floor"
                else:
                    self.tiles.add(Tile(identifier, row, col))
                #print(row,",",col,": ",identifier)

    def draw(self):
        self.screen.fill(WHITE)
        self.tiles.draw(self.screen)
        self.player_group.draw(self.screen)
        self.spider_group.draw(self.screen)
        timer_surface = self.myfont.render(str(self.time), True, [255,0,0])
        self.screen.blit(timer_surface, (4,4))
        pygame.display.update()

    def update(self):
        self.player_group.update()

    def run(self):
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





arr = ([["empty", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "empty"],
        ["wall", "player", "key", "wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
        ["wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
        ["wall", "wall", "wall", "wall", "floor", "floor", "floor", "wall", "wall", "wall", "wall", "wall", "wall", "floor", "floor", "wall"],
        ["wall", "wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "knife", "floor", "floor", "floor", "floor", "wall"],
        ["wall", "door", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
        ["wall", "wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
        ["wall", "wall", "wall", "wall", "floor", "floor", "floor", "wall", "wall", "wall", "wall", "wall", "wall", "floor", "floor", "wall"],
        ["wall", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
        ["wall", "floor", "knife", "wall", "floor", "spider", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "floor", "wall"],
        ["empty", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "wall", "empty"]])
g = Game(arr, 100)
g.run()
