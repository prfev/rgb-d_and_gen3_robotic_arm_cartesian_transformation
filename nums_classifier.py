from sklearn import datasets
from skimage import io
import matplotlib
matplotlib.rcParams['image.interpolation'] = 'nearest'
import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn import svm


digits = datasets.load_digits()
# print(digits)
# print(digits.data.shape)
# print(digits.target.shape)
# print(digits.images.shape)
np.all(digits.data[0].reshape((8, 8)) == digits.images[0])
# plt.imshow(digits.images[0], cmap='gray')
print("target: ", digits.target[0])
clf = svm.SVC(gamma=0.001, C=100.)
clf.fit(digits.data[:-10], digits.target[:-10])
a = cv2.imread(r'C:\Users\prfev\Desktop\TCC_Scripts\tcc_finals\data\teeest0.jpg')
a = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
a = a.astype("float64")
print(digits.data[-2])
print(clf.predict(a)) #digits.data[-2:]
# fig, axes = plt.subplots(1, 2)
# axes[0].imshow(digits.images[-2], cmap='gray')
# axes[1].imshow(digits.images[-1], cmap='gray')