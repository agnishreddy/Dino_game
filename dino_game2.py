import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Upgraded Dino Game")
clock = pygame.time.Clock()

# Load assets
dino_image = pygame.image.load("dino.png")  # Replace with the path to your dino sprite
dino_image = pygame.transform.scale(dino_image, (50, 50))

obstacle_image = pygame.image.load("cactus.png")  # Replace with the path to your obstacle sprite
obstacle_image = pygame.transform.scale(obstacle_image, (40, 50))

jump_sound = pygame.mixer.Sound("jump.wav")  # Replace with the path to your jump sound
game_over_sound = pygame.mixer.Sound("game_over.wav")  # Replace with the path to your game-over sound

# Dino settings
dino = pygame.Rect(50, HEIGHT - 70, 50, 50)
gravity = 0.5
jump_power = -10
dino_velocity_y = 0
is_jumping = False

# Obstacle settings
obstacle_speed = 6
obstacle_gap = 1000  # Gap between obstacles
obstacles = []

# Font for score
font = pygame.font.Font(None, 36)

# Initialize score and difficulty
score = 0
difficulty_increment = 0.1  # Increase speed with each score

def draw_dino():
    screen.blit(dino_image, (dino.x, dino.y))

def draw_obstacles():
    for obstacle in obstacles:
        screen.blit(obstacle_image, (obstacle.x, obstacle.y))

def move_obstacles():
    for obstacle in obstacles:
        obstacle.x -= obstacle_speed

def check_collision():
    for obstacle in obstacles:
        if dino.colliderect(obstacle):
            return True
    return False

# Main game loop
def main():
    global dino_velocity_y, is_jumping, score, obstacle_speed
    
    # Generate the first obstacle
    obstacles.append(pygame.Rect(WIDTH, HEIGHT - 70, 40, 50))

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    dino_velocity_y = jump_power
                    is_jumping = True
                    jump_sound.play()

        # Dino movement
        dino_velocity_y += gravity
        dino.y += dino_velocity_y
        if dino.y >= HEIGHT - 70:  # Reset if dino lands
            dino.y = HEIGHT - 70
            is_jumping = False

        # Move obstacles and generate new ones
        move_obstacles()
        if obstacles and obstacles[0].x < -40:  # Remove off-screen obstacles
            obstacles.pop(0)
            score += 1  # Increment score
            obstacle_speed += difficulty_increment  # Increase speed as score increases

        if len(obstacles) == 0 or (obstacles[-1].x < WIDTH - obstacle_gap):
            new_obstacle = pygame.Rect(WIDTH, HEIGHT - 70, 40, 50)
            obstacles.append(new_obstacle)

        # Check collision
        if check_collision():
            game_over_sound.play()
            print("Game Over! Final Score:", score)
            running = False

        # Draw everything
        draw_dino()
        draw_obstacles()

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update the screen
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
