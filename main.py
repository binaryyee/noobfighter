import pygame
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *

#used to initialize the game
pygame.init()

#constants are defined here.
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
FPS = 60

#creates display change the title of the game
displaysurface = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Happy Fighter")

#initializing the classes
class Background(pygame.sprite.Sprite) :
	def __init__(self) :
		super().__init__()
		self.bgimage = pygame.image.load("Background.png")
		self.bgY = 0
		self.bgX = 0
	def render(self) :
		displaysurface.blit(self.bgimage,(self.bgX,self.bgY))

class Ground(pygame.sprite.Sprite) :
	def __init__(self) :
		super().__init__()
		self.image = pygame.image.load("Ground.png")
		self.rect = self.image.get_rect(center = (350, 350))
	def render(self) :
		displaysurface.blit(self.image,(self.rect.x,self.rect.y))

class Player(pygame.sprite.Sprite) :
	def __init__(self) :
		super().__init__()
		self.image = pygame.image.load("Player_Sprite_R.png")
		self.rect = self.image.get_rect()

		#position and direction
		self.vx = 0
		self.pos = vec((340,240))
		self.vel = vec(0,0)
		self.acc = vec(0,0)
		self.direction = "RIGHT"
		self.jumping = False
		self.running = False
		self.move_frame = 0

		#Combat
		self.attacking = False
		self.cooldown = False
		self.attack_frame = 0

	def player_hit(self) :
		if self.cooldown == False :
			self.cooldown = True #Enable the cooldown
			pygame.time.set_timer(hit_cooldown,1000) #Resets the cooldown

			print("hit")
			pygame.display.update()

	def update(self) :
		#check for collision
		hits = pygame.sprite.spritecollide(self,Playergroup,False)

		#Activates upon either of the two expressions being trur
		if hits and player.attacking == True:
			self.kill()
			#print("Enemy Killed")
		#If collision has occoured and player not in attacking mode
		elif hits and player.attacking == False :
			player_hit()

	def move(self) :
		#keep a constant acc of 0.5 in the downward direction (gravity)
		self.acc = vec(0,0.5)
		#will set running to False if the player has slowed down to  a certian level
		if abs(self.vel.x) > 0.3:
			self.running = True
		else :
			self.running = False

		#returns the current key pressed
		pressed_keys = pygame.key.get_pressed()

		#acclerate the player in the direction 
		if pressed_keys[K_LEFT] :
			self.acc.x = -ACC
		if pressed_keys[K_RIGHT] :
			self.acc.x = ACC

		#Formulas to calc velocity and frictions
		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc #updates pos

		#Wraping players from one place to other so it not go outside screen
		if self.pos.x > WIDTH :
			self.pos.x = 0
		if self.pos.x < 0 :
			self.pos.x = WIDTH

		self.rect.midbottom = self.pos #updates rect with new pos


		# Run animation for the RIGHT
		run_ani_R = [pygame.image.load("Player_Sprite_R.png"), pygame.image.load("Player_Sprite2_R.png"),
		             pygame.image.load("Player_Sprite3_R.png"),pygame.image.load("Player_Sprite4_R.png"),
		             pygame.image.load("Player_Sprite5_R.png"),pygame.image.load("Player_Sprite6_R.png"),
		             pygame.image.load("Player_Sprite_R.png")]
 
		# Run animation for the LEFT
		run_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Sprite2_L.png"),
		             pygame.image.load("Player_Sprite3_L.png"),pygame.image.load("Player_Sprite4_L.png"),
		             pygame.image.load("Player_Sprite5_L.png"),pygame.image.load("Player_Sprite6_L.png"),
		             pygame.image.load("Player_Sprite_L.png")]
	
		# Move the character to the next frame if conditions are met 
		if self.jumping == False and self.running == True:  
		      if self.vel.x > 0:
		            self.image = run_ani_R[self.move_frame]
		            self.direction = "RIGHT"
		      elif self.vel.y < 1:
		            self.image = run_ani_L[self.move_frame]
		            self.direction = "LEFT"
		      self.move_frame += 1

		#Returns to base frame
		if abs(self.vel.x) < 0.2 and self.move_frame != 0 :
			self.move_frame = 0
			if self.direction == "RIGHT" :
				self.image = run_ani_R[self.move_frame]
			elif self.direction == "LEFT" :
				self.image = run_ani_L[self.move_frame]

	def gravity_check(self) :
		hits = pygame.sprite.spritecollide(player,ground_group,False)
		if self.vel.y > 0 :
			if hits :
				lowest = hits[0]
				if self.pos.y < lowest.rect.bottom :
					self.pos.y = lowest.rect.top + 1
					self.vel.y = 0
					self.jumping = False

	def update(self) :
		#Return to base frame if at end of movement sequence
		if self.move_frame > 6 :
			self.move_frame = 0
			return
	
	def attack(self) :
		#If attack frame has reached end of sequence, return to base frame
		if self.attack_frame > 10 :
			self.attack_frame = 0
			self.attacking = False

		
		#Attack animation from Right 
		attack_ani_R = [pygame.image.load("Player_Sprite_R.png"),pygame.image.load("Player_Attack_R.png"),pygame.image.load("Player_Attack2_R.png"),pygame.image.load("Player_Attack2_R.png"),pygame.image.load("Player_Attack3_R.png"),pygame.image.load("Player_Attack3_R.png"),pygame.image.load("Player_Attack4_R.png"),pygame.image.load("Player_Attack4_R.png"),pygame.image.load("Player_Attack5_R.png"),pygame.image.load("Player_Attack5_R.png"),pygame.image.load("Player_Sprite_R.png")]

		#Attack animation from Left
		attack_ani_L = [pygame.image.load("Player_Sprite_L.png"),pygame.image.load("Player_Attack_L.png"),pygame.image.load("Player_Attack2_L.png"),pygame.image.load("Player_Attack2_L.png"),pygame.image.load("Player_Attack3_L.png"),pygame.image.load("Player_Attack3_L.png"),pygame.image.load("Player_Attack4_L.png"),pygame.image.load("Player_Attack4_L.png"),pygame.image.load("Player_Attack5_L.png"),pygame.image.load("Player_Attack5_L.png"),pygame.image.load("Player_Sprite_L.png")]



		#Check direction for correct animation 
		if self.direction == "RIGHT" :
			self.image = attack_ani_R[self.attack_frame]
		elif self.direction == "LEFT" :
			self.correction()
			self.image = attack_ani_L[self.attack_frame]

		#Update the current attack frame
		self.attack_frame += 1

	def correction(self) :
		#Function is used to correct an error
		#with character position on left attack frames
		if self.attack_frame == 1:
			self.pos.x -= 20
		if self.attack_frame == 10 :
			self.pos.x += 20

	
	def jump(self) :
		self.rect.x += 1

		#check to see if player is in contact with the ground
		hits = pygame.sprite.spritecollide(self,ground_group, False)

		self.rect.x -= 1

		#If touching the ground and currently jumping, cause the player to jump
		if hits and not self.jumping :
			self.jumping = True
			self.vel.y = - 12


class Enemy(pygame.sprite.Sprite) :
	def __init__(self) :
		super().__init__()

		self.image = pygame.image.load("Enemy.png")
		self.rect = self.image.get_rect()
		self.pos = vec(0,0)
		self.vel = vec(0,0)

		self.direction = random.randint(0,1) # 0 for Right, 1 for Left
		self.vel.x = random.randint(2,6)/2 #Randomized Velocity of Enemy

		#Sets the initial positions of the enemy
		if self.direction == 0:
			self.pos.x = 0
			self.pos.y = 235
		if self.direction == 1:
			self.pos.x = 700
			self.pos.y = 250

	def move(self) :
		#Causes the enemy to change directions upon reaching the end of the screen
		if self.pos.x >= (WIDTH-20):
			self.direction = 1
		elif self.pos.x <= 0:
			self.direction = 0

		#updates position with new values
		if self.direction == 0 :
			self.pos.x += self.vel.x 
		if self.direction == 1 :
			self.pos.x -= self.vel.x	

		self.rect.center = self.pos #updates rect

	def render(self) :
		#Displas the enemy on screen
		displaysurface.blit(self.image,(self.pos.x, self.pos.y))

class Castle() :
	def __init__(self) :
		super().__init__()		
		self.hide = False
		self.image = pygame.image.load("castle.png")

	def update(self) :
		if self.hide == False:
			displaysurface.blit(self.image,(400,80))
 

class EventHandler():
	def __init__(self):
		self.enemy_count = 0
		self.battle = False
		self.enemy_generation = pygame.USEREVENT + 1

		self.stage_enemies = []
		for x in range(1,21):
			self.stage_enemies.append(int((x**2/2)+1))

	def next_stage(self):
		self.enemy_count = 0
		print("Stage: " + str(self.stage))
		pygame.time.set_timer(self.enemy_generation, 1500-(50 * self.stage))

	def stage_handler(self) :
		#Code for the Tkinter stage selection window
		self.root = Tk()
		self.root.geometry('200x170')

		button1 = Button(self.root, text = "Twilight Dungeon", width = 18, height = 2, command = self.world1)
		button2 = Button(self.root, text = "Skyward Dungoen", width = 18, height = 2, command = self.world2)
		button3 = Button(self.root, text = "Hell Dungeon", width = 18, height = 2, command = self.world3)

		button1.place(x=40,y=15)
		button2.place(x=40,y=65)
		button3.place(x=40,y=115)

	def world1(self) :
		self.root.destroy()
		pygame.time.set_timer(self.enemy_generation,2000)
		castle.hide = True
		self.battle = True

	def world2(self) :
		self.battle = True

	def world3(self) :
		self.battle = True



#building the objects out of the classes
background = Background()
ground = Ground()
player = Player()
Playergroup = pygame.sprite.Group()
Playergroup.add(player)
ground_group = pygame.sprite.Group()
ground_group.add(ground)
enemy = Enemy()
castle = Castle()
handler = EventHandler()



#The game is controlled here
while True :

	player.gravity_check()
	hit_cooldown = pygame.USEREVENT+1

	for event in pygame.event.get() :
		if event.type == hit_cooldown :
			player.cooldown = False
			pygame.time.set_timer(hit_cooldown,0)

		#will run when close window button is clicked
		if event.type == QUIT :
			pygame.quit()
			sys.exit()

		#for events that occur upon clicking the mouse left click
		if event.type == pygame.MOUSEBUTTONDOWN :
			pass
		
		#Even handling for a range of different key presses
		if event.type == pygame.KEYDOWN :
			if event.key == pygame.K_e and 450 < player.rect.x < 550:
				handler.stage_handler()

			if event.key == pygame.K_n:
				if handler.battle == True and len(Enemies) == 0:
					handler.next_stage()

			if event.key == pygame.K_SPACE :
				player.jump()

			if event.key == pygame.K_RETURN :
				if player.attacking == False :
					player.attack()
					player.attacking = True
		
		if event.type == handler.enemy_generation:
			if handler.enemy_count < handler.stage_enemies[player.stage - 1]:
				enemy = Enemy()
				Enemies.add(enemy)
				handler.enemy_count += 1


		
	#Renders display and background
	background.render()
	ground.render()
	castle.update()
	#Rendering Sprites
	displaysurface.blit(player.image, player.rect)
	#entity.update()
	#entity.move()
	#entity.render()
	enemy.update()
	enemy.move()
	enemy.render()


	#Rendering Player
	player.update()
	if player.attacking == True :
		player.attack()
	player.move()

	pygame.display.update()
	FPS_CLOCK.tick(FPS)


#fix left movement
#backtrack  a bit more if needed

