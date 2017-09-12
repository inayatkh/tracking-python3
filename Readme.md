

# Tracking Using OpenCV and Python-3.5


In this repository I will give some implementation of tracking algorithms.
I will update the repository regullarly as soon as new algo is added to it


##Dirtory Structure:

 -tracking-py3
 -- trackers
 -- utils
 -- videos
 
 
 
 ## Tracking Algos and some usefull utils
 
### fastframerate.py 

Following [1], here I include python code to show how to grab frames from video at a very hight frame per second (FPS)

####usage: 

	$ python fastframerate.py  -v ./videos /boy-walking.mp4


***
***

### hogdetectory.py

This is an example to use  hog person detector for detection at every frame
####usage: 

	$ python hogdetectory.py -v ./videos /boy-walking.mp4
***
***

### kalmanhogtrack.py
This examples, shows the use of Kalman Filter for tracking along with Hog detection for correction

####usage: 

	$ python kalmanhogtracker.py -v ./videos /boy-walking.mp4

***
***


##*References*
1. [Pyimagesearch Adrian Rosebrock](http://www.learnopencv.com)  
 
2.  [Learn OpenCV, Satya Mallick](http://www.pyimagesearch.com/)  
