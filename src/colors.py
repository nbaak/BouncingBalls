import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def generate_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def make_transparent(color, transparent_value=128):
    col = list(color)
    col.append(transparent_value)
    return tuple(col)
