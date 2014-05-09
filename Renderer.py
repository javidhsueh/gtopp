from GenerateFakeData import *
import sys
from PIL import Image, ImageDraw, ImageFont
from random import randint
from GenerateFakeData import *
from math import floor


def load_grid(fn):
    new_grid = genEmptyGrid()
    h = 0
    with open(fn, "r") as file:
        for d in file.read().split("/t"):
            d2 = d.split(",")

            d2.pop()
            # print d2
            for w in range(len(d2)):
                new_grid[h][w] = float(d2[w])
            h += 1
    # print new_grid
    return new_grid


# new_grid = genEmptyGrid()
# showNumGrid(new_grid)
#
# g = load_grid("./test_data2/325.txt")
# showNumGrid(g)
#
# exit()



CANVAS_WIDTH = 1800
CANVAS_HEIGHT = 900

TOTAL_SPEICES = 1

color_tables = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

from_day = 325
end_day = 334

all_grid = []


for day in range(from_day, end_day):

    all_grid = []#number of species
    grid = load_grid("./test_data2/"+str(day)+".txt")
    # showNumGrid(grid)
    all_grid.append(grid)

    print "start to draw day: %s" % day

    im = Image.new('RGBA', (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 255))
    draw = ImageDraw.Draw(im)

    for species_idx in xrange(TOTAL_SPEICES):

        layer = Image.new('RGBA', (CANVAS_WIDTH, CANVAS_HEIGHT))
        layer_draw = ImageDraw.Draw(layer)

        pixels = layer.load()
        grid = all_grid[species_idx]
        color = color_tables[species_idx]

        for x in xrange(CANVAS_WIDTH):
            for y in xrange(CANVAS_HEIGHT):

                value = int(floor(grid[y][x]/0.2)*0.2*170)
                pixels[x,y] = (color[0], color[1], color[2], value)

        im.paste(layer, mask=layer)

    # im.show()
    output_file = "./output3/%03d.png" % day
    im.save(output_file)
    print "done %s.png" % day


