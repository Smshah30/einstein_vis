import numpy as np
import cv2
import glob

# Number of inner corners in the chessboard
board_size = (9, 6)

# Prepare object points
objp = np.zeros((board_size[0] * board_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images
obj_points = []  # 3D points in real world space
img_points = []  # 2D points in image plane
gray = None
# Load images
images = glob.glob(".\P3Data\P3Data\Calib\\front\\frame*.jpg")

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, board_size, None)

    # If found, add object points, image points (after refining them)
    if ret:
        obj_points.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        img_points.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, board_size, corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

# Perform camera calibration
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

# Save the camera matrix and distortion coefficients

# Test undistortion on an image
img = cv2.imread('.\P3Data\P3Data\Calib\\front\\frame1303.jpg')
h, w = img.shape[:2]
new_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
undistorted_img = cv2.undistort(img, mtx, dist, None, new_mtx)
np.savez('calibration.npz', mtx=mtx, dist=dist,new_mtx=new_mtx,roi=roi)

# Display the undistorted image
cv2.imshow('img', img)
cv2.imshow('undistorted_img', undistorted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()


mean_error = 0
for i in range(len(obj_points)):
 imgpoints2, _ = cv2.projectPoints(obj_points[i], rvecs[i], tvecs[i], mtx, dist)
 error = cv2.norm(img_points[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
 mean_error += error
print( "total error: {}".format(mean_error/len(obj_points)) )