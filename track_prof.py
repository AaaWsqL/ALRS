##written by Ananda Mazumder on 5/02/17

import cv2
import argparse
import time
import imutils
import dlib
import numpy as np


# cons- can't track if object goes out of view
def using_correlationDLIB(roi,img,source):
    (x,y,w,h)=roi
    tracker = dlib.correlation_tracker()
    tracker.start_track(img, dlib.rectangle(x,y,x+w,y+h))
    cam= cv2.VideoCapture(source)
    while True:
        retval,img = cam.read()
        img = imutils.resize(img, width=500)
        if not retval:
            print "Cannot capture frame device | CODE TERMINATING :("
            exit()
        # Update the tracker  
        tracker.update(img)
        # Get the position of the object, draw a 
        # bounding box around it and display it.
        rect = tracker.get_position()
        pt1 = (int(rect.left()), int(rect.top()))
        pt2 = (int(rect.right()), int(rect.bottom()))
        cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
        # print ()"Object tracked at [{}, {}] \r".format(pt1, pt2)

        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)
        # Continue until the user presses ESC key
        if cv2.waitKey(1) == 27:
            break

    # Relase the VideoCapture object
    cam.release()
