# The main script to run this project.
# In this script, we provide you the following:
#     A sequence of images onto which you will project a logo image.
#    The corners in each video frame that the logo should project onto.
#    The logo image itself.

# %% 
import cv2
import numpy as np
from calculate_interior_pts import calculate_interior_pts
from warp_pts import warp_pts
from inverse_warping import inverse_warping

# %% bellingham_bicycle
logo_img = cv2.imread('images/logos/bellingham.jpg')
height, width = logo_img.shape[:2]
logo_pts = np.array([[0, 0], [width, 0], [width, height], [0, height]])
video_pts = np.array([[40, 350], [274, 278], [278, 405], [43, 483]]) 
test = cv2.imread('images/engSlo/engSlo_27.jpg') 
interior_pts = calculate_interior_pts(test.shape, video_pts) # Find all points in the video frame inside the polygon defined by video_pts
warped_logo_pts = warp_pts(video_pts, logo_pts, interior_pts) # Warp the interior_pts to coordinates in the logo image
test = inverse_warping(test, logo_img, interior_pts, warped_logo_pts) # Copy the RGB values from the logo_img to the video frame
cv2.imwrite('images/output/test1.png', test)
