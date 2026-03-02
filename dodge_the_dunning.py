import pygame
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

smartphone_img = pygame.image.load('assets/smartphone.png').convert_alpha()
invoice_img = pygame.image.load('assets/invoice.png').convert_alpha()
av_user_img = pygame.image.load('assets/avarege_user.png').convert_alpha()
bg_img = pygame.image.load('assets/office_background.png').convert()

smartphone_sprite = pygame.transform.scale(smartphone_img, (60, 60))
invoice_sprite = pygame.transform.scale(invoice_img, (60, 60))
av_user_sprite = pygame.transform.scale(av_user_img, (100, 100))
bg_sprite = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

class FallingItem:
    def __init__(self):
        self.size = 50
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = random.randint(4, 8)
        self.type = random.choice(["GOOD", "BAD"])
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def fall(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, surface):
        sprite = smartphone_sprite if self.type == "GOOD" else invoice_sprite
        surface.blit(sprite, (self.x, self.y))

player_width = 100
player_height = 120
player_x = WIDTH // 2
player_y = HEIGHT - player_height
player_speed = 10
score = 0

all_items = []

pygame.font.init()
score_font = pygame.font.SysFont('Arial', 32, True)

time_limit = 60  
start_ticks = pygame.time.get_ticks() 

running = True
while running:
    screen.blit(bg_sprite, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = max(0, time_limit - seconds_passed)

    if time_left <= 0:
        print("Time's up!")
        running = False 

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_d] and player_x < WIDTH - player_width:
        player_x += player_speed
    
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Spawns only if there are fewer than 3 on screen AND a random chance hits
    if len(all_items) < 3 and random.randint(1, 30) == 1:
        all_items.append(FallingItem())

    # Update and Draw Items
    for item in all_items[:]:
        item.fall()
        item.draw(screen)

        # Collision Check
        if player_rect.colliderect(item.rect):
            if item.type == "GOOD":
                score += 1
            else:
                score -= 2
            all_items.remove(item)

        # Remove if off-screen
        elif item.y > HEIGHT:
            all_items.remove(item)

    # player
    screen.blit(av_user_sprite, (player_x, player_y))

    # points
    score_text = score_font.render(f"PROFIT: ${score * 100}", True, (255, 215, 0))
    screen.blit(score_text, (20, 20))

    #time
    timer_text = score_font.render(f"Time Left: {int(time_left)}s", True, (255, 255, 255))
    screen.blit(timer_text, (20, 60))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()