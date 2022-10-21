import area_measurement
import calibrate_camera
import operate_camera

operate_camera.takePicture()
img, pos0, pos1 = calibrate_camera.detectMarker()
pixel_len = calibrate_camera.calcPixelLen(img, pos0, pos1)
