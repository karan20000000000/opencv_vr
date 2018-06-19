import cv2
import numpy as np
import random

img=cv2.imread('photo3morph.jpg')
imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray=np.float32(imgray)


ret,thresh=cv2.threshold(imgray, 127, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

lines = []
for contour in contours[1:]:
	# hulls = cv2.convexHull(contour)
	epsilon = 0.01*cv2.arcLength(contour,True)
	hulls = cv2.approxPolyDP(contour,epsilon,True)
	k=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
	r=tuple(k)

	i = 0
	linesinner = []
	for hull in hulls:
		x,y=hull[0].ravel()
		cv2.circle(img,(x,y),8,r,-1)
		# print(x,y)
		# print(linesinner)

		if(i==0):
			linesinner.append( { "start": (x,y)} )
			i += 1
			continue
		elif(i==(len(hulls)-1)):
			linesinner.append( {"start": (x,y), "end": linesinner[0]["start"] } )
			linesinner[i-1]["end"] = (x,y)
			continue
		linesinner.append( { "start" : (x,y) } )
		linesinner[i-1]["end"] = (x,y)
		i += 1

	# print(linesinner)
	lines.extend(linesinner)

cv2.imwrite('Try2.jpg',img)

dataDict = {}
dataDict['walls'] = lines
import json
# print(json.dumps(dataDict))
with open("data_file.json", "w") as write_file:
    json.dump(dataDict, write_file, indent=1)

cv2.destroyAllWindows()
