'''
Created on Sep 9, 2017

@author: inayat
'''

# import the required  packages
from imutils.video import WebcamVideoStream
#from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

from utils.fps2 import FPS2



    
if __name__ == '__main__':
    
   
    
       
    
    print("[info] starting to read a webcam ...")
    capWebCam = WebcamVideoStream(0).start()
    time.sleep(1.0)
    
    # start the frame per second  (FPS) counter
    fps = FPS2().start() 
    
    
    
    # loop over the frames obtained from the webcam
    while True:
        # grab each frame from the threaded  stream,
        # resize
        # it, and convert it to grayscale (while still retaining 3
        # channels)
        frame1 = capWebCam.read()
        frame = cv2.flip(frame1,1)
        #frame = imutils.resize(frame, width=450)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #frame = np.dstack([frame, frame, frame])
        
        # display the size of the queue on the frame
        #cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
        #            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        
        fps.update()
        cv2.putText(frame, "FPS: {:.2f}".format(fps.fps()),
                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        
        # show the frame and update the FPS counter
        cv2.imshow("Face Tracking", frame)
        
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break
        
        
        
        
    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    
    # do a bit of cleanup
    cv2.destroyAllWindows()
    capWebCam.stop()
    
    