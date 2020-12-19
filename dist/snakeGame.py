import pygame as _P
import random
import os


# initializing pygame
_P.mixer.init()
_P.init()

# game related colors
_White = (255 , 255 , 255)
_Black = (0 ,0 ,0)
_Red = (255 , 0, 0)
_Green = "#54BF6D"



#Fonts
mons = "Montserrat"

# gameWindow size
_Height = 700
_Width = 900


# setting up game window
_P.display.set_caption("Snake game by Dulen")
_Game_Window = _P.display.set_mode((_Width , _Height))


# function to plot texts
def text_plot(text , color, x , y , font_fmaily):
	font = _P.font.SysFont(font_fmaily, 30)
	screen_font = font.render(text, True, color)
	_Game_Window.blit(screen_font, [x, y])


# #image
Game_back = _P.image.load("gameBack.jpg")
Game_back = _P.transform.scale(Game_back ,( _Width , _Height ))

Welcome_back = _P.image.load("welcomePage.jpg")
Welcome_back = _P.transform.scale(Welcome_back ,( _Width , _Height ))

# function to draw a snake
def Snake(surface , color , coordinate , size):
	for x , y in coordinate:
		_P.draw.rect(surface , color , [x , y , size , size] )

# welcome window
def Welcome():
	_Game_Exit = False
	_P.mixer.music.load("music/WelcomeMusic.mp3")
	_P.mixer.music.play()
	while not _Game_Exit:
		_Game_Window.fill(_White)
		_Game_Window.blit(Welcome_back , (0,0))
		text_plot("WELCOME !" , _Black , 350 , 300 , mons)
		text_plot("Press Enter To Play" , _Black, 300 , 350 , mons)
		for event in _P.event.get():
			if event.type == _P.QUIT:
				_Game_Exit = True
			if event.type == _P.KEYDOWN:
				if event.key == _P.K_RETURN:
					Game_loop()
		_P.display.update()
		Clock.tick(40)

Clock = _P.time.Clock()
# game loop function
def Game_loop():
	_P.mixer.music.load("music/gameMusic.mp3")
	_P.mixer.music.play(-1)
	# game variables
	snake_list = []
	snake_length = 1

	snake_size = 15
	snake_x = 50
	snake_y = 100
	food_x = random.randint(100, _Width-100)
	food_y = random.randint(100, _Height-100)
	food_size = 10

	velocity_x = 0
	velocity_y = 0

	_Game_Over = False
	_Game_Exit = False

	_FPS = 40
	_SCORE = 0
	# High score
	if not os.path.exists("highScore.txt"):
		with open("highScore.txt", 'w') as E:
			E.write("0")
	with open("highScore.txt", 'r') as H:
		_HEIGHT_SCORE = H.read()



	# game loop
	while not _Game_Exit:
		if _Game_Over:
			with open("highScore.txt", 'w') as W:
				W.write(str(_HEIGHT_SCORE))
			_Game_Window.fill(_White)

			text_plot("Game over! Press enter to continue " , _Red , 200 , 300 , mons)
			if _SCORE > int(_HEIGHT_SCORE) :
				text_plot(f"SCORE : {str(_SCORE)}  NEW HIGH SCORE : {str(_HEIGHT_SCORE)}" , _Red , 250 , 350 , mons)
			else:
				text_plot(f"SCORE : {str(_SCORE)}", _Red, 350, 350, mons)
			_P.display.update()

			for event in _P.event.get():
				# game conditions
				if event.type == _P.QUIT:
					_Game_Exit = True

				if event.type == _P.KEYDOWN:
					if event.key == _P.K_RETURN:
						Game_loop()

		else:
			for event in _P.event.get():
				# game conditions
				if event.type == _P.QUIT:
					_Game_Exit = True

				if event.type == _P.KEYDOWN:

					if event.key == _P.K_RIGHT:
						velocity_x = 5
						velocity_y = 0
					if event.key == _P.K_LEFT:
						velocity_x = -5
						velocity_y = 0
					if event.key == _P.K_UP:
						velocity_y = -5
						velocity_x = 0
					if event.key == _P.K_DOWN:
						velocity_y = 5
						velocity_x = 0


				# defining the velocity of the snake
				snake_x += velocity_x
				snake_y += velocity_y

				# if our snake eats the food
				if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
					food_eat = _P.mixer.Sound("music/eat_food.mp3")
					food_eat.play()
					food_x = random.randint(100, _Width - 200)
					food_y = random.randint(100, _Height - 200)

					snake_length += 5
					_SCORE += 1
					if _SCORE > int(_HEIGHT_SCORE):
						_HEIGHT_SCORE = _SCORE

				# snake had
				snake_head = []
				snake_head.append(snake_x+1)
				snake_head.append(snake_y+1)
				snake_list.append(snake_head)

				if len(snake_list) > snake_length:
					del snake_list[0]


				#Game Over
				if snake_x > _Width or snake_x < 0 or snake_y > _Height or snake_y < 0:
					_Game_Over = True
					_P.mixer.music.load("music/Game_End.mp3")
					_P.mixer.music.play()

				if snake_head in snake_list[:-1]:
					_Game_Over = True
					_P.mixer.music.load("music/Game_End.mp3")
					_P.mixer.music.play()

				# filling color to game
				_Game_Window.fill(_White)
				_Game_Window.blit(Game_back, (0, 0))

				# display score
				text_plot(f"SCORE : {str(_SCORE)}    HIGH SCORE : {str(_HEIGHT_SCORE)}" , _Black , 50 , 30 , mons)

				# plotting food
				_P.draw.rect(_Game_Window , _Red ,[food_x , food_y , food_size ,food_size] )

				# making the snake
				Snake(_Game_Window , _Green ,snake_list, snake_size)
			Clock.tick(_FPS)
			_P.display.update()


	_P.quit()
	quit()

Welcome()
