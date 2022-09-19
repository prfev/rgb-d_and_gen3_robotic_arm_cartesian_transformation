# Import the modules
import joblib
from sklearn import datasets
from skimage.feature import hog
from sklearn.svm import LinearSVC
import numpy as np
from collections import Counter
from scipy.io import loadmat



# Load the dataset
# dataset = datasets.fetch_openml("mnist_784", version=1)

mnist = loadmat(r"C:\Users\prfev\Desktop\TCC_Scripts\tcc_finals\robot_test\mnist-original.mat")
mnist_data = mnist["data"].T
mnist_label = mnist["label"][0]

# Extract the features and labels
features = np.array(mnist_data, 'int16')
labels = np.array(mnist_label, 'int')

# Extract the hog features
list_hog_fd = []
for feature in features:
    fd = hog(feature.reshape((28, 28)), orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1))
    list_hog_fd.append(fd)

hog_features = np.array(list_hog_fd, 'float64')

print ("Count of digits in dataset", Counter(labels))

# Create an linear SVM object
clf = LinearSVC()

# Perform the training
clf.fit(hog_features, labels)

# Save the classifier as pkl file
joblib.dump(clf, "digits_cls.pkl", compress=3)