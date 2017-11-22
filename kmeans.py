# import
from copy import deepcopy

import matplotlib.pyplot as plt, mpld3
import numpy as np
import pandas as pd

#plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')


def dist(a, b, ax=1):
    return np.linalg.norm(a - b, axis=ax)

# Main method


def main():
    csvdata = pd.read_csv(r"./dataset.csv")
    print(csvdata.shape)
    csvdata.head()
    lbl = csvdata['lab'].values
    f1 = csvdata['x'].values
    f2 = csvdata['y'].values
    # printing the variables
    #print("f1",f1)
    #print("f2",f2)
    #print("lbl", lbl)
    X = np.array(list(zip(f1, f2)))
    #plt.scatter(f1, f2, c='black', s=5)
    # Number of clusters
    k = 3
    np.random.seed()
    # X coordinates of random centroids
    C_x = np.random.randint(0, np.max(X)-50, size=k)
    # Y coordinates of random centroids
    C_y = np.random.randint(0, np.max(X)-50, size=k)
    C = np.array(list(zip(C_x, C_y)), dtype=np.float32)
    #print("C" , C)
    # Plotting along with the Centroids
    #plt.scatter(f1, f2, c='#050505', s=7)
    #plt.scatter(C_x, C_y, marker='*', s=50, c='g')
    
    # To store the value of centroids when it updates
    C_old = np.zeros(C.shape)
    #print("C_old", C_old)
    # Cluster Lables(0, 1, 2)
    clusters = np.zeros(len(X))
    #print("clusters", clusters)
    # Error func. - Distance between new centroids and old centroids
    error = dist(C, C_old, None)
    #print("error",error)
    # Loop will run till the error becomes zero
    while error != 0:
        # Assigning each value to its closest cluster
        for i in range(len(X)):
            distances = dist(X[i], C)
            cluster = np.argmin(distances)
            clusters[i] = cluster
        # Storing the old centroid values
        C_old = deepcopy(C)
        #print("C_old after deepcopy",C_old)
        # Finding the new centroids by taking the average value
        for i in range(k):
            points = [X[j] for j in range(len(X)) if clusters[j] == i]
            C[i] = np.mean(points, axis=0)
        error = dist(C, C_old, None)
    
    colors = ['r', 'g', 'b', 'y', 'c', 'm']
    fig, ax = plt.subplots(subplot_kw=dict(facecolor='#EEEEEE'))
    elements = []

    for i in range(k):
            points = np.array([X[j] for j in range(len(X)) if clusters[j] == i])
            element = ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
            elements.append([element])
    
    element = ax.scatter(C[:, 0], C[:, 1], marker='*', s=50, c='#050505')
    elements.append([element])
    #ax.grid(color='white', linestyle='solid')
    ax.set_title("Scatter Plot for clusters", size=20)
    new_labels = ['pnt {0}'.format(i) for i in lbl]
    print(new_labels)
    tooltip = mpld3.plugins.PointLabelTooltip(elements, labels=new_labels)
    mpld3.plugins.connect(fig, tooltip)

    mpld3.show()


if __name__ == "__main__":
    main()
