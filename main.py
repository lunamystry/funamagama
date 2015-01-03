import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.uix.button import Button

from generate import Grid


class Tile(Button):
    selected = BooleanProperty()

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.selected = True


class GridView(AnchorLayout):
    grid = ObjectProperty()

    def __init__(self, data, **kwargs):
        super(GridView, self).__init__(**kwargs)
        self.reset_grid(data)
        self.selected = []

    def reset_grid(self, data):
        self.grid.clear_widgets()
        self.grid.rows = len(data)
        self.grid.cols = len(data[0])

        for row in data:
            for letter in row:
                self.grid.add_widget(Tile(text=str(letter)))


class Funamagama(App):
    def build(self):
        grid = Grid(20, 20)
        grid.place(*['leonard',
                     'mandla',
                     'phoebie',
                     'book',
                     'classic',
                     'homecoming',
                     'breast',
                     'sibling',
                     'war',
                     'sand',
                     'diary',
                     'door',
                     'cocky',
                     'perfect',
                     'nothing',
                     'coven'])
        mainview = GridView(grid._grid)
        return mainview


if __name__ == "__main__":
    Funamagama().run()
