import pygame
import random
import math
import time
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

IMAGE_FOLDER = "assets/"
AUDIO_FOLDER = "audio/"

icon = pygame.image.load(IMAGE_FOLDER + 'pixel_ship_blue_small.png')
pygame.display.set_icon(icon)

background = pygame.image.load(IMAGE_FOLDER + 'background-black.png')
background = pygame.transform.scale(background, (800, 600))

mixer.music.load(AUDIO_FOLDER + 'background.wav')
mixer.music.play(-1)

player_img = pygame.image.load(IMAGE_FOLDER + 'pixel_ship_blue_small.png')
player_x = 370
player_y = 480
player_x_change = 0

enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

enemy_images = [
    IMAGE_FOLDER + 'pixel_ship_red_small.png',
    IMAGE_FOLDER + 'pixel_ship_green_small.png',
    IMAGE_FOLDER + 'pixel_ship_yellow.png'
]
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load(random.choice(enemy_images)))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(2)
    enemy_y_change.append(30)

bullet_img = pygame.image.load(IMAGE_FOLDER + 'pixel_laser_blue.png')
bullet_x = 0
bullet_y = 480
bullet_y_change = 10
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def restart_text():
    restart = font.render("Press 'R' to Restart", True, (255, 255, 255))
    screen.blit(restart, (250, 350))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    return distance < 27

def reset_game():
    global score_value, bullet_state, bullet_y, player_x, enemy_x, enemy_y
    score_value = 0
    bullet_state = "ready"
    bullet_y = 480
    player_x = 370
    for i in range(num_of_enemies):
        enemy_x[i] = random.randint(0, 736)
        enemy_y[i] = random.randint(50, 150)

running = True
game_over = False
game_over_time = 0

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE and not game_over:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound(AUDIO_FOLDER + 'laser.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

            if event.key == pygame.K_r and game_over:
                reset_game()
                game_over = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    if not game_over:
        player_x += player_x_change
        player_x = max(0, min(736, player_x))

        for i in range(num_of_enemies):
            if enemy_y[i] > 440:
                game_over_time = time.time()
                game_over = True
                break

            enemy_x[i] += enemy_x_change[i]
            if enemy_x[i] <= 0:
                enemy_x_change[i] = 2
                enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] >= 736:
                enemy_x_change[i] = -2
                enemy_y[i] += enemy_y_change[i]

            if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
                explosion_sound = mixer.Sound(AUDIO_FOLDER + 'explosion.wav')
                explosion_sound.play()
                bullet_y = 480
                bullet_state = "ready"
                score_value += 1
                enemy_x[i] = random.randint(0, 736)
                enemy_y[i] = random.randint(50, 150)

            enemy(enemy_x[i], enemy_y[i], i)

        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change
            if bullet_y <= 0:
                bullet_y = 480
                bullet_state = "ready"

        player(player_x, player_y)
        show_score(text_x, text_y)

    else:
        game_over_text()
        restart_text()
        if time.time() - game_over_time > 5:
            running = False

    pygame.display.update()
