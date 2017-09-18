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
import sys

from utils.fps2 import FPS2
from matplotlib import tight_bbox



    
if __name__ == '__main__':
    
    # Initialize the argument parse which is used to parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=True,
                    help="path to input video file")
    
    ap.add_argument("-t", "--type", required=True,
                    help="input  from [0..5] for selection of type of tracker from ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN'] ")
    args = vars(ap.parse_args())
    
    print("[info] tracker selected is ", args["type"])
    
    
    
       
    
    
    # a list of trackers type available in OpenCV3.2
    #
    trackerTypes = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    
    trackerType = trackerTypes[int(args["type"])]
    
    
    # initialize  multiple Tracker object with tracking algo
    multipleTrackerOpenCV  = cv2.MultiTracker(trackerType)
    
    
    # Since the read method of the openCV cv2.VideoCapture
    # is blocking IO operation
    # Therefore I am going to use thread enable version of reading
    # the video. It is implemented in imutil package (pyImagesearch.com)
    
    # start and open a pointer to the file video stream thread
    # and allow the buffer to start to fill
    print("[info] starting to read a video file ...")
    fvs = FileVideoStream(args["video"]).start()
    time.sleep(1.0)
    
    
    
    # read the first frame
    
    
    frame = fvs.read()
    
    #if not success:
    #   print("[info]: Failed to read the video")
    #   sys.exit(1)
        
        
    # 
    init = False
    
    bboxes = [] # contains bounding boxes around the objects to be tracked
    
    # initialize various objects in the first frame of the video
    
    while True:
        # select the ROI around the object to be tracked
        box = cv2.selectROI('tracking', frame, showCrossair=False, fromCenter=False)
        print(box)
        bboxes.append(box)
        print("[info] print q to quit object selection and anyother key for next object selection")
        k = cv2.waitKey(0) & 0xff
        if(k== 113):
            break
        
    print("[info] selecting objects {}".format(bboxes))
    
    
    
    # start the frame per second  (FPS) counter
    fps = FPS2().start() 
    
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
        
        
        # initialize the trackers only once
        if not init:
            success = multipleTrackerOpenCV.add(frame,bboxes)
            init = True
            
        success, boxes = multipleTrackerOpenCV.update(frame)
        
        print("[info] no boxes {}".format(len(boxes)))
        
        for box in boxes:
            p1= (int(box[0]), int(box[1]))
            p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
            cv2.rectangle(frame, p1, p2, (200, 0, 0))
            
        
        
        fps.update()
        cv2.putText(frame, "FPS: {:.2f}".format(fps.fps()),
                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        cv2.putText(frame, trackerType + " Tracker", (20,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        
        # show the frame and update the FPS counter
        cv2.imshow("Frame", frame)
        
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
        
        
        
        
    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    
    # do a bit of cleanup
    cv2.destroyAllWindows()
    fvs.stop()