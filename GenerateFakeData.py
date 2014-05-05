#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from utils.Decay import decay
from math import hypot
from utils.Gaussian import gaussian

GRID_GAP = 0.1
GRID_WIDTH = 1800
GRID_HEIGHT = 900

# GRID_WIDTH = 30
# GRID_HEIGHT = 20

TIME_FRAME_WINDOW = 50

TOTAL_DAYS = 200

GAUSSIAN_RANGE = 250


def genEmptyGrid():
    grid = [ [ 0 for i in range(GRID_WIDTH) ] for j in range(GRID_HEIGHT) ]
    return grid


def showGrid(grid):
    print "show grid:"
    for row in grid:
        row_text = ""
        for cell in row:
            if cell == 0:
                row_text += "░"
            else:
                row_text += "█"
        print row_text

def showNumGrid(grid):
    print "show grid:"
    for row in grid:
        print row


def genPath(num):
    path = []

    source = (randint(GRID_WIDTH*0.7, GRID_WIDTH-1), randint(GRID_HEIGHT*0.7, GRID_HEIGHT-1))
    # source = (GRID_WIDTH-1, GRID_HEIGHT-1)

    path.append(source)
    previous_point_idx = 0

    direction_x = 1
    direction_y = -1
    for i in range(num):

        off_x = direction_x * randint(10, 30)
        off_y = direction_y * randint(10, 30)

        new_x = path[previous_point_idx][0] + off_x
        new_y = path[previous_point_idx][1] + off_y

        if new_x < 0:
            new_x = 0
            direction_x *= -1
        if new_x > GRID_WIDTH-1:
            new_x = GRID_WIDTH-1
            direction_x *= -1

        if new_y < 0:
            new_y = 0
            direction_y *= -1
        if new_y > GRID_HEIGHT-1:
            new_y = GRID_HEIGHT-1
            direction_y *= -1

        new_position = (new_x, new_y)
        path.append(new_position)
        previous_point_idx += 1

    return path
#
#
# path = genPath(TOTAL_DAYS)
# print path
#
# for day in range(TOTAL_DAYS):
#
#     grid = genEmptyGrid()
#
#     # seed points and decay and gaussian
#     if day < TIME_FRAME_WINDOW:
#         for p in range(0, day+1):
#             (x, y) = path[p]
#
#             # decay by time
#             grid[y][x] += 1 * decay(day-p)
#
#             # apply gaussian to neighborhood, decay by distance
#             for i in range(-1*GAUSSIAN_RANGE, GAUSSIAN_RANGE):
#                 for j in range(-1*GAUSSIAN_RANGE, GAUSSIAN_RANGE):
#                     if 0 < x+i < GRID_WIDTH-1 and 0 < y+j < GRID_HEIGHT-1:
#                         dist = hypot(i, j)
#                         grid[y+j][x+i] += gaussian(grid[y][x], dist)
#
#     else:
#         for p in range(day-TIME_FRAME_WINDOW, day+1):
#             (x, y) = path[p]
#
#             # decay by time
#             grid[y][x] += 1 * decay(day-p)
#
#             # apply gaussian to neighborhood, decay by distance
#             for i in range(-1*GAUSSIAN_RANGE, GAUSSIAN_RANGE):
#                 for j in range(-1*GAUSSIAN_RANGE, GAUSSIAN_RANGE):
#                     if 0 < x+i < GRID_WIDTH-1 and 0 < y+j < GRID_HEIGHT-1:
#                         dist = hypot(i, j)
#                         grid[y+j][x+i] += gaussian(grid[y][x], dist)
#
#     # clamp the value range to 0 - 1
#
#     for j in xrange(GRID_HEIGHT):
#         for i in xrange(GRID_WIDTH):
#             if grid[j][i] > 1:
#                 grid[j][i] = 1
#
#     # showGrid(grid)
#     showNumGrid(grid)
