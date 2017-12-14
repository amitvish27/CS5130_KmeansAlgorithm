#imports 
import math
import random

import numpy as np
import pandas as pd
import plotly
from plotly.graph_objs import Figure, Layout, Scatter, Scattergeo

from cluster import Cluster, Point, distance

'''
This program is an implementation of K-means clustering algorithm
which reads the restaurants datasets to find the best location
'''
#global variables for configuration
dataset_file = "./dataset.csv"
ds_col_list = ["name", "latitude", "longitude", "rating"]
clusters_count = 4
tolerance = 0.2
drawMap = False


def make_points(list_x, list_y, wt_list):
    '''
    create point objects from 3 lists and return list with coordinates 
    '''
    p = []
    for x,y,wt in zip(list_x, list_y, wt_list) :
        p.append(Point([x, y], wt))
    return p

def read_from_csv(col_list):
    '''
    returns a list of points containing col1 as labels, and col2,col3
    as coordinate (x,y) from the dataset 
    '''
    csv_data = pd.read_csv(dataset_file)
    csv_data.head()
    wts_list = []
    labels = csv_data[col_list[0]].values
    list_lat = csv_data[col_list[1]].values
    list_lon = csv_data[col_list[2]].values
    p=[]
    wts_list=[]
    if len(col_list) == 4 :
        wts_list = csv_data[col_list[3]].values
    else:
        wts_list = [1 for _ in csv_data[col_list[0]].values]    
    #make points list
    #print(wts_list)
    p = make_points(list_lat, list_lon, wts_list)
    
    return labels, p


def kmeans(points):
    '''
    This function applies kmeans algorithm to sets of points and
    returns set of points defined for n no. of cluster
    '''
    #select and initialize random points for clusters
    initial = random.sample(points,clusters_count)
    clusters = [Cluster([p]) for p in initial]
    i=0
    while True:
        i+=1
        lists = [[] for _ in clusters]
        count = len(clusters)

        for p in points:
            d = distance(p, clusters[0].centroid)
            c_ind=0
            for j in range(count-1):
                new_d = distance(p, clusters[j+1].centroid)
                if new_d < d:
                    d = new_d
                    c_ind = j+1
            lists[c_ind].append(p)
        max_diff = 0.0
       
        for j in range(count):
            diff = clusters[j].update(lists[j])
            max_diff = max(max_diff,diff)
        
        if max_diff < tolerance:
            print("Total iterations to converge ", i)
            break
    return clusters

def plot_gmap(data):
    '''
    method to plot clusters on map using google map api
    '''
    from bokeh.io import output_file, output_notebook, show
    from bokeh.models import (
    GMapPlot, GMapOptions, ColumnDataSource, Circle, LogColorMapper, BasicTicker, ColorBar,
    Range1d, PanTool, WheelZoomTool, BoxSelectTool
    )
    from bokeh.models.mappers import ColorMapper, LinearColorMapper
    from bokeh.palettes import Viridis5

    latlist = [] #
    lonlist = []
    sizelist = []
    colorlist = []
    
    for i,c in enumerate(data):
        cluster_data = []
        for point in c.points:
            cluster_data.append(point.coords)
        
        for ind,item in enumerate(cluster_data):
            latlist.append(item[0])
            lonlist.append(item[1])
            sizelist.append(10)
            colorlist.append(50*(i+1))
        #add all centroids
        latlist.append(c.centroid.coords[0])
        lonlist.append(c.centroid.coords[1])
        sizelist.append(20)
        colorlist.append(0)
    
    source = ColumnDataSource(
        data = dict(
            lat=latlist,
            lon=lonlist,
            size=sizelist,
            color=colorlist
        )
    )
    
    mapcenter_lat = np.median(latlist)
    mapcenter_lon = np.median(lonlist)
    map_options = GMapOptions(lat=mapcenter_lat, lng=mapcenter_lon, map_type="roadmap", zoom=4)

    plot = GMapPlot(x_range=Range1d(), y_range=Range1d(), map_options=map_options)
    plot.title.text = "Found %s best locations" % str(len(data))
    plot.api_key = "AIzaSyBYrbp34OohAHsX1cub8ZeHlMEFajv15fY"
    
    color_mapper = LinearColorMapper(palette=Viridis5)
    circle = Circle(x="lon", y="lat", size="size", fill_color={'field': 'color', 'transform': color_mapper}, fill_alpha=0.75, line_color=None)
    plot.add_glyph(source, circle)
    plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
    output_file("gmap_plot.html")
    show(plot)


### For plotting graph and map working
def plot_graph(data):
    tracelist = [] #
    for i,c in enumerate(data):
        cluster_data = []
        for point in c.points:
            cluster_data.append(point.coords)
        trace = {}
        centroid = {}
        #trace cluster points
        trace['mode'] = 'markers'
        trace['marker'] = {}
        trace['marker']['symbol'] = i
        trace['marker']['size'] = 5
        trace['name'] = str(i)
        if drawMap :
            trace['lat'], trace['lon'] = zip(*cluster_data)
            tracelist.append(Scattergeo(**trace))
        else:
            trace['x'], trace['y'] = zip(*cluster_data)
            tracelist.append(Scatter(**trace))
        
        #draw centroids
        centroid['mode'] = 'markers'
        centroid['marker'] = {}
        centroid['marker']['symbol'] = i
        centroid['marker']['color'] = 'rgb(200,10,10)'
        centroid['name'] = "Centroid "+str(i)
        
        if drawMap:
            centroid['lat'] = [c.centroid.coords[0]]
            centroid['lon'] = [c.centroid.coords[1]]
            tracelist.append(Scattergeo(**centroid))
        else:
            centroid['x'] = [c.centroid.coords[0]]
            centroid['y'] = [c.centroid.coords[1]]
            tracelist.append(Scatter(**centroid))
        print("-----centroid %s ----- " %str(i+1))
        print(str(c.centroid.coords[0]) + ", " +str(c.centroid.coords[1]))

    layout = Layout(
        title = "Found %s best locations" % str(len(data)),
        geo = dict(
            resolution = 100,
            scope = 'usa',
            showframe = True,
            showcoastlines = True,
            showland = True,
            landcolor = "rgb(229, 229, 229)",
            countrycolor = "rgb(255, 255, 255)" ,
            coastlinecolor = "rgb(255, 255, 255)",
            projection = dict(
                type = 'albers usa'
            )
        )
    ) if drawMap else Layout (
        title = "Found %s best locations" % str(len(data))
    )
    fig = Figure(layout=layout, data=tracelist)
    plotly.offline.plot(fig, validate=False)


def main():
    print("in main")
    labels, points = read_from_csv(ds_col_list)
    clusters = kmeans(points)
    print("---------clusters---------")
    print(clusters)
    plot_graph(clusters)
    plot_gmap(clusters)


if __name__ == "__main__":
    main()
