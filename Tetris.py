import pygame, sys
from game import Game
from colors import Colors

#100 points for a single line clear
#300 ponits for a double line clear
#500 points for a triple line clear
#1 point for each move down by the player

pygame.init() 

title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.red)

score_rect = pygame.Rect(360, 55, 150, 60) #320 x axis , 55 y axis ,170 width
next_rect = pygame.Rect(360, 215, 150, 180)

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
            if event.key == pygame.K_LEFT or event.key == pygame.K_a and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN or event.key == pygame.K_s and game.game_over == False:
                game.move_down()
                game.update_score(0, 1)
            if event.key == pygame.K_UP or event.key == pygame.K_w and game.game_over == False:
                game.rotate()
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()
            

    #Drawing
    score_value_surface = title_font.render(str(game.score), True, Colors.white)

    screen.fill(Colors.dark_blue) #background color
    screen.blit(score_surface, (395, 20, 50, 50)) #blit == block image trnasfer # (365, 20, 50, 50)
    screen.blit(next_surface, (405, 180, 50, 50))

    if game.game_over == True:
        screen.blit(game_over_surface, (350, 450, 50, 50))

    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx,
                                                                  centery =score_rect.centery))
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)

    pygame.display.update() #update screen
    clock.tick(60) #the game will run at 60 frames per secondSddd