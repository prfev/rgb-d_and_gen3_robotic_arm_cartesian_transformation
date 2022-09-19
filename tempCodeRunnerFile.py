pts/HOGNumPy/frame1860.jpg')
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

# spices = io.imread('C:/Users/prfev/Desktop/TCC_Scripts/HOGNumPy/frame1860.jpg')
# plt.imshow(spices)

# im_lab = color.rgb2lab(spices)
# data = np.array([im_lab[..., 1].ravel(),
#                  im_lab[..., 2].ravel()])

# kmeans = KMeans(n_clusters=3, random_state=1).fit(data.T)
# labels = kmeans.labels_.reshape(spices.shape[:-1])
# color_mean = color.label2rgb(labels, spices, kind='avg')
# plt.imshow(color_mean)

# plt.imshow(segmentation.mark_boundaries(spices, labels))

# segments = segmentation.slic(spices, n_segments=25, compactness=200)
# plt.imshow(segmentation.mark_boundaries(spices, segments))
# result = color.label2rgb(segments, spices, kind='overlay')
# plt.imshow(result)

# im_lab = color.rgb2lab(result)
# data = np.array([im_lab[..., 1].ravel(),
#                  im_lab[..., 2].ravel()])

# kmeans = KMeans(n_clusters=5, random_state=0).fit(data.T)
# labels = kmeans.labels_.reshape(spices.shape[:-1])
# color_mean = color.label2rgb(labels, spices, kind='overlay')
# plt.imshow(segmentation.mark_boundaries(spices, labels))

# result = segmentation.felzenszwalb(spices, scale=30000)
# plt.imshow(color.label2rgb(result, spices, kind='overlay'))
# plt.imshow(segmentation.mark_boundaries(spices, result, color=(0,255,0), outline_color=(0,255,0)))

