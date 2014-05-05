
import sys
from PIL import Image, ImageDraw, ImageFont
from random import randint
from GenerateFakeData import *
from math import floor

# import Image,colorsys

use = '''
  Require:
  -i : input file name
  Option:
  -o : output filename
'''


def main(argv):

    # if len(argv) < 1:
    #     print use
    #     return
    #
    # filename = ""
    # output_name = ""
    # for arg in argv:
    #     ary = arg.split('=')
    #     if ary[0] == '-i':
    #         filename = ary[1]
    #     if ary[0] == '-o':
    #         output_name = ary[1]
    #
    # if filename == "":
    #     print use
    #     exit()

    # load data

    all_grid = []
    TOTAL_SPEICES = 3

    for species_idx in xrange(TOTAL_SPEICES):

        grid = genEmptyGrid()

        path = genPath(TOTAL_DAYS)
        day = TOTAL_DAYS - 1

        for p in range(day-TIME_FRAME_WINDOW, day+1):
            (x, y) = path[p]

            center_value = 1 * decay(day-p)
            grid[y][x] += center_value

            for i in range(-1*GAUSSIAN_RANGE, +1*GAUSSIAN_RANGE):
                for j in range(-1*GAUSSIAN_RANGE, +1*GAUSSIAN_RANGE):

                    if i == 0 and j == 0:
                        continue

                    if 0 < x+i < GRID_WIDTH-1 and 0 < y+j < GRID_HEIGHT-1:

                        dist = hypot(i, j)
                        if dist <= GAUSSIAN_RANGE:
                            grid[y+j][x+i] += gaussian(center_value, dist)

        for j in xrange(GRID_HEIGHT):
            for i in xrange(GRID_WIDTH):
                if grid[j][i] > 1:
                    grid[j][i] = 1

        all_grid.append(grid)


    #  start to draw
    # CANVAS_WIDTH = 3600
    # CANVAS_HEIGHT = 1800

    CANVAS_WIDTH = 1800
    CANVAS_HEIGHT = 900


    TOTAL_SPEICES = 3

    all_path = []
    for species_idx in xrange(TOTAL_SPEICES):
        path = genPath(TOTAL_DAYS)
        all_path.append(path)

    for day in xrange(TOTAL_DAYS):

        all_grid = []
        for species_idx in xrange(TOTAL_SPEICES):
            grid = genEmptyGrid()
            path = all_path[species_idx]

            if day < TIME_FRAME_WINDOW:
                for p in range(0, day+1):
                    (x, y) = path[p]
                    center_value = 1 * decay(day-p)
                    grid[y][x] += center_value
                    for i in range(-1*GAUSSIAN_RANGE, +1*GAUSSIAN_RANGE):
                        for j in range(-1*GAUSSIAN_RANGE, +1*GAUSSIAN_RANGE):
                            if i == 0 and j == 0:
                                continue
                            if 0 < x+i < GRID_WIDTH-1 and 0 < y+j < GRID_HEIGHT-1:
                                dist = hypot(i, j)
                                if dist <= GAUSSIAN_RANGE:
                                    grid[y+j][x+i] += gaussian(center_value, dist)

            else:
                for p in range(day-TIME_FRAME_WINDOW, day+1):
                    (x, y) = path[p]
                    center_value = 1 * decay(day-p)
                    grid[y][x] += center_value
                    for i in range(-1*GAUSSIAN_RANGE, +1*GAUSSIAN_RANGE):
                        for j in range(-1*GAUSSIAN_RANGE, +1*GAUSSIAN_RANGE):
                            if i == 0 and j == 0:
                                continue
                            if 0 < x+i < GRID_WIDTH-1 and 0 < y+j < GRID_HEIGHT-1:
                                dist = hypot(i, j)
                                if dist <= GAUSSIAN_RANGE:
                                    grid[y+j][x+i] += gaussian(center_value, dist)

            for j in xrange(GRID_HEIGHT):
                for i in xrange(GRID_WIDTH):
                    if grid[j][i] > 1:
                        grid[j][i] = 1

            all_grid.append(grid)

        print "start to draw day: %s" % day

        im = Image.new('RGBA', (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 255))
        draw = ImageDraw.Draw(im)

        # h,l,s = colorsys.rgb_to_hls(rd/255.,gn/255.,bl/255.)
        color_tables = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for species_idx in xrange(TOTAL_SPEICES):

            layer = Image.new('RGBA', (CANVAS_WIDTH, CANVAS_HEIGHT))
            layer_draw = ImageDraw.Draw(layer)

            pixels = layer.load()
            grid = all_grid[species_idx]
            color = color_tables[species_idx]

            for x in xrange(CANVAS_WIDTH):
                for y in xrange(CANVAS_HEIGHT):

                    value = int(grid[y][x]*170)
                    pixels[x,y] = (color[0], color[1], color[2], value)

            im.paste(layer, mask=layer)

        # im.show()
        im.save("./test_data/"+str(day)+".png")
        print "done %s.png" % day

    # im_after = im.resize( (CANVAS_WIDTH*2, CANVAS_HEIGHT*2), Image.BILINEAR)
    # im_after.show()






if __name__ == '__main__':
    main(sys.argv[1:])