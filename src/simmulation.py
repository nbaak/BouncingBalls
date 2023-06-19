import pygame
from pygame.locals import *
from sys import exit
from random import randint, choice
import os
import uuid
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

# Create screenshots folder if it doesn't exist
screenshots_folder = "screenshots"
if not os.path.exists(screenshots_folder):
    os.makedirs(screenshots_folder)


def take_screenshot():
    # Generate a unique filename for the screenshot
    filename = str(uuid.uuid4()) + ".png"
    screenshot_path = os.path.join(screenshots_folder, filename)
    pygame.image.save(screen, screenshot_path)
    print("Screenshot saved as:", screenshot_path)


# Game loop
def main():
    # Ball list
    balls = []

    # Add initial balls
    for _ in range(config.NUMBER_OF_BALLS):
        pos = [randint(100, window_width - 100), randint(100, window_height - 100)]
        speed = [randint(-5, 5), randint(-5, 5)]
        radius = randint(20, 50)
        balls.append(Ball(pos, speed, radius))

    gravity_enabled = True

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
                elif event.key == K_s:
                    take_screenshot()
                elif event.key == K_q:
                    exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = list(pygame.mouse.get_pos())
                    speed = [randint(-5, 5), randint(-5, 5)]
                    radius = randint(20, 50)
                    balls.append(Ball(pos, speed, radius))

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


if __name__ == "__main__":
    main()
