




tiles=[pygame.image.load('tile1.png'),pygame.image.load('tile2.png'),pygame.image.load('tile3.png'),pygame.image.load('tile4.png'),pygame.image.load('tile5.png'),pygame.image.load('tile6.png'),pygame.image.load('tile7.png')]
map_data = []


      
load_data(map_data)
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
      #if tile != '0':
        #tile_rects.append(pygame.Rect(x*32+scroll[0],y*32+scroll[1],32,32))
      x += 1
    y += 1
  


        
def redrawGameWindow():
  screen.blit(bg, (0,0))
  draw_tiles(map_data)
  
  p.draw(screen)
  for e in enemies:
    e.draw(screen)
  for bullet in bullets:
    bullet.draw(screen)
  pygame.display.update()

#main
font = pygame.font.SysFont('comicsans', 25, True, True)
p=Player(0, screen_size[1]-3*32-86, 50, 86)
enemies=[]
enemies.append(Enemy(150, screen_size[1]-3*32-86, 70, 84, 500))
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
      bullets.append(Bullet(round(p.x+p.width //2),round(p.y+p.height //2), 6, (255,0,0), direction))
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
    if p.x < 700 - p.vel - p.width:
        p.x += p.vel
    else:
        p.x = 700 - p.vel - p.width
        scroll[0]-=p.vel
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
