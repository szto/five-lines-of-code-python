import pygame
from enum import Enum, auto
from pygame.locals import *

# Constants
TILE_SIZE = 30
FPS = 30

# Enums
class Tile(Enum):
    AIR = auto()
    FLUX = auto()
    UNBREAKABLE = auto()
    PLAYER = auto()
    STONE = auto()
    FALLING_STONE = auto()
    BOX = auto()
    FALLING_BOX = auto()
    KEY1 = auto()
    LOCK1 = auto()
    KEY2 = auto()
    LOCK2 = auto()

class Input(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

# Initial game state
playerx, playery = 1, 1
map = [
    [Tile.UNBREAKABLE, Tile.UNBREAKABLE, Tile.UNBREAKABLE, Tile.UNBREAKABLE, Tile.UNBREAKABLE, Tile.UNBREAKABLE, Tile.UNBREAKABLE, Tile.UNBREAKABLE],
    [Tile.UNBREAKABLE, Tile.PLAYER, Tile.AIR, Tile.FLUX, Tile.FLUX, Tile.UNBREAKABLE, Tile.AIR, Tile.UNBREAKABLE],
    [Tile.UNBREAKABLE, Tile.STONE, Tile.UNBREAKABLE, Tile.BOX, Tile.FLUX, Tile.UNBREAKABLE, Tile.AIR, Tile.UNBREAKABLE],
    [Tile.UNBREAKABLE, Tile.KEY1, Tile.STONE, Tile.FLUX, Tile.FLUX, Tile.UNBREAKABLE, Tile.AIR, Tile.UNBREAKABLE],
    [Tile.UNBREAKABLE, Tile.STONE, Tile.FLUX, Tile.FLUX, Tile.FLUX, Tile.LOCK1, Tile.AIR, Tile.UNBREAKABLE],
    [Tile.UNBREAKABLE, Tile.UNBREAKABLE, Tile.UNBREAKABLE, Tile.UNBREAKABLE, Tile.UNBREAKABLE, Tile.UNBREAKABLE, Tile.UNBREAKABLE, Tile.UNBREAKABLE],
]

inputs = []

def remove(tile):
    global map
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == tile:
                map[y][x] = Tile.AIR

def moveToTile(newx, newy):
    global playerx, playery, map
    map[playery][playerx] = Tile.AIR
    map[newy][newx] = Tile.PLAYER
    playerx, playery = newx, newy

def moveHorizontal(dx):
    global map
    target = map[playery][playerx + dx]
    if target in [Tile.FLUX, Tile.AIR]:
        moveToTile(playerx + dx, playery)
    elif (target in [Tile.STONE, Tile.BOX] and map[playery][playerx + dx + dx] == Tile.AIR and map[playery + 1][playerx + dx] != Tile.AIR):
        map[playery][playerx + dx + dx] = map[playery][playerx + dx]
        moveToTile(playerx + dx, playery)
    elif target == Tile.KEY1:
        remove(Tile.LOCK1)
        moveToTile(playerx + dx, playery)
    elif target == Tile.KEY2:
        remove(Tile.LOCK2)
        moveToTile(playerx + dx, playery)

def moveVertical(dy):
    global map
    target = map[playery + dy][playerx]
    if target in [Tile.FLUX, Tile.AIR]:
        moveToTile(playerx, playery + dy)
    elif target == Tile.KEY1:
        remove(Tile.LOCK1)
        moveToTile(playerx, playery + dy)
    elif target == Tile.KEY2:
        remove(Tile.LOCK2)
        moveToTile(playerx, playery + dy)

def update():
    global inputs, map
    while inputs:
        current = inputs.pop()
        if current == Input.LEFT:
            moveHorizontal(-1)
        elif current == Input.RIGHT:
            moveHorizontal(1)
        elif current == Input.UP:
            moveVertical(-1)
        elif current == Input.DOWN:
            moveVertical(1)

    for y in range(len(map) - 1, -1, -1):
        for x, cell in enumerate(map[y]):
            if cell in [Tile.STONE, Tile.FALLING_STONE] and map[y + 1][x] == Tile.AIR:
                map[y + 1][x] = Tile.FALLING_STONE
                map[y][x] = Tile.AIR
            elif cell in [Tile.BOX, Tile.FALLING_BOX] and map[y + 1][x] == Tile.AIR:
                map[y + 1][x] = Tile.FALLING_BOX
                map[y][x] = Tile.AIR
            elif cell == Tile.FALLING_STONE:
                map[y][x] = Tile.STONE
            elif cell == Tile.FALLING_BOX:
                map[y][x] = Tile.BOX

def draw(screen):
    screen_init(screen)
    draw_map(screen)
    draw_player(screen)


def screen_init(screen):
    screen.fill((0, 0, 0))


def draw_player(screen):
    pygame.draw.rect(screen, (255, 0, 0), (playerx * TILE_SIZE, playery * TILE_SIZE, TILE_SIZE, TILE_SIZE))


def draw_map(screen):
    tile_colors = {
        Tile.FLUX: (204, 255, 204),
        Tile.UNBREAKABLE: (153, 153, 153),
        Tile.STONE: (0, 0, 204),
        Tile.FALLING_STONE: (0, 0, 204),
        Tile.BOX: (139, 69, 19),
        Tile.FALLING_BOX: (139, 69, 19),
        Tile.KEY1: (255, 204, 0),
        Tile.LOCK1: (255, 204, 0),
        Tile.KEY2: (0, 204, 255),
        Tile.LOCK2: (0, 204, 255),
    }
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            color = tile_colors.get(cell, (0, 0, 0))
            if cell != Tile.AIR:
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


def main():
    pygame.init()
    screen = pygame.display.set_mode((len(map[0]) * TILE_SIZE, len(map) * TILE_SIZE))
    pygame.display.set_caption('Game Conversion')
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key in [K_LEFT, K_a]:
                    inputs.append(Input.LEFT)
                elif event.key in [K_UP, K_w]:
                    inputs.append(Input.UP)
                elif event.key in [K_RIGHT, K_d]:
                    inputs.append(Input.RIGHT)
                elif event.key in [K_DOWN, K_s]:
                    inputs.append(Input.DOWN)

        update()
        draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()