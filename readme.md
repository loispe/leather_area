# Project: Leather skin size measurement

In this project I'll try to implement a script which is able to measure the size of a cows leather skin from a picture. With only basic knowledge about pyhton and image processing I hope to learn about both in the process. 

The basic idea is to calibrate a fixed camera to the environment in a way to get information about the real physical distance a pixel of the imported image is representing. By detecting the pixels which are located within the area of interest (leather skin), I think I should be able to calculate the physical area in m^2. 