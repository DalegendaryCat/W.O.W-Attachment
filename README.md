# W.O.W-Attachment

This project aims to use a robot arm to perform daily tasks, such as sorting items, by using the Universal Robot Arm. Machine learning was used to teach the computer how to idenify objects, which used the SSD MobileNet V2 FPNLite 320x320 model to train, as it is able to balance out both speed and accuracy as the robot arm will be constanly moving, hence, fast detection of objects is important. 

To test out object detection abilities, use script.py and change the necessary image path in order to import the image for object detection

Some changes to the logic has been made, and now I intended to use blob detections instead of object detection, code can be found in cracked_camera_detection.py

Using OpenCV, the robot arm is able to "see" the objects laid out in front of it using an external camera, and hence, detect the object. Final code can be found in Final_Robot.py
  

  
