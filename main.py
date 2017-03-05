import argparse
import time
from Queue import Queue
from threading import Thread
import dlib
import cv2
import imutils
from Tracker import Tracker
from Detector import Detector

# cv2.imshow was not running on another thread-- learn why??


# Function for sending signals to arduino(this function will run on a thread)
stop_arduino_thread=False
def send_arduino(in_q):
	global stop_arduino_thread
	while(1):
		if(stop_arduino_thread==True):
			return
		print "...."
		data=in_q.get()
		print "cX = ", data[0]
		time.sleep(0.5)


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--videopath", help="Path to video")
	ap.add_argument("-d", "--detector", help="Detection Algo")
	
	args = vars(ap.parse_args())
	if(args["videopath"]=="0"):
		source=0
	elif(args["videopath"]=="1"):
		source=1
	else:
		source=args["videopath"]

	if(args["detector"]=="HG" or args["detector"]=="HC"):
		detector_algo=args["detector"]
	else:
		print " Detector algo not correct"
		quit()

############ Detection Part starts here ##############
	dtector=Detector(src=source,detector=detector_algo).start()
	while True:
		frame=dtector.read()
		frame=imutils.resize(frame, width=400)
		cv2.imshow("Detection", frame)
		key = cv2.waitKey(20) & 0xFF
		if key == 27:
			break
	dtector.stop()
	rect, img=dtector.get_roi()
	
	cv2.destroyAllWindows()
	# print rect

############ Detection Part ends here ##############


############ Tracking Part starts here ##############

	global stop_arduino_thread
	q=Queue()
	tracker=Tracker(rect,img,src=source).start()
	print tracker
	data=tracker.get_points()
	q.put(data)
	thread_arduino = Thread(target=send_arduino, args=(q,))
	thread_arduino.start()
	while True:
		frame=tracker.read()
		frame=imutils.resize(frame, width=400)
		cv2.imshow("Frame", frame)
		data=tracker.get_points()
		q.put(data)
		key = cv2.waitKey(50) & 0xFF
		if key==27:
			break
	stop_arduino_thread=True
	tracker.stop()
	cv2.destroyAllWindows()
############ Tracking ends starts here ##############



if __name__ == '__main__':
    main()








