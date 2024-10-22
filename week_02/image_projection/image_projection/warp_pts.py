# warp_pts computes the homography that warps the points inside
# video_pts to those inside logo_pts. It then uses this
# homography to warp the points in sample_pts to points in the logo
# image
# Inputs:
#     video_pts: a 4x2 matrix of (x,y) coordinates of corners in the
#         video frame
#     logo_pts: a 4x2 matrix of (x,y) coordinates of corners in
#         the logo image
#     sample_pts: a nx2 matrix of (x,y) coordinates of points in the video
#         video that need to be warped to corresponding points in the
#         logo image
# Outputs:
#     warped_pts: a nx2 matrix of (x,y) coordinates of points obtained
#         after warping the sample_pts
# %%
import numpy as np
from est_homography import est_homography

def warp_pts(video_pts, logo_pts, sample_pts):
    H = est_homography(video_pts, logo_pts)
    pts_num = sample_pts.shape[0]
    sample_pts = np.hstack((sample_pts, np.ones((pts_num, 1))))
    
    warped_pts = []
    for sample_pt in sample_pts:
        warped_pt = np.dot(H, sample_pt)
        warped_pt = warped_pt / warped_pt[-1]
        warped_pts.append(warped_pt)
    warped_pts = np.array(warped_pts)
    return warped_pts[:, 0 : 2]