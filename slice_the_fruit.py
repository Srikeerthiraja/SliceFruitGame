import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slice the Fruit")
clock = pygame.time.Clock()

# Load assets
background_image = pygame.image.load("tree_backround.png")  # Add your background image here
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

fruit_images = [
    pygame.image.load("apple.png"),
    pygame.image.load("orange.png"),
    pygame.image.load("banana.png"),
]

# Resize images
fruit_images = [pygame.transform.scale(img, (60, 60)) for img in fruit_images]

# Load sounds
background_music = pygame.mixer.Sound("backroundmusic.wav")  # Add your background music here
slice_sound = pygame.mixer.Sound("slice_sound.wav")  # Add your slice sound here

# Play background music
pygame.mixer.Sound.play(background_music, loops=-1)

# Fruit class
class Fruit:
    def __init__(self, x, y, image, speed):
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.active = True

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))

    def update(self):
        if self.active:
            self.y += self.speed
            self.rect.y = self.y
            if self.y > HEIGHT:
                self.active = False

# Create fruits
fruits = []
SCORE = 0
LIVES = 3
FONT = pygame.font.Font(None, 36)

# Function to create a new fruit
def create_fruit():
    x = random.randint(0, WIDTH - 60)
    y = -60
    image = random.choice(fruit_images)
    speed = random.randint(4, 8)
    return Fruit(x, y, image, speed)

# Main game loop
running = True
while running:
    screen.blit(background_image, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for fruit in fruits:
                if fruit.rect.collidepoint(pos) and fruit.active:
                    fruit.active = False
                    SCORE += 1
                    pygame.mixer.Sound.play(slice_sound)

    # Update fruits
    for fruit in fruits:
        fruit.update()
        if not fruit.active and fruit.y > HEIGHT:
            LIVES -= 1
            fruits.remove(fruit)

    # Draw fruits
    for fruit in fruits:
        fruit.draw(screen)

    # Create new fruits
    if random.random() < 0.02:  # Adjust frequency
        fruits.append(create_fruit())

    # Draw score and lives
    score_text = FONT.render(f"Score: {SCORE}", True, BLACK)
    lives_text = FONT.render(f"Lives: {LIVES}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    # Game over
    if LIVES <= 0:
        game_over_text = FONT.render("Better Luck Next Time", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Update display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
