'''
Created on Sep 9, 2017

@author: inayat
'''

# import the required  packages
from imutils.video import FileVideoStream
#from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

from utils.fps2 import FPS2
from trackers.hogpeopledetector import  HogPeopleDetector

from trackers.kalmantracker import KalmanTracker
from numpy.random import random

    
if __name__ == '__main__':
    
    # Initialize the argument parse which is used to parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=True,
                    help="path to input video file")
    args = vars(ap.parse_args())
    
       
    
    # Since the read method of the openCV cv2.VideoCapture
    # is blocking IO operation
    # Therefore I am going to use thread enable version of reading
    # the video. It is implemented in imutil package (pyImagesearch.com)
    
    # start and open a pointer to the file video stream thread
    # and allow the buffer to start to fill
    print("[info] starting to read a video file ...")
    fvs = FileVideoStream(args["video"]).start()
    time.sleep(1.0)
    
    # start the frame per second  (FPS) counter
    fps = FPS2().start() 
    
    # initialize time variables these re used for calculating dt
    
    ticks = 0
    preticks = 0
    # initialize dt for transition matrix
    dt = 0.0
    # initialized hog people detector
    
    hogPersonDetector = HogPeopleDetector()
    
    kalmanTrack = KalmanTracker()
    
    ticks = kalmanTrack.initialTrackerwithHog( fvs, hogPersonDetector )

        
    # loop over the frames obtained from the video file stream
    while fvs.more():
        # grab each frame from the threaded video file stream,
        # resize
        # it, and convert it to grayscale (while still retaining 3
        # channels)
        frame = fvs.read()
        #frame = imutils.resize(frame, width=450)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #frame = np.dstack([frame, frame, frame])
        
        # display the size of the queue on the frame
        #cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
        #            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        
        # we had set the transition matrix to identity
        # we will now measure the time elapsed b/w two frames
        # inorder to fix the off diagonal elements of the transition
        # matrix
        preticks = ticks
        ticks = cv2.getTickCount()
        dt = (ticks - preticks) / cv2.getTickFrequency()
        
        kalmanTrack.setOffDiagTransitionMatrix(dt)
        
        kalmanTrack.predict()
        
        updateState = np.random.randint(0, 100) < 15
        
        #we will use hog detection to update tracking on 15 % of the time
        
        kalmanTrack.update(updateState, hogPersonDetector, frame) 
        
        
        if kalmanTrack.meastsWasUpdated :
            # use updated measuremnet
            kalmanTrack.objTracked[0:3,0] = kalmanTrack.updatedMeasts[0:3, 0].astype(np.int32)
            kalmanTrack.objTracked[3,0] = 2 * kalmanTrack.updatedMeasts[2, 0].astype(np.int32)
            
        else:
            # if measurements are not updated used predicted values
            kalmanTrack.objTracked[0:3,0] = kalmanTrack.predictedMeasts[0:3, 0].astype(np.int32)
            kalmanTrack.objTracked[3,0] = 2 * kalmanTrack.predictedMeasts[2, 0].astype(np.int32)
            
            
        x1, y1, w1, h1 = kalmanTrack.objTracked.ravel()
        cv2.rectangle(frame, (x1, y1), (x1+w1, y1+h1), (0,0,255), 2, 4)
        
        fps.update()
        cv2.putText(frame, "Frame Size(wxh)  {}x{}".format(frame.shape[1],frame.shape[0]),
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, "Hog plus Kalman Tracking --> FPS: {:.2f}".format(fps.fps()),
                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        
        # show the frame and update the FPS counter
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)
        
        
        
        
    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    
    # do a bit of cleanup
    cv2.destroyAllWindows()
    fvs.stop()