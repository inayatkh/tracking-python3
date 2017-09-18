

# Tracking Using OpenCV >= 3.2 and Python-3.5

In this repository I will give some implementation of single and multiple object tracking algorithms. These include meanShift, CamShift, Boosting, MIL, KCF, TLD , GoTurn, and MedianFlow. Additionally I will show you how to grab frames at a very high FPS from camera and videos.


## Directory Structure:

.
├──  tracking-py3 

	└──
	   |
	   
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
 
## Meanshift and CAMshift 
 
 The MeanShift algorithm looks to object tracking as mode-seeking problem. Mean-shift was first presented by [Fukunaga et al in 1975](http://ieeexplore.ieee.org/document/1055330/). It is a non-parametric approach for finding the maxima of a density function. The process is an iterative approach that involves calculating and shifting the mean of a set of data points, which fall in a circle, in the direction of the mean shift vector and thus it is called Meanshift. The radius of the circle is also called window size.
 
 The value of the radius does matter. Very small value will generate local maxima while veray large value of the radius will let the algo to find true maxima. If there are more than one mode then they will be merged. To handle this problem radius of the circle needs to be changed adaptively. This is done by CAMshift algorithm ( Continuously Adaptive Meanshift)
 
 For the widow located at \\(x\\), the center of the mass \\(m(x)\\)of the neighboring points  \\(x_i\\) is calculated as 

$$m(x) = \frac{\sum_i{K(x - x_i)}x_i}{\sum_i{K(x - x_i)}}$$
where \\( K\\) is the kernel used to decide the widow size and how the weights of different points will be accumulated


### Tracking using MeanShift in OpenCV
We will use the following steps for live tracking of face using web cam:

1.  Detect the face, which we want to track, using dlib face detector. Compute the histogram of the face region using Hue Channel of the HSV color space. However, both H and S can be used. Its worthy to note that color information is very sensitive to lighting variations.

	use calcHist() function of OpenCV for computing the histogram and normalize the values in the range [0,255] 
 	
 	
 2. Find the back projected image for every new frame using calcBackPorject() function
 
 3. Use meanShift() function to find the maxima in the backprojected image in the neigborhood of the old position. This alog finds the mode of the back projected image which obviously a confidence map of similarity between the color distribution of the face and the new image.
 
 #### Remarks

 The MeanShift trackers sometimes fails when the scale of the object of interest changes, because the tracker is initialized to the scale of the object in the first frame. Later when scale of the object is changed then the tracker window size does not match the actual size of the object. This problem is handeled by the CAMshift tracker.
 
 #### usage: 

	$ python meanShiftTrack.py
	
### Tracking using CAMshift in OpenCV
CAMshift tries to tackle the scale problem by using varying window size for applying meanshift. CamShift was developed by [Gary Bradski in 1998](http://dl.acm.org/citation.cfm?id=836819).

Steps 1 and 2 are the same as that of MeanShift. In the third step, we find the backproject image and then use CamShift() openCV function to track the position of the object in the new frame. This function finds the an object center using meanshift and then adjust the window size. This funciton returns the rotaed rectangle that includes the object position, size, and orientation.

 #### usage: 

	$ python CAMShiftTrack.py
___
___ 

### Tracking by using OpenCV 3.2 Api and Python

OpenCV 3.2 has its own implementation of the following six single object tracking methods:

- BOOSTING based on online AdaBoost HAAR cascade detector
- Multiple Instance Learning (MIL)
- Kernelized Correlation Filters (KCF)
- Tracking, Learning and Detection (TLD)
- MedianFlow
- GoTurn (Deep Learning Based tracker)

#### usage single object tracking: 

	$ python trackeOneObject.py -t 0  
	
the input t specifies the methd:
	0  for boosting, 1 for MKL, 2 for KCF, 3 for TLD, 4 for MedianFlow, and 5 for GOTURN
	
This code will track the face in the live video stream from webcam


#### usage multiple object tracking: 

	$ python trackMultipleObjects.py -t 0  -v path-to-video-file
	
the input t specifies the methd:
	0  for boosting, 1 for MKL, 2 for KCF, 3 for TLD, 4 for MedianFlow, and 5 for GOTURN


## *References*

1. [Pyimagesearch Adrian Rosebrock](http://www.pyimagesearch.com/)  
 
2.  [Learn OpenCV, Satya Mallick](http://www.learnopencv.com)  
