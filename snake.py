import pygame
import random

# constants
WIDTH, HEIGHT = 1280, 720
SNAKE_BLOCK = 20
SNAKE_SPEED = 15

# colors
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
x1_change, y1_change = 0, 0
snake_List = []
Length_of_snake = 1

# Random Food Location
foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and y1_change == 0:
        x1_change = 0
        y1_change = -SNAKE_BLOCK
    if keys[pygame.K_s] and y1_change == 0:
        x1_change = 0
        y1_change = SNAKE_BLOCK
    if keys[pygame.K_a] and x1_change == 0:
        x1_change = -SNAKE_BLOCK
        y1_change = 0
    if keys[pygame.K_d] and x1_change == 0:
        x1_change = SNAKE_BLOCK
        y1_change = 0

    player_pos.x += x1_change
    player_pos.y += y1_change

    pygame.draw.rect(screen, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
    
    snake_Head = [player_pos.x, player_pos.y]
    snake_List.append(snake_Head)

    # delete snake extra tail
    if len(snake_List) > Length_of_snake:
            del snake_List[0]

    # self-collision check
    for x in snake_List[:-1]:
        if x == snake_Head:
            pygame.quit()

    # boundary wrap-around logic
    if player_pos.x >= WIDTH:
        player_pos.x = 0
    elif player_pos.x < 0:
        player_pos.x = WIDTH - SNAKE_BLOCK

    if player_pos.y >= HEIGHT:
        player_pos.y = 0
    elif player_pos.y < 0:
        player_pos.y = HEIGHT - SNAKE_BLOCK

    our_snake(SNAKE_BLOCK, snake_List)

    pygame.display.flip()
    pygame.display.update()

    # check if snake ate food
    if player_pos.x == foodx and player_pos.y == foody:
        foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
        foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0
        Length_of_snake += 1

    dt = clock.tick(SNAKE_SPEED) / 1000

pygame.quit()