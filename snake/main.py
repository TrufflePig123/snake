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
from kivy.core.window import Window

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


class GameView(Screen): #TODO -- give this boy a direct reference to its GameGrid (probably through an objprop)
    '''Screen where the game actually takes place. Handles keyboard input from the user.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Only request the keyboard when we navigate into this view. 
        self.bind(on_pre_enter=self.get_keyboard)
    
    def get_keyboard(self, value):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(f"The key {text} was pressed") #dummy testing code for now
    

class GameOverView(Screen):
    '''Screen that appears upon a loss. Displays the user's total score and prompts them to either return to the menu or play again.'''


class GameGrid(GridLayout): #Gridlayout? look for other layouts to test and stuff
    '''Represents the main board where the game wil be played. Displays key information about the game, such as
    location of the snake and location of food, and responds to the input''' #finish docs bc yk

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 10
        self.cols = 10

        #Add cells to the board
        for i in range(self.rows*self.cols):
            self.add_widget(self.create_cell())
    
    def create_cell(self): 
        return GridCell()
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(f"The key {text} was pressed")
    

class GridCell(Widget):
    '''Graphical representation of an individual cell. Consists of a rectangle and a line (for drawing the border).'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(80/255, 140/255, 164/255) #TODO -- fix color
            self.rect = Rectangle(pos=self.pos, size=self.size)

        with self.canvas:
            Color(145/255, 174/255, 193/255) # TODO -- fix color
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

        instance.border.rectangle = (self.x, self.y, self.width, self.height)
    

#Can't place a direct call to main here. For the class rules defined in kv to reflect on the screens,
#The screen objects need to be instantiated once (and only once) the application loop is already running.
if __name__ == '__main__':
    SnakeApp().run()
    