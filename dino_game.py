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
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Dino Game")
clock = pygame.time.Clock()

# Dino settings
dino = pygame.Rect(50, HEIGHT - 70, 50, 50)
dino_color = (50, 168, 82)
gravity = 0.5
jump_power = -10
dino_velocity_y = 0
is_jumping = False

# Obstacle settings
obstacle_width, obstacle_height = 40, 50
obstacle_color = RED
obstacle_speed = 6
obstacle_gap = 1000  # Gap between obstacles
obstacles = []

# Font for score
font = pygame.font.Font(None, 36)

# Initialize score
score = 0

def draw_dino():
    pygame.draw.rect(screen, dino_color, dino)

def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(screen, obstacle_color, obstacle)

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
    global dino_velocity_y, is_jumping, score
    
    # Generate the first obstacle
    obstacles.append(pygame.Rect(WIDTH, HEIGHT - obstacle_height - 20, obstacle_width, obstacle_height))

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

        # Dino movement
        dino_velocity_y += gravity
        dino.y += dino_velocity_y
        if dino.y >= HEIGHT - 70:  # Reset if dino lands
            dino.y = HEIGHT - 70
            is_jumping = False

        # Move obstacles and generate new ones
        move_obstacles()
        if obstacles and obstacles[0].x < -obstacle_width:
            obstacles.pop(0)
            score += 1  # Increment score

        if len(obstacles) == 0 or (obstacles[-1].x < WIDTH - obstacle_gap):
            new_obstacle = pygame.Rect(WIDTH, HEIGHT - obstacle_height - 20, obstacle_width, obstacle_height)
            obstacles.append(new_obstacle)

        # Check collision
        if check_collision():
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
