import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
PAD_WIDTH = 10
PAD_HEIGHT = 100
BALL_RADIUS = 10
PAD_SPEED = 5
BALL_SPEED = 3  

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Load sounds
paddle_sound = pygame.mixer.Sound("archivo.mp3")  # Adjust the file name as per your sound file
paddle_sound.set_volume(0.5)  # Set the volume of the sound

# Define the Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PAD_WIDTH, PAD_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def move(self, dy):
        self.rect.y += dy
        # Keep the paddle within the screen bounds
        self.rect.y = max(0, min(self.rect.y, HEIGHT - PAD_HEIGHT))

# Define the Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.speed_x = BALL_SPEED
        self.speed_y = BALL_SPEED
        # Randomize initial direction
        if random.random() > 0.5:
            self.speed_x *= -1
        if random.random() > 0.5:
            self.speed_y *= -1

    def draw(self):
        pygame.draw.circle(screen, WHITE, self.rect.center, BALL_RADIUS)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Check collisions with top and bottom edges
        if self.rect.y <= 0 or self.rect.y >= HEIGHT - BALL_RADIUS * 2:
            self.speed_y *= -1

# Create paddles and ball
paddle1 = Paddle(20, HEIGHT // 2 - PAD_HEIGHT // 2)
paddle2 = Paddle(WIDTH - 30, HEIGHT // 2 - PAD_HEIGHT // 2)
ball = Ball()

clock = pygame.time.Clock()

# Font for menu text and score
font = pygame.font.Font(None, 36)

# Flag to track if game is running
game_running = False

# Scores
score1 = 0
score2 = 0

# Main menu loop
while not game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Check if start button is clicked
                if WIDTH // 2 - 50 <= event.pos[0] <= WIDTH // 2 + 50 and HEIGHT // 2 - 25 <= event.pos[1] <= HEIGHT // 2 + 25:
                    game_running = True

    # Draw menu bar
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50))
    start_text = font.render("Start", True, BLACK)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))

    pygame.display.flip()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1.move(-PAD_SPEED)
    if keys[pygame.K_s]:
        paddle1.move(PAD_SPEED)
    if keys[pygame.K_UP]:
        paddle2.move(-PAD_SPEED)
    if keys[pygame.K_DOWN]:
        paddle2.move(PAD_SPEED)

    # Move the ball
    ball.move()

    # Check collisions with paddles
    if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
        ball.speed_x *= -1
        paddle_sound.play()  # Play paddle sound when collision occurs

    # Check if ball goes out of bounds
    if ball.rect.x <= 0:
        score2 += 1
        ball.__init__()  # Reset ball position and speed
    elif ball.rect.x >= WIDTH - BALL_RADIUS * 2:
        score1 += 1
        ball.__init__()  # Reset ball position and speed

    # Check if one player reaches the winning score
    if score1 >= 10 or score2 >= 10:
        # Display game over screen
        game_over_text = font.render("Game Over", True, WHITE)
        winner_text = font.render("Player 1 wins!" if score1 >= 10 else "Player 2 wins!", True, WHITE)
        restart_text = font.render("Restart", True, BLACK)
        screen.fill(BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50 + restart_text.get_height() // 2))
        pygame.display.flip()

        # Wait for restart button to be clicked
        restart_clicked = False
        while not restart_clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if WIDTH // 2 - 50 <= event.pos[0] <= WIDTH // 2 + 50 and HEIGHT // 2 + 50 <= event.pos[1] <= HEIGHT // 2 + 100:
                            restart_clicked = True

        # Reset game state
        score1 = 0
        score2 = 0
        ball.__init__()

    # Clear the screen
    screen.fill(BLACK)

    # Draw paddles, ball, and score
    paddle1.draw()
    paddle2.draw()
    ball.draw()
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
