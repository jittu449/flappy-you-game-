import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

# Screen
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy You")

# Colors
blue = (135, 206, 250)
green = (0, 200, 0)

# Load Image safely
try:
    bird_img_original = pygame.image.load("Aura.jpg").convert_alpha()
except:
    print("Image file not found!")
    pygame.quit()
    sys.exit()

bird_img_original = pygame.transform.scale(bird_img_original, (35, 35))

bird_x = 50
bird_y = 250
gravity = 0.5
velocity = 0
jump = -10

# Load sounds safely
try:
    jump_sound = pygame.mixer.Sound("jump.wav.mpeg")
    hit_sound = pygame.mixer.Sound("jump.wav.mpeg")
    jump_sound.set_volume(1.0)
    hit_sound.set_volume(1.0)
except:
    jump_sound = None
    hit_sound = None
    print("Sound files missing. Game running without sound.")

# Pipe
pipe_width = 60
pipe_gap = 180
pipe_x = width
pipe_height = random.randint(100, 400)
pipe_speed = 3

clock = pygame.time.Clock()

def draw_pipe(x, height):
    pygame.draw.rect(screen, green, (x, 0, pipe_width, height))
    pygame.draw.rect(screen, green, (x, height + pipe_gap, pipe_width, height))

running = True
while running:
    clock.tick(60)
    screen.fill(blue)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = jump
                if jump_sound:
                    jump_sound.play()

    velocity += gravity
    bird_y += velocity

    angle = -velocity * 3
    bird_img = pygame.transform.rotate(bird_img_original, angle)
    bird_rect = bird_img.get_rect(center=(bird_x + 35, bird_y + 35))

    pipe_x -= pipe_speed
    if pipe_x < -pipe_width:
        pipe_x = width
        pipe_height = random.randint(100, 400)

    pipe_top_rect = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
    pipe_bottom_rect = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, height)

    screen.blit(bird_img, bird_rect.topleft)
    draw_pipe(pipe_x, pipe_height)

    if bird_rect.colliderect(pipe_top_rect) or bird_rect.colliderect(pipe_bottom_rect):
        if hit_sound:
            hit_sound.play()
        running = False

    if bird_y <= 0 or bird_y >= height:
        if hit_sound:
            hit_sound.play()
        running = False

    pygame.display.update()

pygame.quit()
sys.exit()