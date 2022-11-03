import cv2
import imutils
import subprocess

CAM_PIXEL_WIDTH = 4288
CAM_PIXEL_HEIGHT = 2848

#pkill -f gphoto2
#----------------------------------------------------------------------
def callShellCmd(command_arr):
    process = subprocess.Popen(command_arr,
        stdout = subprocess.PIPE)

    return process.communicate()[0].decode()
#----------------------------------------------------------------------
def takePicture(file_name):

    capture_rtn = callShellCmd([
        "gphoto2",
        "--capture-image-and-download",
        "--filename", "/home/louis/projects/leather_area/data/" + file_name + ".jpg",
        "--force-overwrite"])

    #resize image to minimize future processing time
    img = cv2.imread("data/" + file_name + ".jpg")
    img = imutils.resize(img, width = int(CAM_PIXEL_WIDTH / 2))
    cv2.imwrite("data/" + file_name + ".jpg", img)

    print(capture_rtn)
#----------------------------------------------------------------------
def killProcesses():
    kill_rtn = callShellCmd(["pkill", "gphoto2"])

    if kill_rtn == "": 
        return True
    else:
        return False
#----------------------------------------------------------------------
def checkCamera():
    detect_rtn = callShellCmd([
        "gphoto2", "--auto-detect"])

    if "Nikon DSC D90" in detect_rtn:
        print("> Camera successfully detected!")
        return True
    else:
        print("Couldn't find any Camera. Please check the USB connection and if the camera is turned on! ")
        return False

if __name__ == "__main__":
    killProcesses()
    if checkCamera():
        takePicture("test")