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
import dlib

from utils.fps2 import FPS2



    
if __name__ == '__main__':
    
    
    # Initialize the argument parse which is used to parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--type", required=True,
                    help="input  from [0..5] for selection of type of tracker from ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN'] ")
    args = vars(ap.parse_args())
    
    print("[info] tracker selected is ", args["type"])
   
    # a list of trackers type available in OpenCV3.2
    #
    trackerTypes = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    
    trackerType = trackerTypes[int(args["type"])]
    
    trackerOpenCV = cv2.Tracker_create("MIL")
    
    
    # for initialization of the tracker we use dlib face detector
    
    # initialize dlib face detector
    
    frontFaceDetector = dlib.get_frontal_face_detector() 
    initOnce = False
       
    
    print("[info] starting to read a webcam ...")
    capWebCam = WebcamVideoStream(0).start()
    time.sleep(1.0)
    
    # start the frame per second  (FPS) counter
    #fps = FPS2().start() 
    
    
    
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
        
        
        if not initOnce:
            
            faceRect = frontFaceDetector(frame, 0)
            
            if(len(faceRect) == 0):
                continue
            
            
            # start the frame per second  (FPS) counter
            fps = FPS2().start()
            
            bbox = faceRect[0]
            
            print(bbox)
            
                        
            # convert dlib rect to opencv rect
            
            curFaceBbox = (int(bbox.left()), int(bbox.top()), int(bbox.right() - bbox.left()),
                         int(bbox.bottom() - bbox.top()) )
            
            # intialize the  Tracker
            
            #curFaceBbox = cv2.selectROI("tracking", frame)
            
            success = trackerOpenCV.init(frame, curFaceBbox)
            
            
            initOnce = True
            #continue
            
            
                           
        
        # Update tracker
        success, curFaceBbox = trackerOpenCV.update(frame) 
        print(success, curFaceBbox)
        if success:
            # Tracking success
            topLeft = (int(curFaceBbox[0]), int(curFaceBbox[1]))
            bottomRight = (int(curFaceBbox[0] + curFaceBbox[2]), int(curFaceBbox[1] + curFaceBbox[3]))
            cv2.rectangle(frame, topLeft,bottomRight, (255,0,0), 2,1 )
        else:
            # Tracking failure 
            cv2.putText(frame, trackerType + " Tracking failure detected", (20,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)     
        
        fps.update()
        cv2.putText(frame, "FPS: {:.2f}".format(fps.fps()),
                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        cv2.putText(frame, trackerType + " Tracker", (20,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        
        # show the frame and update the FPS counter
        cv2.imshow("OpenCV Tracking by " + trackerType,  frame)
        
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
    
    