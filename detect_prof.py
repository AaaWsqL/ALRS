##written by Ananda Mazumder on 5/02/17


import cv2
import argparse
import time
import imutils
import numpy as np
import track_prof

def using_HaarCascade(source):
	face_cascade = cv2.CascadeClassifier('HS.xml')
	cap = cv2.VideoCapture(source)
	min_area=3000
	max_area=9000
	start = time.time()
	flag=0
	while 1:
		ret, frame = cap.read()
		frame = imutils.resize(frame, width=500)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		end=time.time()
		for face in faces:
			
			(x,y,w,h)=face.astype(int)
			if (w*h)>min_area:
				cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
				
	        if end-start>7:
	        	rect_roi=(x, y, w, h)
	        	img=frame.copy()
	        	flag=1
	        	break

		cv2.imshow('img',frame)
		k = cv2.waitKey(100) & 0xff
		if k == 27:
			break
		if(flag):
			break
	
	cap.release()
	cv2.destroyAllWindows()

	return rect_roi, img




#returns the roi_rectangle, and the image where it found it
def using_MOG2(source):
	cap= cv2.VideoCapture(source)
	fgbg = cv2.createBackgroundSubtractorMOG2()

	#wait 3 seconds to make the feed stable
	start = time.time()
	time.sleep(2)

	#minimim  and maximum area of the bounding box to track
	min_area=8000
	max_area=90000
	flag=0
	while True:
		#capture the feed
		ret, frame= cap.read()

		if not ret:
			print("Cannot capture video feed, something's wrong")
			quit()

		#resize the frame and do some image pre-processing stuff which everyone seems to do
		#but i dont know why
		frame = imutils.resize(frame, width=500)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)

		#apply the foreground-background mask to seperate foreground from background
		fgmask = fgbg.apply(frame)

		#thresehold the masked image to discared small irregularities
		thresh = cv2.threshold(fgmask, 20, 255, cv2.THRESH_BINARY)[1]

		# dilate the thresholded image to fill in holes, then find contours
		# on thresholded image
		thresh = cv2.dilate(thresh, None, iterations=2)
		_, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

		#loop over all the contours
		for c in cnts:
			# if the contour is too small or too big, ignore it
			if cv2.contourArea(c) < min_area or cv2.contourArea(c)> max_area:
				continue
	 
			# compute the bounding box for the contour, draw it on the frame,
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
			#when only the prof is standing(assuming that only the prof stands during the initial setup)
			# currently it is waiting for 7 seconds to wait and capture the professor
			# later we would incorporate haar casacde to do a face detection on the bounding box and then select the points
			end=time.time()
			if(end-start>7 ):
				rect_roi=(x, y, w, h)
				img=frame.copy()
				flag=1
				break
			
		cv2.imshow('original', frame)
		cv2.imshow('fg', thresh)
		if(flag):
			break
	

		#press escape to exit
		k=cv2.waitKey(30) & 0xff
		if k==27:
			break
	cap.release()
	cv2.destroyAllWindows()

	return rect_roi, img

if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--videopath", required=True, help="Path to video")
	ap.add_argument("-a", "--algo", required=True, help="algo to detect professor,1. M -> BackgroundSubtractorMOG2, 2. H-> HaarCascade")

	args = vars(ap.parse_args())
	try:
		im = cv2.imread(args["videopath"])
	except:
		print("Cannot read video and exiting")
		exit()

	# if MOG2 was input as algo
	if(args["algo"]=="M"):
		print("Using background Subtractor MOG2 for detecting professor..")
		points,img=using_MOG2(args["videopath"])

		print("Rectangular points selected are: ", points)

	# if HaarCascade was given as algo
	if(args["algo"]=="H"):
		print("Using Haar Cascade for detecting professor..")
		points,img=using_HaarCascade(args["videopath"])

		print("Rectangular points selected are: ", points)
		# while True:
		# 	cv2.imshow('selected',img)
		# 	k=cv2.waitKey(100) & 0xff
		# 	if k==27:
		# 		break
	while True:
		cv2.imshow('selected', img)
		k=cv2.waitKey(30) & 0xff
		if k==27:
			break

	cv2.destroyAllWindows()
	
	track_prof.using_correlationDLIB(points,img,args["videopath"])
	
