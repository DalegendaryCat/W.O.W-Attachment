from charset_normalizer import detect
import cv2
from cv2 import threshold
from cv2 import waitKey
from cv2 import VideoCapture
from urx import Robot
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
import numpy as np
import os
import time

rob = Robot("192.168.1.5")
grip = Robotiq_Two_Finger_Gripper(rob)

def movehome():
    rob.movej((0, -1.57, -1.57, -1.57, 1.57, 1.57), 0.4, 0.3)


movehome()
rob.movel((0.5, -0.17397448177738706, 0.8, -2.2193353675931933, 2.219729011477007, 0.0008452331317947986), 0.4, 0.2)
print(rob.getl())
path = "/Volumes/PYTHON/Robot/frame"

if not os.path.exists(path):
  os.mkdir(path)

print(os.path.dirname(path))

cam = VideoCapture(4)
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k % 256 == 27: 
        print("Esc")
        break
    
    elif k%256 == 32:
        imgname = os.path.join(path,'pic1.jpg')
        cv2.imwrite(imgname, frame)
        
cam.release()
cv2.destroyAllWindows()

time.sleep(5)

image = cv2.imread('/Volumes/PYTHON/Robot/frame/pic1.jpg')
tmp = image.copy()
tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
#Blur processing
tmp = cv2.GaussianBlur(tmp, (11, 11), 0)
#Binarization process
th = 55 #Binarization threshold(Adjustment required)
_,tmp = cv2.threshold(tmp,th,255,cv2.THRESH_BINARY_INV) 

cv2.imshow("bruh", tmp)
cv2.waitKey(0)
cv2.destroyAllWindows()
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

detected_obj = [{'x': 0.433745, 'y': 0.0080076, 'w': 0.0480456, 'h': 0.0320304, 'cx': 0.45704148707482994, 'cy': 0.021858387482993197},
                {'x': 0.407053, 'y': 0.6085776, 'w': 0.0480456, 'h': 0.0240228, 'cx': 0.43062087547826083, 'cy': 0.6202408434782609},
                {'x': 0.040038000000000004, 'y': 0.300285, 'w': 0.0320304, 'h': 0.040038000000000004, 'cx': 0.05595474590163934, 'cy': 0.3191881868852459},
                {'x': 0.774068, 'y': 0.300285, 'w': 0.0240228, 'h': 0.0387034, 'cx': 0.7856766682819383, 'cy': 0.31940740748898677}]

count = 0
for i, obj in enumerate (detected_obj,1):
  movehome()
  x = (.6124 + 0.1949 - obj["cy"] + 0.13)
  y = (0.2753 + 0.0427 - obj["cx"])
  print(x)
  print(y)
  if(count == 0 or count==1):
    rob.movel((x, y, 0.3,  0.04986107480597996, 3.1388997833526004, -0.0025419470206463823), 0.2, 0.2)
    rob.movel((x, y, 0.15,  0.04986107480597996, 3.1388997833526004, -0.0025419470206463823), 0.2, 0.2)
    if count == 0:
      grip.close_gripper()
      rob.movel((x-0.15, y, 0.3, -0.0013366219951001586, 3.1400000708539193, 0.0035162987187208157), .2, .2)
      rob.movel((x-0.17 - 0.15, y, 0.2, -0.0013366219951001586, 3.1400000708539193, 0.0035162987187208157), .2, .1)
      #rob.movel((x+.15, -0.17395463326938498, 0.3, -0.0013366219951001586, 3.1400000708539193, 0.0035162987187208157), .2, .2)
      #rob.movel((x, -0.17395463326938498, 0.2, -0.0013366219951001586, 3.1400000708539193, 0.0035162987187208157), .2, .1)
      grip.open_gripper()

    elif count == 1:
      grip.close_gripper()
      rob.movel((x+0.15, y, 0.3, -0.0013366219951001586, 3.1400000708539193, 0.0035162987187208157), .2, .2)
      rob.movel((x+0.17 + 0.15, y, 0.25, -0.0013366219951001586, 3.1400000708539193, 0.0035162987187208157), .2, .1)
      grip.open_gripper()

    print(rob.getl())
    count += 1
  
  elif(count == 2 or count == 3):
    rob.movel((x, y, 0.3,  0.04986107480597996, 3.1388997833526004, -0.0025419470206463823), 0.2, 0.2)
    rob.movel((x, y, 0.15, -2.219417111504553, 2.2196286232847435, 0.0007778377317632664), 0.2, 0.2)
    if count == 2:
      grip.close_gripper()
      rob.movel((x, y-0.33, 0.5, -2.219417111504553, 2.2196286232847435, 0.0007778377317632664), .2, .2)
      rob.movel((x, y-0.33-0.33, 0.2, -2.219417111504553, 2.2196286232847435, 0.0007778377317632664), .2, .1)
      grip.open_gripper()

    elif count == 3:
      grip.close_gripper()
      rob.movel((x, y+0.13, 0.3,-2.219417111504553, 2.2196286232847435, 0.0007778377317632664), .2, .2)
      rob.movel((x, y+0.13+0.13, 0.2, -2.219417111504553, 2.2196286232847435, 0.0007778377317632664), .2, .1)
      grip.open_gripper()

    print(rob.getl())
    count += 1
  

print(detected_obj)

rob.close()
