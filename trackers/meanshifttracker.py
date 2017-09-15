'''
Created on Sep 15, 2017

@author: inayat
'''
import numpy as np
import cv2
import sys


class MeanShiftTracker(object):
    '''
    classdocs
    '''


    def __init__(self, curWindowRoi, imgBGR):
        '''
        curWindow =[x,y, w,h] // initialize the window to be tracked by the tracker 
        '''
        self.updateCurrentWindow(curWindowRoi)
        self.updateHistograms(imgBGR)
        
        # set up the termination criteria for meanshift, either 10 iterations or move by at least 1 pt
        self.term_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
       
        
    def updateCurrentWindow(self,  curWindowRoi ):
        
        self.curWindow = curWindowRoi;
        
        
    def updateHistograms(self, imgBGR):
        '''
          update the histogram and rois according to the current object in the current image
        
        '''
        
             
        
        self.bgrObjectRoi = imgBGR[self.curWindow[1]: self.curWindow[1]+ self.curWindow[3],
                                self.curWindow[0]: self.curWindow[0]+ self.curWindow[2]]
        self.hsvObjectRoi = cv2.cvtColor(self.bgrObjectRoi, cv2.COLOR_BGR2HSV)
        
        # get the mask for calculating histogram and also remove some noise
        self.mask = cv2.inRange(self.hsvObjectRoi, np.array((0., 50. , 50.)), np.array((180, 255., 255.)))
        
        # use 180 bins for each H value, and normalize the histogram to lie b/w [0, 255]
        self.histObjectRoi = cv2.calcHist([self.hsvObjectRoi], [0], self.mask, [180], [0,180])
        cv2.normalize(self.histObjectRoi, self.histObjectRoi, 0, 255, cv2.NORM_MINMAX)
        
    def getBackProjectedImage(self, imgBGR):
        '''
           convert the current BGR image, imgBGR, to HSV color space 
           and return the backProjectedImg
        '''
        #print("[info] getBackprjectImage calls", imgBGR.shape)
        imgHSV = cv2.cvtColor(imgBGR,cv2.COLOR_BGR2HSV)
        
        # obtained the back projected image using the histogram obtained earlier
        
        backProjectedImg = cv2.calcBackProject([imgHSV], [0], self.histObjectRoi, [0,180], 1)
        
        self.backProjectedImg = backProjectedImg
        
        return backProjectedImg.copy()
    
    def computeNewWindow(self, imgBGR):
        '''
            Track the window enclosing the object of interest using meanShift function of openCV for the 
            current frame imgBGR
        '''
        
        self.getBackProjectedImage(imgBGR)
        
        _ , curWindow = cv2.meanShift(self.backProjectedImg, self.curWindow, self.term_criteria)
        
        self.updateCurrentWindow(curWindow)
        
    def getCurWindow(self):
        
        return self.curWindow
        
        
    
        
        
         