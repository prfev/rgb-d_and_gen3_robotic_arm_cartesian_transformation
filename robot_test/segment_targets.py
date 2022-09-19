import numpy as np
import imutils
import time
import cv2

def find_target_centroide(frame):
    # define the lower and upper boundaries of the colors in the HSV color space
    lower = {#'orange': (0, 172, 28),
            #'green': (29, 119, 37),
            'wine' :(159, 71, 76)
            }

    upper = {#'orange': (11, 255, 255),
    #         'green': (175, 255, 255),
            'wine' : (180, 255, 128)
            }

    # define standard colors for circle around the object
    colors = {#'orange': (0, 100, 255),
            #'green': (0, 175, 0),
            'wine': (0, 255, 255)
            }
    centroides = []

    # transform in to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # for each color in dictionary check object in frame
    for key, value in upper.items():
        # construct a mask for the color from dictionary`1, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        kernel = np.ones((9, 9), np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centroides.append(cx)
            centroides.append(cy)
            # only proceed if the radius meets a minimum size. Correct this value for your obect's size
            if radius > 0.5:
                cv2.drawContours(frame, cnts, 0, (0,255,0), 3)


                cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                cv2.putText(frame, "Target", (int(x-radius), int(y - radius)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[key], 2)
                # cv2.imwrite(r"C:\Users\prfev\Desktop\TCC_Scripts\tcc_finals\data\results\targets_segmented", frame)
    # cv2.imshow("Frame", frame)
    # key = cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return centroides

# img = cv2.imread(r'C:\Users\prfev\Desktop\TCC_Scripts\tcc_finals\data\frame_camera.jpg')

# find_target_centroide(img)