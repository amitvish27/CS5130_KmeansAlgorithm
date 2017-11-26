import math

class Point(object):
    '''
    A point object with coords(x, y) and n dimension
    '''
    def __init__(self, coords):
        self.coords = coords
        self.n = len(coords)

    def __repr__(self):
        return str(self.coords)

class Cluster(object):
    '''
    Cluster of points with a centroid
    '''
    def __init__(self, points):
        if len(points)==0:
            raise Exception("ERROR: empty cluster")
        self.points = points
        self.n = points[0].n
        self.centroid = self.calc_centroid()
    
    def __repr__(self):
        return str(self.points)

    def calc_centroid(self):
        '''
        '''
        count = len(self.points)
        coords = [p.coords for p in self.points]
        centroid = Point([math.fsum(lst)/count for lst in zip(*coords)])
        return centroid

    def update(self, points):
        '''
        update current centroid with the new centroid
        '''
        curr_centroid = self.centroid
        self.points = points
        self.centroid = self.calc_centroid()
        return distance(curr_centroid, self.centroid)

def distance(a, b):
    '''
    Caculate the Euclidean distance between points a and b as
    distance(a,b) = sqrt(sum(pow(a-b,2)))
    '''
    diff = 0.0
    for i in range(a.n):
        diff += pow((a.coords[i]-b.coords[i]),2)
    return math.sqrt(diff)