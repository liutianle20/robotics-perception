# est_homography estimates the homography to transform each of the video_pts into the logo_pts
# Inputs:
#     video_pts: a 4x2 matrix of corner points in the video
#     logo_pts: a 4x2 matrix of logo points that correspond to video_pts
# Outputs:
#     H: a 3x3 homography matrix such that logo_pts ~ H*video_pts

# %% 
import numpy as np

def est_homography(video_pts, logo_pts):

    # extract xs, ys, x_primes, y_primes
    xs = video_pts[:, 0]
    ys = video_pts[:, 1]
    x_primes = logo_pts[:, 0]
    y_primes = logo_pts[:, 1]
    # Vectorize
    A = []
    for i in range(4):
        x = xs[i]
        y = ys[i]
        x_prime = x_primes[i]
        y_prime = y_primes[i]
        ax = [-x, -y, -1, 0, 0, 0, x * x_prime, y * x_prime, x_prime]
        ay = [0, 0, 0, -x, -y, -1, x * y_prime, y * y_prime, y_prime]
        A.append(ax)
        A.append(ay)
    A = np.array(A)
    _, _, Vt = np.linalg.svd(A, full_matrices=True)
    H = np.reshape(Vt[-1, :], (3, 3))
    return H