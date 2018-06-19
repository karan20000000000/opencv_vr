import cv2 as cv
import numpy as np
img = cv.imread('photo4.jpeg',0)
r=cv.getStructuringElement(cv.MORPH_RECT,(5,5))
c=cv.getStructuringElement(cv.MORPH_CROSS,(5,5))
erosion = cv.dilate(img,r,iterations = 6)
dilation = cv.erode(erosion,r,iterations = 5)


cv.imwrite('Try.jpg',dilation)
