#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
SCORE_COIN = 0

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


#Defines a new class called Enemy that inherits from the pygame.sprite.Sprite class
class Enemy(pygame.sprite.Sprite):
      
#The __init__() method is called when an instance of the Enemy class is created. 
#super().__init__() calls the constructor of the Sprite class, which initializes the sprite.      
      def __init__(self):
        super().__init__() 

        self.image = pygame.image.load("Enemy.png")

        #self.rect is set to the rectangle that defines the position and size of the sprite. The center attribute of self.rect is set to a tuple representing the position of the enemy at the top of the screen, with a random x-coordinate within a certain range.
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

      def move(self):
        #global SCORE tells the method to use the global variable SCORE, which keeps track of the player's score.
        global SCORE

        #Moves the enemy sprite down the screen by a constant speed (SPEED). move_ip() is a method of the Rect class that moves the rectangle by a given offset.
        self.rect.move_ip(0,SPEED)

        #Checks if the bottom of the enemy sprite's rectangle has reached the bottom of the screen. If so, it adds 1 to the player's score, resets the enemy sprite's position to the top of the screen with a random x-coordinate within a certain range.
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

random_number = random.randint(10, 470)

class Coin(pygame.sprite.Sprite):
        
      def __init__(self):
        super().__init__() 

        self.image = pygame.image.load("coin.png")

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), random.randint(40,SCREEN_WIDTH-40))
        

      def move(self):
          global SCORE_COIN

          self.rect.move_ip(0, 2)
          if (self.rect.bottom > 600):
            self.rect.center = (random.randint(40,SCREEN_WIDTH-40), random.randint(40,SCREEN_WIDTH-40))
          if pygame.sprite.spritecollideany(P1, coins):
              SCORE_COIN += 1
              pygame.mixer.Sound('Sound_19349.mp3').play() 
              self.rect.center = (random.randint(40,SCREEN_WIDTH-40), random.randint(40,SCREEN_WIDTH-40))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()

        #The center attribute of self.rect is set to a fixed position near the bottom center of the screen.
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                  self.rect.move_ip(0, 5)
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                  self.rect.move_ip(0, -5)          
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                  

#Setting up Sprites        
P1 = Player()
E1 = Enemy()
C = Coin()
#Creating Sprites Groups
coins = pygame.sprite.Group()
coins.add(C)
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#Game Loop
while True:
      
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    


    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    coin_scores = font_small.render(str(SCORE_COIN), True, BLACK)
    DISPLAYSURF.blit(coin_scores, (10, SCREEN_WIDTH-10))

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
        

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('crash.wav').play()
          time.sleep(1)
                   
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
          
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()        
        
     

                   
          

    pygame.display.update()
    FramePerSec.tick(FPS)
