import pygame
import pygame, random
from pygame.locals import *
import os

pygame.init()
width=350
height=400
screen = pygame.display.set_mode( (width, height ) )
pygame.display.set_caption('clicked on image')
redSquare = pygame.image.load("player.png").convert()#player.png cambiar por imagen deseada
 
x = 20; # x coordnate of image
y = 30; # y coordinate of image
screen.blit(redSquare ,  ( x,y)) # paint to screen
pygame.display.flip() # paint screen one time
 
running = True
while (running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Set the x, y postions of the mouse click
            x, y = event.pos
            if redSquare.get_rect().collidepoint(x, y):
                print('clicked on image')
#loop over, quite pygame
pygame.quit()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Playerb(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = 500
		self.rect.y = 500





def main():
    pygame.init()
    width=350
    height=400
    player=Playerb()
    screen = pygame.display.set_mode( (width, height ) )
    pygame.display.set_caption('clicked on image')
    redSquare = pygame.image.load("player.png").convert()#player.png cambiar por imagen deseada

    x = 20; # x coordnate of image
    y = 30; # y coordinate of image
    screen.blit(redSquare ,  ( x,y)) # paint to screen
    pygame.display.flip() # paint screen one time

    running = True
    while (running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Set the x, y postions of the mouse click
                x, y = event.pos
                if redSquare.get_rect().collidepoint(x, y):
                    print('clicked on image')
    #loop over, quite pygame
    pygame.quit()

main()