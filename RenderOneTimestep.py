
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


    #  start to draw
    # CANVAS_WIDTH = 3600
    # CANVAS_HEIGHT = 1800


    GRID_WIDTH = 1800
    GRID_HEIGHT = 900

    TIME_FRAME_WINDOW = 50

    TOTAL_DAYS = 200


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

            # collect the points in time frame
            candidate_points = []
            candidate_points_table = dict()
            if day < TIME_FRAME_WINDOW:
                for p in range(0, day+1):
                    (x, y) = path[p]
                    center_value = 1 * decay(day-p)
                    grid[y][x] = center_value
                    candidate_points.append(path[p])
                    candidate_points_table[(x, y)] = center_value

            else:
                for p in range(day-TIME_FRAME_WINDOW, day+1):
                    (x, y) = path[p]
                    center_value = 1 * decay(day-p)
                    grid[y][x] = center_value
                    candidate_points.append(path[p])
                    candidate_points_table[(x, y)] = center_value


            # calculate the density map
            for j in xrange(GRID_HEIGHT):
                for i in xrange(GRID_WIDTH):
                    if (i,j) in candidate_points:
                        continue
                    else:
                        aggregated_value = 0
                        for p in candidate_points:
                            dist = hypot(abs(i-p[0]), abs(j-p[1]))
                            seed_value = candidate_points_table[p]
                            aggregated_value += gaussian(seed_value, dist)
                        grid[j][i] = aggregated_value


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

                    value = int(floor(grid[y][x]/0.2)*0.2*170)
                    pixels[x,y] = (color[0], color[1], color[2], value)

            im.paste(layer, mask=layer)

        # im.show()
        output_file = "./output4/%03d.png" % day
        im.save(output_file)
        print "done %s.png" % day

    # im_after = im.resize( (CANVAS_WIDTH*2, CANVAS_HEIGHT*2), Image.BILINEAR)
    # im_after.show()






if __name__ == '__main__':
    main(sys.argv[1:])