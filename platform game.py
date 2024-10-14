import math
import sys
import pygame
import sys
from os import path
pygame.init()

screen_size=[704,416]#32*22+32*13
screen = pygame.display.set_mode(screen_size)
bg = pygame.image.load('BG.png')
#pygame.mouse.set_visible(0)
pygame.display.set_caption('platform game')

clock = pygame.time.Clock()

walkRight = [pygame.image.load('Run000.png'), pygame.image.load('Run001.png'), pygame.image.load('Run002.png'), pygame.image.load('Run003.png'), pygame.image.load('Run004.png'), pygame.image.load('Run005.png'), pygame.image.load('Run006.png'), pygame.image.load('Run007.png'), pygame.image.load('Run008.png'), pygame.image.load('Run009.png')]
walkLeft = [pygame.image.load('Run100.png'), pygame.image.load('Run101.png'), pygame.image.load('Run102.png'), pygame.image.load('Run103.png'), pygame.image.load('Run104.png'), pygame.image.load('Run105.png'), pygame.image.load('Run106.png'), pygame.image.load('Run107.png'), pygame.image.load('Run108.png'), pygame.image.load('Run109.png')]
still = [pygame.image.load('Idle000.png'), pygame.image.load('Idle100.png')]

score = 0
tiles=[pygame.image.load('tile1.png'),pygame.image.load('tile2.png'),pygame.image.load('tile3.png'),pygame.image.load('tile4.png'),pygame.image.load('tile5.png'),pygame.image.load('tile6.png'),pygame.image.load('tile7.png'),pygame.image.load('tile8.png'),pygame.image.load('tile9.png'),pygame.image.load('tileA.png')]
map_data = []
enemies = []


class Player(object):
  def __init__(self,x,y,width, height):
    #self.image=pygame.image.load(name)
    self.x=x
    self.y=y
    self.vel= 10.0
    self.width=width
    self.height=height
    self.isJump=False
    self.jumpCount=10
    self.left=False
    self.right=False
    self.walkCount=0
    self.still=True
    self.hitbox = (self.x + 2, self.y + 2, 50, 86)
    self.health = 3
    self.visible = True
    
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

      pygame.draw.rect(screen, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 51, 10))
      pygame.draw.rect(screen, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 51 - (17 * (3 - self.health)), 10))
      self.hitbox = (self.x + 2, self.y + 2, 50, 86) #stalno updatujem
      
  def hit(self):
    self.x = 0
    self.y = screen_size[1]-3*32-86
    self.walkCount = 0
    self.health-=1
    if self.health==0:
      self.visible=False
    font1 = pygame.font.SysFont('comicsans', 50)
    text = font1.render('-1', 1, (255,0,0))
    screen.blit(text, (250 - (text.get_width()/2),200))
    pygame.display.update()
    i = 0
    while i < 100:
      pygame.time.delay(10)
      i += 1
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          i = 101
          pygame.quit()
                

class Bullet(object):
  def __init__(self, x, y, r, color, direction):
    self.x=x
    self.y=y
    self.r=r
    self.color=color
    self.direction=direction #+1 za desno, -1 za levo
    self.vel = 8*direction

  def draw(self, screen):
    pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

class Enemy(object):
  
  def __init__(self, x, y, width, height, end):
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
        screen.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
        self.walkCount+=1
      else:
        screen.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
        self.walkCount+=1

      pygame.draw.rect(screen, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 51, 10))
      pygame.draw.rect(screen, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 51 - (17 * (3 - self.health)), 10))
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
          self.vel=self.vel*-1-scroll[0]
          self.walkCount=0
    
  def hit(self): 
    if self.health > 0:
      self.health -= 1
    else:
      self.visible = False

def load_data(map_data, enemies):
  game_folder = path.dirname(__file__)
  with open(path.join(game_folder, 'map.txt'), 'rt') as f:
    for line in f:
      map_data.append(line)
  y = 0  
  for layer in map_data:
      x = 0
      for tile in layer:
          if tile == 'e':
              enemies.append(Enemy(x*32,screen_size[1]-3*32-84, 70, 84, x*32+150))
          x+= 1
      y+= 1
          
      
load_data(map_data, enemies)
scroll=[0,0]
def draw_tiles(map_data):
  y = 0
  for layer in map_data:
    x = 0
    for tile in layer:
      if tile == '1':
        screen.blit(tiles[0],(x*32+scroll[0],y*32+scroll[1]))
      if tile == '2':
        screen.blit(tiles[1],(x*32+scroll[0],y*32+scroll[1]))
      if tile == '3':
        screen.blit(tiles[2],(x*32+scroll[0],y*32+scroll[1]))
      if tile == '4':
        screen.blit(tiles[3],(x*32+scroll[0],y*32+scroll[1]))
      if tile == '5':
        screen.blit(tiles[4],(x*32+scroll[0],y*32+scroll[1]))
      if tile == '6':
        screen.blit(tiles[5],(x*32+scroll[0],y*32+scroll[1]))
      if tile == '7':
        screen.blit(tiles[6],(x*32+scroll[0],y*32+scroll[1]))
      if tile == '8':
        screen.blit(tiles[7],(x*32+scroll[0],y*32+scroll[1]))
      if tile == '9':
        screen.blit(tiles[8],(x*32+scroll[0],y*32+scroll[1]))
      if tile == 'A':
        screen.blit(tiles[9],(x*32+scroll[0],y*32+scroll[1]))
      #if tile != '0':
        #tile_rects.append(pygame.Rect(x*16,y*16,16,16))
      x += 1
    y += 1
  

def redrawGameWindow():
  screen.blit(bg, (0,0))
  draw_tiles(map_data)
  text=font.render('Score: '+ str(score), 1,(255,255,255))
  screen.blit(text,(600, 10))
  p.draw(screen)
  for e in enemies:
    e.draw(screen)
  for bullet in bullets:
    bullet.draw(screen)
  pygame.display.update()

#main
font = pygame.font.SysFont('comicsans', 25, True, True)
p=Player(0, screen_size[1]-3*32-86, 50, 86)
bLoop = 0
bullets = []
run=True
while run:
    
  clock.tick(30)

  for e in enemies:
    if e.visible==True:
      if p.hitbox[1] < e.hitbox[1] + e.hitbox[3] and p.hitbox[1] + p.hitbox[3] > e.hitbox[1]:
        if p.hitbox[0] + p.hitbox[2] > e.hitbox[0] and p.hitbox[0] < e.hitbox[0] + e.hitbox[2]:
          p.hit()
      
  if bLoop > 0:
    bLoop += 1
  if bLoop > 3:
    bLoop = 0

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  for e in enemies:
    for bullet in bullets:
          if bullet.y - bullet.r < e.hitbox[1] + e.hitbox[3] and bullet.y + bullet.r > e.hitbox[1]:
              if bullet.x + bullet.r > e.hitbox[0] and bullet.x - bullet.r < e.hitbox[0] + e.hitbox[2]:
                  e.hit()
                  score+=1
                  bullets.pop(bullets.index(bullet))
    if e.health==0:
      enemies.pop(enemies.index(e))
  
  for bullet in bullets:
    if bullet.x> 0 and bullet.x < screen_size[0]:
      bullet.x+=bullet.vel
    else:
      bullets.pop(bullets.index(bullet))
      
  keys = pygame.key.get_pressed()

  if keys[pygame.K_SPACE] and bLoop == 0:
    if p.left:
      direction=-1
    else:
      direction=1
    if len(bullets)<6:
      bullets.append(Bullet(round(p.x+p.width //2),round(p.y+p.height //2), 4, (255,0,0), direction))
    bLoop = 1
  
  if keys[pygame.K_LEFT] and p.x > p.vel: 
    p.x -= p.vel
    p.left = True
    p.right = False
    p.still=False
  elif keys[pygame.K_RIGHT]: 
    p.left = False
    p.right = True
    p.still=False
    if p.x < screen_size[0] - p.vel - p.width - 150: 
      p.x+=p.vel
    else:
      p.x =screen_size[0] - p.vel - p.width - 150
      scroll[0]-= p.vel
      for e in enemies:
          e.path[0]+=scroll[0]
          e.path[1]+=scroll[0]
  else: 
    p.still=True
    p.walkCount = 0
        
  if not(p.isJump):
    if keys[pygame.K_UP]:
      p.isJump = True
      p.left = False
      p.right = False
      p.walkCount = 0
  else:
    if p.jumpCount >= -10:
      p.y -= (p.jumpCount * abs(p.jumpCount)) * 0.5
      p.jumpCount -= 1
    else: 
      p.jumpCount = 10
      p.isJump = False

  redrawGameWindow() 
    
    
pygame.quit()
  

