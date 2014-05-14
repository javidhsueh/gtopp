
import sys
from PIL import Image, ImageDraw, ImageFont
from random import randint
from math import floor
import gzip



CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 700

TOTAL_SPEICES = 1



def genEmptyGrid():
    grid = [ [ 0 for i in range(CANVAS_WIDTH) ] for j in range(CANVAS_HEIGHT) ]
    return grid



def load_grid(fn):
    new_grid = genEmptyGrid()
    h = 0
    with gzip.open(fn, "rb") as file:
        for d in file.read().split("/t"):
            d2 = d.split(",")

            d2.pop()
            # print d2
            for w in range(len(d2)):
                new_grid[h][w] = float(d2[w])
            h += 1
    # print new_grid
    return new_grid


color_tables = [(123, 161, 215), (95, 210, 173), (208, 143, 111), (255,127,140), (248,190,83), (254,101,113)]

from_day = 0
end_day = 594

# species_data_folder = ["BlueShark", "CommonThresherShark", "JuvenileWhiteShark", "SalmonShark", "WhiteShark"]
species_data_folder = [ "JuvenileWhiteShark", "WhiteShark"]

TOTAL_SPECIES = len(species_data_folder)

aggregate_grid = genEmptyGrid()
max_agg_value = 0


counter = 0
for day in range(from_day, end_day+1):

    print "start to draw day: %s" % day
    # create base image
    im = Image.new('RGBA', (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 255))
    draw = ImageDraw.Draw(im)
    layers = []

    # bottom layer
    background = Image.open ("images/map.png")
    im.paste(background, mask=background)

    for s_idx in xrange(TOTAL_SPECIES):

        grid = load_grid("./keep_it/day_result/"+species_data_folder[s_idx]+"/"+str(day)+".gz")

        # accumulate grid:
        for y in xrange(CANVAS_HEIGHT):
            for x in xrange(CANVAS_WIDTH):
                aggregate_grid[y][x] += grid[y][x]
                if aggregate_grid[y][x] > max_agg_value:
                    max_agg_value = aggregate_grid[y][x]


        # normalize the grid:
        # max_value = 0
        # for y in xrange(CANVAS_HEIGHT):
        #     temp_max = max(grid[y])
        #     max_value = max(max_value, temp_max)
        # print max_value

        # create layer
        layer = Image.new('RGBA', (CANVAS_WIDTH, CANVAS_HEIGHT))

        color = color_tables[s_idx]
        pixels = layer.load()

        for x in xrange(CANVAS_WIDTH):
            for y in xrange(CANVAS_HEIGHT):
                if grid[y][x] == 0:
                    continue
                else:
                    # value = int(((floor(grid[y][x]/0.2))*0.2+0.01)*170)
                    value = int( (floor(grid[y][x]/0.2))*0.2*180 )
                    # value = int( (grid[y][x]/max_value)*155)+30
                    # value = int(grid[y][x]*180)
                    # value = int(grid[y][x]*180)
                    pixels[x,y] = (color[0], color[1], color[2], value)
        # im.paste(layer, mask=layer)
        layers.append(layer)

    # agg_layer = Image.new('RGBA', (CANVAS_WIDTH, CANVAS_HEIGHT))
    # pixels = agg_layer.load()
    # for x in xrange(CANVAS_WIDTH):
    #         for y in xrange(CANVAS_HEIGHT):
    #             value = int(aggregate_grid[y][x] * 140)
    #             if value > 140:
    #                 value = 140
    #             pixels[x,y] = (200, 200, 200, value)
    # im.paste(agg_layer, mask=agg_layer)

    for layer in layers:
        im.paste(layer, mask=layer)


    # draw legends
    legend_font = ImageFont.truetype("./resources/pointfree.ttf", 15)
    legend_count = 0
    # print category
    for name in species_data_folder:
        x1, x2 = 50, 70
        y1, y2 = CANVAS_HEIGHT - 200 + 25*legend_count, CANVAS_HEIGHT - 180 + 25*legend_count
        draw_points = ((x1, y1), (x2, y1), (x2, y2), (x1, y2))
        color = color_tables[legend_count]
        draw.polygon(draw_points, fill=(color[0],color[1],color[2],180))
        draw.text((x2 + 10, y1), name, fill="black", font=legend_font)
        legend_count += 1

    # im.show()
    output_file = "./day_composite_2/%03d.png" % counter
    im.save(output_file)
    print "done %s.png" % day

    counter += 1


