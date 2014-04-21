import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import LineCollection
import numpy as np
import csv

def plot_ts(node1, node2):
	ts = np.genfromtxt('bird_timeseries.csv', delimiter=',');
	x = np.linspace(0,52,52);
	y = ts[node1,:];
	plt.plot(x, y);
	plt.hold(True);
	y = ts[node2,:];
	plt.plot(x, y);
	plt.show();
	plt.hold(False);

def my_color(val):
	return plt.cm.RdBu(val)

def get_edges_from_period(period):
	data = np.genfromtxt('map_vals.csv', delimiter=',');
	edges = data[data[:, 0] == period];
	edges = edges[edges[:, 1] == 2];
	edges = edges[:,2::];
	return edges;

def PlotBirdGraph(edges):
	data = np.genfromtxt('bird_coords.csv', delimiter=',');
	data = np.genfromtxt('map_vals.csv', delimiter=',');
	coords = data[:,3:5].transpose();

	# Lambert Conformal map of USA lower 48 states
	m = Basemap(llcrnrlon=-119, llcrnrlat=22, urcrnrlon=-64,
	urcrnrlat=49, projection='lcc', lat_1=33, lat_2=45,
	lon_0=-95, resolution='h', area_thresh=10000)

	m.drawcoastlines()
	m.drawcountries(linewidth=2)
	m.drawstates()

	m.drawmapboundary(fill_color='aqua')
	m.fillcontinents(color='coral',lake_color='aqua')
	m.drawparallels(np.arange(25,65,20),labels=[1,0,0,0])
	m.drawmeridians(np.arange(-120,-40,20),labels=[0,0,0,1])

	lat = coords[0,:];
	lon = coords[1,:];

	#edges = np.array([[1651,1701,0.5], [1701,1651,0.5], [1794,1844,0.5], [1844,1794,0.5], [1744,1794,0.5], [1794,1744,0.5], [2008,2058,0.5], [2058,2008,0.5], [1844,1894,0.5], [1894,1844,0.5], [1945,1995,0.5], [1995,1945,0.5], [1995,2045,0.5], [2045,1995,0.5], [1733,1734,0.5], [1734,1733,0.5], [2085,2134,0.5], [2134,2085,0.5], [1534,1584,0.5], [1584,1534,0.5], [1552,1603,0.5], [1603,1552,0.5], [1408,1459,0.5], [1459,1408,0.5], [1958,2009,0.5], [2009,1958,0.5], [1557,1608,0.5], [1608,1557,0.5], [1908,1959,0.5], [1959,1908,0.5], [2007,2008,0.5], [2008,2007,0.5], [2007,2058,0.5], [2058,2007,0.5], [1408,1409,0.5], [1409,1408,0.5], [1358,1409,0.5], [1409,1358,0.5], [1406,1457,0.5], [1457,1406,0.5], [1958,1959,0.5], [1959,1958,0.5], [1353,1404,0.5], [1404,1353,0.5], [1606,1657,0.5], [1657,1606,0.5], [1607,1658,0.5], [1658,1607,0.5], [1808,1859,0.5], [1859,1808,0.5], [1617,1666,0.5], [1666,1617,0.5], [1259,1310,0.5], [1310,1259,0.5], [1367,1416,0.5], [1416,1367,0.5], [1958,2009,0.5], [2009,1958,0.5], [1353,1354,0.5], [1354,1353,0.5], [1567,1616,0.5], [1616,1567,0.5], [1353,1404,0.5], [1404,1353,0.5], [1808,1859,0.5], [1859,1808,0.5], [1367,1416,0.5], [1416,1367,0.5], [1259,1310,0.5], [1310,1259,0.5], [1606,1657,0.5], [1657,1606,0.5], [1259,1260,0.5], [1260,1259,0.5], [1958,1959,0.5], [1959,1958,0.5], [1607,1658,0.5], [1658,1607,0.5], [1251,1302,0.5], [1302,1251,0.5], [1251,1302,0.5], [1302,1251,0.5], [1259,1310,0.5], [1310,1259,0.5], [1567,1616,0.5], [1616,1567,0.5], [1353,1404,0.5], [1404,1353,0.5], [1259,1260,0.5], [1260,1259,0.5], [1808,1859,0.5], [1859,1808,0.5], [1252,1302,0.5], [1302,1252,0.5], [1367,1416,0.5], [1416,1367,0.5], [1209,1210,0.5], [1210,1209,0.5], [1606,1657,0.5], [1657,1606,0.5], [1209,1260,0.5], [1260,1209,0.5], [1251,1302,0.5], [1302,1251,0.5], [1747,1797,0.5], [1797,1747,0.5], [1252,1302,0.5], [1302,1252,0.5], [1301,1302,0.5], [1302,1301,0.5], [1259,1310,0.5], [1310,1259,0.5], [1259,1260,0.5], [1260,1259,0.5], [1660,1661,0.5], [1661,1660,0.5], [1209,1210,0.5], [1210,1209,0.5], [1353,1404,0.5], [1404,1353,0.5], [1209,1260,0.5], [1260,1209,0.5], [1746,1797,0.5], [1797,1746,0.5], [1796,1797,0.5], [1797,1796,0.5], [1660,1661,0.5], [1661,1660,0.5], [1747,1797,0.5], [1797,1747,0.5], [1610,1661,0.5], [1661,1610,0.5], [1251,1302,0.5], [1302,1251,0.5], [1610,1611,0.5], [1611,1610,0.5], [1301,1302,0.5], [1302,1301,0.5], [1252,1302,0.5], [1302,1252,0.5], [1796,1797,0.5], [1797,1796,0.5], [1746,1797,0.5], [1797,1746,0.5], [1209,1260,0.5], [1260,1209,0.5], [1209,1260,0.5], [1209,1260,0.5], [1209,1260,0.5], [1209,1260,0.5], [1209,1260,0.5], [1209,1260,0.5], [1209,1260,0.5], [1209,1260,0.5], [1209,1260,0.5], [1209,1260,0.5], [1209,1260,0.5], [1209,1260,0.5], [1209,1260,0.5], [1209,1260,0.5]]);   #dis line a dick... <--the stuff
	edges = get_edges_from_period(20);

	# get coordinates of each edge
	edge_lats_src = np.array([lat[i] for i in edges[:,0]],ndmin=2);
	edge_lons_src = np.array([lon[i] for i in edges[:,0]],ndmin=2);
	edge_lats_trg = np.array([lat[i] for i in edges[:,1]],ndmin=2);
	edge_lons_trg = np.array([lon[i] for i in edges[:,1]],ndmin=2);

	#weights = 3*edges[:,2].T;
	colors = weights;
	max_weight = weights.max();
	colors = 1 - (colors/max_weight); #normalize to 0..1 and reverse

	sx, sy = m(edge_lons_src, edge_lats_src);
	tx, ty = m(edge_lons_trg, edge_lats_trg);

	x, y = m(lon, lat);
	plt.plot(x, y, 'ro', markersize=2)

	# use line collections if this slows down
	for i in range(len(weights)-1):
	    plt.plot([sx[0][i], tx[0][i]], [sy[0][i], ty[0][i]], linewidth=weights[i], color=my_color(colors[i]));

	plt.show()