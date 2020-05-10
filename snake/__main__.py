#!/usr/bin/python
# coding=utf-8

__author__ = 'Simon Charest'
__copyright__ = 'Copyright 2019, SLCIT inc.'
__credits__ = ['Harry Frank Fogleman', 'Carl E Grindle']
__email__ = 'simoncharest@gmail.com'
__license__ = 'GPL'
__maintainer__ = 'Simon Charest'
__project__ = 'Snake'
__status__ = 'Developement'
__version__ = '1.0.0'

import pygame
import pygame.locals
import random

BACKGROUND_WIDTH = 640
BACKGROUND_HEIGHT = 480
BACKGROUND_COLOR = (0, 0, 0)
SNAKE_SIZE = min(BACKGROUND_HEIGHT, BACKGROUND_WIDTH) / 20
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
APPLE_SIZE = SNAKE_SIZE
SCORE_FONT = 'Ubuntu Monospace'
SCORE_SIZE = 48
SCORE_COLOR = (255, 255, 255)


def main():
    # Initialize game
    pygame.init()
    screen = pygame.display.set_mode((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

    # Initialize snake
    snake = list()
    snake.insert(0, get_point(SNAKE_SIZE))
    score = 0
    length = 1
    speed = 0.5
    move = ''

    apple = list()
    apple.insert(0, get_point(APPLE_SIZE))

    # Manage game loop
    run = True

    while run:

        # Exit game
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False

        # Manage keypress
        keys = pygame.key.get_pressed()

        # Manage game end
        if is_quit(keys):
            run = False

        # Manage keypress
        if is_up(keys):
            move = 'up'
        if is_down(keys):
            move = 'down'
        if is_left(keys):
            move = 'left'
        if is_right(keys):
            move = 'right'

        # Manage snake head
        x = snake[0][0]
        y = snake[0][1]

        # Manage movement
        if move == 'up' and y > 0:
            y -= speed
        elif move == 'down' and y < BACKGROUND_HEIGHT - SNAKE_SIZE:
            y += speed
        elif move == 'left' and x > 0:
            x -= speed
        elif move == 'right' and x < BACKGROUND_WIDTH - SNAKE_SIZE:
            x += speed

        # Manage snake tail
        snake.insert(0, [x, y])
        snake = snake[:length]

        # if is_collide(snake):
            # run = False

        if is_picked(snake, apple):
            score += 1
            length += 10
            speed += 0.05

        # Redraw
        draw(snake, apple, score, screen)


# TODO: Fix this. Too restrictive.
def is_collide(snake):
    head = pygame.Rect(snake[0][0], snake[0][1], SNAKE_SIZE, SNAKE_SIZE)

    for s in range(0, len(snake) - 1):
        if s % 100 == 0:
            rect = pygame.Rect(snake[s][0], snake[s][1], SNAKE_SIZE, SNAKE_SIZE)

            if rect.colliderect(head):
                return True

    return False


def is_picked(snake, apple):
    head = pygame.Rect(snake[0][0], snake[0][1], SNAKE_SIZE, SNAKE_SIZE)

    for a in apple:
        rect = pygame.Rect(a[0], a[1], APPLE_SIZE, APPLE_SIZE)

        if rect.colliderect(head):
            apple.remove(a)

            # Add new apple
            apple.insert(0, get_point(APPLE_SIZE))

            return True

    return False


def get_point(size):
    x = random.randint(0, BACKGROUND_WIDTH - size - 1)
    y = random.randint(0, BACKGROUND_HEIGHT - size - 1)
    return [x, y]


def add_apple(screen):
    x = random.randint(0, BACKGROUND_WIDTH - APPLE_SIZE - 1)
    y = random.randint(0, BACKGROUND_HEIGHT - APPLE_SIZE - 1)
    rect = pygame.Rect(x, y, APPLE_SIZE, APPLE_SIZE)
    pygame.draw.rect(screen, APPLE_COLOR, rect)


def draw(snake, apple, score, screen):
    # Draw background
    screen.fill(BACKGROUND_COLOR)
    screen_rect = screen.get_rect()

    # Draw apple
    for a in apple:
        apple_rect = pygame.Rect(a[0], a[1], APPLE_SIZE, APPLE_SIZE)
        pygame.draw.rect(screen, APPLE_COLOR, apple_rect)

    # Draw snake
    for s in snake:
        snake_rect = pygame.Rect(s[0], s[1], SNAKE_SIZE, SNAKE_SIZE)
        snake_rect.clamp_ip(screen_rect)
        pygame.draw.rect(screen, SNAKE_COLOR, snake_rect)

    show_score(score, screen)

    # Update display
    pygame.display.flip()


def show_score(score, screen):
    font = pygame.font.SysFont(SCORE_FONT, SCORE_SIZE)
    text = font.render('Score: %d' % score, True, SCORE_COLOR)
    screen.blit(text, (0, 0))


def is_up(keys):
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        return True
    return False


def is_down(keys):
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        return True
    return False


def is_left(keys):
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        return True
    return False


def is_right(keys):
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        return True
    return False


def is_move(keys):
    if is_up(keys) or is_down(keys) or is_left(keys) or is_right(keys):
        return True
    return False


def is_quit(keys):
    if keys[pygame.K_q] or keys[pygame.K_x] or keys[pygame.K_ESCAPE]:
        return True
    return False


main()
