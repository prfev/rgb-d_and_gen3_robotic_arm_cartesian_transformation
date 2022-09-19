from xml.etree.ElementInclude import XINCLUDE
from skimage import io, color
import numpy as np
from sklearn.cluster import KMeans
from skimage import segmentation as seg
import matplotlib.pyplot as plt
import cv2
from math import sqrt



def segment_buttons_from_terminal(img):
    centroides = []
    result = seg.felzenszwalb(img, scale=30000)
    result_felzenszwalb = seg.mark_boundaries(img, result, color=(255,255,255), outline_color=(0,255,0), mode='thick')
    # cv2.convertScaleAbs(result_felzenszwalb, alpha=(255.0))
    # cv2.imwrite('result_teste.jpg', result_felzenszwalb)
    result = cv2.convertScaleAbs(result, alpha=(255.0))
    contours, _ = cv2.findContours(result, mode= cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    i=0
    for c in contours:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        if len(approx) == 4:
            if perimeter >120 and perimeter<170:
                rect = cv2.minAreaRect(c)
                width = int(rect[1][0])
                height = int(rect[1][1])
                m = cv2.moments(c)
                cx = int(m['m10']/(m['m00']+1))
                cy = int(m['m01']/(m['m00']+1))
                centroides.append((cx,cy))
                
                y_ini = int(cy - (height/2))
                y_fin = int(cy + (height/2))
                x_ini = int(cx - (width/2))
                x_fin = int(cx + (width/2))
                
                cropped_img = img[y_ini:y_fin, x_ini:x_fin]
                # cv2.imwrite("teeest"+str(i)+".jpg", cropped_img)
                i+=1

    return centroides

# img = cv2.imread('C:/Users/prfev/Desktop/TCC_Scripts/tcc_finals/data/frame1920.jpg')
# segment_buttons_from_terminal(img)


