import pygame
from pygame.locals import *
from sys import exit
from random import randint, choice
import config
import colors
from ball import Ball

# Initialize pygame
pygame.init()

# Set up the window
window_width = config.WINDOW_WIDTH
window_height = config.WINDOW_HEIGHT
window_size = (window_width, window_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Bouncing Balls")

# Set up the clock
clock = pygame.time.Clock()

# Ball list
balls = []

# Add initial balls
for _ in range(config.NUMBER_OF_BALLS):
    pos = [randint(100, window_width - 100), randint(100, window_height - 100)]
    speed = [randint(-5, 5), randint(-5, 5)]
    radius = randint(20, 50)
    balls.append(Ball(pos, speed, radius))

gravity_enabled = True

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_g:
                gravity_enabled = not gravity_enabled
            elif event.key == K_r:
                balls = []
                for _ in range(config.NUMBER_OF_BALLS):
                    pos = [randint(100, window_width - 100), randint(100, window_height - 100)]
                    speed = [randint(-5, 5), randint(-5, 5)]
                    radius = randint(20, 50)
                    balls.append(Ball(pos, speed, radius))
            elif event.key == K_a:
                pos = [randint(100, window_width - 100), randint(100, window_height - 100)]
                speed = [randint(-5, 5), randint(-5, 5)]
                radius = randint(20, 50)
                balls.append(Ball(pos, speed, radius))
            elif event.key == K_d:
                if balls:
                    balls.pop(choice(range(len(balls))))

    # Clear the screen
    screen.fill(colors.WHITE)

    # Update and draw the balls
    for ball in balls:
        ball.move(gravity_enabled=gravity_enabled)
        ball.handle_boundary_collision(window_width, window_height)
        for other_ball in balls:
            if other_ball != ball:
                ball.check_collision(other_ball)

        pygame.draw.circle(screen, ball.color, [int(ball.pos[0]), int(ball.pos[1])], ball.radius)

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(60)
