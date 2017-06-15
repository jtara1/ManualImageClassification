class MyCanvas:
    def __init__(self):
        pass

    def _assign_each_category_to_hotkey(self):
        for i in range(len(self.categories)):
            self._window.bind(str(i+1), lambda e, c=self.categories[i]: self._change_category(c))

    def _change_category(self, category):
        print(category)
        self._current_category = category