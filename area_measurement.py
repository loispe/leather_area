from math import exp
from tracemalloc import start
from PIL import Image
import imutils
import cv2
import matplotlib.pyplot as plt
import numpy as np

source_image = "data/test_area_edited.jpg"

#----------------------------------------------------------------------
def visualizePixels(pixels, img):

    fig, axs = plt.subplots(1, 2, sharex=True)
    axs[0].imshow(pixels)
    axs[1].imshow(img)

#----------------------------------------------------------------------
def getAreafromEdges(edgedImage):

    pixel_arr = np.zeros(shape=(edgedImage.size[1], edgedImage.size[0]))   #create empty array with the image size

    for x in range(0, edgedImage.size[0]):
        for y in range(0, edgedImage.size[1]):
            if edgedImage.getpixel((x,y)) > 150:        #check if greyscale is greater than 150 (edge)
                pixel_arr[y, x] = 1                     #set every pixel within the skin area to 1

    pixel_arr = scanForEdges(pixel_arr, edgedImage)

    return pixel_arr
#----------------------------------------------------------------------
def scanForEdges(pixel_arr, edgedImage):
    for column_idx in range(edgedImage.size[0]):
            column = pixel_arr[:, column_idx]                  #extract one column from matrix at a time
            edges = np.asarray(np.where(column == 1))[0]       #extract all identified edge positions
            #print(f"Array column {column_idx}: {edges}")
            if edges.size > 0:                              #if there are edges in the extracted column, find the area inbetween the edges and set them to 1 as well
                #print(f"Edges amount column {column_idx}: {edges.size}")
                for edge_idx in range(0, len(edges)):
                    if edge_idx != len(edges) - 1:
                        for gap_pixel_idx in range(edges[edge_idx], edges[edge_idx + 1]):
                            column[gap_pixel_idx] = 1
    
    return pixel_arr
#----------------------------------------------------------------------
def startCalc():
    #duplicate and rotate the original picture to capture indents in the skin edge no matter of their direction
    haut = cv2.imread(source_image)
    haut = imutils.resize(haut, width=720, height=1080)     #add resize when taking the picture 
    haut_90 = cv2.rotate(haut, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite("data\Haut_bsp_90.jpg", haut_90)

    #edge detection
    haut_grey = cv2.cvtColor(haut, cv2.COLOR_BGR2GRAY)
    haut_edged = cv2.Canny(haut_grey, 30, 200)
    cv2.imwrite("data\Haut_Umrisse.jpg", haut_edged)

    #rotate edged picture
    im_haut_edged = Image.open("data\Haut_Umrisse.jpg")
    im_haut_edged_90 = im_haut_edged.rotate(270, Image.NEAREST, expand = 1)

    #ectract the pixels which are enclosed by the skin edge as a 2d array
    area_pixels = getAreafromEdges(im_haut_edged)
    area_pixels_90 = getAreafromEdges(im_haut_edged_90)

    #combine the two area arrays into a single one
    pixels_combined = np.add(np.flip((area_pixels_90.T), 0), area_pixels)
    pixel_cnt = 0
    for x in range(im_haut_edged.size[0]):
        for y in range(im_haut_edged.size[1]):
            if pixels_combined[y, x] != 2:
                pixels_combined[y, x] = 0
            else:
                pixels_combined[y, x] = 1     
                pixel_cnt += 1

    #read out calibration
    f = open("calibration.txt", "r")
    calibration = float(f.readline())

    # Print size
    print(f"Leather pixel count: {pixel_cnt} Pixel")#
    print(f"Calibration: 1 Pixel length = {calibration}m")
    print(f"Calibration: 1 Pixel area   = {calibration**2}m^2")
    print(f"Leather surface area = {pixel_cnt * (calibration ** 2)} m^2")

    #convert binary array to cv2 image
    cv2.imwrite("data\maske_ergebnis.jpg", pixels_combined * 255)
    mask = Image.open("data\maske_ergebnis.jpg").convert("RGB")  

    # Show result
    plt_img = plt.imread(source_image)
    plt_img_90 = plt.imread("data\haut_bsp_90.jpg")
    visualizePixels(area_pixels, plt_img)
    visualizePixels(area_pixels_90, plt_img_90)

    background = cv2.imread(source_image)
    haut_maske = cv2.addWeighted(np.array(mask), 0.4, np.array(background), 0.6, 0)
    cv2.imwrite("data\haut+maske.jpg", haut_maske)
    cv2.imshow("Haut + Maske", haut_maske)

    # Showing the result in a plot:
    # plt_img_haut_maske = plt.imread("data\haut+maske.jpg")
    # fig, ax = plt.subplots()
    # ax.imshow(plt_img_haut_maske)

    plt.show()

if __name__ == "__main__":
    startCalc()