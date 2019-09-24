import cv2
import pyautogui
import numpy as np


cap = cv2.VideoCapture(0)
centroid_x = 0
centroid_y = 0

while(cap.isOpened()):
    _, frame = cap.read()
    #Flipping inorder to read the move correctly
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #To identify only the red object(Red bottle cap in my case).
    lower_red = np.array([0,115,169])
    upper_red = np.array([197,202,255])

    #Threshold the HSV image to get red elements
    threshVal = cv2.inRange(hsv, lower_red, upper_red)

    #Finding and drawing Contours
    contours, hierarchy = cv2.findContours(threshVal , cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        # draw in blue the contours that were founded
        cv2.drawContours(frame, contours, -1, 255, 3)

        # find the biggest area
        c = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(c)
        # draw the book contour (in green)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #Finding the Middle Point / Centroid of the
        centroid_x = (2*x + w)/2
        centroid_y = (2*y + h)/2

        #Draw the centroid point inside the rectangle
        cv2.circle(frame ,(np.float32(centroid_x),np.float32(centroid_y)), 2, (0,0,255), 2)

        #Create 4 Quadrants for UP/DOWN/LEFT/RIGHT
        cv2.line(frame, (200, 0), (200, 700), (255, 0, 0), 5)
        cv2.line(frame, (400, 0), (400, 700), (255, 0, 0), 5)
        cv2.line(frame, (200, 250), (400, 250), (255, 0, 0), 5)

        #Depending on the quadrant select which side to move
        if centroid_x <=200 and centroid_x >=0 and centroid_y >=0 and centroid_y <=700:
            print('Left')
            pyautogui.press('left')
        if centroid_x <=700 and centroid_x >=400 and centroid_y >=0 and centroid_y <=700:
            print('Right')
            pyautogui.press('right')
        if centroid_x <=400 and centroid_x >=200 and centroid_y >=0 and centroid_y <=250:
            print('Up')
            pyautogui.press('up')
        if centroid_x <=400 and centroid_x >=200 and centroid_y >250 and centroid_y <=700:
            print('Down')
            pyautogui.press('down')

    #Show the images
    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()