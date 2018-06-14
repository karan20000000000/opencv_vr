import numpy as np
import cv2

im = cv2.imread('photo2.jpeg')
# im = cv2.resize(im, (1000,1000))
print(im)
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)

#removing wrinkles
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

_, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(im, contours, -1, (0,255,0), 3)


cv2.imwrite("contourTest.jpg", im)
# cv2.imshow("im", thresh)
# cv2.waitKey()
