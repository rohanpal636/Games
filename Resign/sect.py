import pygame
import random


pygame.init()


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = pygame.font.SysFont('Arial', 40)
MILESTONES = [10, 20, 30, 40, 50]  

background_img = pygame.image.load('assets/background.png')
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird_img = pygame.image.load('assets/bird.png')
bird_img = pygame.transform.scale(bird_img, (50, 35))  

pipe_img = pygame.image.load('assets/pipe.png')
pipe_img = pygame.transform.scale(pipe_img, (150, 300))  


flap_sound = pygame.mixer.Sound('assets/flap.wav')
hit_sound = pygame.mixer.Sound('assets/hit.wav')
score_sound = pygame.mixer.Sound('assets/score.wav')
celebration_sound = pygame.mixer.Sound('assets/celebration.wav')


gravity = 0.25
bird_movement = 0
pipe_gap = 200  
pipe_speed = 3  
bird_rect = bird_img.get_rect(center=(50, SCREEN_HEIGHT // 2))
score = 0
high_score = 0
milestones_reached = set()



def create_pipe():
    pipe_height = random.randint(150, 350)  
    pipe_top = pygame.Rect(SCREEN_WIDTH + 50, 0, 50, pipe_height)
    pipe_bottom = pygame.Rect(SCREEN_WIDTH + 50, pipe_height + pipe_gap, 50, SCREEN_HEIGHT - pipe_height - pipe_gap)
    return pipe_top, pipe_bottom


def move_pipes(pipes):
    for pipe in pipes:
        pipe.left -= pipe_speed
    return [pipe for pipe in pipes if pipe.right > 0]


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        hit_sound.play()
        return False
    return True


def display_score(score, high_score, game_over=False):
    score_surface = FONT.render(f"Score: {int(score)}", True, WHITE)
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(score_surface, score_rect)

    if game_over:
        high_score_surface = FONT.render(f"High Score: {int(high_score)}", True, WHITE)
        high_score_rect = high_score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(high_score_surface, high_score_rect)

        game_over_surface = FONT.render('Game Over', True, WHITE)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(game_over_surface, game_over_rect)

        retry_surface = FONT.render('Press SPACE to Retry', True, WHITE)
        retry_rect = retry_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(retry_surface, retry_rect)

def restart_game():
    global bird_movement, bird_rect, gravity, milestones_reached
    bird_rect.center = (50, SCREEN_HEIGHT // 2)
    bird_movement = 0
    gravity = 0.25
    milestones_reached = set()
    return 0, [], True


def main_menu():
    screen.fill(BLACK)
    title_surface = FONT.render('Flappy Bird', True, WHITE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(title_surface, title_rect)

    start_surface = FONT.render('Press SPACE to Start', True, WHITE)
    start_rect = start_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(start_surface, start_rect)

    pygame.display.update()


def celebration_effect():
    for _ in range(5):  
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2 + 100)
        for _ in range(20):  
            pygame.draw.circle(screen, RED, (x, y), random.randint(5, 10))
            pygame.display.update()
            pygame.time.wait(50)  


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pipes = []
game_active = False
start_game = False
spawn_pipe_event = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe_event, 1200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not start_game:
                    start_game = True
                    game_active = True
                elif game_active:
                    bird_movement = 0
                    bird_movement -= 7
                    flap_sound.play()
                else:
                    
                    score, pipes, game_active = restart_game()

        if event.type == spawn_pipe_event and game_active:
            pipes.extend(create_pipe())

    screen.blit(background_img, (0, 0))

    if start_game:
        if game_active:
            
            gravity = 0.25 + score / 1000
            bird_movement += gravity
            bird_rect.centery += bird_movement
            screen.blit(bird_img, bird_rect)

            
            pipes = move_pipes(pipes)
            for pipe in pipes:
                screen.blit(pipe_img, pipe)

            
            game_active = check_collision(pipes)

           
            for pipe in pipes:
                if pipe.centerx == bird_rect.centerx:
                    score += 1
                    score_sound.play()
                    if score in MILESTONES and score not in milestones_reached:
                        milestones_reached.add(score)
                        celebration_sound.play()
                        celebration_effect()

            display_score(score, high_score)
        else:
            high_score = max(score, high_score)
            display_score(score, high_score, game_over=True)
            main_menu()
    else:
        main_menu()

    pygame.display.update()
    clock.tick(60)
