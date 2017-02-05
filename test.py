try:
	import cv2
except Exception as e:
	print("Warning: OpenCV not installed.")

import argparse as ap
import datetime
import imutils


# Parse command line arguments
# Creating an instance of the argument parser
parser = ap.ArgumentParser()
    
#stores the value video_path given input as -v video_path in args.video 
parser.add_argument("-v", "--video", help="path to video file, 0 for webcam")
    
# reading the passed arguments and storing them in a list called args,
# and can acces individual argument as args.arg where arg is the long aname pf the option
args=parser.parse_args()
print("Video path given as an argument "+ args.video )
#capture the camera
camera = cv2.VideoCapture(args.video)
# if camera.isOpened():
#     print("Video path given as an argument "+ args.video )
# else:
#     print("No video file path or an incorrect path was given, please enter a valid video file")
#     quit()

# print("Detecting professor...please wait..")
# points,img=detect_prof.using_MOG2(args.video)

# print("Tracking the professor...")
# track_prof.using_correlationDLIB(img, points)

    
