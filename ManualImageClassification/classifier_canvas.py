import os
from tkinter import *
from PIL import Image, ImageTk
from queue import LifoQueue
import json
from glob import glob  # grab all files w/ certain extension


class ClassifierCanvas:
    def __init__(self,
                 directory_of_images,
                 categories,
                 output_file_path=os.path.join(os.getcwd(), "img_classifications.json")):
        self.window_size = [1280, 720]
        self.scaled_img_size = self.window_size
        self._window = None  # Tkinter window
        self._scale_ratio = 1  # Multiplier to scale the image to fit the Tk window
        self._second_click = True
        self._rect_coords = []
        self._rect = None
        self._all_rectangles = LifoQueue()  # all rectangles drawn on the canvas

        # dict of str as keys (image_path) mapping to dict of str as keys (category name)
        # mapping to a list of lists of ints (each list is a rect coordinates)
        self.area_data = {}

        self._current_category = categories[0]
        self.categories = categories

        self._image_file_path = os.path.abspath(directory_of_images)
        self._output_file_path = output_file_path

        glob_dir = os.path.join(directory_of_images, "*")  # match every file in the folder
        for img_path in glob(glob_dir):
            if not os.path.isfile(img_path):
                continue
            self._image_file_path = img_path
            self._main()

    def _main(self):
        master = Tk()
        self._window = Canvas(master, width=self.window_size[0], height=self.window_size[1])

        # load image and draw on canvas
        image = Image.open(self._image_file_path)
        self.scaled_img_size = self._fit_img(image.size[0], image.size[1])
        image.thumbnail(size=self.scaled_img_size)
        print("rescaled img to: {}".format(image.size))
        photo = ImageTk.PhotoImage(image=image)

        img_coords = image.size[0] / 2, image.size[1] / 2
        bg_image = self._window.create_image(img_coords[0], img_coords[1], image=photo)
        self._window.pack()

        def on_mouse_click(event):
            print("clicked at {}, {}".format(event.x, event.y))
            self._second_click = not self._second_click
            if not self._second_click:
                self._rect_coords = [event.x, event.y]
                # create guide lines
                self._window.create_line(event.x, 0, event.x, self.window_size[1],
                                         fill="red", dash=(4, 4), tag="guide_line")
                self._window.create_line(0, event.y, self.window_size[0], event.y,
                                         fill="red", dash=(4, 4), tag="guide_line")
            else:
                # delete guide lines
                self._window.delete("guide_line")
                # create rectangle
                self._rect_coords.append(event.x)
                self._rect_coords.append(event.y)
                self._rect = self._window.create_rectangle(self._rect_coords[0],
                                                           self._rect_coords[1],
                                                           self._rect_coords[2],
                                                           self._rect_coords[3],)
                self._all_rectangles.put(self._rect)
                # scale coordinates to represent the same area of the original image (before it was scaled)
                self._add_to_area_data(list(map(lambda x: round(x * (1 / self._scale_ratio)),
                                                self._clamp_coords_and_sort(self._rect_coords))))

        def remove_prev_rect(event):
            """ Rm rect from queue, del drawing on canvas, rm from area_data dict """
            if not self._all_rectangles.empty():
                self._window.delete(self._all_rectangles.get())  # pop newest entry & delete from canvas
            if self._current_category in self.area_data and len(self.area_data[self._current_category]) > 0:
                del self.area_data[self._current_category][-1]
            # rm guide lines in case user was on first click cycle
            self._second_click = True
            self._window.delete("guide_line")

        def save_and_continue(event):
            self._serialize_as_json()
            master.destroy()
            self._clear_image_attributes()
            return

        def save_and_exit():
            self._serialize_as_json()
            master.destroy()
            exit(0)

        master.bind("<Button-1>", on_mouse_click)  # left mouse btn
        master.bind("<Button-3>", remove_prev_rect)  # right mouse btn
        master.bind("<Escape>", save_and_continue)
        self._assign_each_category_to_hotkey()
        master.protocol("WM_DELETE_WINDOW", save_and_exit)
        mainloop()

    def _fit_img(self, w, h):
        """ Get width & height to scale image to to fit window size """
        w2 = w
        h2 = h
        # assumes wind. width > wind. height (most aspect ratios work that way)
        if w > h:
            w2 = self.window_size[0]
            self._scale_ratio = float(w2)/w
            h2 = self._scale_ratio * h
        elif h >= w:
            h2 = self.window_size[1]
            self._scale_ratio = float(h2)/h
            w2 = self._scale_ratio * w
        return w2, h2

    def _clamp_coords_and_sort(self, coords):
        """ Keep the coordinates [x1, y1, x2, y2] within the boundaries of the scaled image """
        for i in range(0, 4, 2):
            coords[i] = max(0, min(coords[i], self.scaled_img_size[0]))
        for i in range(1, 4, 2):
            coords[i] = max(0, min(coords[i], self.scaled_img_size[1]))
        if coords[0] > coords[2]:
            coords[0], coords[2] = coords[2], coords[0]  # swap
        if coords[1] > coords[3]:
            coords[1], coords[3] = coords[3], coords[1]  # swap

        return coords

    def _add_to_area_data(self, coordinates):
        if self._current_category not in self.area_data:
            self.area_data[self._current_category] = [coordinates]
        else:
            self.area_data[self._current_category].append(coordinates)

    def _assign_each_category_to_hotkey(self):
        if len(self.categories) > 9:
            raise ValueError("Does not support more than 9 categories for automatic hotkey mapping")

        for i in range(len(self.categories)):
            self._window.bind(str(i+1), lambda e, c=self.categories[i]: self._change_category(c))

    def _change_category(self, category):
        print(category)
        self._current_category = category

    def _clear_image_attributes(self):
        """ Resets all attributes associated with a specific image """
        self._all_rectangles = LifoQueue()
        self._second_click = True
        self._rect_coords = []
        self.area_data = {}

    def _serialize_as_json(self, overwrite_prev_entry=True):
        if not overwrite_prev_entry:
            raise ValueError("Not implemented yet")

        if not os.path.isfile(self._output_file_path):
            data = {}
        else:
            try:
                data = json.load(open(self._output_file_path, 'r'))
            except json.decoder.JSONDecodeError:  # in case an empty file was found or json was mal-formatted
                data = {}
        data[self._image_file_path] = self.area_data
        json.dump(fp=open(self._output_file_path, 'w'), obj=data)
