import os
from tkinter import *
from PIL import Image, ImageTk
from queue import Queue


class MyCanvas:
    def __init__(self, image_file_path):
        self.window_size = [1280, 720]
        self._second_click = True
        self._rect_coords = []
        self._rect = None
        self._all_items = Queue()  # all rectangles drawn on the canvas
        self._image_file_path = image_file_path

        self._main()

    def _main(self):
        master = Tk()
        window = Canvas(master, width=self.window_size[0], height=self.window_size[1])

        # load image and draw on canvas
        image = Image.open(self._image_file_path)
        image.thumbnail(self._fit_img(self.window_size[0], self.window_size[1]))
        print(image.size)
        photo = ImageTk.PhotoImage(image=image)

        img_coords = image.size[0] / 2, image.size[1] / 2
        window.create_image(img_coords[0], img_coords[1], image=photo)
        window.pack()

        def on_mouse_click(event):
            print("clicked at {}, {}".format(event.x, event.y))
            self._second_click = not self._second_click
            if not self._second_click:
                self._rect_coords = [event.x, event.y]
            else:
                self._rect_coords.append(event.x)
                self._rect_coords.append(event.y)
                self._rect = window.create_rectangle(self._rect_coords[0],
                                                     self._rect_coords[1],
                                                     self._rect_coords[2],
                                                     self._rect_coords[3],)
                self._all_items.put(self._rect)

        master.bind("<Button-1>", on_mouse_click)
        # window.create_line(0, 0, 200, 100)
        # window.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
        #
        # window.create_rectangle(50, 25, 150, 75, fill="blue")

        mainloop()

    def _fit_img(self, w, h):
        """ Get width & height to scale image to to fit window size """
        w2 = w
        h2 = h
        # assumes wind. width > wind. height (most aspect ratios work that way)
        if w > h:
            w2 = self.window_size[0]
            ratio = float(w2)/w
            h2 = ratio * h
        elif h >= w:
            h2 = self.window_size[1]
            ratio = float(h2)/h
            w2 = ratio * w
        return w2, h2


if __name__ == "__main__":
    MyCanvas(image_file_path=os.path.join(os.getcwd(), "11.jpg"))
    # MyCanvas(image_file_path="11.jpg")