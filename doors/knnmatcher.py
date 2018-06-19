import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
img1 = cv.imread('door.png',0)          # queryImage
img2 = cv.imread('tilteddoor.png',0) # trainImage
# Initiate SIFT detector
sift = cv.ORB_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
# BFMatcher with default params
bf = cv.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)
# Apply ratio test
good = []
for m,n in matches:
    if m.distance < n.distance:
        good.append([m])
# cv.drawMatchesKnn expects list of lists as matches.
img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,good,flags=2, outImg=img2)
# plt.imshow(img3),plt.show()

bbpts = []
for match in good:
	m = match[0]
	x,y = kp2[m.trainIdx].pt
	x = int(x)
	y = int(y)
	bbpts.append((x,y))
	cv.circle(img2, (x,y), 5, (0,0,255), -1 )


bbpts = np.array(bbpts)
x,y,w,h = cv.boundingRect(bbpts)
cv.circle(img2, (x,y), 5, (0,0,255), -1 )
cv.circle(img2, (x+w, y+w), 5, (0,0,255), -1 )

rect = cv.minAreaRect(np.array(bbpts))
box = cv.boxPoints(rect)
box = np.int0(box)
cv.drawContours(img2, [box], 0, (0,0,255), 2)
# print(bb)
cv.rectangle(img2, (x,y), (x+w, y+w), (0,0,255))
cv.imwrite("Try2.jpg", img2)
