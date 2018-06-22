class Vector:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.checked = False
	def dist(self, v):
		import math
		return math.sqrt( math.pow(v.x - self.x, 2) + math.pow(v.y - self.y, 2) )
	def group(self, v):
		return [self, v]
	def is_black_in_mid(self, v, img):
		col = (self.x + v.x)/2
		row = (self.y + v.y)/2
		return img[row,col] <= 15
	def __str__(self):
		return "Vector("+str(self.x) + ", " + str(self.y)+")"
	def __repr__(self):
		return "Vector("+str(self.x) + ", " + str(self.y)+")"
	def __eq__(self, v):
		return self.x == v.x and self.y == v.y

def removeDuplicates(l):
	nl = []
	for v in l:
		if(v not in nl):
			nl.append(v)
	return nl

def find_nearest_white(target):
    # nonzero = cv2.findNonZero(img)
    distances = np.sqrt((nonzero[:,:,0] - target[0]) ** 2 + (nonzero[:,:,1] - target[1]) ** 2)
    nearest_index = np.argmin(distances)
    return nonzero[nearest_index]

def nearest_white_dist(target):
	arr = find_nearest_white(target).tolist()
	x,y = arr[0][0], arr[0][1]
	import math
	dist = math.sqrt( math.pow(target[0] - x, 2) + math.pow(target[1] - y, 2) )
	return dist

import cv2
import numpy as np

img=cv2.imread('Test2-1.jpg')
img = cv2.copyMakeBorder(img, 30, 30, 30, 30, cv2.BORDER_CONSTANT, value = (255,255,255))
imgray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray=np.float32(imgray)

#threshold the imgray img, then use that to ignore redundant red points
_, graythresh = cv2.threshold(imgray, 30, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU )
nonzero = cv2.findNonZero(graythresh)

#detecting and placing blue corners
corners=cv2.goodFeaturesToTrack(graythresh, 100, 0.15 ,10)
corners=np.int0(corners)

#vector stuff
pointlist = []
for corner in corners:
	x,y=corner.ravel()
	cv2.circle(img,(x,y),5,255,-1)
	pointlist.append(Vector(x,y))
	# print(x,y)

pairs = []


#grouping blue points (shabby corners)
for i in pointlist:
	distarr = []
	for j in pointlist:
		if j is not i:
			distarr.append((i.dist(j), j))
	# temp = min(distarr)
	# i.checked = True
	# temp[1].checked = True
	# pairs.append(i.group(temp[1]))

	sortedPoints = sorted(distarr)
	templist = []
	for p in sortedPoints:
		if(i.is_black_in_mid(p[1], graythresh)):
			templist.append(p)
	if(len(templist) > 0):
		temp = min(templist)
		i.checked = True
		temp[1].checked = True
		pairs.append(i.group(temp[1]))

#final corner points in red
red = []
for pair in pairs:
	x = (pair[0].x+pair[1].x)/2
	y = (pair[0].y+pair[1].y)/2
	v = (x,y)
	if(v not in red):
		#if the color at x,y at this place is white, then don't place the red shit here
		#row, col
		if(cmp(list(img[y,x]), [255,255,255]) is not 0):

			#ignoring this place if its close to white

			if(nearest_white_dist((x,y)) <= 3 ):
				continue

			red.append((x,y))
			cv2.circle(img,(x,y), 6, (0,0,255), -1)
			# print(v, pair)

# grouping
# for vect in red:
# 	for vect2 in red:
# 		if(traverse(vect,vect2)):
# 			lines.append([vect, vect2])

cv2.imwrite('Try2.jpg',img)
cv2.destroyAllWindows()
