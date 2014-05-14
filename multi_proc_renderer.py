
from PIL import Image, ImageDraw, ImageFont
from math import floor
import gzip
from multiprocessing import Process

CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 700
color_tables = [(123, 161, 215), (95, 210, 173), (208, 143, 111), (255,127,140), (248,190,83), (254,101,113)]


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
            for w in range(len(d2)):
                new_grid[h][w] = float(d2[w])
            h += 1
    return new_grid


def draw_image(species, idx, input_folder, dest_folder):
    print "start to draw day: %s" % day
    # create base image
    im = Image.new('RGBA', (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 255))
    draw = ImageDraw.Draw(im)

    background = Image.open ("images/map.png")
    im.paste(background, mask=background)

    for s_idx in xrange(TOTAL_SPECIES):
        grid = load_grid(input_folder+species[s_idx]+"/"+str(idx)+".gz")
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
                    pixels[x, y] = (color[0], color[1], color[2], value)
        im.paste(layer, mask=layer)

    # draw legends
    legend_font = ImageFont.truetype("./resources/pointfree.ttf", 15)
    legend_count = 0
    for name in species_data_folder:
        x1, x2 = 50, 70
        y1, y2 = CANVAS_HEIGHT - 200 + 25*legend_count, CANVAS_HEIGHT - 180 + 25*legend_count
        draw_points = ((x1, y1), (x2, y1), (x2, y2), (x1, y2))
        color = color_tables[legend_count]
        draw.polygon(draw_points, fill=(color[0],color[1],color[2],180))
        draw.text((x2 + 10, y1), name, fill="black", font=legend_font)
        legend_count += 1

    output_file = dest_folder+"%03d.png" % idx
    im.save(output_file)
    print "done %s.png" % day


# species_data_folder = ["BlueShark", "CommonThresherShark", "JuvenileWhiteShark", "SalmonShark", "WhiteShark"]
# species_data_folder = ["JuvenileWhiteShark", "WhiteShark"]
species_data_folder = ["CommonThresherShark"]
TOTAL_SPECIES = len(species_data_folder)

input_folder = "./day_result/"
dest_folder = "./temp_circle/"

from_day = 0
end_day = 64
for day in range(from_day, end_day+1):
    p = Process(target=draw_image, args=(species_data_folder, day, input_folder, dest_folder))
    p.start()
