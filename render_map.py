from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# resolution = 'c' means use crude resolution coastlines.
my_dpi = 96
fig = plt.figure(figsize=(16.67, 7.29), dpi=my_dpi)
m = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=62,
            llcrnrlon=120, urcrnrlon=260, resolution='i')
# m = Basemap(projection='merc', llcrnrlat=0, urcrnrlat=70,
#             llcrnrlon=-240, urcrnrlon=-100, resolution='c')
# m.drawcoastlines(color='#888888')
m.fillcontinents(color='#888888', lake_color='#999999')

m.drawmapboundary(fill_color='white')

startx, starty = m(120, 62)
endx, endy = m(260, 0)

print startx, starty
print endx, endy
unit = 10000
GRID_WIDTH = int((endx-startx)/unit)+1
GRID_HEIGHT = int((starty-endy)/unit)+1
print "canvas:", GRID_WIDTH, "X", GRID_HEIGHT
# m.bluemarble()
# plt.title("Miller Cylindrical Projection")

# plt.figure(figsize=(1600/my_dpi, 700/my_dpi), dpi=my_dpi)
plt.savefig('my_fig.png', dpi=my_dpi)
plt.show()
#cyl