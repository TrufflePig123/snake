from controller import Controller
from model import Model
from kivy.app import App
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen , ScreenManager, NoTransition
from kivy.uix.widget import Widget

class SnakeApp(App):
    '''Kivy base application class. Initalizes the model, view, and controller during application startup. Acts as application entry point.

    Attributes
    ----------
    sm: SnakeScreenManager
        ScreenManager that handles inter-view navigation.

    Methods
    --------
    main():
        Instantiates both the model and the controller using the views created in the setup_views method.
    setup_views():
        Creates instances of each of the application screens and of the application ScreenManager.
    build():
        Built-in kivy method to setup the application root widget. See kivy docs for info: https://kivy.org/doc/stable/api-kivy.app.html        
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = None

    def main(self): # might rename
        '''Instantiates both the model and the controller using the views created in the setup_views method.'''
        sm = self.sm
        model = Model()
        controller = Controller(sm.title, sm.game_view, sm.gameover_view, model)
       
    def setup_views(self):
        '''Creates instances of each of the application screens and of the application screenmanager.'''
        title_view = TitleView(name='TitleView')
        game_view = GameView(name='GameView')
        gameover_view = GameOverView(name='GameOverView')

        self.sm = SnakeScreenManager(title_view, game_view, gameover_view)

    def build(self):
        '''Built-in kivy method to setup the application root widget. See kivy docs for info: https://kivy.org/doc/stable/api-kivy.app.html   '''
        self.setup_views()
        self.main()
        return self.sm


class SnakeScreenManager(ScreenManager):
    '''Application ScreenManager that handles inter-view navigation.
    
    Attributes
    ----------
    title: TitleView
        Starting screen of the application; first screen the user interacts with. Contains buttons to start the game and exit the application.
    game_view: GameView
        Screen where the game actually takes place.
    gameover_view: GameOverView
        Screen that appears upon a loss. Displays the user's total score and prompts them to either return to the menu or play again.

    Methods
    -------
    add_screens():
        Adds the individual screen widgets into the ScreenManager's knowledge-base.
    '''

    def __init__(self, title_view, game_view, gameover_view, **kwargs):
        super().__init__(**kwargs)
        self.transition = NoTransition()

        self.title = title_view
        self.game_view = game_view
        self.gameover_view = gameover_view

        self.add_screens()

    def add_screens(self):
        '''Adds the individual screen widgets into the ScreenManager's knowledge-base.'''

        self.add_widget(self.title)
        self.add_widget(self.game_view)
        self.add_widget(self.gameover_view)


class TitleView(Screen):
    '''Starting screen of the application; first screen the user interacts with. Contains buttons to start the game and exit the application.'''


class GameView(Screen):
    '''Screen where the game actually takes place.'''


class GameOverView(Screen):
    '''Screen that appears upon a loss. Displays the user's total score and prompts them to either return to the menu or play again.'''


class GameGrid(GridLayout): #Gridlayout? look for other layouts to test and stuff
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 10
        self.cols = 10

        for i in range(self.rows*self.cols):
            self.add_widget(self.create_cell())
    
    def create_cell(self): #might be better to export into a different class
        return GridCell()


class GridCell(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(1, 0, 0) #TODO -- fix color
            self.rect = Rectangle(pos=self.pos, size=self.size)

        with self.canvas:
            Color(0, 0, 0) # TODO -- fix color
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=2)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
    def update_rect(self, instance, value):
        '''Method to ensure that the drawn rectangle + border reacts to changes in size and position. Code stolen from https://kivy.org/doc/stable/guide/widgets.html#adding-widget-background
        
        Parameters
        ----------
        instance: Widget
            The widget that owns the drawn rectangle
        value: float
            Represents the rectangle's new size/position values. Required param acessed via Kivy behind-the-scenes magic. 
            More info here: https://kivy.org/doc/stable/api-kivy.event.html
        '''
        
        instance.rect.pos = instance.pos 
        instance.rect.size = instance.size
        #Also update size/pos of the border.
        instance.border.rectangle = (self.x, self.y, self.width, self.height)
    

            
            




#Can't place a direct call to main here. For the class rules defined in kv to reflect on the screens,
#The screen objects need to be instantiated once (and only once) the application loop is already running.
if __name__ == '__main__':
    SnakeApp().run()
    