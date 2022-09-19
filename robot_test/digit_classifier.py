# Import the modules
import cv2
import joblib
from skimage.feature import hog
import numpy as np

# Load the classifier
clf = joblib.load(r"C:\Users\prfev\Desktop\TCC_Scripts\tcc_finals\robot_test\digits_cls.pkl")

# Read the input image
im = cv2.imread(r"C:\Users\prfev\Desktop\TCC_Scripts\tcc_finals\data\teeest0.jpg")
w = im.shape[0]
h = im.shape[1]
im = im[4:h, 3:w]
# Convert to grayscale and apply Gaussian filtering
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im_gray = cv2.GaussianBlur(im_gray, (1, 1), 0)


# Threshold the image
im_th = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,7,7)

im_th = cv2.resize(im_gray, (28, 28), interpolation=cv2.INTER_AREA)
im_th = cv2.dilate(im_th, (1, 1))

roi_hog_fd = hog(im_th, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1))
nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
print(nbr)


# cv2.imshow("Resulting Image with Rectangular ROIs", im_th)
cv2.imwrite("prediction_result.jpg", im_th)
# cv2.waitKey(0)
# cv2.destroyAllWindows()