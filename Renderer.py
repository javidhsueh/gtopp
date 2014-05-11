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

from_day = 0
end_day = 1981

all_grid = []

counter = 0
for day in range(from_day, end_day, 30):

    all_grid = [] #number of species
    grid = load_grid("./BlueShark_365/"+str(day)+".txt")
    # showNumGrid(grid)
    all_grid.append(grid)

    # normalize the grid:
    max_value = 0
    for y in xrange(CANVAS_HEIGHT):
        temp_max = max(grid[y])
        max_value = max(max_value, temp_max)

    print max_value

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
                if grid[y][x] == 0:
                    continue
                else:
                    # value = int( (floor( (grid[y][x]/max_value)/0.2))*0.2*170 )
                    value = int( (floor(grid[y][x]/0.2))*0.2*170 )
                    pixels[x,y] = (color[0], color[1], color[2], value)

        im.paste(layer, mask=layer)


    # im.show()
    output_file = "./blueshark_output_365_2/%03d.png" % counter
    im.save(output_file)
    print "done %s.png" % day

    counter += 1


