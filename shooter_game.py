from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

class GameSprite(sprite.Sprite):
     def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
          super().__init__()
          self.image = transform.scale(image.load(player_image), (size_x, size_y))
          self.speed = player_speed     
          self.rect = self.image.get_rect()
          self.rect.x = player_x
          self.rect.y = player_y
     def reset(self):
          window.blit(self.image, (self.rect.x, self.rect.y)) 

bullets = sprite.Group()
class Player(GameSprite):
     def update(self):
          keys = key.get_pressed()
          if keys[K_LEFT] and self.rect.x > -20:
               self.rect.x -= self.speed
          if keys[K_RIGHT] and self.rect.x < 1100 - 200:
               self.rect.x += self.speed
     def fire(self):
          bullet = Gun('bullet.png', self.rect.centerx, self.rect.top, 25, 25, -15)
          bullets.add(bullet)
          fire = mixer.Sound('fire.ogg')
          fire.play()

lost = 0 
class Enemy(GameSprite):
     def update(self):
          self.rect.y += self.speed
          global lost 
          if self.rect.y > 750:
               self.rect.x = randint(80, 1100 - 80)
               self.rect.y = 0
               lost += 1

good = 0
class Gun(GameSprite):
     def update(self):
          self.rect.y += self.speed
          if self.rect.y < 0:
               self.kill()

window = display.set_mode((1100, 750))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (1100, 750))  

font.init()
font = font.SysFont('Arial', 36)

player = Player('rocket.png', 0, 550, 200, 200, 15)

sprite1 = transform.scale(image.load('rocket.png'), (125, 120))

monsters = sprite.Group()
for i in range(1, 6):
     monster = Enemy('ufo.png', randint(80, 1100 - 80), -10, 100, 100, randint(1, 3))
     monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
     asteroid = Enemy('asteroid.png', randint(80, 1100 - 80), -10, 100, 100, randint(1, 2))
     asteroids.add(asteroid)

life = 3
clock = time.Clock()
FPS = 60
num_fire = 0
rel = False
finish = False
game = True
while game:
     for e in event.get():
          if e.type == QUIT:
               game = False
          elif e.type == KEYDOWN:
               if e.key == K_SPACE:
                    if num_fire < 5 and rel == False:
                         player.fire()
                         num_fire += 1
                    if num_fire >= 5 and rel == False:
                         last_t = timer()
                         rel = True     
     if finish != True:
          window.blit(background, (0, 0)) 
          player.update()
          player.reset()
          display.update()
          monsters.draw(window)
          monsters.update()
          bullets.update()
          bullets.draw(window)
          asteroids.update()
          asteroids.draw(window)
          lost1 = font.render('Пропущено: ' + str(lost), True, (255, 0, 0))
          win1 = font.render('Убил: ' + str(good), True, (255, 0, 0))
          life1 = font.render('Жизней: ' + str(life), True, (255, 0, 0))
          window.blit(lost1, (15, 15))
          window.blit(win1, (15, 40))
          window.blit(life1, (15, 60))
          if lost == 15:
               lost2 = font.render('Проиграл', True, (255, 0, 0))
               window.blit(lost2, (500, 325))
               finish = True
          if rel == True:
               time = timer()     
               if time - last_t < 3:
                    reload = font.render('Идёт перезарядка', 1, (255, 0, 0))
                    window.blit(reload, (450, 700))
               else:
                    num_fire = 0
                    rel = False
          collide = sprite.groupcollide(monsters, bullets, True, True)
          collides = sprite.spritecollide(player, asteroids,False) 
          for z in collides:
               asteroid = Enemy('asteroid.png', randint(80, 1100 - 80), -10, 100, 100, randint(1, 2))
               asteroids.add(asteroid)
               sprite.spritecollide(player, asteroids, True)
               life = life - 1
          for i in collide:
               monster = Enemy('ufo.png', randint(80, 1100 - 80), -10, 100, 100, randint(1, 3))
               monsters.add(monster)
               good += 1
          if good == 15:
               win2 = font.render('Выиграл', True, (255, 255, 0))
               window.blit(win2, (500, 325))
               finish = True
          if life == 0:
               lost2 = font.render('Проиграл', True, (255, 0, 0))
               window.blit(lost2, (500, 325))
               finish = True
     
     display.update()
     clock.tick(FPS)