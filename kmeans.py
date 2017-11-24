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
dataset_file = "./restaurant_ds_sample.csv"
clusters_count = 3
tolerance = 0.2
drawMap=False


def make_points(list_x, list_y):
    '''
    create point objects from 2 lists and return list with coordinates 
    '''
    p = []
    for x,y in zip(list_x, list_y) :
        p.append(Point([x, y]))
    return p
    

def read_from_csv(col1, col2, col3):
    '''
    returns a list of points containing col1 as labels, and col2,col3
    as coordinate (x,y) from the dataset 
    '''
    csv_data = pd.read_csv(dataset_file)
    csv_data.head()
    list1 = csv_data[col1].values
    list2 = csv_data[col2].values
    list3 = csv_data[col3].values
    #make points list
    p = make_points(list2, list3)
    #print(p)
    return list1, p


def kmeans(points):
    initial = random.sample(points,clusters_count)
    clusters = [Cluster([p]) for p in initial]
    #print("clusters",clusters)
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
            print("Total iterations to converge %s", i)
            break
    return clusters

def plot_graph(data):
    tracelist = []
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
        trace['name'] = "Cluster-"+str(i)
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
        centroid['name'] = "Centroid-"+str(i)
        
        if drawMap:
            centroid['lat'] = [c.centroid.coords[0]]
            centroid['lon'] = [c.centroid.coords[1]]
            tracelist.append(Scattergeo(**centroid))
        else:
            centroid['x'] = [c.centroid.coords[0]]
            centroid['y'] = [c.centroid.coords[1]]
            tracelist.append(Scatter(**centroid))
        
    
    
    layout = Layout(
        title = "K-means clustering with %s clusters" % str(len(data)),
        geo = dict(
            resolution = 100,
            scope = 'usa',
            showframe = False,
            showcoastlines = True,
            showland = True,
            landcolor = "rgb(229, 229, 229)",
            countrycolor = "rgb(255, 255, 255)" ,
            coastlinecolor = "rgb(255, 255, 255)",
            projection = dict(
                type = 'Mercator'
            )
        )
    ) if drawMap else Layout (
        title = "K-means clustering with %s clusters" % str(len(data))
    )
    fig = Figure(layout=layout, data=tracelist)
    plotly.offline.plot(fig, validate=False)



def main():
    print("in main")
    labels, points = read_from_csv("name", "latitude", "longitude")
    clusters = kmeans(points)
    plot_graph(clusters)


if __name__ == "__main__":
    main()
