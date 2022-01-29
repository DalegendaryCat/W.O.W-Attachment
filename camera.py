import cv2
cam = cv2.VideoCapture(4)

cv2.namedWindow("bruh")

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