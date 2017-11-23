#imports 
import math

import numpy as np
import pandas as pd
import plotly
from plotly.graph_objs import Layout, Scatter, Scatter3d

from cluster import Cluster, Point, distance

'''
This program is an implementation of K-means clustering algorithm
which reads the restaurants datasets to find the best location
'''
#global variables for configuration
dataset_file = "./restaurants-data.csv"
num_clusters = 3
tolerance = 0.2



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


def main():
    print("in main")
    labels, points = read_from_csv("premise_name", "latitude", "longitude")
    print(points)
    print(labels)
    


if __name__ == "__main__":
    main()
