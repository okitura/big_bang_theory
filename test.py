import sys, pygame, pyganim, random
from game_objects import *
from settings import *


pygame.init()
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.

pygame.display.set_caption("BIG BANG THEORY")
myfont = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()

screen = pygame.display.set_mode(SIZE)
winner = pygame.image.load('assets/winner.png')
loser = pygame.image.load('assets/loser.png')
score = 0
health = 1000
explosion_animation = pyganim.PygAnimation([
('assets/affects/explosion{}.png'.format(i), 250) for i in range(1,4)], loop=False)
#explode_anim = pygame.image.load(explode_animation)
	

# Game Groups
all_objects= pygame.sprite.OrderedUpdates()
rockets = pygame.sprite.Group()
aliens = pygame.sprite.Group()
shells = pygame.sprite.Group()

explosions = []

# music = pygame.mixer.Sound('assetss/music/bg.wav')
# music.play(-1)

# Game objects
player = Player(clock, rockets)
background = Background()

tank = Tank()

gun = Gun((137, HEIGHT-80), shells)


#rocket = Rocket(player.rect.midtop)


all_objects.add(background)
all_objects.add(tank)
all_objects.add(gun)


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
		# if event.type == pygame.MOUSEMOTION:
		# 	mousex, mousey = event.pos
		# 	moveVector = (mousex, mousey)

	fast_esc = pygame.key.get_pressed()
	if fast_esc[pygame.K_ESCAPE]:
		sys.exit()

	screen.fill(WHITE)

	Alien.process_aliens(clock, aliens)
	textsurface = myfont.render('SCORE:'+str(score), False, WHITE)
	healthsurface = myfont.render('HEALTH:'+str(health), False, WHITE)

	all_objects.update()
	rockets.update()
	aliens.update()
	shells.update()
	aliens_and_bomb_collided = pygame.sprite.groupcollide(aliens, shells, True, True)
	for collied in aliens_and_bomb_collided:
		explosion = explosion_animation.getCopy()
		explosion.play()
		explosions.append((explosion, (collied.rect.center)))
		
		
	player_and_aliens_collided = pygame.sprite.spritecollide(player, aliens, True)

	if player_and_aliens_collided:
		all_objects.remove(player)
	

		
	all_objects.draw(screen)
	rockets.draw(screen)
	aliens.draw(screen)
	shells.draw(screen)
	


	for explosion, position in explosions[:]:
		if explosion.isFinished():
			# print(explosions)
			# print('/************************/')
			# print(explosion)
			explosions.remove((explosion, position))
		else:
			x, y = position
			explosion.blit(screen, (x-20, y-30))
			score += 1 
	
	#if score > 100:
		#winner.blit(screen, (0, 0))
	for i in aliens:
		if i.rect.right < 0 or i.rect.left < -WIDTH:
			health -=100 

	if health <= 0:
		screen.blit(loser,(50, 50)) 
		pygame.display.update()

	if score >= 100:
		screen.blit(winner,(50, 50)) 
		pygame.display.update()


	screen.blit(textsurface,(5, 5))
	screen.blit(healthsurface, (200, 5))

	pygame.display.flip()
	clock.tick(30)

	

