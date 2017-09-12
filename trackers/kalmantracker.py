'''
Created on Sep 10, 2017

@author: inayat
'''
import cv2

import  numpy as np
from numpy import dtype


from imutils.video import FileVideoStream

#from hogpeopledetector import  HogPeopleDetector
'''
  Kalman filter adopts the following strategy
  1.. Predict: Make predictions about the internal state of the system, such as the position and veloicity of 
  the vehicle, based on the previous internal state and any control input (e.g propeller force)
  2.. Update: When new measurments are available then use it to update the prediction made in step 1
'''
class KalmanTracker(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Initialize Kalman filter for tracking one person
        In openCV Kalman filter is initialized using 
        KalmanFilter KF(nmbStateVars, nmbMeasts, nmbControlInputs, type)
        Here we will use the state of our kalman filter which consists of
        6 elments (x,y,w,vx,vy,vw)
        where
        x,y are the coord  of the top left corner of the bounding box
        w is the width of the detected person
        vx,vy are the x and y velocities of the top left corner
        vw is the rate of change of the width w.r.to time
        
        the height of the bounding box is not considered as the part
        of the state because it is assumed to be equal to twice the width
        
        '''
        
        nmbStateVars =  6
        
        # the measurement matrix has 3 elements (x,y, w)
        nmbMeasts = 3
        
        # there are no control inputs , as we will this class
        # for tracking in video file and there is no way to change
        #  the affect of the state of the person walking
        
        nmbControlInputs = 0
        
        # the type is float32
        
        self.KF = cv2.KalmanFilter(nmbStateVars, nmbMeasts, nmbControlInputs)
        
        
        '''
         bz our motion model is
          x = x + vx * dt
          y = y + vy * dt
          w = y + vw * dt
          
          here for simplicity we assume zero accelaration, therefore
           vx = vx
           vy = vy
           vw = vw
           
          Our transition matrix is of the following form
          [
           1, 0, 0, dt, 0,  0,
           0, 1, 0, 0, dt, 0
           0, 0, 1, 0, 0, dt
           0, 0, 0, 1, 0, 0
           0, 0, 0, 0, 1, 0
           0, 0, 0, 0, 0, 1
           ]
           
           which is 6x6 identity matrix and later we add dt in a loop
        
        '''
        
        self.KF.transitionMatrix = cv2.setIdentity(self.KF.transitionMatrix)
        
        '''
          our measurment matrix is the following form
          bz we are only detecting x, y, and w, the measurment matrix
          picks only these quantities and leaves vx, vy and vw
          
          [
            1, 0, 0, 0, 0, 0,
            0, 1, 0, 0, 0, 0
            0, 0, 1, 0, 0, 0
            ]
        ''' 
        self.KF.measurementMatrix = cv2.setIdentity(self.KF.measurementMatrix)
        
        # initializing variables to be used of tracking
        
        # initialize var to store detected x, y, w
        self.measurement = np.zeros((3, 1), dtype= np.float32)
        
        # initialize vars to store tracked object
        self.objTracked = np.zeros((4, 1), dtype = np.float32)
        
        # vars used to store the results of the predict and update
        self.updatedMeasts = np.zeros((3, 1), dtype= np.float32)
        self.predictedMeasts = np.zeros((6, 1), dtype= np.float32)
        
        # boolean for the indication of whether the measurments are updated
        self.meastsWasUpdated = False
        
        
    def initialTrackerwithHog(self, fvs, hogPersonDetector ):
        '''
         initialize kalman tracker with hog detector
         by reading frames until the first person is detected
        '''      
        
        # loop over the frames obtained from the video file stream
        while fvs.more():
                   
            frame = fvs.read()
            
            objectDetected = hogPersonDetector.detectLargest(frame)
            
            if len(objectDetected) > 0:
                #x1, y1, w1, h1 = objectDetected.ravel()
                #cv2.rectangle(frame, (x1, y1), (x1+w1, y1+h1), (0,0,255), 2, 4)
                
                # copy max area to kalman filter
                self.measurement = objectDetected[:3].astype(np.float32)
                
                # update state , its worthy to note that x,y, w are set
                # to measured values where vx= vy= vw = 0 as we have no idea
                # about the velocities yet
                
                self.KF.statePost[0:3, 0] = self.measurement[:, 0]
                self.KF.statePost[3:6] = 0.0
                
                # set processNoisCon (Q) and measurementNoiseCov (R)
                # these values are set by trial and error by trying various values
                # set diagnal values for covariance matrices . processNoiseCon is Q
                self.KF.processNoiseCov = cv2.setIdentity(self.KF.processNoiseCov, (1e-2))
                
                                
                self.KF.measurementNoiseCov = cv2.setIdentity(self.KF.measurementNoiseCov, (1e-2))
                
                return cv2.getTickCount()
            
            
    def setOffDiagTransitionMatrix(self, dt):
        
        self.KF.transitionMatrix[0,3] = dt
        self.KF.transitionMatrix[1,4] = dt
        self.KF.transitionMatrix[2, 5] = dt
        
    def predict(self):
        
        self.predictedMeasts = self.KF.predict()
        
    def update(self, updateState, hogPersonDetector, frame):
        
        
        if updateState:
            
            objectDetected = hogPersonDetector.detectLargest(frame)
            
            if len(objectDetected) > 0:
                
                # copy x, y and w from the detected rect
                self.measurement = objectDetected[0:3].astype(np.float32)
                
                # perform kalman update step
                self.updatedMeasts =  self.KF.correct(self.measurement)
                self.meastsWasUpdated = True
            else:
                # measurment not updated bz person not detected
                self.meastsWasUpdated = False
        else:
            # measurments not update
            self.meastsWasUpdated = False
            
                

                 
          
        