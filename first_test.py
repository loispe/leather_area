from math import exp
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

source_image = "data\haut_bsp.jpg"

#----------------------------------------------------------------------
def getAreafromEdges(edgedImage):

    pixels = np.zeros(shape=(edgedImage.size[1], edgedImage.size[0]))   #create empty array with the image size

    for x in range(edgedImage.size[0]):
        for y in range(edgedImage.size[1]):
            if edgedImage.getpixel((x,y)) > 150:    #check if greyscale is greater than 150 (edge)
                pixels[y, x] = 1                    #set every pixel within the skin area to 1


    for column_idx in range(edgedImage.size[0]):
        column = pixels[:, column_idx]                  #extract one column from matrix at a time
        edges = np.asarray(np.where(column == 1))[0]    #extract all identified edge positions

        if edges.size > 0:                              #if there are edges in the extracted column, find the area inbetween the edges and set them to 1 as well
            print(f"Column: {column_idx}: Edges detected: {edges.size}")
            for edge_idx in range(0, len(edges)):
                if edge_idx != len(edges) - 1:
                   for gap_pixel_idx in range(edges[edge_idx], edges[edge_idx + 1]):
                        column[gap_pixel_idx] = 1

    return pixels
#----------------------------------------------------------------------

haut = cv2.imread(source_image)
haut_90 = cv2.rotate(haut, cv2.ROTATE_90_CLOCKWISE)
haut_180 = cv2.rotate(haut, cv2.ROTATE_180)
haut_270 = cv2.rotate(haut, cv2.ROTATE_90_COUNTERCLOCKWISE)
cv2.imwrite("data\Haut_bsp_90.jpg", haut_90)
cv2.imwrite("data\Haut_bsp_180.jpg", haut_180)
cv2.imwrite("data\Haut_bsp_270.jpg", haut_270)

haut_grey = cv2.cvtColor(haut, cv2.COLOR_BGR2GRAY)
haut_edged = cv2.Canny(haut_grey, 30, 200)
cv2.imwrite("data\Haut_Umrisse.jpg", haut_edged)

im_haut_edged = Image.open("data\Haut_Umrisse.jpg")
im_haut_edged_90 = im_haut_edged.rotate(270, Image.NEAREST, expand = 1)
im_haut_edged_180 = im_haut_edged.rotate(180, Image.NEAREST, expand = 1)
im_haut_edged_270 = im_haut_edged.rotate(90, Image.NEAREST, expand = 1)

pixels = getAreafromEdges(im_haut_edged)
pixels_90 = getAreafromEdges(im_haut_edged_90)
pixels_180 = getAreafromEdges(im_haut_edged_180)
pixels_270 = getAreafromEdges(im_haut_edged_270)

pixels_combined = np.add(np.flip((pixels_90.T), 0), pixels)
pixels_combined = np.add(pixels_combined, np.flip(pixels_180))
pixels_combined = np.add(pixels_combined, np.flip(pixels_270, 0).T)

pixel_cnt = 0

for x in range(im_haut_edged.size[0]):
    for y in range(im_haut_edged.size[1]):
        if pixels_combined[y, x] != 4:
            pixels_combined[y, x] = 0
        else:
            pixels_combined[y, x] = 1
            pixel_cnt += 1
       

plt_img = plt.imread(source_image)
plt_img_90 = plt.imread("data\haut_bsp_90.jpg")
plt_img_180 = plt.imread("data\haut_bsp_180.jpg")
plt_img_270 = plt.imread("data\haut_bsp_270.jpg")

fig, axs = plt.subplots(4, 2, sharex=True)
axs[0, 0].imshow(pixels)
axs[0, 1].imshow(plt_img)
axs[1, 0].imshow(pixels_90)
axs[1, 1].imshow(plt_img_90)
axs[2, 0].imshow(pixels_180)
axs[2, 1].imshow(plt_img_180)
axs[3, 0].imshow(pixels_270)
axs[3, 1].imshow(plt_img_270)

print(f"Leather pixel count: {pixel_cnt} Pixel")#
print(f"Calibration: 1 Pixel = 91.796*10^-6 m^2")
print(f"Leather surface area = {pixel_cnt * 0.000091796} m^2")

cv2.imwrite("data\maske.jpg", pixels_combined * 255)

background = cv2.imread(source_image)

mask = Image.open("data\maske.jpg").convert("RGB")
width, hight = mask.size
haut_maske = cv2.addWeighted(np.array(mask), 0.4, np.array(background), 0.6, 0)
cv2.imwrite("data\haut_maske.jpg", haut_maske)

plt_img_haut_maske = plt.imread("data\haut_maske.jpg")
fig, ax = plt.subplots()
ax.imshow(plt_img_haut_maske)
plt.show()