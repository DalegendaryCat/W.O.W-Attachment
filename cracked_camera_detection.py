import enum
from charset_normalizer import detect
import cv2
from cv2 import threshold
from cv2 import waitKey
from urx.robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
from urx import Robot
import numpy


#image = cv2.imread('IMG_9559.JPG')
cap = cv2.VideoCapture(4)

#tmp = image.copy()
while True:
  ret, frame = cap.read()
  if not ret:
      print("failed to grab frame")
      break

  #cv2.imshow("test", frame)

  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  frame = cv2.GaussianBlur(frame, (11, 11), 0)

  th = 50
  _,frame = cv2.threshold(frame,th,255,cv2.THRESH_BINARY_INV) 

  #=cv2.imshow("bruh", tmp)

  n, img_label, data, center = cv2.connectedComponentsWithStats(frame)

  detected_obj = list() 
  tr_x = lambda x : x * 150 / 500 
  tr_y = lambda y : y * 150 / 500 

  #img_trans_marked = image.copy()

  for i in range(1,n):
    x, y, w, h, size = data[i]
    if size < 700: 
      continue
    detected_obj.append( dict( x = tr_x(x),
                                y = tr_y(y),
                                w = tr_x(w),
                                h = tr_y(h),
                                cx = tr_x(center[i][0]),
                                cy = tr_y(center[i][1])))  
    
    #cv2.rectangle(img_trans_marked, (x,y), (x+w,y+h),(0,255,0),2)
    #cv2.circle(img_trans_marked, (int(center[i][0]),int(center[i][1])),5,(0,0,255),-1)
    cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)
    cv2.circle(frame, (int(center[i][0]),int(center[i][1])),5,(0,0,255),-1)

    cv2.imshow("bruh", frame)
    for i, obj in enumerate(detected_obj,1) :
      print(f'■ Detected object{i}Center position X={obj["cx"]:>3.0f}mm Y={obj["cy"]:>3.0f}mm ')
    
    k=cv2.waitKey(1)
    if k%256 == 27:
      print("Escape hit, closing...")
      break

cap.release()
cv2.destroyAllWindows()



#cv2.imshow("bruh", img_trans_marked)

#cv2.waitKey(0)
#cv2.destroyAllWindows()