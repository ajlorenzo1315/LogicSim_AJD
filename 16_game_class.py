import pygame, random ,sys
from pygame.locals import *
import os
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("meteor.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()

	def update(self):
		self.rect.y += 1

		if self.rect.y > SCREEN_HEIGHT:
			self.rect.y = -10
			self.rect.x = random.randrange(SCREEN_WIDTH)


class Player(pygame.sprite.Sprite):
	def __init__(self,selecionado=False):
		super().__init__()
		self.image = pygame.image.load("player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.selecionado=selecionado
		

	def update(self):
		if self.selecionado == True:
			mouse_pos = pygame.mouse.get_pos()
			self.rect.x = mouse_pos[0]
			self.rect.y = mouse_pos[1]

class Playerb(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = 500
		self.rect.y = 500



class Game(object):
	def __init__(self):
		self.score = 0
		self.tengoalgo=None
		self.cantidadaselscion=0
		self.meteor_list = pygame.sprite.Group()
		self.all_sprites_list = pygame.sprite.Group()
		self.all_bottoms_list= pygame.sprite.Group()
		self.all_player=pygame.sprite.Group()
		for i in range(50):
			meteor = Meteor()
			meteor.rect.x = random.randrange(SCREEN_WIDTH)
			meteor.rect.y = random.randrange(SCREEN_HEIGHT)

			self.meteor_list.add(meteor)
			self.all_sprites_list.add(meteor)

		self.playerbootom = Playerb()
		self.all_sprites_list.add(self.playerbootom)
		self.all_bottoms_list.add(self.playerbootom)
		self.player = None
		
	def process_events(self):
		self.click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				# Set the x, y postions of the mouse click
				x, y = event.pos
				if self.tengoalgo ==None:
					#cick_hit_list = pygame.sprite.spritecollide((x,y),self.all_bottoms_list , False)
					for box in self.all_bottoms_list:
						if box.rect.collidepoint(x,y):
							#print("hola")
							self.crear_nave()
					if self.player != None:
						for box in self.all_player:
							if box.rect.collidepoint(x,y):
								#print("hola")
								box.selecionado=True
								self.tengoalgo=box

				elif self.tengoalgo !=None :
					#cick_hit_list = pygame.sprite.spritecollide((x,y),self.all_bottoms_list , False)
					for box in self.all_player:
						if box.rect.collidepoint(x,y):
							#print("hola")
							if self.tengoalgo !=None:
								self.tengoalgo.selecionado=False
								self.tengoalgo=None

				
							
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.type == pygame.QUIT:
					return True
		return False

	def crear_nave(self):
		self.player=Player(True)
		self.all_player.add(self.player)
		self.all_sprites_list.add(self.player)
		self.tengoalgo=self.player


	def run_logic(self):
		mx, my = pygame.mouse.get_pos()
		self.all_sprites_list.update()
		
		if self.player!=None:
			meteor_hit_list = pygame.sprite.spritecollide(self.player, self.meteor_list, True)
			
			for meteor in meteor_hit_list:
				self.score += 1
				print(self.score)

	def display_frame(self, screen):
		screen.fill(WHITE)
		self.all_sprites_list.draw(screen)
		pygame.display.flip()

def main():
	pygame.init()

	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

	done = False
	clock = pygame.time.Clock()

	game = Game()

	while not done:
		done = game.process_events()
		game.run_logic()
		game.display_frame(screen)
		clock.tick(60)
	pygame.quit()


main()