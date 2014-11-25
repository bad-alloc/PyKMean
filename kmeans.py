from __future__ import division
from copy import copy, deepcopy
import math
import sys

# Note on print: In order to avoid print emitting a newline, a
# trailing comma is added in some cases. I.e. 'print "a"' emits the
# string "a\n", while 'print "a",' only emits the string "a".

def printMatrix(matrix):
    for row in matrix:
        print row

# Note on comparing floating point matrices: If you don't round your
# distances, floating point errors might cause problems here.
def matrixEqual(a, b):
    if len(a) == len(b) and len(a[0]) == len(b[0]):
        for i in range(0, len(a[0])):
            for j in range(0, len(a)):
                if a[j][i] != b[j][i]:
                    return False
        return True
    else:
        return False

def printClusters(x, y, centroids, groupMatrix):
    # print points in each cluster:
    for centroidIndex in range(0, len(centroids)):
        print "Cluster", centroidIndex, ":",
        for pointIndex in range(0, len(groupMatrix[0])):
            if groupMatrix[centroidIndex][pointIndex] == 1:
                print "(", x[pointIndex], y[pointIndex], ")",
        print " "
    
def kMeans(x, y, centroids):
    prevCentroids = []
    prevDistances = []
    
    while True:
        distMatrix = []
        # empty matrix: one row per centroid, one column per point
        groupMatrix = [[0 for a in range(len(x))] for b in range(len(centroids))]
    
        # calculate distances of centroids to all other points
        for cnt in centroids:
            distances = []
            for i in range(0, len(x)):
                d = math.sqrt((cnt[0] - x[i]) ** 2 + (cnt[1] - y[i]) ** 2)
                d = round(d, 2)
                distances.append(d)
            distMatrix.append(distances)
        
        # assign each point to to cluster by finding minimum element of each
        # column of the distance matrix.
        for colIndex in range(0, len(distMatrix[0])):
            min = sys.maxint
            minIndex = (-1, -1)
            for rowIndex in range(0, len(distMatrix)):
                currentDistance = distMatrix[rowIndex][colIndex]
                if currentDistance < min:
                    min = currentDistance
                    minIndex = (rowIndex, colIndex)
            groupMatrix[minIndex[0]][minIndex[1]] = 1
        
        printMatrix(distMatrix)
        printMatrix(groupMatrix)
        
        # compute new centroids as mean of positions of points in cluster
        for centroidIndex in range(0, len(centroids)):
            xAvg = 0
            yAvg = 0
            totalAssigned = 0
            # Row i of group matrix corresponds to ith centroid
            # if the kth entry of the row is 1, point k belongs
            # to the cluster round centroid i.
            for pointIndex in range(0, len(groupMatrix[0])):
                if groupMatrix[centroidIndex][pointIndex] == 1:
                    xAvg += x[pointIndex]
                    yAvg += y[pointIndex]
                    totalAssigned += 1
            newCentroidX = xAvg / totalAssigned
            newCentroidY = yAvg / totalAssigned
            centroids[centroidIndex] = [newCentroidX, newCentroidY]
    
        print "Old centroids:", prevCentroids
        print "New centroids:", centroids
        printClusters(x, y, centroids, groupMatrix)
        print " "
        
        # are we done yet?
        if matrixEqual(centroids, prevCentroids):
            print "done"
            exit(0)
        else:
            prevCentroids = deepcopy(centroids)

if __name__ == "__main__":
    x1 = [3, 6, 8, 1, 2, 2, 6, 6, 7, 7, 8, 8]
    y1 = [5, 2, 3, 5, 4, 6, 1, 8, 3, 6, 1, 7]
    centroids1 = [[3, 5], [6, 2], [8, 3]]
    
    #kMeans(x1,y1,centroids1)

    x2 = [3, 3, 4, 4, 5, 6, 7, 7, 8, 9, 1, 2, 2, 3, 4, 5, 5, 6, 7, 7]
    y2 = [1, 2, 2, 3, 3, 4, 4, 6, 5, 7, 3, 4, 5, 6, 6, 7, 8, 8, 8, 9]
    centroids2 = [[3 , 1], [3 , 2]]

    kMeans(x2,y2,centroids2)
