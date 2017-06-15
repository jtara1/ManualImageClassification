from tkinter import *


class MyCanvas:
    def __init__(self,
                 categories):
        self.categories = categories
        self._current_category = categories[0]
        self._window = None

        self._main()

    def _main(self):
        master = Tk()
        self._window = Canvas(master, width=200, height=100)
        self._window.pack()

        self._assign_each_category_to_hotkey()
        mainloop()

    def _assign_each_category_to_hotkey(self):
        for i in range(len(self.categories)):
            self._window.bind(str(i+1), lambda e, c=self.categories[i]: self._change_category(c))

    def _change_category(self, category):
        print(category)
        self._current_category = category


if __name__ == "__main__":
    MyCanvas(categories=['tree', 'monster'])
