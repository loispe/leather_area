import area_measurement
import calibrate_camera
import operate_camera
import lp_functions


ask_newPic = lp_functions.yesOrNo("Do you want to take a new picture?", default = "Yes")
if ask_newPic:
    if operate_camera.killProcesses():
        if operate_camera.checkCamera():

            ask_calibrate = lp_functions.yesOrNo("Do you want do calibrate the camera?")
            if ask_calibrate:

                while True:
                    try:
                        operate_camera.takePicture("calibration_pic")
                        img, pos0, pos1 = calibrate_camera.detectMarker()
                        pixel_len = calibrate_camera.calcPixelLen(img, pos0, pos1)
                        break
                    except UnboundLocalError as err:
                        print("Calibration failed!", err)
                        input("Press enter to try again...")

            operate_camera.takePicture("measurement_pic")

area_measurement.startCalc()

