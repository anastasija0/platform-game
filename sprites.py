import pygame
from settings import *

class Player(pg.sprite.Sprite):
  def __init__(self,game, x,y, width, height, image):
    self.groups = game.all_sprites
    pygame.sprite.Sprite.__init__(self, self.groups)
    self.game=game
    self.x=x
    self.y=y
    self.vel= 10.0
    self.width=width
    self.height=height
    self.image=image
    self.isJump=False
    self.jumpCount=10
    self.left=False
    self.right=False
    self.walkCount=0
    self.still=True
    self.hitbox = (self.x + 2, self.y + 2, 50, 86)
    self.health = 3
    self.visible = True
    self.score = 0
    self.walkRight = [pygame.image.load('Run000.png'), pygame.image.load('Run001.png'), pygame.image.load('Run002.png'), pygame.image.load('Run003.png'), pygame.image.load('Run004.png'), pygame.image.load('Run005.png'), pygame.image.load('Run006.png'), pygame.image.load('Run007.png'), pygame.image.load('Run008.png'), pygame.image.load('Run009.png')]
    self.walkLeft = [pygame.image.load('Run100.png'), pygame.image.load('Run101.png'), pygame.image.load('Run102.png'), pygame.image.load('Run103.png'), pygame.image.load('Run104.png'), pygame.image.load('Run105.png'), pygame.image.load('Run106.png'), pygame.image.load('Run107.png'), pygame.image.load('Run108.png'), pygame.image.load('Run109.png')]
    still = [pygame.image.load('Idle000.png'), pygame.image.load('Idle100.png')]
    
  def draw(self, screen):
    if self.visible:
      if self.walkCount + 1 >= 30:
        self.walkCount = 0
      
      if not(self.still):
        if self.left:  
          screen.blit(walkLeft[self.walkCount//3], (self.x,self.y))
          self.walkCount += 1                          
        elif self.right:
          screen.blit(walkRight[self.walkCount//3], (self.x,self.y))
          self.walkCount += 1
      else:
        if self.left:
          screen.blit(still[1],(self.x,self.y))
        else:
          screen.blit(still[0],(self.x,self.y))

      pygame.draw.rect(screen, RED, (self.hitbox[0], self.hitbox[1] - 20, 51, 10))
      pygame.draw.rect(screen, GREEN, (self.hitbox[0], self.hitbox[1] - 20, 51 - (17 * (3 - self.health)), 10))
      self.hitbox = (self.x + 2, self.y + 2, 50, 86) #stalno updatujem
      
  def hit(self): #da li je sve ovo ok??
    self.x = 0
    self.y = SCREEN_SIZE[1]-self.height-3*32 #zbog mape 3*32
    self.walkCount = 0
    self.health-=1
    if self.health==0:
      self.visible=False
    font1 = pygame.font.SysFont('comicsans', 50) #da li da prepravljam ista
    text = font1.render('-1', 1, (255,0,0))
    self.game.screen.blit(text, (250 - (text.get_width()/2),200))
    pygame.display.update()
    i = 0
    while i < 100:
      pygame.time.delay(10)
      i += 1
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          i = 101
          pygame.quit() #imacu samo 1 igraca
    #def collide_with_walls(self,x,y):
        #for wall in self.game.walls:
            #if wall.x == self.x and wall.y == self.y:
                #return True
        #return False

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        #self.rect.x = x * TILESIZE
        #self.rect.y = y * TILESIZE

class Bullet(pygame.sprite.Sprite):
  def __init__(self, game, x, y, r, color, direction):
    self.groups = game.all_sprites, game.bullets
    pygame.sprite.Sprite.__init__(self, self.groups)
    self.game=game
    self.x=x
    self.y=y
    self.r=r
    self.color=color
    self.direction=direction #+1 za desno, -1 za levo
    self.vel = 8*direction

  def draw(self, screen):
    pygame.draw.circle(self.game.screen, self.color, (self.x, self.y), self.r)

class Enemy(pygame.sprite.Sprite):
  def __init__(self,game, x, y, width, height, end):
    self.groups = game.all_sprites, game.enemies
    pygame.sprite.Sprite.__init__(self, self.groups)
    self.game=game
    self.x=x
    self.y=y
    self.width=width
    self.height=height
    self.end=end
    self.path=[self.x, self.end]
    self.walkCount = 0
    self.vel = 3
    self.walkRight = [pygame.image.load('ER0.png'), pygame.image.load('ER1.png'), pygame.image.load('ER2.png'), pygame.image.load('ER3.png'), pygame.image.load('ER4.png'), pygame.image.load('ER5.png'), pygame.image.load('ER6.png'), pygame.image.load('ER7.png'), pygame.image.load('ER8.png'), pygame.image.load('ER9.png')]
    self.walkLeft = [pygame.image.load('EL0.png'), pygame.image.load('EL1.png'), pygame.image.load('EL2.png'), pygame.image.load('EL3.png'), pygame.image.load('EL4.png'), pygame.image.load('EL5.png'), pygame.image.load('EL6.png'), pygame.image.load('EL7.png'), pygame.image.load('EL8.png'), pygame.image.load('EL9.png')]
    self.hitbox = (self.x + 2, self.y+5, 55, 84)
    self.health = 3
    self.visible = True

  def draw(self, screen):
    self.move()
    if self.visible:
      if self.walkCount + 1 >=30:
        self.walkCount = 0
        
      if self.vel > 0:
        self.game.screen.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
        self.walkCount+=1
      else:
        self.game.screen.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
        self.walkCount+=1

      pygame.draw.rect(self.game.screen, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 51, 10))
      pygame.draw.rect(self.game.screen, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 51 - (17 * (3 - self.health)), 10))
      self.hitbox = (self.x + 2, self.y+5, 55, 84)
  
  def move(self):
    if self.visible:
      if self.vel>0:
        if self.x + self.vel < self.path[1]:
          self.x+=self.vel
        else:
          self.vel=self.vel*-1
          self.walkCount=0
      else:
        if self.x - self.vel > self.path[0]:
          self.x+=self.vel
        else:
          self.vel=self.vel*-1
          self.walkCount=0
  def hit(self): 
    if self.health > 0:
      self.health -= 1
    else:
      self.visible = False
    
