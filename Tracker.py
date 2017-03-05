##written by Ananda Mazumder on 5/03/17
from threading import Thread 
import cv2
import dlib
import imutils

class Tracker:
	def __init__(self,roi,img,src=0):
		self.rect=(roi[0],roi[1],roi[2],roi[3])
		self.img=img
		self.stream=cv2.VideoCapture(src)
		(self.grabbed, self.frame)= self.stream.read()
		#temporary till adding another tracking algo
		self.tracker=dlib.correlation_tracker()

		self.cX=0
		self.cY=0
		self.stopped=False

	def start(self):
		print self.rect[1]

		self.tracker.start_track(self.img, dlib.rectangle(self.rect[0],self.rect[1],self.rect[0]+self.rect[2],self.rect[1]+self.rect[3]))
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
		while True:
			if(self.stopped==True):
				return
			else:
				(self.grabbed, self.frame) = self.stream.read()
				self.frame=imutils.resize(self.frame, width=400)
				self.tracker.update(self.frame)
				rect = self.tracker.get_position()
				pt1 = (int(rect.left()), int(rect.top()))
				pt2 = (int(rect.right()), int(rect.bottom()))
				self.cX=pt1[0]+self.rect[2]/2
				self.cY=pt1[1]+self.rect[3]/2
				self.rect=(pt1[0],pt1[1],self.rect[2],self.rect[3])
				# cv2.rectangle(self.frame, pt1, pt2, (255, 255, 255), 3)
	
	def read(self):
		cv2.rectangle(self.frame, (self.rect[0],self.rect[1]),(self.rect[0]+self.rect[2],self.rect[1]+self.rect[3]), (255, 255, 255), 3)
		return self.frame

	def stop(self):
		self.stopped=True
		self.stream.release()
		

	def get_points(self):
		return self.cX,self.cY




