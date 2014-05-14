
import csv
import numpy
import datetime
import simplejson
import json
from utils.Decay import decay
from math import hypot
from utils.Gaussian import gaussian, decay_gaussian
from datetime import date
from dateutil.rrule import rrule, DAILY
import sys
import StringIO
import gzip

GRID_WIDTH = 1600 #120~280
GRID_HEIGHT = 700 #0~60

GAUSSIAN_RANGE = 180

TIME_FRAME_WINDOW = 150
#GAUSSIAN_RANGE = 250

use = '''
  Require:
  -i : input file name
  Option:
  -o : output folder
'''


def main(argv):

    if len(argv) < 1:
        print use
        return
    
    filename = ""
    outputfolder = ""
    for arg in argv:
        ary = arg.split('=')
        if ary[0] == '-i':
            filename = ary[1]
        if ary[0] == '-o':
            outputfolder = ary[1]
    
    if filename == "":
        print use
        exit()

    # start your program
    create_grid(filename, outputfolder)


def read_data(fn):
    f = fn.split(".")[0]

    days = dict()
    raw_data = csv.reader(open(fn, 'rb'), delimiter='\t')
    for row in raw_data:
        obj = dict()
        elements = row[0].split(",")
        mydate = datetime.datetime.strptime(elements[6], "%Y-%m-%dT%H:%M:%SZ")
        #print date.year
        #obj=[elements[0], date.day, elements[7], elements[8]]
        #obj["species"] = elements[0]
        obj["long"] = elements[7]
        obj["lat"] = elements[8]
        #onedate = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
        onedate = date(mydate.year, mydate.month, mydate.day).strftime("%Y-%m-%d")

        print onedate
        if onedate in days:
            days[onedate].append(obj)
        else:
            days[onedate] = []
            days[onedate].append(obj)
        # obj["day"] = date.day

        # time = str(date.year)+"-"+str(date.month)
        # months[time].append(obj)

        print obj
    #print simplejson.dumps(days)
    with open(f + ".json", "w") as json_file:
        json_file.write(simplejson.dumps(days))


def read_json(fn):
    with open(fn, "rb") as json_file:
        raw_data = json.load(json_file)
    return raw_data


def genEmptyGrid():
    grid = [ [ 0 for i in range(GRID_WIDTH) ] for j in range(GRID_HEIGHT) ]
    return grid


def gaussian_table(d_table):
    g_table = dict()
    for i in range(GAUSSIAN_RANGE+1):
        for j in range(GAUSSIAN_RANGE+1):
            d = d_table[(i, j)]
            g_table[d] = gaussian(1, d)
            # if d < GAUSSIAN_RANGE:
            # # g_table[d] = gaussian(1, d)
            #     g_table[d] = d/GAUSSIAN_RANGE
            # else:
            #     g_table[d] = 0
    return g_table


def gen_decay_table():
    d_table = dict()
    for i in xrange(TIME_FRAME_WINDOW+1):
        d_table[i] = decay_gaussian(TIME_FRAME_WINDOW/2, i)
    return d_table


def dist_table():
    d_table = dict()
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            d_table[(i,j)] = hypot(i, j)
    return d_table


def create_grid(fn, fo):
    d_table = dist_table()
    g_table = gaussian_table(d_table)
    decay_table = gen_decay_table()

    all_position = read_json(fn)
    total_day = 0
    #print all_position
    dd = []
    for single in all_position:
        dd.append(single)
    dd.sort()
    start = str(dd[0]).split("-")
    end = str(dd.pop()).split("-")

    a = date(int(start[0]), int(start[1]), int(start[2]))
    b = date(int(end[0]), int(end[1]), int(end[2]))
    #index = 0
    table = []
    for dt in rrule(DAILY, dtstart=a, until=b):
        table.append(dt.strftime("%Y-%m-%d"))
        total_day += 1
        #print dt.strftime("%Y-%m-%d")
    print total_day
    #sys.exit()

    # total_day = 301
    for one in range(0, total_day): #total_day
        grid = genEmptyGrid()

        # collect the points in time frame
        candidate_points = []
        candidate_points_table = dict()

        # seed points with decay
        if one < TIME_FRAME_WINDOW:
            for p in range(one+1):
                if table[p] in all_position:
                    #print table[p], all_position[table[p]]
                    for sample in all_position[table[p]]:
                        lng = float(sample["long"])
                        lat = float(sample["lat"])
                        point = (int(round((lng-120)*10)), int(round(lat*10)))
                        (x, y) = point
                        center_value = decay_table[one-p]
                        # print "day: %s, p: %s, delta_day: %s, decay: %s" %(one,p, (one-p) , center_value)
                        grid[y][x] = center_value
                        candidate_points.append(point)
                        candidate_points_table[(x, y)] = center_value
                        #print point
            # print candidate_points
        else:
            for p in range(one-TIME_FRAME_WINDOW, one+1):
                if table[p] in all_position:
                    # print all_position[table[p]]
                    for sample in all_position[table[p]]:
                        lng = float(sample["long"])
                        lat = float(sample["lat"])
                        point = (int(round((lng-120)*10)), int(round(lat*10)))
                        (x, y) = point
                        center_value = decay_table[one-p]
                        # print "day: %s, p: %s, delta_day: %s, decay: %s" %(one,p, (one-p) , center_value)
                        grid[y][x] = center_value
                        candidate_points.append(point)
                        candidate_points_table[(x, y)] = center_value

        for p_idx in range(len(candidate_points)):
            p = candidate_points[p_idx]
            (x, y) = p
            seed_value = candidate_points_table[p]
            for i in range(-1*GAUSSIAN_RANGE, +1*GAUSSIAN_RANGE):
                for j in range(-1*GAUSSIAN_RANGE, +1*GAUSSIAN_RANGE):
                    # if i == 0 and j == 0:
                    #     continue
                    if 0 <= x+i <= GRID_WIDTH-1 and 0 <= y+j <= GRID_HEIGHT-1:
                        dist = d_table[(abs(i), abs(j))]
                        spread_value = seed_value * g_table[dist]
                        if spread_value > grid[y+j][x+i]:
                            grid[y+j][x+i] = spread_value

        # for j in xrange(GRID_HEIGHT):
        #         for i in xrange(GRID_WIDTH):
        #             aggregated_value = 0
        #             max_val = 0
        #             for p_idx in range(len(candidate_points)):
        #                 p = candidate_points[p_idx]
        #                 dist = d_table[(abs(i-p[0]), abs(j-p[1]))]
        #                 if dist < 190:
        #                     seed_value = candidate_points_table[p]
        #                     # aggregated_value += seed_value * g_table[dist]
        #                     g = seed_value * g_table[dist]
        #                     if g > max_val:
        #                         max_val = g
        #                     # print "pixel(%s,%s), seed point[%s]:(%s,%s)" % (i,j,p_idx, p[0],p[1])
        #                     # print "dist: %s, seed_value: %s, g=%s" % (dist, seed_value, g_table[dist][0])
        #
        #             # grid[j][i] = aggregated_value
        #             grid[j][i] = max_val
        #sys.exit()

        out = StringIO.StringIO()
        with gzip.open("./"+fo+"/"+str(one)+".gz", "w") as f:
            for g in grid:
                row = ",".join("%s" % i for i in g)
                f.write(row+"/t")
        out.close()


if __name__ == '__main__':
    main(sys.argv[1:])
    # load_grid("./BlueShark/0.gz")
    # read_data("BlueShark.csv")
    # read_data("WhiteShark.csv")
    # read_data("SalmonShark.csv")
    # read_data("CommonThresherShark.csv")
    # read_data("ShortfinMakoShark.csv") #problems
    # read_data("JuvenileWhiteShark.csv")

# create_grid("./data/Blue Shark_d.json")

