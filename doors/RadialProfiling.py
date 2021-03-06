import cv2
import numpy as np
import random
import math
import interpoltest


img=cv2.imread('window_cs.jpg')
#img = cv2.copyMakeBorder(img, 30, 30, 30, 30, cv2.BORDER_CONSTANT, value = (255,255,255))
imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray=np.float32(imgray)


ret,thresh=cv2.threshold(imgray, 127, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE  , cv2.CHAIN_APPROX_SIMPLE)

doorlist = []

def rotate(l, n):
    return l[n:] + l[:n]

def getRadialProfile(cont):
	tempVar = len(cont)
	cNum = [float(x)/tempVar for x in range(len(cont))]
	rDist = []
	idxArr = [x for x in range(len(cont))]

	M = cv2.moments(cont)
	
	if(M["m00"] == 0):
		return None
	cX = int(M["m10"] / M["m00"])	#col pixel of center
	cY = int(M["m01"] / M["m00"])  #row pixel of center

	for p in cont:
		x,y = p.ravel()
		rDist.append( math.sqrt( (x-cX)**2 + (y-cY)**2 ) ) #append dist of (x,y) from (cx, cy)


	#scale invariance
	maxD = max(rDist)
	rDist = [ i/maxD for i in rDist ]


	#rotation invariance
	minD = min(rDist)
	minDIdx = rDist.index(minD)
	rDist = rotate(rDist, minDIdx)
	idxArr = rotate(idxArr, minDIdx)
	# cNum = rotate(cNum, minDIdx)
	return (cNum, rDist, idxArr )

def pltCont(img, cont):
	img2 = img.copy()
	cv2.drawContours(img2, [contour], -1, (0,0,255), 10)
	# idx = 0
	# for p in cont:
	# 	x,y = p.ravel()
	# 	cv2.circle(img2,(x,y),5*(idx+1),(0,255,255),-1)
	# 	idx += 1
	M = cv2.moments(cont)
	cX = int(M["m10"] / M["m00"])	#col pixel of center
	cY = int(M["m01"] / M["m00"])  #row pixel of center
	cv2.circle(img2, (cX, cY), 7, (0,255,255), -1)
	# diff = img2-img
	diff = img2
	return diff[:,:,::-1]

def drawRadialProfile(fname, cont):
	radprof = getRadialProfile(cont)  #x is cNum list, y is rDist list
	if(radprof is None):
		return
	x,y,_ = radprof
	#debug for console
	# print(fname, x, y)
	b = interpoltest.isADoor(x,y)
	print(fname)
	if(b):
		print(fname, "is a door")
	import matplotlib.pyplot as plt
	plt.subplot(2,1,1)
	plt.plot(x, y, 'o-')

	# for i in range(len(x)):
	# 	plt.plot(x[i],y[i], 'bo', markersize = 2*(i+1))

	plt.subplot(2,1,2)
	plt.imshow(pltCont(img, cont))
	plt.savefig(fname)
	plt.clf()
	# plt.show()

def putDoorsInList(cont):
	radprof = getRadialProfile(cont)
	if(radprof is None):
		return
	x, y, idxArr = radprof
	if(interpoltest.isADoor(x,y)):
		yMaxIdx = 0
		for i in range(len(y)):
			if(y[i] > y[yMaxIdx]):
				yMaxIdx = i
			if(y[i] < y[yMaxIdx]):
				doorlist.append({ "start": tuple(cont[idxArr[yMaxIdx]].ravel()), "pivot": tuple(cont[idxArr[yMaxIdx]+1].ravel()) })
				return

def updateJsonData():
	dataDict = {}
	dataDict['doors'] = doorlist
	import json
	# print(json.dumps(dataDict))
	with open("data_file_doors.json", "w") as write_file:
	    json.dump(dataDict, write_file, indent=1)

idx = 0
for contour in contours[1:]:
	# hulls = cv2.convexHull(contour)
	epsilon = 0.008*cv2.arcLength(contour,True)
	hulls = cv2.approxPolyDP(contour,epsilon,True)
	k=[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
	r=tuple(k)
	# for hull in hulls:
	# 	x,y=hull[0].ravel()
	# 	# cv2.circle(img,(x,y),3,r,-1)
	# 	print(x,y)


		# compute the center of the contour
	# M = cv2.moments(contour)
	# cX = int(M["m10"] / M["m00"])
	# cY = int(M["m01"] / M["m00"])

	# draw the contour and center of the shape on the image
	# cv2.drawContours(img, [contour], -1, r , 2)
	# cv2.circle(img, (cX, cY), 7, r, -1)
	# drawRadialProfile("RadialProfiles/RadProf"+str(idx)+".png", hulls)
	putDoorsInList(hulls)
	idx += 1

print(doorlist)
print(img.shape)
updateJsonData()

cv2.imwrite('Try2.jpg',img)

cv2.destroyAllWindows()
