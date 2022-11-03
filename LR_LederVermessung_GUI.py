import area_measurement
import calibrate_camera
import operate_camera
import tkinter as tk
from PIL import ImageTk, Image

CAM_WIDTH_PXL           = 4288
CAM_HEIGHT_PXL          = 2848
WINDOW_HEIGHT_PXL       = 800
WINDOW_WIDTH_PXL        = 1000
PICTURE_WIDTH_PXL       = int(CAM_WIDTH_PXL / 5)
PICTURE_HEIGHT_PXL      = int(CAM_HEIGHT_PXL / 5)

LEFT_INTERFACE_EDGE = 69 #pixels
TOP_INTERFACE_EDGE = 30 

class MainApp(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        #self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=6)
        self.grid_columnconfigure(2, weight=3)

        #Picture canvas
        #--------------------------------------------------------------------------------------------------
        canvas_pic = tk.Canvas(parent, width = PICTURE_WIDTH_PXL, height = PICTURE_HEIGHT_PXL, bg = "grey")
        #canvas_pic.place(x = WINDOW_WIDTH_PXL / 2 - PICTURE_WIDTH_PXL / 2, y = WINDOW_HEIGHT_PXL - PICTURE_HEIGHT_PXL - 20, anchor = tk.NW)
        canvas_pic.image = self.prepareImg("data/calibration_pic.jpg")
        canvas_pic.create_image(0, 0, anchor = tk.NW, image = canvas_pic.image)

        #Interface area
        #--------------------------------------------------------------------------------------------------
        canvas_int = tk.Canvas(parent, width = WINDOW_WIDTH_PXL, height = 10)
        #canvas_int.place(x = 0, y = WINDOW_HEIGHT_PXL - PICTURE_HEIGHT_PXL - 40 , anchor = tk.NW)
        self.update()
        print(canvas_int.winfo_height(), canvas_int.winfo_width())
        canvas_int.create_line(40, canvas_int.winfo_height() - 10, canvas_int.winfo_width() - 40, canvas_int.winfo_height() - 10)

        btn_check = tk.Button(parent, text = "Kamera Test", height = 1, width = 17)
        #btn_check.place(x = LEFT_INTERFACE_EDGE, y = TOP_INTERFACE_EDGE, anchor = tk.NW)
        btn_check.grid(column = 0, row = 0, sticky = tk.NW, padx=5, pady=5)

        btn_calibrate = tk.Button(parent, text = "Kamera Kalibrieren", width = 17)
        #btn_calibrate.place(x = LEFT_INTERFACE_EDGE, y = TOP_INTERFACE_EDGE + 40, anchor = tk.NW)
        btn_calibrate.grid(column = 1, row = 0, sticky = tk.NW, padx=5, pady=5)

        btn_measure = tk.Button(parent, text = "Messung Starten", height = 3, width = 17)
        #btn_measure.place(x = LEFT_INTERFACE_EDGE, y = TOP_INTERFACE_EDGE + 80, anchor = tk.NW)
        btn_measure.grid(column = 2, row = 0, sticky = tk.NW, padx=5, pady=5)

        txt_output = tk.Text(parent, height = 8, width = 53)
        txt_output.insert(tk.END, "**************************\n*LR Leder Vermessung - V1*\n**************************")
        #txt_output.place(x = WINDOW_WIDTH_PXL / 2, y = TOP_INTERFACE_EDGE, anchor = tk.NW)
        txt_scrlbar = tk.Scrollbar(parent, command = txt_output.yview)
        #txt_scrlbar.place(x = 700, y = TOP_INTERFACE_EDGE, anchor = tk.NW)
        self.update()

    def prepareImg(self, img_path):
        img = Image.open(img_path)
        resized_image = img.resize((PICTURE_WIDTH_PXL, PICTURE_HEIGHT_PXL), Image.ANTIALIAS)
        new_image= ImageTk.PhotoImage(resized_image)

        return new_image
    

    
def main():
    root = tk.Tk()
    #MainApp(root).pack(side = "top", fill = "both", expand = True)
    #MainApp(root).grid(column = 0, row = 0, sticky = tk.NW)
    root.geometry(f"{WINDOW_WIDTH_PXL}x{WINDOW_HEIGHT_PXL}")
    root.title("LR Leder Vermessung - V0.1")
    mainapp = MainApp(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()

