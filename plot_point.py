__author__ = 'tlfung'
import csv
import numpy
import datetime
import simplejson
import json
from math import hypot
from datetime import date
from dateutil.rrule import rrule, DAILY
import sys
from PIL import Image, ImageDraw, ImageFont
import gzip
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

GRID_WIDTH = 1557
GRID_HEIGHT = 885

TIME_FRAME_WINDOW = 150
#GAUSSIAN_RANGE = 250
FIGDPI=96
PADDING = 2

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
    data = []
    with open(fn, "rb") as json_file:
        raw_data = json.load(json_file)
        #raw_data=json_file.read()
        #print raw_data["2003-12"]
    #print raw_data
    return raw_data


def genEmptyGrid():
    grid = [ [ 0 for i in range(GRID_WIDTH) ] for j in range(GRID_HEIGHT) ]
    return grid


def grid_point(fn, fo):
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

    for one in range(0, total_day, 30): #total_day
        grid = genEmptyGrid()
        lats = []
        lons = []
        # collect the points in time frame
        candidate_points = []
        candidate_points_table = dict()

        # seed points with decay
        if one < TIME_FRAME_WINDOW:
            for p in range(one+1):
                if table[p] in all_position:
                    #print table[p], all_position[table[p]]
                    for sample in all_position[table[p]]:
                        long = sample["long"]
                        lat = sample["lat"]

                        grid[lat][long] = 1
                        # candidate_points.append(point)

                        #print point
            # print candidate_points
        else:
            for p in range(one-TIME_FRAME_WINDOW, one+1):
                if table[p] in all_position:
                    # print all_position[table[p]]
                    for sample in all_position[table[p]]:
                        long = sample["long"]
                        lat = sample["lat"]

                        grid[lat][long] = 1
                        #candidate_points.append(point)

        # set dpi of figure, so that all calculations use this value

        im = Image.new('RGBA', (GRID_WIDTH, GRID_HEIGHT), (0, 0, 0, 255))
        draw = ImageDraw.Draw(im)

        background = Image.open("images/map_i.png")
        im.paste(background, mask=background)

        layer = Image.new('RGBA', (GRID_WIDTH, GRID_HEIGHT))
        layer_draw = ImageDraw.Draw(layer)
        pixels = layer.load()
        color = (180, 50, 130)
        for j in xrange(GRID_HEIGHT):
            for i in xrange(GRID_WIDTH):
                if grid[j][i] == 0:
                    continue
                else:
                    layer_draw.point((i, j), fill=color)

        #sys.exit()
        im.paste(layer, mask=layer)


        output_file = "./SalmonShark_output_point/" + table[one] + ".png"
        im.save(output_file)



if __name__ == '__main__':
    grid_point("./output_data/SalmonShark.json", "out")

