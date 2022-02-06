import pygame
import os
import time
import random
pygame.font.init()

#screen variables
WIDTH,HEIGHT=700,700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Space Shooter Turtorial')

#load images
RED_SPACE_SHIP=pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
GREEN_SPACE_SHIP=pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
BLUE_SPACE_SHIP=pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))

#Player Ship
YELLOW_SPACE_SHIP=pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))

#Laser
RED_LASER=pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
GREEN_LASER=pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
BLUE_LASER=pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
YELLOW_LASER=pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))

#COLOR
WHITE=(255,255,255)

#BACKGROUND
BACKGROUND=pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT)),90)

#GAME VARIABLES
VEL=10
player_shoot_vel=50
enemy_shoot_vel=10

#PYGAME FONTS
main_font=pygame.font.SysFont("Arial Black",50)
lost_font=pygame.font.SysFont('Arial Black',60)
title_font=pygame.font.SysFont("Arial Black",60)

class Laser:
	def __init__(self,x,y,img):
		self.x=x 
		self.y=y 
		self.img=img
		self.mask=pygame.mask.from_surface(self.img)
	def draw(self,window):
		window.blit(self.img,(self.x,self.y))
	def move(self,vel):
		self.y+=vel 
	def off_screen(self,height):
		return not(self.y<=height and self.y>=0)
	def collision(self,obj):
		return collide(self,obj)
		
class Ship:
	COOLDONW = 5
	def __init__(self,x,y,health=100):
		self.x=x
		self.y=y
		self.health=health
		self.ship_img=None
		self.laser_img=None
		self.lasers=[]
		self.cool_down_counter=0
	def draw(self,window):
		window.blit(self.ship_img,(self.x,self.y))
		for laser in self.lasers:
			laser.draw(window)

	def move_lasers(self,vel,obj):
		self.cool_down()
		for laser in self.lasers:
			laser.move(vel)
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			elif laser.collision(obj):
				obj.health-=10
				self.lasers.remove(laser)

	def cool_down(self):
		if self.cool_down_counter == self.COOLDONW:
			self.cool_down_counter = 0
		elif self.cool_down_counter > 0:
			self.cool_down_counter += 1

	def shoot(self):
		if self.cool_down_counter==0:
			laser=Laser(self.x,self.y,self.laser_img)
			self.lasers.append(laser)
			self.cool_down_counter=1
		
	def get_width(self):
		return self.ship_img.get_width()
	def get_height(self):
		return self.ship_img.get_height()

class Enemy(Ship):
	COLOR={"red":(RED_SPACE_SHIP,RED_LASER),"green":(GREEN_SPACE_SHIP,GREEN_LASER),"blue":(BLUE_SPACE_SHIP,BLUE_LASER)}
	def __init__(self,x,y,color,health=100):
		super().__init__(x,y,health)
		self.ship_img,self.laser_img=self.COLOR[color]
		self.mask=pygame.mask.from_surface(self.ship_img)
	def move(self,vel):
		self.y+=vel 
	def shoot(self):
		if self.cool_down_counter==0:
			laser=Laser(self.x-20,self.y,self.laser_img)
			self.lasers.append(laser)
			self.cool_down_counter=1

class Player(Ship):
	def __init__(self,x,y,health=100):
		super().__init__(x,y,health)
		self.ship_img=YELLOW_SPACE_SHIP
		self.laser_img=YELLOW_LASER
		self.mask=pygame.mask.from_surface(self.ship_img)
		self.max_health=health

	def move_lasers(self,vel,objs):
		self.cool_down()
		for laser in self.lasers:
			laser.move(vel)
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			else:
				for obj in objs:
					if laser.collision(obj):
						objs.remove(obj)
						if laser in self.lasers:
							self.lasers.remove(laser)
	def draw(self,window):
		super().draw(window)
		pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 20))
		pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 20))


def collide(obj1,obj2):
	offset_x=obj1.x-obj2.x 
	offset_y=obj1.y-obj2.y
	return obj2.mask.overlap(obj1.mask,(offset_x,offset_y)) !=None

def main():
	run = True
	FPS = 60
	level=0
	lives=10
	main_font=pygame.font.SysFont("Arial Black",50)
	lost=False
	lost_count=0
	enemies=[]
	wave_length=5
	num_of_enemies=5
	enemy_vel=2
	clock=pygame.time.Clock()
	player=Player(300,550)
	def redraw():
		WIN.blit(BACKGROUND,(0,0))
		#draw text
		level_label=main_font.render('Level : {} '.format(level),1,WHITE)
		lives_label=main_font.render('Lives : {} '.format(lives),1,WHITE)
		WIN.blit(lives_label,(10,10))
		WIN.blit(level_label,(WIDTH-level_label.get_width()-10,10))
		player.draw(WIN)
		if lost:
			lost_label=lost_font.render("You Lost !",1,(WHITE))
			WIN.blit(lost_label,(WIDTH/2-lost_label.get_width()/2,350))

		for enemy in enemies:
			enemy.draw(WIN)
		pygame.display.update()

	while run:
		clock.tick(FPS)
		redraw()
		if lives<=0 or player.health<=0:
			lost=True
			lost_count+=1

		if lost:
			if lost_count>FPS*3:
				run=False
			else:
				continue

		if len(enemies)==0:
			level+=1
			num_of_enemies+=1
			wave_length=random.randint(level//2 , num_of_enemies)
			for i in range(wave_length):
				enemy=Enemy(random.randrange(50,WIDTH-100),random.randrange(-500,-100),random.choice(("red","blue","green")))
				enemies.append(enemy)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				quit()

		keys=pygame.key.get_pressed()
		if keys[pygame.K_LEFT] and player.x-VEL>0:
			player.x-=VEL
		if keys[pygame.K_RIGHT] and player.x+VEL+player.get_height()<WIDTH:
			player.x+=VEL
		if keys[pygame.K_UP] and player.y-VEL>0:
			player.y-=VEL		
		if keys[pygame.K_DOWN] and player.y+VEL+player.get_height()<HEIGHT:
			player.y+=VEL
		if keys[pygame.K_SPACE]:
			player.shoot()

		for enemy in enemies:
			enemy.move(enemy_vel)
			enemy.move_lasers(enemy_shoot_vel,player)
			if random.randrange(1,120) == 1:
				enemy.shoot()

			if collide(enemy,player):
				player.health-=10
				enemies.remove(enemy)

			elif enemy.y+enemy.get_height()>HEIGHT:
				lives-=1
				enemies.remove(enemy)

		player.move_lasers(-player_shoot_vel,enemies)	
	
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BACKGROUND, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
main_menu()