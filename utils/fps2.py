'''
Created on Sep 9, 2017

@author: inayat (inayatkh@gmail.com)
'''

import datetime

class FPS2(object):
    '''
     FPS2 class is used to calculate the frames per second time
    '''


    def __init__(self):
        '''
        store the start time, end time, and total number of frames
        that were examined between the start and end intervals
        '''
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        '''
            start the timer
        '''
        
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        '''
         stop the timer
        '''
        
        self._end = datetime.datetime.now()

    def update(self):
        '''
         increment the total number of frames examined during the
         start and end intervals
        '''
        self._end = datetime.datetime.now() 
        # the above is the change in my version of FPS
        # from the andrian imutils package 
        # the imutils fps gives an error NoneType when 
        # fps.fps() is called with in the loop for getting current FPS 
        self._numFrames += 1

    def elapsed(self):
        '''
         return the total number of seconds between the start and
         end interval
        '''
        return (self._end - self._start).total_seconds()

    def fps(self):
        '''
         compute the (approximate) frames per second
        '''
        return self._numFrames / self.elapsed()
    
        