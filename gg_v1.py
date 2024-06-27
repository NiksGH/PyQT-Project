import pygame
from pygame import *

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game")

bg = pygame.image.load('bg.png')
player = pygame.image.load('front.png')
walk_right = [
	pygame.image.load('right1.png'),
	pygame.image.load('right2.png')
]

walk_left = [
	pygame.image.load('left1.png'),
	pygame.image.load('left2.png')
]

stay = [
	pygame.image.load('front.png')
]

platforms = [
	pygame.image.load('platform3blocks.png'),
	pygame.image.load('platform1block.png')
]

platforms_list = []

n = 0

player_speed_x = 10
player_speed_y = 10
player_x = 400
player_y = 550

is_jump = False
jump_count = 8
a = 0

FPS = 10

running = True
while running:
	screen.blit(bg, (0, 0))

	player_rect = stay[0].get_rect(topleft=(player_x, player_y))
	platform1 = platforms[0].get_rect(topleft=(150, 500))
	platform2 = platforms[1].get_rect(topleft=(0, 400))

	if player_rect.colliderect(platform1) or player_rect.colliderect(platform2):
		if keys[pygame.K_d] or [pygame.K_a]:
			player_speed_x = 10
		if jump_count != 8 and jump_count != -8:
			jump_count = 8
			is_jump = False
	#else:
		#if player_y < 554:
			#player_y += 1

	keys = pygame.key.get_pressed()

	if keys[pygame.K_a]:
		screen.blit(walk_left[n], (player_x, player_y))
	elif keys[pygame.K_d]:
		screen.blit(walk_right[n], (player_x, player_y))
	else:
		screen.blit(stay[0], (player_x, player_y))

	screen.blit(platforms[0], (150, 500))
	screen.blit(platforms[1], (0, 400))
	#screen.blit(walk_left[n], (player_x, player_y))
	#screen.blit(walk_left[n], (player_x, player_y))

	if not is_jump:
		if keys[pygame.K_SPACE]:
			is_jump = True

	else:
		if jump_count >= -8:
			if jump_count > 0:
				player_y -= (jump_count ** 2) / 2
			else:
				player_y += (jump_count ** 2) / 2
			jump_count -= 1
		else:
			is_jump = False
			jump_count = 8

	if keys[pygame.K_d] and player_x <= 800:
		player_x += player_speed_x
	elif keys[pygame.K_a] and player_x >= 0:
		player_x -= player_speed_x

	if n == 1:
		n = 0
	else:
		n += 1

	pygame.display.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()

	clock.tick(FPS)