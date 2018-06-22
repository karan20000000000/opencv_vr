import cv2
import numpy as np

img=cv2.imread('door.png')
orig = img.copy()
imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray=np.float32(imgray)


ret,thresh=cv2.threshold(imgray, 127, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE  , cv2.CHAIN_APPROX_SIMPLE)

for contour in contours[1:]:
		cv2.drawContours(img, [contour], -1, (255, 255, 255) , 2)

diff = img - orig
cv2.imshow("Diff", diff)
cv2.waitKey(0)


def pltCont(img, cont):
	img2 = img.copy()
	cv2.drawContours(img2, [contour], -1, (255,255,255), 2)
	diff = img2-img
	return diff[:,:,::-1]
