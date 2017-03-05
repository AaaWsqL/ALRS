##written by Ananda Mazumder on 5/03/17
import cv2
from threading import Thread 
import argparse
import time
import imutils
from imutils.object_detection import non_max_suppression
import numpy as np

class Detector:
	def __init__ (self,src=0,detector="HC"):
		self.detector=detector
		print self.detector
		self.min_area=3000
		self.rect=(0,0,0,0)
		self.stream=cv2.VideoCapture(src)
		(self.grabbed, self.frame)= self.stream.read()
		self.stopped=False

	# start() will start the proper detection function in a seperate thread
	def start(self):
		if(self.detector=="HC"):
			print 'dff'
			Thread(target=self.using_HaarCascade, args=()).start()
		if(self.detector=="HG"):
			Thread(target=self.using_HOG, args=()).start()
		return self

	# reading the frame
	def read(self):
		cv2.rectangle(self.frame,(self.rect[0],self.rect[1]),(self.rect[0]+self.rect[2],self.rect[1]+self.rect[3]),(255,0,0),2)
		return self.frame

	# stop the thread
	def stop(self):
		self.img=self.frame.copy()
		self.stream.release()
		self.stopped=True

	# get the roi( region of interest and the image)
	def get_roi(self):
		return self.rect,self.img


	# find better cascades
	def using_HaarCascade(self):
		face_cascade = cv2.CascadeClassifier('HS.xml')
		while True:
			if(self.stopped==True):
				return
			else:
				(self.grabbed, self.frame) = self.stream.read()
				self.frame = imutils.resize(self.frame, width=400)
				gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
				faces = face_cascade.detectMultiScale(gray, 1.3, 5)
				for face in faces:
					(x,y,w,h)=face.astype(int)
					if (w*h)>self.min_area:
						self.rect=(x,y,w,h)
				# cv2.rectangle(self.frame,(x,y),(x+w,y+h),(255,0,0),2)

	# currently impllemented it directly from http://www.pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/
	# lots of errors
	def using_HOG(self):
		# for now the default openCV Hog descriptor had been used
		# make our own cascade classifier
		hog=cv2.HOGDescriptor()
		hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
		while True:
			if(self.stopped==True):
				return
			else:
				(self.grabbed, self.frame) = self.stream.read()
				self.frame = imutils.resize(self.frame, width=min(400, self.frame.shape[1]))
				(rects, weights) = hog.detectMultiScale(self.frame, winStride=(4,4),
					padding=(8,8), scale=1.05)
				rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
				pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

				for (xA, yA, xB, yB) in pick:
					cv2.rectangle(self.frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
					self.rect=(xA,yA,xB-xA,yB-yA)

	




