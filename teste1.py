from skimage import io, color
import numpy as np
from sklearn.cluster import KMeans
from skimage import segmentation as seg
import matplotlib.pyplot as plt
import cv2
from math import sqrt

def write_image(path, img):
    # img = img*(2**16-1)
    # img = img.astype(np.uint16)
    # img = img.astype(np.uint8)
    img = cv2.convertScaleAbs(img, alpha=(255.0))
    cv2.imwrite(path, img)

# im = io.imread('C:/Users/prfev/Desktop/TCC_Scripts/tcc_finals/data/frame1920.jpg')
# im_lab = color.rgb2lab(im)
# data = np.array([im_lab[..., 1].ravel(), im_lab[..., 2].ravel()])
# kmeans = KMeans(n_clusters=3, random_state=0).fit(data.T)
# segmentation = kmeans.labels_.reshape(im.shape[:-1])
# plt.imshow(im)
# plt.contour(segmentation, colors='y')
# plt.show()
# im = io.imread('C:/Users/prfev/Desktop/TCC_Scripts/tcc_finals/data/frame1920.jpg')
# im_lab = color.rgb2lab(im)
# data = np.array([im_lab[..., 0].ravel(),
#                  im_lab[..., 1].ravel(),
#                  im_lab[..., 2].ravel()])

# kmeans = KMeans(n_clusters=3, random_state=0).fit(data.T)
# segmentation = kmeans.labels_.reshape(im.shape[:-1])

# color_mean = color.label2rgb(segmentation, im, kind='overlay')
# fig, axes = plt.subplots(1, 2)
# axes[0].imshow(im)
# axes[0].axis('off')
# axes[1].imshow(color_mean)
# axes[1].axis('off')

# data = np.array([im_lab[..., 1].ravel(),
#                  im_lab[..., 2].ravel()])

# kmeans = KMeans(n_clusters=3).fit(data.T)
# segmentation = kmeans.labels_.reshape(im.shape[:-1])

# color_mean = color.label2rgb(segmentation, im, kind='overlay')
# fig, axes = plt.subplots(1, 2)
# axes[0].imshow(im)
# axes[0].axis('off')
# axes[1].imshow(color_mean)
# axes[1].axis('off')

spices = cv2.imread('C:/Users/prfev/Desktop/TCC_Scripts/tcc_finals/data/frame1920.jpg')
# plt.imshow(spices)


im_lab = color.rgb2lab(spices)
data = np.array([im_lab[..., 1].ravel(),
                 im_lab[..., 2].ravel()])

kmeans = KMeans(n_clusters=3, random_state=1).fit(data.T)
labels = kmeans.labels_.reshape(spices.shape[:-1])
color_mean = color.label2rgb(labels, spices, kind='avg')
# plt.imshow(color_mean)

# plt.imshow(seg.mark_boundaries(spices, labels))
# plt.show()
segments = seg.slic(spices, n_segments=25, compactness=200)
# plt.imshow(seg.mark_boundaries(spices, segments))
result = color.label2rgb(segments, spices, kind='overlay')
# plt.imshow(result)

im_lab = color.rgb2lab(result)
data = np.array([im_lab[..., 1].ravel(),
                 im_lab[..., 2].ravel()])

kmeans = KMeans(n_clusters=7, random_state=0).fit(data.T)
labels = kmeans.labels_.reshape(spices.shape[:-1])
color_mean = color.label2rgb(labels, spices, kind='overlay')

result = seg.felzenszwalb(spices, scale=30000)
result_cvt = cv2.convertScaleAbs(result, alpha=(255.0))
write_image('result.jpg', result)

# plt.imshow(seg.mark_boundaries(spices, labels))
# plt.imshow(color.label2rgb(result, spices, kind='overlay'))
# plt.imshow(seg.mark_boundaries(spices, result, color=(0,255,0), outline_color=(0,255,0), mode='thick'))
# plt.savefig("result")

result_felzenszwalb = seg.mark_boundaries(spices, result, color=(255,255,255), outline_color=(0,255,0), mode='thick')
write_image("result_felzenszwalb.jpg", result_felzenszwalb)

# img = cv2.imread('result_felzenszwalb.jpg')
# img = cv2.cvtColor(result,  cv2.COLOR_BGR2GRAY)
# img = cv2.adaptiveThreshold(result, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,17,1)
# cv2.imshow("eeeeeeee", result)
# cv2.waitKey(2000)
contours, hierarchy = cv2.findContours(result_cvt, mode= cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
i = 0
for c in contours:
    perimeter = cv2.arcLength(c, True)
 
    approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
    
    if len(approx) == 4:
        if perimeter >120:
            print(perimeter)
            rect = cv2.minAreaRect(c)
            teste = cv2.drawContours(result_cvt, c,-1,(0,255,0),3)
            cv2.imwrite("contornos.jpg", teste)
            i+=1
            print(i)
        
        

