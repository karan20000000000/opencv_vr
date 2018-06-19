import json
import cv2
import numpy as np

img=cv2.imread('photo3morph.jpg')
fin = np.ones(img.shape, np.uint8) * 255

# cv2.imshow("Orig", img)

with open("data_file.json", "r") as read_file:
	ob = json.load(read_file)
	for wall in ob['walls']:
		start = tuple(wall['start'][::-1])
		end = tuple(wall['end'][::-1])
		# print(wall['start'][::-1], wall['end'][::-1])
		cv2.line(fin, start, end,(0,150,255),2 )

cv2.imshow("Fin", fin)

cv2.waitKey(0)
