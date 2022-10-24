import cv2
import time

#----------------------------------------------------------------------
def takePicture():
    cv2.namedWindow("Vorschau")
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if cam.isOpened(): 
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow("Preview", frame)
        rval, frame = cam.read()

        #check if a key is pressed
        key = cv2.waitKey(20)
        if key == 27:           #ESC
            break
        elif key == 32:         #Spacebar
            img_name = "camera_output.png"
            cv2.imwrite("data/" + img_name, frame)
            print("> Picture taken sucessfully!")
            break

    cv2.destroyWindow("Preview")
    cam.release()

if __name__ == "__main__":
    takePicture()