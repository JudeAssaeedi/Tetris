import pygame, sys
from game import Game

pygame.init() 

title_front = pygame.font("Andalus", 40)

screen = pygame.display.set_mode((530 ,620)) #350 = width 600 = height
pygame.display.set_caption("Testris")

clock = pygame.time.Clock() #how fast the game will run (frame rate)

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.game_over == True:
                game.game_over = False
                game.reset()
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
            if event.key == pygame.K_a and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_d and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_s and game.game_over == False:
                game.move_down()
            if event.key == pygame.K_w and game.game_over == False:
                game.rotate()
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()
            

    #Drawing
    screen.fill(dark_blue) #background color
    game.draw(screen)

    pygame.display.update() #update screen
    clock.tick(60) #the game will run at 60 frames per secondSddd