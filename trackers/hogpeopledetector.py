'''
Created on Sep 10, 2017

@author: inayat (inayatkh@gmail.com)
'''
import cv2
import numpy as np
class HogPeopleDetector(object):
    '''
    this class implements the opencv Hog People Detector detector
    '''


    def __init__(self):
        '''
        Constructor
        initialize hog for people detection
        '''
        winSize = (64, 128)
        blockSize = (16, 16)
        blockStride = (8, 8)
        cellSize = (8, 8)
        nbins = 9
        derivAperture = 1
        winSigma = -1
        histogramNormType = 0
        L2HysThreshold = 0.2
        gammaCorrection = True
        nlevels = 64
        signedGradient = False
        self.params={}
        self.params["winSize"]= winSize
        self.params["blockSize"] = blockSize 
        self.params["blockStride"] = blockStride
        self.params["cellSize"] = cellSize
        self.params["nbins"] = nbins
        self.params["derivAperture"] = derivAperture
        self.params["winSigma"] = winSigma
        self.params["histogramNormType"] = histogramNormType
        self.params["L2HysThreshold"] = L2HysThreshold
        self.params["gammaCorrection"] = gammaCorrection
        self.params["nlevels"] = nlevels
        self.params["signedGradient"] = signedGradient
        
        # Initialize HOG
        self.hog = cv2.HOGDescriptor(self.params["winSize"], self.params["blockSize"],
                                     self.params["blockStride"],
                                     self.params["cellSize"], self.params["nbins"],
                                     self.params["derivAperture"],self.params["winSigma"],
                                     self.params["histogramNormType"], self.params["L2HysThreshold"],
                                     self.params["gammaCorrection"], self.params["nlevels"],
                                     self.params["signedGradient"])
        
        
                            
                                                 
        self.svmDetector = cv2.HOGDescriptor_getDefaultPeopleDetector()
        self.hog.setSVMDetector(self.svmDetector)
        
        #return self
    
    def  maxRectArea(self, rects):
        '''
            returns the largest rectangle
            
        '''
        area = 0
        maxRect = rects[0].copy()
        for rect in rects:
            x, y, w, h = rect.ravel()
            if w*h > area:
                area = w*h
                maxRect = rect.copy()
        maxRect = maxRect[:, np.newaxis]
        return maxRect
       
    def detectLargest(self,image):
        '''
        returns the one largest detected people bounding 
        box 
         
        '''
        objects, weights = self.hog.detectMultiScale(image, winStride=(8, 8),
                                                     padding=(32, 32), scale=1.05,
                                                     hitThreshold=0, finalThreshold=1,
                                                     useMeanshiftGrouping=False)
        objectDetected = []
        if len(objects) > 0:
            # Find largest object
            objectDetected = self.maxRectArea(objects)
            
        
        # Display detected rectangle
        #x1, y1, w1, h1 = objectDetected.ravel()
        # cv2.rectangle(frameDisplayDetection, (x1, y1), (x1+w1, y1+h1), red, 2, 4)
        return objectDetected



        