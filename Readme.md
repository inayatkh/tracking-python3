

# Tracking Using OpenCV and Python-3.5


In this repository I will give some implementation of tracking algorithms.
I will update the repository regullarly as soon as new algo is added to it


## Directory Structure:

.
├──  tracking-py3 

	└──
	
           ├──  trackers
	   
	   | 
	   
	   ├── utils
	   
	   | 
	   
	   ├── videos
	    
 
 
 
##  Tracking Algos and some Usefull utils
 ---

### fastframerate.py 

Following [1], here I include python code to show how to grab frames from video at a very hight frame per second (FPS)

#### usage: 

	$ python fastframerate.py  -v ./videos /boy-walking.mp4


***
***

### hogdetectory.py

This  example shows how  to use  hog detector for person detection at every frame.

#### usage: 

	$ python hogdetectory.py -v ./videos /boy-walking.mp4
***
***
## Kalman Filtering

Kalman Filtering is a popular signal processing algo. It used to predict the location of a moving object based on prior motion info.

### kalmanhogtrack.py

This example, which is a single person tracker,  shows the use of Kalman Filter for tracking along with Hog detection for correction

#### usage: 

	$ python kalmanhogtracker.py -v ./videos /boy-walking.mp4
	
	
---
---
 
## Meanshift and Camshift 
 
___
___ 


## *References*
1. [Pyimagesearch Adrian Rosebrock](http://www.pyimagesearch.com/)  
 
2.  [Learn OpenCV, Satya Mallick](http://www.learnopencv.com)  
