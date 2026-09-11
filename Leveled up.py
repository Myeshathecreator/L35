import math
import random
from array import array
import pygame

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
PLAYER_START_X = 370
PLAYER_START_Y = 380
ENEMY_START_Y_MIN = 50
ENEMY_START_Y_MAX = 150
ENEMY_SPEED_X = 2
ENEMY_SPEED_Y = 20
BULLET_SPEED_Y = 20
COLLISION_DISTANCE = 27

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def make_sound(start_frequency, end_frequency, duration):
    sample_rate = 44100
    sample_count = int(sample_rate * duration)
    samples = array("h")

    for sample_index in range(sample_count):
        progress = sample_index / max(1, sample_count - 1)
        frequency = start_frequency + (end_frequency - start_frequency) * progress
        volume = 1 - progress
        value = math.sin(2 * math.pi * frequency * sample_index / sample_rate)
        samples.append(int(32767 * 0.35 * volume * value))

    return pygame.mixer.Sound(buffer=samples.tobytes())


def make_coin_sound():
    sample_rate = 44100
    frequencies = (660, 880, 1320)
    note_duration = 0.11
    samples = array("h")

    for frequency in frequencies:
        note_samples = int(sample_rate * note_duration)
        for sample_index in range(note_samples):
            progress = sample_index / max(1, note_samples - 1)
            volume = 1 - progress
            value = math.sin(2 * math.pi * frequency * sample_index / sample_rate)
            samples.append(int(32767 * 0.32 * volume * value))

    return pygame.mixer.Sound(buffer=samples.tobytes())


def make_theme_music():
    sample_rate = 44100
    note_duration = 0.12
    melody = [
        330, 392, 523, 659, 523, 392, 330, 262,
        294, 440, 587, 784, 587, 440, 294, 247,
    ]
    samples = array("h")

    for note_index, frequency in enumerate(melody):
        note_samples = int(sample_rate * note_duration)
        for sample_index in range(note_samples):
            progress = sample_index / max(1, note_samples - 1)
            envelope = min(progress * 20, 1, (1 - progress) * 10)
            time = sample_index / sample_rate
            lead = math.sin(2 * math.pi * frequency * time)
            harmony = math.sin(2 * math.pi * frequency * 2 * time) * 0.35
            bass = math.sin(2 * math.pi * frequency / 2 * time) * 0.2
            value = lead + harmony + bass
            samples.append(int(32767 * 0.09 * envelope * value))

    return pygame.mixer.Sound(buffer=samples.tobytes())


shoot_sound = make_sound(700, 220, 0.12)
hit_sound = make_sound(180, 520, 0.16)
level_up_sound = make_coin_sound()
game_over_sound = make_sound(260, 70, 0.45)
theme_music = make_theme_music()
theme_music.play(loops=-1)
game_over_sound_played = False
game_over = False

background = pygame.image.load("C:/Users/user/Desktop/Python/L35/background.png")

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("C:/Users/user/Desktop/Python/L35/ufo.png")
pygame.display.set_icon(icon)

playerImg = pygame.image.load("C:/Users/user/Desktop/Python/L35/player.png")

playerX = PLAYER_START_X
playerY = PLAYER_START_Y
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for _i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("C:/Users/user/Desktop/Python/L35/enemy.png"))
    enemyX.append(random.randint(0, SCREEN_WIDTH - 64))
    enemyY.append(random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))
    enemyX_change.append(ENEMY_SPEED_X)
    enemyY_change.append(ENEMY_SPEED_Y)

bulletImg = pygame.image.load("C:/Users/user/Desktop/Python/L35/bullet.png")

bulletX = 0
bulletY = PLAYER_START_Y
bulletX_change = 0
bulletY_change = BULLET_SPEED_Y
bullet_state = "ready" 

# "ready" means the bullet is ready to be fired, "fire" means the bullet is currently moving

score_value = 0
font=pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    return distance < COLLISION_DISTANCE

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state== "ready":
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
                shoot_sound.play()
        if event.type == pygame.KEYUP and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            playerX_change = 0

    playerX += playerX_change
    playerX = max(0, min(playerX, SCREEN_WIDTH - 64))

    for i in range(num_of_enemies):
        if not game_over and enemyY[i] > 340:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            game_over = True
            if not game_over_sound_played:
                game_over_sound.play()
                game_over_sound_played = True
            break
        if not game_over:
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0 or enemyX[i] >= SCREEN_WIDTH - 64:
                enemyX_change[i] *= -1
                enemyY[i] += enemyY_change[i]

            if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
                bulletY = PLAYER_START_Y
                bullet_state = "ready"
                score_value += 1
                hit_sound.play()
                if score_value % num_of_enemies == 0:
                    level_up_sound.play()
                enemyX[i] = random.randint(0, SCREEN_WIDTH - 64)
                enemyY[i] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)

        enemy(enemyX[i], enemyY[i], i)

    if game_over:
        game_over_text()

    if bulletY <= 0:
        bulletY = PLAYER_START_Y
        bullet_state = "ready"
    elif bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
                