__author__ = 'tlfung'
import csv
import numpy
import datetime
import simplejson
import json
from utils.Decay import decay
from math import hypot
from utils.Gaussian import gaussian
from datetime import date
from dateutil.rrule import rrule, DAILY
import sys

GRID_WIDTH = 1800
GRID_HEIGHT = 900

TIME_FRAME_WINDOW = 30
GAUSSIAN_RANGE = 250

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
    output_name = ""
    for arg in argv:
        ary = arg.split('=')
        if ary[0] == '-i':
            filename = ary[1]
        if ary[0] == '-o':
            output_folder = ary[1]
    
    if filename == "":
        print use
        exit()

    # start your program
    create_grid(filename, output_folder)


def init():
    for y in range(2002, 2015):
        for m in range(1, 13):
            s=str(y)+"-"+str(m)
            # months[s] = []


def read_data(fn):
    f=fn.split(".")[0]
    # months = dict()
    # for y in range(2002, 2015):
    #     for m in range(1, 13):
    #         s=str(y)+"-"+str(m)
    #         months[s] = []
    days = dict()
    raw_data = csv.reader(open(fn, 'rb'), delimiter='\t')
    for row in raw_data:
        obj = dict()
        elements = row[0].split(",")
        date = datetime.datetime.strptime(elements[6], "%Y-%m-%dT%H:%M:%SZ")
        #print date.year
        #obj=[elements[0], date.day, elements[7], elements[8]]
        #obj["species"] = elements[0]
        obj["long"] = elements[7]
        obj["lat"] = elements[8]
        onedate=str(date.year)+"-"+str(date.month)+"-"+str(date.day)
        if onedate in days:
            days[onedate].append(obj)
        else:
            days[onedate] = []
            days[onedate].append(obj)
        #obj["day"] = date.day

        time = str(date.year)+"-"+str(date.month)
        # months[time].append(obj)

        print obj
    #print simplejson.dumps(days)
    with open(f+"_d.json", "w") as json_file:
        json_file.write(simplejson.dumps(days))


def read_json(fn):
    data=[]
    with open(fn, "rb") as json_file:
        raw_data=json.load(json_file)
        #raw_data=json_file.read()
        #print raw_data["2003-12"]
    #print raw_data
    return raw_data


def genEmptyGrid():
    grid = [ [ 0 for i in range(GRID_WIDTH) ] for j in range(GRID_HEIGHT) ]
    return grid


def create_grid(fn,fo):
    all_position = read_json(fn)
    total_day=0
    #print all_position
    a = date(2002, 1, 1)
    b = date(2003, 12, 31)
    index = 0
    table = []
    for dt in rrule(DAILY, dtstart=a, until=b):
        table.append(dt.strftime("%Y-%m-%d"))
        index +=1
        #print dt.strftime("%Y-%m-%d")

    for one in range(335,336):
        grid = genEmptyGrid()
        # seed points and decay and gaussian
        if one < TIME_FRAME_WINDOW:
            for p in range(one):
                #print table[p],"------------"
                if table[p] in all_position:
                    # print all_position[table[p]]
                    for sample in all_position[table[p]]:
                        long = float(sample["long"])
                        lat = float(sample["lat"])
                        (x, y) = (int(round(long))*5, (int(round(lat))+90)*5)

                        # decay by time
                        center_value = 1 * decay(one-p)
                        grid[y][x] += center_value

                        # apply gaussian to neighborhood, decay by distance
                        for i in range(-1*GAUSSIAN_RANGE, GAUSSIAN_RANGE):
                            for j in range(-1*GAUSSIAN_RANGE, GAUSSIAN_RANGE):
                                if i == 0 and j == 0:
                                    continue

                                if 0 < x+i < GRID_WIDTH-1 and 0 < y+j < GRID_HEIGHT-1:

                                    dist = hypot(i, j)
                                    if dist <= GAUSSIAN_RANGE:
                                        grid[y+j][x+i] += gaussian(center_value, dist)
        else:
            for p in range(one-TIME_FRAME_WINDOW, one+1):
                if table[p] in all_position:
                    # print all_position[table[p]]
                    for sample in all_position[table[p]]:
                        long = float(sample["long"])
                        lat = float(sample["lat"])
                        (x, y) = (int(round(long))*5, (int(round(lat))+90)*5)
                        # decay by time
                        center_value = 1 * decay(one-p)
                        grid[y][x] += center_value

                        # apply gaussian to neighborhood, decay by distance
                        for i in range(-1*GAUSSIAN_RANGE, GAUSSIAN_RANGE):
                            for j in range(-1*GAUSSIAN_RANGE, GAUSSIAN_RANGE):
                                if i == 0 and j == 0:
                                    continue

                                if 0 < x+i < GRID_WIDTH-1 and 0 < y+j < GRID_HEIGHT-1:

                                    dist = hypot(i, j)
                                    if dist <= GAUSSIAN_RANGE:
                                        grid[y+j][x+i] += gaussian(center_value, dist)

        with open("./"+fo+"/"+str(one)+".txt", "w") as f:
            for g in grid:
                for gg in g:
                    f.write(str(gg)+",")
                f.write("/t")


def load_grid(fn):
    new_grid = genEmptyGrid()
    h=0
    with open(fn, "r") as file:
        for d in file.read().split("/t"):
            d2 = d.split(",")

            d2.pop()
            # print d2
            for w in range(len(d2)):
                new_grid[h]=d2
            h+=1
    # print new_grid
    return new_grid
        # months = dict()

# init()
# read_data("Blue Shark.csv")
# read_data("White Shark.csv")
# read_data("Salmon Shark.csv")
# read_data("Common Thresher Shark.csv")
# read_data("Shortfin Mako Shark.csv")
# read_data("Juvenile White Shark.csv")

# create_grid("./data/Blue Shark_d.json")
#load_grid("330_1.txt")

if __name__ == '__main__':
    main(sys.argv[1:])


