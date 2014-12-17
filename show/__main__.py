import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout


class MainView(AnchorLayout):
    pass


class Funamagama(App):
    def build(self):
        main_view = MainView()
        return main_view


if __name__ == "__main__":
    Funamagama().run()
