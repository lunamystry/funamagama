import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line

from random import random

from generate import Grid


class Tile(Button):
    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.selected.append(self)


class GridView(GridLayout):

    def reset(self, data):
        self.clear_widgets()
        self.rows = len(data)
        self.cols = len(data[0])
        self.selected = []

        for row in data:
            for letter in row:
                self.add_widget(Tile(text=str(letter)))

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            color = (random(), random(), random(), 0.5)
            with self.canvas:
                Color(*color, mode='rgb')
                width = 10.
                self.start = [touch.x, touch.y]
                self.end = self.start
                touch.ud['line'] = Line(points=self.start, width=width)

    def on_touch_move(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.end = [touch.x, touch.y]
        touch.ud['line'].points = self.start + self.end


class MainView(AnchorLayout):
    grid = ObjectProperty()

    def __init__(self, data, **kwargs):
        super(MainView, self).__init__(**kwargs)
        self.grid.reset(data)


class Funamagama(App):
    def build(self):
        grid = Grid(5, 5)
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
        mainview = MainView(grid._grid)
        return mainview


if __name__ == "__main__":
    Funamagama().run()
