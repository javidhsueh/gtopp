
import json
from PIL import Image, ImageDraw, ImageFont
from math import floor
from multiprocessing import Process
from math import hypot
from utils.Gaussian import gaussian, decay_gaussian
from datetime import date
from dateutil.rrule import rrule, DAILY
from math import sqrt

GRID_WIDTH = 1557 #120~280
GRID_HEIGHT = 885 #0~60

MAX_VALUE = 0.85

GAUSSIAN_RANGE = 20
TIME_FRAME_WINDOW = 150
COLOR_TABLE = [(123, 161, 215), (95, 210, 173), (208, 143, 111), (255, 127, 140), (248, 190, 83), (153, 190, 196)]


def read_json(fn):
    with open(fn, "rb") as json_file:
        raw_data = json.load(json_file)
    return raw_data


def gen_emptyGrid():
    grid = [[0 for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)]
    return grid


def gen_gaussian_table(d_table):
    g_table = dict()
    for i in range(GAUSSIAN_RANGE+1):
        for j in range(GAUSSIAN_RANGE+1):
            d = d_table[(i, j)]
            if d < GAUSSIAN_RANGE:
                # g_table[d] = 1.0-(d/GAUSSIAN_RANGE)
                g_table[d] = gaussian(1,d)
            else:
                g_table[d] = 0
    return g_table


def gen_decay_table():
    d_table = dict()
    for i in xrange(TIME_FRAME_WINDOW+1):
        d_table[i] = decay_gaussian(TIME_FRAME_WINDOW/2, i)
    return d_table


def gen_dist_table():
    d_table = dict()
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            d_table[(i,j)] = hypot(i, j)
    return d_table


def build_species_grid(day, all_position, gaussian_table, decay_table, dist_table):
    grid = gen_emptyGrid()

    # collect the points in time frame
    candidate_points = []
    candidate_points_table = dict()

    # seed points with decay
    if day < TIME_FRAME_WINDOW:
        for p in range(day+1):
            if table[p] in all_position:
                for sample in all_position[table[p]]:
                    (x, y) = (sample["long"], sample["lat"])
                    center_value = decay_table[day-p]
                    grid[y][x] = center_value
                    candidate_points.append((x, y))
                    candidate_points_table[(x, y)] = center_value
    else:
        for p in range(day-TIME_FRAME_WINDOW, day+1):
            if table[p] in all_position:
                for sample in all_position[table[p]]:
                    (x, y) = (sample["long"], sample["lat"])
                    center_value = decay_table[day-p]
                    if y < 0 or y > GRID_HEIGHT or x < 0 or x > GRID_WIDTH:
                        continue
                    grid[y][x] = center_value
                    candidate_points.append((x, y))
                    candidate_points_table[(x, y)] = center_value

    for p_idx in range(len(candidate_points)):
        (x, y) = candidate_points[p_idx]
        seed_value = candidate_points_table[(x, y)]
        for i in range(-1*GAUSSIAN_RANGE, +1*GAUSSIAN_RANGE):
            for j in range(-1*GAUSSIAN_RANGE, +1*GAUSSIAN_RANGE):
                if 0 <= x+i <= GRID_WIDTH-1 and 0 <= y+j <= GRID_HEIGHT-1:
                    dist = dist_table[(abs(i), abs(j))]
                    grid[y+j][x+i] += seed_value * gaussian_table[dist]
                    if grid[y+j][x+i] > MAX_VALUE:
                        grid[y+j][x+i] = MAX_VALUE

    return grid

# init settings
all_species = ["BlueShark", "CommonThresherShark", "JuvenileWhiteShark", "SalmonShark", "WhiteShark", "ShortfinMakoShark"]
# all_species = ["BlueShark"]
TOTAL_SPECIES = len(all_species)

# build pre-calculation tables
dist_table = gen_dist_table()
gaussian_table = gen_gaussian_table(dist_table)
decay_table = gen_decay_table()

# read data from files
legend_font = ImageFont.truetype("./resources/pointfree.ttf", 15)
species_position_table = dict()
species_color_table = dict()
species_idx = 0
for species in all_species:
    species_position_table[species] = read_json("./data_new_unit/"+species+".json")
    species_color_table[species] = COLOR_TABLE[species_idx]

    dd = []
    for single in species_position_table[species]:
        dd.append(single)
    dd.sort()
    start = str(dd[0]).split("-")
    end = str(dd.pop()).split("-")

    a = date(int(start[0]), int(start[1]), int(start[2]))
    b = date(int(end[0]), int(end[1]), int(end[2]))
    table = []
    total_day = 0
    for dt in rrule(DAILY, dtstart=a, until=b):
        table.append(dt.strftime("%Y-%m-%d"))
        total_day += 1
    print "%s has %s days." % (species, total_day)
    species_idx += 1

dest_folder = "./demo_result/"

from_day = 0
end_day = 2035
interval = 5
file_name_count = 0

for day in range(from_day, end_day+1, interval):
    print "start to draw day: %s" % day
    # create base image
    im = Image.new('RGB', (GRID_WIDTH, GRID_HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    paper_ocean = Image.open ("images/paper_map_ocean.png")
    im.paste(paper_ocean, mask=paper_ocean)

    pixels = im.load()

    # build all grids of species and draw
    for species in all_species:
        grid = build_species_grid(day, species_position_table[species], gaussian_table, decay_table, dist_table)
        color = species_color_table[species]
        for x in xrange(GRID_WIDTH):
            for y in xrange(GRID_HEIGHT):
                if grid[y][x] == 0:
                    continue
                else:
                    unlinear_scale = grid[y][x]
                    # unlinear_scale = pow(grid[y][x], 2)
                    # if grid[y][x] < 0.1:
                    #     alpha = 0.01
                    # else:
                    #     alpha = floor(unlinear_scale/0.2)*0.2
                    alpha = floor(unlinear_scale/0.2)*0.2
                    blended_r = int(color[0]*alpha + (1-alpha)*pixels[x, y][0])
                    blended_g = int(color[1]*alpha + (1-alpha)*pixels[x, y][1])
                    blended_b = int(color[2]*alpha + (1-alpha)*pixels[x, y][2])
                    pixels[x, y] = (blended_r, blended_g, blended_b)

    paper_continent = Image.open ("images/paper_map_land.png")
    im.paste(paper_continent, mask=paper_continent)

    # draw legends
    legend_count = 0
    for species in all_species:
        x1, x2 = 50, 70
        y1, y2 = GRID_HEIGHT - 200 + 25*legend_count, GRID_HEIGHT - 180 + 25*legend_count
        draw_points = ((x1, y1), (x2, y1), (x2, y2), (x1, y2))
        color = species_color_table[species]
        draw.polygon(draw_points, fill=(color[0], color[1], color[2],180))
        draw.text((x2 + 10, y1), species, fill="black", font=legend_font)
        legend_count += 1

    output_file = dest_folder+"%04d.png" % file_name_count
    im.save(output_file)
    print "done %s.png" % day

    file_name_count += 1