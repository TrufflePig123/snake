from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import Screen

class SnakeApp(App):
    pass


class TitleView(Screen):
    pass


class GameView(Screen):
    pass


class GameOverView(Screen):
    pass


class GameGrid(StackLayout):
    pass

if __name__ == '__main__':
    SnakeApp().run()