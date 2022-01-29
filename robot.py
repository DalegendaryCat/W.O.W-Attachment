import cv2
from cv2 import threshold
from cv2 import waitKey
import urx
import imutils
import numpy

image = cv2.imread('IMG_9468.JPG')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.blur(gray, (7,7))
gray = cv2.GaussianBlur(gray, (5,5), 0)
edged=cv2.Canny(gray,30,200)
#ret, thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)

cv2.imshow('a',edged)
#contours = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
contours, hierarchy=cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
c = max(contours, key=cv2.contourArea)
#cv2.imshow('canny edges after contouring', edged)
left = tuple(c[c[:, :, 0].argmin()][0])
right = tuple(c[c[:, :, 0].argmax()][0])
top = tuple(c[c[:, :, 1].argmin()][0])
bottom = tuple(c[c[:, :, 1].argmax()][0])
print(contours)
print('Numbers of contours found=' + str(len(contours)))

cv2.circle(image, left, 8, (0, 50, 255), -1)
cv2.circle(image, right, 8, (0, 255, 255), -1)
cv2.circle(image, top, 8, (255, 50, 0), -1)
cv2.circle(image, bottom, 8, (255, 255, 0), -1)

cv2.drawContours(image,contours,-1,(0,255,0),3)
cv2.imshow('contours',image)
cv2.waitKey(0)

"""
ret, thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=2)
#thresh = cv2.bitwise_not(thresh)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = max(cnts, key=cv2.contourArea)

extLeft = tuple(c[c[:,:,0].argmin()][0])
extRight = tuple(c[c[:,:,0].argmax()][0])
extTop = tuple(c[c[:,:,1].argmin()][0])
extBot = tuple(c[c[:,:,1].argmax()][0])
print(extTop)
print(extBot)
print(extLeft)
print(extRight)

cv2.drawContours(image, [c], -1, (128,0,0), 2)
cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
cv2.circle(image, extRight, 8, (0, 255, 0), -1)
cv2.circle(image, extTop, 8, (255, 0, 0), -1)
cv2.circle(image, extBot, 8, (255, 255, 0), -1)

#cv2.imshow("thresh", thresh)
cv2.imshow("image", image)
cv2.waitKey(0)

"""
cv2.destroyAllWindows()