import area_measurement
import calibrate_camera
import operate_camera

if operate_camera.killProcesses():
    if operate_camera.checkCamera():
        while True:
            try:
                operate_camera.takePicture("calibration_pic")
                img, pos0, pos1 = calibrate_camera.detectMarker()
                break
            except UnboundLocalError as err:
                print("Calibration failed!", err)
                input("Press enter to continue...")

        pixel_len = calibrate_camera.calcPixelLen(img, pos0, pos1)
        operate_camera.takePicture("measurement_pic")
        area_measurement.startCalc()

