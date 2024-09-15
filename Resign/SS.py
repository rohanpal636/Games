import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT = pygame.font.SysFont('Arial', 30)
OBSTACLE_SIZE = (50, 50)
PLAYER_SIZE = (50, 50)
OBSTACLE_SPEED = 5
PLAYER_SPEED = 7

# Load images
player_img = pygame.image.load('assets/bird.png')
player_img = pygame.transform.scale(player_img, PLAYER_SIZE)

obstacle_img = pygame.image.load('assets/pipe.png')
obstacle_img = pygame.transform.scale(obstacle_img, OBSTACLE_SIZE)

background_img = pygame.image.load('assets/background.png')
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Game variables
player_rect = player_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70))
obstacles = []
score = 0

# Function to create obstacles
def create_obstacle():
    x_pos = random.randint(0, SCREEN_WIDTH - OBSTACLE_SIZE[0])
    obstacle = pygame.Rect(x_pos, -OBSTACLE_SIZE[1], *OBSTACLE_SIZE)
    return obstacle

# Function to move obstacles
def move_obstacles(obstacles):
    for obstacle in obstacles:
        obstacle.y += OBSTACLE_SPEED
    return [obstacle for obstacle in obstacles if obstacle.y < SCREEN_HEIGHT]

# Function to check collisions
def check_collision(player_rect, obstacles):
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            return True
    return False

# Function to display score
def display_score(score):
    score_surface = FONT.render(f"Score: {score}", True, WHITE)
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(score_surface, score_rect)

# Game setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Main game loop
obstacle_event = pygame.USEREVENT
pygame.time.set_timer(obstacle_event, 1500)
game_active = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_rect.x += PLAYER_SPEED

    screen.blit(background_img, (0, 0))

    if game_active:
        # Update obstacles
        if pygame.event.get(obstacle_event):
            obstacles.append(create_obstacle())

        obstacles = move_obstacles(obstacles)

        # Check collision
        if check_collision(player_rect, obstacles):
            game_active = False

        # Draw player
        screen.blit(player_img, player_rect)

        # Draw obstacles
        for obstacle in obstacles:
            screen.blit(obstacle_img, obstacle)

        # Update score
        score += 1
        display_score(score)

    else:
        # Game Over screen
        game_over_surface = FONT.render('Game Over', True, RED)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(game_over_surface, game_over_rect)

        final_score_surface = FONT.render(f"Final Score: {score}", True, WHITE)
        final_score_rect = final_score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(final_score_surface, final_score_rect)

        restart_surface = FONT.render('Press SPACE to Retry', True, GREEN)
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        screen.blit(restart_surface, restart_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # Restart the game
            player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70)
            obstacles = []
            score = 0
            game_active = True

    pygame.display.update()
    clock.tick(30)
