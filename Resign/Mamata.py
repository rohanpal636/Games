import pygame
import random
import sys
import time
import math
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 450
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT_PATH = 'assets2/NotoSansBengali-ExtraBold.ttf'
FONT = pygame.font.Font(FONT_PATH, 30)
BOLD_FONT = pygame.font.Font(FONT_PATH, 30)
#FONT.set_script("Deva")
#MILESTONES = [100, 150, 200]

background_img = pygame.image.load('assets2/BG2.png')
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird_img = pygame.image.load('assets2/mamata.jpg')
bird_img = pygame.transform.scale(bird_img, (80, 45))

pipe_img = pygame.image.load('assets2/chair2.PNG')
pipe_img = pygame.transform.scale(pipe_img, (120, 180))
floor_img = pygame.image.load("img_50.png")
floor_x = 0

pygame.mixer.music.load('assets2/AarKobe.mp3')
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_pos(13)

hit_sound = pygame.mixer.Sound('assets/hit.wav')
score_sound = pygame.mixer.Sound('assets/score.wav')
celebration_sound = pygame.mixer.Sound('assets/celebration.wav')

hit_sound.set_volume(0.1)
score_sound.set_volume(0.1)
celebration_sound.set_volume(0.01)

gravity = 0.2
bird_movement = 0
pipe_gap = 180
pipe_speed = 6
bird_rect = bird_img.get_rect(center=(20, SCREEN_HEIGHT // 2))
score = 0
high_score = 0
milestones_reached = set()

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def draw_gradient_background(surface, offset):
    for y in range(surface.get_height()):
        color1 = (
            clamp(int(128 + 127 * math.sin(offset / 100)), 0, 255),
            clamp(int(0 + 127 * math.cos(offset / 100)), 0, 255),
            128
        )
        color2 = (
            clamp(int(255 - 127 * math.sin(offset / 100)), 0, 255),
            clamp(int(182 - 127 * math.cos(offset / 100)), 0, 255),
            193
        )
        color = (
            clamp(int(color1[0] * (1 - y / surface.get_height()) + color2[0] * (y / surface.get_height())), 0, 255),
            clamp(int(color1[1] * (1 - y / surface.get_height()) + color2[1] * (y / surface.get_height())), 0, 255),
            clamp(int(color1[2] * (1 - y / surface.get_height()) + color2[2] * (y / surface.get_height())), 0, 255)
        )
        pygame.draw.line(surface, color, (0, y), (surface.get_width(), y))

def render_text_with_outline(text, font, color, outline_color, surface, position):
    outline_surface = font.render(text, True, outline_color)
    outline_rect = outline_surface.get_rect(center=position)
    outline_offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    for offset in outline_offsets:
        outline_surface = font.render(text, True, outline_color)
        outline_rect = outline_surface.get_rect(center=(position[0] + offset[0], position[1] + offset[1]))
        surface.blit(outline_surface, outline_rect)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    surface.blit(text_surface, text_rect)

def display_score(score, high_score, game_over=False):
    if not game_over:
        score_text = f"Crimes: {int(score)}"
        render_text_with_outline(score_text, BOLD_FONT, WHITE, BLACK, screen, (SCREEN_WIDTH // 2, 50))
    else:
        high_score_text = f"Most Crimes: {int(high_score)}"
        render_text_with_outline(high_score_text, BOLD_FONT, WHITE, BLACK, screen,
                                 (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

def create_pipe():
    pipe_height = random.randint(200, 400)
    pipe_top = pipe_img.get_rect(midbottom=(SCREEN_WIDTH + 50, pipe_height - pipe_gap // 2))
    pipe_bottom = pipe_img.get_rect(midtop=(SCREEN_WIDTH + 50, pipe_height + pipe_gap // 2))
    return pipe_top, pipe_bottom

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return [pipe for pipe in pipes if pipe.right > 0]

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= SCREEN_HEIGHT:
        hit_sound.play()
        return False
    return True

def update_score(pipes):
    global score
    for pipe in pipes:
        if pipe.centerx < bird_rect.centerx < pipe.centerx + pipe_speed and pipes.index(pipe) % 2 == 1:
            score += 1
            score_sound.play()

def restart_game():
    global bird_movement, bird_rect, gravity, milestones_reached, score, pipes, game_over_start_time
    bird_rect.center = (50, SCREEN_HEIGHT // 2)
    bird_movement = 0
    gravity = 0.25
    milestones_reached = set()
    score = 0
    pipes = []
    game_over_start_time = pygame.time.get_ticks()
    return True

def draw_multiline_text(text, font, color, surface, position):
    lines = text.split(' ')
    max_line_length = SCREEN_WIDTH // font.size(' ')[0]
    lines_to_render = []
    line = ''

    for word in lines:
        if font.size(line + word)[0] <= SCREEN_WIDTH:
            line += word + ' '
        else:
            lines_to_render.append(line)
            line = word + ' '

    lines_to_render.append(line)

    y_offset = position[1] - len(lines_to_render) * (font.get_height() // 2)
    for line in lines_to_render:
        text_surface = font.render(line.strip(), True, color)
        text_rect = text_surface.get_rect(center=(position[0], y_offset))
        surface.blit(text_surface, text_rect)
        y_offset += font.get_height()

def celebration_effect():
    screen.blit(background_img, (0, 0))
    draw_gradient_background(screen, pygame.time.get_ticks())
    #screen.fill((128, 0, 128))

    screen.fill(BLACK)
    text = 'Sorry! You cannot resign... নাহলে দেবাংশু দরজায় শুয়ে পড়বে'
    draw_multiline_text(text, FONT, WHITE, screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(500)

    image = pygame.image.load('assets2/debangshu.png')
    image_width, image_height = image.get_size()
    scale_factor = SCREEN_WIDTH / image_width
    new_height = int(image_height * scale_factor)
    image = pygame.transform.scale(image, (SCREEN_WIDTH, new_height))

    image_rect = image.get_rect(midtop=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(image, image_rect)

    pygame.display.update()
    pygame.time.wait(2000)

    display_restart_option()

def display_restart_option():
    screen.blit(background_img, (0, 0))
   # draw_gradient_background(screen, pygame.time.get_ticks()/10)
    screen.fill(BLACK)

    restart_text_line1 = 'Say জয় বাংলা'
    restart_surface_line1 = FONT.render(restart_text_line1, True, WHITE)
    restart_rect_line1 = restart_surface_line1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(restart_surface_line1, restart_rect_line1)

    restart_text_line2 = 'to Restart the Game'
    restart_surface_line2 = FONT.render(restart_text_line2, True, WHITE)
    restart_rect_line2 = restart_surface_line2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    screen.blit(restart_surface_line2, restart_rect_line2)

    pygame.display.update()

    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_for_restart = False
                    return

def show_developer_screen():
    screen.blit(background_img, (0, 0))
    draw_gradient_background(screen, pygame.time.get_ticks())
    screen.fill((128, 0, 128))
    screen.fill(BLACK)
    dev_surface = FONT.render('Developed by Rohan Pal', True, WHITE)
    dev_rect = dev_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(dev_surface, dev_rect)
    pygame.display.update()
    pygame.time.wait(1000)

def main_menu():
    screen.blit(background_img,(0,0))
    draw_gradient_background(screen, pygame.time.get_ticks())
    screen.fill(BLACK)
    title_surface = FONT.render('The Lady Hitler', True, WHITE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(title_surface, title_rect)
    start_surface = FONT.render('Press SPACE to Resign', True, WHITE)
    start_rect = start_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(start_surface, start_rect)
    pygame.display.update()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pipes = []
game_active = False
start_game = False
spawn_pipe_event = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe_event, 1200)

game_over_start_time = 0  # Initialize the game over start time

show_developer_screen()

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
                else:
                    game_active = restart_game()

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
                    # if score in MILESTONES and score not in milestones_reached:
                    #     milestones_reached.add(score)
                    #     celebration_sound.play()
                    #     #celebration_effect()
            display_score(score, high_score)
        else:
            if pygame.time.get_ticks() - game_over_start_time >= 5000:  # 3 seconds delay
                high_score = max(score, high_score)
                #celebration_effect2()
                #display_restart_option2()
                display_score(score, high_score, game_over=True)
                main_menu()
            else:


                celebration_sound.play()
                celebration_effect()
                screen.fill(BLACK)
                text = "Sorry! Your resignation has been declined"
                draw_multiline_text(text, FONT, WHITE, screen, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                display_score(score, high_score, game_over=True)
                pygame.display.update()
                pygame.time.wait(1000)
                pygame.display.update()
    else:
        main_menu()

    pygame.display.update()
    clock.tick(60)
