# The main script to run dolly zoom.

# %%
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import project_objects, compute_focal_length, compute_f_pos

# load points.mat file
mat_file_path = '/Users/vincent/Documents/main/learn/robotics/robotics-perception/week_01/dolly_zoom/dolly_zoom/points.mat'
mat_contents = scipy.io.loadmat(mat_file_path)
points = {key: mat_contents[key] for key in mat_contents.keys() if not key.startswith('__')}
 # %%

d_ref = 4
f_ref = 400
pos = np.arange(0, -10, -0.1)

d1_ref = 4
d2_ref = 20
H1 = points['points_A'][0, 1] - points['points_A'][1, 1]
H2 = points['points_C'][0, 1] - points['points_C'][1, 1]
ratio = 2

# Dolly Zoom: keep one object's height constant 
f = compute_focal_length.compute_focal_length(d_ref, f_ref, pos)
project_objects.project_objects(f, pos, points, 1)

# Dolly Zoom:  keep one object's height constant and adjust another objects height
# The image when object in the front is twice larger then the object in the background
f, pos = compute_f_pos.compute_f_pos(d1_ref, d2_ref, H1, H2, ratio, f_ref)
project_objects.project_objects_image(f, pos, points, 2)