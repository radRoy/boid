"""pygame_icebreaker.py
code taken from https://www.pygame.org/docs/tut/PygameIntro.html (official pygame documentation)"""

import sys
import pygame

pygame.init()

size = width, height = 1028, 720  # size = (width,height) = 320,420
speed = [1, 1]
black = 0, 0, 0

# Pygame represents images as Surface objects.
screen = pygame.display.set_mode(size)
# display.set_mode((xres,yres)) creates a new Surface object. Any drawing done to this Surface will become visible on
# the monitor (in the window where this Surface is displayed).

ball = pygame.image.load("intro_ball.gif")  # load image we move later
ballrect = ball.get_rect()


while 1:  # while True
    for event in pygame.event.get():
        # print(f"event = {event}")
        if event.type == pygame.QUIT:  # when the pygame window is closed
            sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)

    pygame.display.flip()  # somehow makes the ball appear...?
