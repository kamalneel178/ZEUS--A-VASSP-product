# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import os
from multiprocessing import Process

def cv():
	for files in os.listdir("/root/md/"):
		os.remove("/root/md/"+files)

	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", help="path to the video file")
	ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
	args = vars(ap.parse_args())
	 
	# if the video argument is None, then we are reading from webcam
	if args.get("video", None) is None:
		camera = cv2.VideoCapture(0)
		#time.sleep(0.25)
	 
	# otherwise, we are reading from a video file
	else:
		camera = cv2.VideoCapture(args["video"])
	 
	# initialize the first frame in the video stream
	firstFrame = None
	a=0
	naming=0

	# loop over the frames of the video
	for c in range(0,10):
		
		# grab the current frame and initialize the occupied/unoccupied
		# text
		(grabbed, frame) = camera.read()
		text = "Unoccupied"
	 
		# if the frame could not be grabbed, then we have reached the end
		# of the video
		if not grabbed:
			break
	 
		# resize the frame, convert it to grayscale, and blur it
		frame = imutils.resize(frame, width=500)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)
	 
		# if the first frame is None, initialize it
		if a == 50:
			firstFrame = None
			a=0
		if firstFrame is None:
			firstFrame = gray
			continue

	# compute the absolute difference between the current frame and
		# first frame
		frameDelta = cv2.absdiff(firstFrame, gray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	 
		# dilate the thresholded image to fill in holes, then find contours
		# on thresholded image
		thresh = cv2.dilate(thresh, None, iterations=2)
		(_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
	 
		# loop over the contours
		for c in cnts:
				# if the contour is too small, ignore it
				if cv2.contourArea(c) < args["min_area"]:
					continue
		 
			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
				(x, y, w, h) = cv2.boundingRect(c)
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				text = "Occupied" + "." + str(naming) + " changes found so far."
				retval, im = camera.read()
				camera_capture = im
				roi=im[y:y+h,x:x+w]
				cv2.imwrite("/root/md/" + str(naming) + '.jpg', roi)
				file = "pic.jpeg"
				cv2.imwrite(file, camera_capture)
				

	# draw the text and timestamp on the frame
		cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
			(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	 
		# show the frame and record if the user presses a key
		cv2.imshow("Security Feed", frame)
		cv2.imshow("Thresh", thresh)
		cv2.imshow("Frame Delta", frameDelta)
		key = cv2.waitKey(1) & 0xFF
	 	a=a+1
		naming=naming+1
		# if the `q` key is pressed, break from the loop
		if key == ord("q"):
			break


	while True:
		
		# grab the current frame and initialize the occupied/unoccupied
		# text
		(grabbed, frame) = camera.read()
		text = "Unoccupied"
	 
		# if the frame could not be grabbed, then we have reached the end
		# of the video
		if not grabbed:
			break
	 
		# resize the frame, convert it to grayscale, and blur it
		frame = imutils.resize(frame, width=500)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)
	 
		# if the first frame is None, initialize it
		if a == 50:
			firstFrame = None
			a=0
		if firstFrame is None:
			firstFrame = gray
			continue

	# compute the absolute difference between the current frame and
		# first frame
		frameDelta = cv2.absdiff(firstFrame, gray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	 
		# dilate the thresholded image to fill in holes, then find contours
		# on thresholded image
		thresh = cv2.dilate(thresh, None, iterations=2)
		(_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
	 
		# loop over the contours
		for c in cnts:
				# if the contour is too small, ignore it
				if cv2.contourArea(c) < args["min_area"]:
					continue
		 
			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
				(x, y, w, h) = cv2.boundingRect(c)
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				text = "Occupied" + "." + str(naming) + " changes found so far."
				retval, im = camera.read()
				camera_capture = im
				roi=im[y:y+h,x:x+w]
				cv2.imwrite("/root/md/" + str(naming) + '.jpg', roi)
				file = "pic.jpeg"
				cv2.imwrite(file, camera_capture)
				

	# draw the text and timestamp on the frame
		cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
			(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	 
		# show the frame and record if the user presses a key
		cv2.imshow("Security Feed", frame)
		cv2.imshow("Thresh", thresh)
		cv2.imshow("Frame Delta", frameDelta)
		key = cv2.waitKey(1) & 0xFF
	 	a=a+1
		naming=naming+1
		# if the `q` key is pressed, break from the loop
		if key == ord("q"):
			break


	# cleanup the camera and close any open windows
	camera.release()

	cv2.destroyAllWindows()


def backend():
		os.system("python li.py")


if __name__=='__main__':
     p1 = Process(target = cv)
     p1.start()
     p2 = Process(target = backend)
     p2.start()
