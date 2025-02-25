import pygame as pg
import sys
from random import random, randrange
from field import Field
from pathfinder import Pathfinder

pg.init()

TILE = 60
cols, rows = 25, 15

screen = pg.display.set_mode((cols * TILE, rows * TILE))
bg = pg.Surface(screen.get_size())

grid = [[0 if random() < 0.2 else randrange(1,10) for row in range(rows)] for col in range(cols)]

def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2

def draw_grid(surface):
    for x in range(cols):
        for y in range(rows):
            pg.draw.rect(surface, pg.Color('darkorange' if grid[x][y] == 0 else 'darkgreen'), get_rect(x, y))

def get_mouse_pos():
    grid_x, grid_y = switch_mouse_coord(pg.mouse.get_pos())
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
    for cell in history:
        position = cell.position
        pg.draw.rect(screen, pg.Color('gray'), get_rect(position[0], position[1]))

def draw_path(path):
    for cell in path:
        position = cell.position
        r = pg.Rect(get_rect(position[0], position[1]))
        pg.draw.circle(screen, pg.Color('yellow'), r.center, TILE / 2 - 2)

def switch_mouse_coord(mouse_coord):
    return (mouse_coord[0] // TILE, mouse_coord[1] // TILE)

def draw_circle(surface, position, color):
    if position != None:
        r = pg.Rect(get_rect(position[0], position[1]))
        pg.draw.circle(surface, pg.Color(color), r.center, TILE / 2 - 2)

def draw_circles(surface, positions_colors):
    for position_color in positions_colors:
        position, color = position_color
        draw_circle(surface, position, color)

def draw_rect(surface, position, color, width = 0):
    if position != None:
        pg.draw.rect(surface, pg.Color(color), get_rect(position[0], position[1]), width)

def visualize_algorithm(history, start_position, end_position):
    end = None
    for cell in history:
        screen.blit(bg, (0, 0))
        end = cell
        current_cell = cell
        while current_cell:
            draw_circle(screen, current_cell.position, 'yellow')
            current_cell = current_cell.previous
        draw_rect(bg, end.position, 'gray', 1)
        draw_circles(screen, [(start_position,'blue'), (end.position,'red'), (end_position, 'purple')])
        draw_text()
        pg.display.flip()
        clock.tick(5)
    draw_grid(bg)

pathfinder = Pathfinder()
start_position = None
end_position = None
visualisation_stop = True
field = Field(grid)
clock = pg.time.Clock()
draw_grid(bg)
while True:
    screen.blit(bg, (0,0))
    mouse_pos = get_mouse_pos()
    if start_position != None and end_position != None:
        path, history = pathfinder.get_path(field, start_position, end_position
                                 #,'bfs'
        )
        
        if not visualisation_stop:
            visualize_algorithm(history, start_position, end_position)
            visualisation_stop = True
        else:
            draw_path(path)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            coord = switch_mouse_coord(event.pos)
            if start_position == None:
                start_position = coord
            elif end_position == None:
                end_position = coord
        if event.type == pg.KEYDOWN and event.key == pg.K_r:
            start_position = None
            end_position = None
            visualisation_stop = True
            draw_grid(bg)
        if event.type == pg.KEYDOWN and event.key == pg.K_v:
            visualisation_stop = False
    draw_circles(screen, [(start_position,'blue'), (end_position,'red')])
    draw_text()
    pg.display.flip()
    