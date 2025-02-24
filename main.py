import pygame as pg
import sys
from random import random, randrange
from bfs import get_path

pg.init()

TILE = 60
cols, rows = 25, 15

screen = pg.display.set_mode((cols * TILE, rows * TILE))

grid = [[0 if random() < 0.2 else randrange(1,10) for row in range(rows)] for col in range(cols)]
#grid = [[0 if random() < 0.2 else 1 for row in range(rows)] for col in range(cols)]

def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2

def draw_grid():
    for x in range(cols):
        for y in range(rows):
            pg.draw.rect(screen, pg.Color('darkorange' if grid[x][y] == 0 else 'darkgreen'), get_rect(x, y))

def get_mouse_pos():
    grid_x, grid_y = switch_mouse_coord(pg.mouse.get_pos())
    #r = pg.Rect(get_rect(grid_x, grid_y))
    #color = pg.Color('red')
    #if grid[grid_x][grid_y] == 0:
        #pg.draw.line(screen, color, r.bottomleft, r.topright, TILE // 10)
        #pg.draw.line(screen, color, r.bottomright, r.topleft, TILE // 10)
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click else False

def draw_text():
    font = pg.font.Font(None, 36)
    for x in range(cols):
        for y in range(rows):
            r = pg.Rect(get_rect(x, y))
            text = font.render(str(grid[x][y]), True, (0, 0, 0))
            text_rect = text.get_rect(center=r.center)
            screen.blit(text, text_rect)

def draw_history(history):
    for position in history:
        pg.draw.rect(screen, pg.Color('gray'), get_rect(position[0], position[1]))


def draw_path(path):
    for position in path:
        r = pg.Rect(get_rect(position[0], position[1]))
        pg.draw.circle(screen, pg.Color('yellow'), r.center, TILE / 2 - 2)


def switch_mouse_coord(mouse_coord):
    return (mouse_coord[0] // TILE, mouse_coord[1] // TILE)

start_position = None
clock = pg.time.Clock()
while True:
    screen.fill(pg.Color('black'))
    draw_grid()
    mouse_pos = get_mouse_pos()
    if mouse_pos != False and start_position != None:
        path, history = get_path(grid, start_position, mouse_pos
                                 #,'bfs'
                                 )
        draw_history(history)
        draw_path(path)
    draw_text()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            coord = switch_mouse_coord(event.pos)
            if start_position != coord:
                start_position = coord
            else:
                start_position = None
    pg.display.flip()
    