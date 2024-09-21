import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Action Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up player variables
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 5
player_lives = 3
is_invincible = False
invincibility_duration = 3000  # 3 seconds
last_invincible_time = 0

# Set up enemy variables
enemy_list = []
enemy_types = [
    {"size": 50, "speed": 5, "color": RED},  # Normal enemy
    {"size": 30, "speed": 7, "color": BLUE},  # Fast enemy
    {"size": 70, "speed": 3, "color": GREEN},  # Slow but large enemy
]

# Set up power-up variables
power_up_list = []
power_up_size = 30
power_up_effect_duration = 5000  # 5 seconds
last_power_up_time = 0
player_speed_boost = False
boost_duration = 5000
boost_start_time = 0

# Set up game variables
clock = pygame.time.Clock()
score = 0
font = pygame.font.SysFont("monospace", 35)

# Function to create enemies
def create_enemy():
    enemy_type = random.choice(enemy_types)
    x_pos = random.randint(0, WIDTH - enemy_type["size"])
    y_pos = 0
    return {"x": x_pos, "y": y_pos, "size": enemy_type["size"], "speed": enemy_type["speed"], "color": enemy_type["color"]}

# Function to drop enemies
def drop_enemies(enemy_list):
    if len(enemy_list) < 10 and random.random() < 0.1:
        enemy_list.append(create_enemy())

# Function to draw enemies
def draw_enemies(enemy_list):
    for enemy in enemy_list:
        pygame.draw.rect(screen, enemy["color"], (enemy["x"], enemy["y"], enemy["size"], enemy["size"]))

# Function to update enemy positions
def update_enemy_positions(enemy_list):
    global score
    for idx, enemy in enumerate(enemy_list):
        if enemy["y"] >= 0 and enemy["y"] < HEIGHT:
            enemy["y"] += enemy["speed"]
        else:
            enemy_list.pop(idx)
            score += 1

# Function to detect collisions
def collision_check(enemy_list, player_x, player_y):
    for enemy in enemy_list:
        if (enemy["x"] >= player_x and enemy["x"] < (player_x + player_size)) or (player_x >= enemy["x"] and player_x < (enemy["x"] + enemy["size"])):
            if (enemy["y"] >= player_y and enemy["y"] < (player_y + player_size)) or (player_y >= enemy["y"] and player_y < (enemy["y"] + enemy["size"])):
                return True
    return False

# Function to create power-ups
def create_power_up():
    x_pos = random.randint(0, WIDTH - power_up_size)
    y_pos = random.randint(0, HEIGHT - power_up_size)
    return [x_pos, y_pos]

# Function to draw power-ups
def draw_power_ups(power_up_list):
    for power_up in power_up_list:
        pygame.draw.rect(screen, BLUE, (power_up[0], power_up[1], power_up_size, power_up_size))

# Function to check if player gets power-up
def power_up_collision_check(power_up_list, player_x, player_y):
    for idx, power_up in enumerate(power_up_list):
        if (power_up[0] >= player_x and power_up[0] < (player_x + player_size)) or (player_x >= power_up[0] and player_x < (power_up[0] + power_up_size)):
            if (power_up[1] >= player_y and power_up[1] < (player_y + player_size)) or (player_y >= power_up[1] and player_y < (power_up[1] + power_up_size)):
                power_up_list.pop(idx)
                return True
    return False

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += player_speed

    # Drop and move enemies
    drop_enemies(enemy_list)
    update_enemy_positions(enemy_list)

    # Check for collisions with enemies
    current_time = pygame.time.get_ticks()
    if not is_invincible and collision_check(enemy_list, player_x, player_y):
        player_lives -= 1
        is_invincible = True
        last_invincible_time = current_time
        if player_lives <= 0:
            running = False

    # Remove invincibility after some time
    if is_invincible and current_time - last_invincible_time > invincibility_duration:
        is_invincible = False

    # Power-up logic
    if len(power_up_list) < 1 and random.random() < 0.01:
        power_up_list.append(create_power_up())

    # Check for collisions with power-ups
    if power_up_collision_check(power_up_list, player_x, player_y):
        player_speed_boost = True
        boost_start_time = current_time
        player_speed = 10

    # Disable speed boost after some time
    if player_speed_boost and current_time - boost_start_time > boost_duration:
        player_speed_boost = False
        player_speed = 5

    # Draw player, enemies, and power-ups
    pygame.draw.rect(screen, GREEN if not is_invincible else WHITE, (player_x, player_y, player_size, player_size))
    draw_enemies(enemy_list)
    draw_power_ups(power_up_list)

    # Display score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    pygame.display.flip()

    # Set frame rate
    clock.tick(30)

# Quit pygame
pygame.quit()
