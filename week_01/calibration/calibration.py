# This snippet mainly addresses distortion calibration implemented by OpenCV
import cv2
import numpy as np
import glob

# define the dimension of chessboard
CHESSBOARD = (6, 9)

# The criteria is used in OpenCV functions that require iterative algorithms to specify the stopping criteria.
# TERM_CRITERIA_EPS specifies the algo. should stop when reaching accuracy 0.001.
# TERM_CRITERIA_MAX_ITER specifies the algo. should stop when reaching 30 iterations even if it does not reach specified accuracy.
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Arrays to store object points and image points from all the images.
# 3D points are called object points and 2D image points are called image points.
objPoints = []
imgPoints = []

# Create an array in a shape of 1 * (6 * 9) * 3 with zeros.
objP = np.zeros((1, CHESSBOARD[0] * CHESSBOARD[1], 3), np.float32)
# Generate all x-y-z pairs where z = 0 for to store coordinates of corners.
coordinates = np.mgrid[0:CHESSBOARD[0], 0:CHESSBOARD[1]]
objP[0, :, :2] =coordinates.T.reshape(-1, 2)

# find all image files in directory
images = glob.glob('*.png')

for fname in images:
    image = cv2.imread(fname)
    grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect chessboard corners
    retval, corners = cv2.findChessboardCorners(grayColor, 
                                                CHESSBOARD, 
                                                cv2.CALIB_CB_ADAPTIVE_THRESH 
                                                + cv2.CALIB_CB_FAST_CHECK 
                                                + cv2.CALIB_CB_NORMALIZE_IMAGE)
    if retval:
        objPoints.append(objP)
        # Refine the corners detected by cv2.findChessboardCorners
        refinedCorners = cv2.cornerSubPix(grayColor, corners, (11, 11), (-1, -1), criteria)
        imgPoints.append(refinedCorners)
        corneredImg = cv2.drawChessboardCorners(image, CHESSBOARD, refinedCorners, retval)
    h, w = corneredImg.shape[:2]
    ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera( 
        objPoints, imgPoints, grayColor.shape[::-1], None, None) 
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(matrix, distortion, (w, h), 1, (w, h))
    undistortedImg = cv2.undistort(grayColor, matrix, distortion, None, new_camera_matrix)

    # crop the image
    x, y, w, h = roi
    undistortedImg = undistortedImg[y:y+h, x:x+w]
    originalImage = grayColor

height = max(originalImage.shape[0], undistortedImg.shape[0])
width1 = int(originalImage.shape[1] * (height / originalImage.shape[0]))
width2 = int(undistortedImg.shape[1] * (height / undistortedImg.shape[0]))
originalImage_resized = cv2.resize(originalImage, (width1, height))
undistortedImg_resized = cv2.resize(undistortedImg, (width2, height))
combined_image = np.hstack((originalImage_resized, undistortedImg_resized))
cv2.imshow('Combined Image', combined_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('cornered.png', corneredImg)
cv2.imwrite('original.png', originalImage)
cv2.imwrite('undistorted.png', undistortedImg)