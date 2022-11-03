import cv2
import imutils
import math

#image_path = "data/camera_output.png"
image_path = "data/calibration_pic.jpg"
CAL_MARKER_DISTANCE_MM = 97   #mm
#----------------------------------------------------------------------
def detectMarker():
    marker_0_pos = [-1, -1]
    marker_1_pos = [-1, -1]

    img = cv2.imread(image_path)
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    aruco_Params = cv2.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv2.aruco.detectMarkers(img, aruco_dict, parameters=aruco_Params)


    if len(corners) > 0:
        ids = ids.flatten()

        for marker, id in zip(corners, ids):
            corners = marker.reshape((4, 2))
            (top_left_corner, top_right_corner, bottom_right_corner, bottom_left_corner) = corners

            top_right_corner = (int(top_right_corner[0]), int(top_right_corner[1]))
            top_left_corner = (int(top_left_corner[0]), int(top_left_corner[1]))
            bottom_right_corner = (int(bottom_right_corner[0]), int(bottom_right_corner[1]))
            bottom_left_corner = (int(bottom_left_corner[0]), int(bottom_left_corner[1]))
            
            #draw square around marker
            cv2.line(img, top_left_corner, top_right_corner, (0, 0, 255), 1)
            cv2.line(img, top_right_corner, bottom_right_corner, (0, 0, 255), 1)
            cv2.line(img, bottom_right_corner, bottom_left_corner, (0, 0, 255), 1)
            cv2.line(img, bottom_left_corner, top_left_corner, (0, 0, 255), 1)

            center_x = int((top_left_corner[0] + bottom_right_corner[0]) / 2.0)
            center_y = int((top_left_corner[1] + bottom_right_corner[1]) / 2.0)
            cv2.circle(img, (center_x, center_y), 6, (0, 255, 0))
            cv2.putText(img, str(id),(top_left_corner[0], top_left_corner[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if id == 0:
                marker_0_pos = [center_x, center_y]
            elif id == 1:
                marker_1_pos = [center_x, center_y]

    else:
        raise UnboundLocalError("No markers detected! Make sure the calibration stick is placed in the picture frame.")
            
    if marker_0_pos[0] == -1 or marker_1_pos[0] == -1:
        raise UnboundLocalError("Coulnd't detect all marker edges! Check calibration picture!")

    return img, marker_0_pos, marker_1_pos
#----------------------------------------------------------------------

def calcPixelLen(img, c0, c1):
    #    
    #     ^
    #   y |
    #
    #
    #  c0 O
    #     XXXX
    #     XXXXXXX
    #leg0 XXXXXXXXXX     opposite
    #     XXXXXXXXXXXXX
    #     XXXXXXXXXXXXXXXX
    #  c2 OXXXXXXXXXXXXXXXXXO c1   --> x
    #           leg1
    #
    # C0 <--> C1 = 1m

    c2 = [c0[0], c1[1]]     #c0 = [x, y]

    cv2.line(img, c0, c2, (255, 0, 0), 1)   #leg0
    cv2.line(img, c0, c1,  (255, 0, 0), 1)  #opposite
    cv2.line(img, c1, c2, (255, 0, 0), 1)   #leg1

    cv2.imwrite("data/current_calibration.jpg", img)

    len_leg0 = abs(c0[1] - c2[1])
    len_leg1 = abs(c1[0] - c2[0])

    # opposite = math.sqrt(len_leg0 ** 2 + len_leg1 ** 2)     # opposite given in pixels = 1 meter
    # pixel_len = 1 / opposite                                # 1000/opposite => length of one pixel in meter

    alpha = math.atan(len_leg0/len_leg1)                        #calc angle alpha between leg1 and opposite by using tan(a) = leg0/leg1 (in pixels)
    pixel_len_mm = (math.cos(alpha) * CAL_MARKER_DISTANCE_MM) / len_leg1                #leg1 (in meter) = cos(a) * opposite (in meter)  


    print(f"Pixel length: f{pixel_len_mm:.9f} mm")

    f = open("calibration.txt", "w")
    f.write(str(pixel_len_mm))
    f.close()
    print("> Calibration saved!")

    
    # cv2.imshow("Calibration", img)
    # cv2.waitKey(0)
    return pixel_len_mm
#----------------------------------------------------------------------
def main():
    img, pos0, pos1 = detectMarker()
    pixel_len = calcPixelLen(img, pos0, pos1)

if __name__ == "__main__":
    main()