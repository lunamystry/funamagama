import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button

from generate import Grid


class MainView(AnchorLayout):
    grid = ObjectProperty()

    def reset_grid(self, data):
        self.grid.clear_widgets()
        self.grid.rows = len(data)
        self.grid.cols = len(data[0])

        for row in range(0, self.grid.rows):
            for col in range(0, self.grid.cols):
                self.grid.add_widget(Button(text=str(data[row][col])))


class Funamagama(App):
    def build(self):
        main_view = MainView()
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
        main_view.reset_grid(grid._grid)
        return main_view


if __name__ == "__main__":
    Funamagama().run()
