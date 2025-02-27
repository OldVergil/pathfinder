import pygame as pg
import sys
from random import random, randrange
from field import Field
from pathfinder import Pathfinder

def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2

def draw_grid(surface):
    for i in range(rows):
        for j in range(cols):
            color = 'darkorange' if grid[i][j] == 0 else 'darkgreen'
            coord = swap(i, j)
            draw_rect(surface, coord, color)

def get_mouse_pos():
    grid_x, grid_y = switch_mouse_coord(pg.mouse.get_pos())
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click else False

def draw_text():
    font = pg.font.Font(None, 36)
    for i in range(rows):
        for j in range(cols):
            coord = swap(i, j)
            r = pg.Rect(get_rect(coord[0], coord[1]))
            text = font.render(str(grid[i][j]), True, (0, 0, 0))
            text_rect = text.get_rect(center=r.center)
            screen.blit(text, text_rect)

def draw_path(path):
    for cell in path:
        coord = swap(cell.position[0], cell.position[1])
        draw_circle(screen, coord, 'yellow')

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

def create_grid():
    return [[0 if random() < 0.2 else randrange(1,10) for col in range(cols)] for row in range(rows)]

def visualize_algorithm(history, start_coord, end_coord):
    temp_bg = pg.Surface(bg.get_size())
    temp_bg.blit(bg, (0,0))
    for cell in history:
        screen.blit(temp_bg, (0, 0))
        last = cell
        current_cell = cell
        while current_cell:
            current_cell_coord = swap(current_cell.position[0], current_cell.position[1])
            draw_circle(screen, current_cell_coord, 'yellow')
            current_cell = current_cell.previous
        last_cell_coord = swap(last.position[0], last.position[1])
        draw_rect(temp_bg, last_cell_coord, 'gray', 1)
        draw_circles(screen, [(start_coord,'blue'), (last_cell_coord,'purple'), (end_coord, 'red')])
        draw_text()
        pg.display.flip()
        clock.tick(7)
    draw_grid(temp_bg)

def swap(a, b):
    return (b, a)

pg.init()
TILE = 60
cols, rows = 25, 15
screen = pg.display.set_mode((cols * TILE, rows * TILE))
bg = pg.Surface(screen.get_size())
grid = create_grid()
pathfinder = Pathfinder()
start_position = None
end_position = None
visualisation_stop = True
draw_grid(bg)
field = Field(grid)
clock = pg.time.Clock()
while True:
    screen.blit(bg, (0,0))
    mouse_pos = get_mouse_pos()
    if start_position != None and end_position != None:
        path, history = pathfinder.get_path(field, swap(start_position[0], start_position[1]), swap(end_position[0], end_position[1])
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
        if event.type == pg.KEYDOWN and event.key == pg.K_c:
            start_position = None
            end_position = None
            visualisation_stop = True
            draw_grid(bg)
        if event.type == pg.KEYDOWN and event.key == pg.K_r:
            start_position = None
            end_position = None
            visualisation_stop = True
            grid = create_grid()
            draw_grid(bg)
            field = Field(grid)
        if event.type == pg.KEYDOWN and event.key == pg.K_v:
            if (start_position != None and end_position != None):
                visualisation_stop = False
        
    draw_circles(screen, [(start_position,'blue'), (end_position,'red')])
    draw_text()
    pg.display.flip()
    