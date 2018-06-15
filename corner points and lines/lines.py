import cv2
import points

# print(points.red)

def is_mid_white(p1, p2, img):
	for i in range(2,100,2):
		col = (p2[0] + i*p1[0])/(1+i)
		row = (p2[1] + i*p1[1])/(1+i)
		if(img[row, col] >= 250):
			# print(p1, p2, row, col)
			cv2.circle(points.img, (col,row), 3, (255,255,0), -1)
			return True
	for i in range(2,100,2):
		col = (i*p2[0] + p1[0])/(1+i)
		row = (i*p2[1] + p1[1])/(1+i)
		if(img[row, col] >= 250):
			# print(p1, p2, row, col)
			cv2.circle(points.img, (col,row), 3, (255,255,0), -1)
			return True
	return False

#lines = [(start, end), ...]
lines = []
for point in points.red:
	for point2 in points.red:
		if(point is not point2):
			if(is_mid_white(point, point2, points.graythresh)):
				continue
			cv2.line(points.img,point,point2,(0,150,255),2)
			lines.append({"start":point,"end":point2})
			print(point)

dataDict = {}
dataDict['walls'] = lines
import json
# print(json.dumps(dataDict))
with open("data_file.json", "w") as write_file:
    json.dump(dataDict, write_file, indent=1)

cv2.imwrite('Try2.jpg',points.img)
