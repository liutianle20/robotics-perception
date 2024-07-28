# calculate_interior_pts takes in the size of an image and a set of corners
# of a shape inside that image, and returns all (x,y) points in that image
# within the corners
import numpy as np
from shapely.geometry import Polygon, Point

# Generate grid coordinates
def calculate_interior_pts(image_size, corners):
    X, Y = np.meshgrid(np.arange(image_size[1]), np.arange(image_size[0]))
    X = X.reshape(-1, 1) # convert to column vector
    Y = Y.reshape(-1, 1)
    polygon = Polygon(corners)
    interior_inds = np.zeros(X.shape, dtype=bool)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            point = Point(X[i, j], Y[i, j])
            interior_inds[i, j] = polygon.contains(point)
    interior_pts = np.vstack((X[interior_inds], Y[interior_inds])).T
    return interior_pts
