"""
Snake Eater
Made with PyGame
"""

import pygame, sys, time, random


# Difficulty settings - speed
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 5


# snake segment size - default 10
snake_segment_size = 10

# window size
frame_size_x = 720
frame_size_y = 480


# errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [100-snake_segment_size, 50], [100-(2*snake_segment_size), 50]]

food_pos = [random.randrange(1, (frame_size_x//snake_segment_size)) * snake_segment_size, random.randrange(1, (frame_size_y//snake_segment_size)) * snake_segment_size]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# game Over
def game_over():
    play_sound(died_sound)
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()


yum_sound = pygame.mixer.Sound("chomp.wav")
died_sound = pygame.mixer.Sound("blip.wav")
blurp_sound = pygame.mixer.Sound("blurp_x.wav")
bloop_sound = pygame.mixer.Sound("bloop_x.wav")

def play_sound(the_sound):
    pygame.mixer.Sound.play(the_sound)
    pygame.mixer.music.stop()


# main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # key is pressed
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
                play_sound(blurp_sound)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
                play_sound(blurp_sound)
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
                play_sound(bloop_sound)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
                play_sound(bloop_sound)

            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                play_sound(died_sound)

    # snake cannot change direction onto itself
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # moving the snake
    if direction == 'UP':
        snake_pos[1] -= snake_segment_size
    if direction == 'DOWN':
        snake_pos[1] += snake_segment_size
    if direction == 'LEFT':
        snake_pos[0] -= snake_segment_size
    if direction == 'RIGHT':
        snake_pos[0] += snake_segment_size

    # snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        play_sound(yum_sound)
        food_spawn = False
    else:
        snake_body.pop()

    # spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//snake_segment_size)) * snake_segment_size, random.randrange(1, (frame_size_y//snake_segment_size)) * snake_segment_size]
    food_spawn = True

    # GFX
    game_window.fill(black)
    for pos in snake_body:
        # snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], snake_segment_size, snake_segment_size))

    # snake food
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], snake_segment_size, snake_segment_size))

    # game over conditions
    # getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-snake_segment_size:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-snake_segment_size:
        game_over()
    # touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, white, 'consolas', 20)
    # refresh game screen
    pygame.display.update()
    # refresh rate
    fps_controller.tick(difficulty)
