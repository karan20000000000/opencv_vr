import cv2

img = cv2.imread("Test2-1.jpg")


img = cv2.resize(img, (400,400))
cv2.imshow("test", img)

cv2.waitKey(0)
