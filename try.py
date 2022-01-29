import enum
from charset_normalizer import detect
import cv2
from cv2 import threshold
from cv2 import waitKey
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
from urx import Robot
import numpy


image = cv2.imread('/Volumes/PYTHON/Robot/frame/pic1.jpg')
tmp = image.copy()
tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
#Blur processing
tmp = cv2.GaussianBlur(tmp, (11, 11), 0)
#Binarization process
th = 55 #Binarization threshold(Adjustment required)
_,tmp = cv2.threshold(tmp,th,255,cv2.THRESH_BINARY_INV) 
# Blob (= mass) detection
n, img_label, data, center = cv2.connectedComponentsWithStats(tmp)
#Organize detection results
detected_obj = list() #Storage destination of detection result
pxl = 0.0013346 #size of 1 pixel in actual measurement in real life
tr_x = lambda x : x * pxl  
tr_y = lambda y : y * pxl  

img_trans_marked = image.copy()
for i in range(1,n):
  x, y, w, h, size = data[i]
  if size < 300: #Ignore areas less than 300px
    continue
  elif size>50000:
    continue
  detected_obj.append( dict( x = tr_x(x),
                              y = tr_y(y),
                              w = tr_x(w),
                              h = tr_y(h),
                              cx = tr_x(center[i][0]),
                              cy = tr_y(center[i][1])))  
  #Verification
  cv2.rectangle(img_trans_marked, (x,y), (x+w,y+h),(0,255,0),2)
  cv2.circle(img_trans_marked, (int(center[i][0]),int(center[i][1])),5,(0,0,255),-1)

# (6)View results
cv2.imshow("bruh", img_trans_marked)
for i, obj in enumerate(detected_obj,1) :
  print(f'■ Detected object{i}Center position X={obj["cx"]:>3.0f}m Y={obj["cy"]:>3.0f}m ')

cv2.waitKey(0)
cv2.destroyAllWindows()