# Project: Leather skin size measurement

In this project I'll try to implement a script which is able to measure the size of a cows leather skin from a picture. With basic knowledge about pyhton and image processing I hope to learn about both in the process. 

<!-- The basic idea is to calibrate a fixed camera to the environment in such a way to get information about the real physical distance a pixel of the imported image is representing. By detecting the pixels which are located within the 2D area of interest (leather skin), I plan to calculate the physical area in m^2 by multipyling the amount of pixels with the surface area which is represented by one pixel. -->

## Approach
The first step is to calibrate the camera. This is needed to understand how far away the measurment plane is and how much surface area each pixel of the captured image is representing. 
To do this, I'm using opencv and the underlaying ArUco markers. A Nikon D90 is pointed to the desired measuring plane and controlled via gphoto2. After placing two ArUco markers next to each other with a known distance inbetween them, I'm able to calculate the "pixel-distance" inbetween them from the captured pixture. Correlating the distance in pixels with the real world distance in mm allows the determination of a pixel "length" (and area). 
Once the calibration is done, the markers can be swapped by the measurement object. At this point, it has to have a notable contrast difference compared to the background to ensure a flawless edge detection by opencv.
I will then transform the result of the error detection into a 2D-Array to enable the area calculation. This is avhieved by detecting the pixels which are located inbetween to edges (beside some edge cases).
The final step is to count all the recored pixels and to multiply the sum with the area of one pixel to get the total area.

The measurement accuracy depends on multiple factors: 
 * Quality of the picture (brightness, sharpness)
 * Calibration accuracy 
 * Cleanliness of the measurement objects edges
 * Contrast of measurement object

 At the moment, I'm able to calculate the area of simple shapes like a DIN A4 sized "L" with the accuracy of 99.7%.






## Dependencies
Linux OS (Ubuntu) with the following packages and Python modules (TBC):

* gphoto2: Operating the DSLR camera via USB
* opencv-python: Edge detection and  ArUco markers
* matplotlib: visualization of matrix modifications 

