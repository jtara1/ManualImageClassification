import os
from tkinter import *
from PIL import Image, ImageTk
from queue import Queue
import json


class MyCanvas:
    def __init__(self,
                 image_file_path,
                 categories,
                 output_file_path=os.path.join(os.getcwd(), "img_classifications.json")):
        self.window_size = [1280, 720]
        self._window = None  # Tkinter window
        self._second_click = True
        self._rect_coords = []
        self._rect = None
        self._all_items = Queue()  # all rectangles drawn on the canvas

        self.area_data = {}  # dict of str as keys (category) mapping to list of tuple of int (rectangle coords)
        self._current_category = categories[0]
        self.categories = categories

        self._image_file_path = os.path.abspath(image_file_path)
        self._output_file_path = output_file_path

        self._main()

    def _main(self):
        master = Tk()
        self._window = Canvas(master, width=self.window_size[0], height=self.window_size[1])

        # load image and draw on canvas
        image = Image.open(self._image_file_path)
        image.thumbnail(self._fit_img(self.window_size[0], self.window_size[1]))
        print("rescaled img to: {}".format(image.size))
        photo = ImageTk.PhotoImage(image=image)

        img_coords = image.size[0] / 2, image.size[1] / 2
        self._window.create_image(img_coords[0], img_coords[1], image=photo)
        self._window.pack()

        def on_mouse_click(event):
            print("clicked at {}, {}".format(event.x, event.y))
            self._second_click = not self._second_click
            if not self._second_click:
                self._rect_coords = [event.x, event.y]
            else:
                self._rect_coords.append(event.x)
                self._rect_coords.append(event.y)
                self._rect = self._window.create_rectangle(self._rect_coords[0],
                                                           self._rect_coords[1],
                                                           self._rect_coords[2],
                                                           self._rect_coords[3],)
                self._all_items.put(self._rect)
                self._add_to_area_data(tuple(self._rect_coords))

        def save_and_exit():
            self._serialize_as_json()
            master.destroy()

        master.bind("<Button-1>", on_mouse_click)
        master.protocol("WM_DELETE_WINDOW", save_and_exit)
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

    def _remove_prev_rect(self):
        """ Rm rect from queue, del drawing on canvas, rm from area_data dict """
        if not self._all_items.empty():
            self._window.delete(self._all_items.get())  # pop newest entry & delete from canvas
        if len(self.area_data[self._current_category]) > 0:
            del self.area_data[self._current_category][-1]

    def _add_to_area_data(self, coordinates):
        if self._current_category not in self.area_data:
            self.area_data[self._current_category] = [coordinates]
        else:
            self.area_data[self._current_category].append(coordinates)

    def _serialize_as_json(self, overwrite_prev_entry=True):
        if not overwrite_prev_entry:
            raise ValueError("Not implemented yet")

        if not os.path.isfile(self._output_file_path):
            data = {}
        else:
            data = json.load(open(self._output_file_path, 'r'))
        data[self._image_file_path] = self.area_data
        json.dump(fp=open(self._output_file_path, 'w'), obj=data)


if __name__ == "__main__":
    MyCanvas(image_file_path=os.path.join(os.getcwd(), "11.jpg"),
             categories=['tree', 'monster'])
    # MyCanvas(image_file_path="11.jpg")