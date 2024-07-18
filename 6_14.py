import cv2 
img = cv2.imread("/Users/outingan/C++/brown.jpg")
cv2.imshow("Display window", img)
k = cv2.waitKey(0) # Wait for a keystroke in the window