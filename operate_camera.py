from tabnanny import check
import cv2
import subprocess

#pkill -f gphoto2

def callShellCmd(command_arr):
    process = subprocess.Popen(command_arr,
        stdout = subprocess.PIPE)

    return process.communicate()[0].decode()

def takePicture(file_name):

    capture_rtn = callShellCmd([
        "gphoto2",
        "--capture-image-and-download",
        "--filename", "/home/louis/projects/leather_area/data/" + file_name + ".jpg",
        "--force-overwrite"])

    print(capture_rtn)

def killProcesses():
    kill_rtn = callShellCmd(["pkill", "gphoto2"])

    if kill_rtn == "": 
        return True
    else:
        return False

def checkCamera():
    detect_rtn = callShellCmd([
        "gphoto2", "--auto-detect"])

    if "Nikon DSC D90" in detect_rtn:
        print("> Camera successfully detected!")
        return True
    else:
        print("Couldn't find any Camera. Please check the USB connection and if the camera is turned on! ")
        return False
# def checkCamera():
#     process = subprocess.Popen([
#         "gphoto2",
#         "--capture-image-and-download",
#         "--filename", "/home/louis/projects/leather_area/data/camera_output.jpg"],
#         stdout = subprocess.PIPE)

#     rtn_str = process.communicate()[0]
#     print(rtn_str)

# #----------------------------------------------------------------------
# def takePicture():
#     cv2.namedWindow("Vorschau")
#     cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#     cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#     cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#     if cam.isOpened(): 
#         rval, frame = cam.read()
#     else:
#         rval = False

#     while rval:
#         cv2.imshow("Preview", frame)
#         rval, frame = cam.read()

#         #check if a key is pressed
#         key = cv2.waitKey(20)
#         if key == 27:           #ESC
#             break
#         elif key == 32:         #Spacebar
#             img_name = "camera_output.png"
#             cv2.imwrite("data/" + img_name, frame)
#             print("> Picture taken sucessfully!")
#             break

#     cv2.destroyWindow("Preview")
#     cam.release()

if __name__ == "__main__":
    killProcesses()
    if checkCamera():
        takePicture()