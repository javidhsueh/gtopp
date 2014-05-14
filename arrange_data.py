__author__ = 'tlfung'
import csv
import numpy
import datetime
import simplejson
import json
from datetime import date
from dateutil.rrule import rrule, DAILY
import sys
from mpl_toolkits.basemap import Basemap

UNIT = 10000
#1780 X 1106
#1557 X 885
GRID_WIDTH = 1557
GRID_HEIGHT = 885


def read_data(fn):
    f = fn.split(".")[0]
    m = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=62,
                llcrnrlon=120, urcrnrlon=260, resolution='c')
    start_x, start_y = m(120, 70)
    end_x, end_y = m(280, 0)
    # print start_x, start_y
    # print end_x, end_y

    days = dict()
    raw_data = csv.reader(open(fn, 'rb'), delimiter='\t')
    for row in raw_data:
        obj = dict()
        elements = row[0].split(",")
        mydate = datetime.datetime.strptime(elements[6], "%Y-%m-%dT%H:%M:%SZ")
        #print date.year
        #obj=[elements[0], date.day, elements[7], elements[8]]
        #obj["species"] = elements[0]
        real_long = float(elements[7])
        real_lat = float(elements[8])
        x, y = m(real_long, real_lat)
        point_x = int(x/UNIT)
        point_y = int(y/UNIT)
        obj["long"] = point_x
        obj["lat"] = GRID_HEIGHT-point_y
        if real_long > 260 or real_lat > 62:
            print real_long, real_lat
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
    print simplejson.dumps(days)
    with open("./output_data/" + f + ".json", "w") as json_file:
        json_file.write(simplejson.dumps(days))


if __name__ == '__main__':
    # load_grid("./BlueShark/0.gz")
    read_data("BlueShark.csv")
    read_data("WhiteShark.csv")
    read_data("SalmonShark.csv")
    read_data("CommonThresherShark.csv")
    # read_data("ShortfinMakoShark.csv") #problems
    read_data("JuvenileWhiteShark.csv")

# create_grid("./data/Blue Shark_d.json")

