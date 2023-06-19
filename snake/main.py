from controller import Controller
from model import Model, Game, Snake
from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.graphics import Color, Rectangle, Line
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen , ScreenManager, NoTransition
from kivy.uix.widget import Widget
from kivy.core.window import Window
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class SnakeApp(App):
    '''Kivy base application class. Initalizes the model, views, and controller during application startup. Acts as application entry point.

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
        model = Model(Game(), Snake())
        controller = Controller(sm, model)
       
    def setup_views(self):
        '''Creates instances of each of the application screens (as well as relevant widgets) and of the application screenmanager.'''
        title_view = TitleView(name='TitleView')
        #Setting size_hint to None to reset relative positioning (otherwise absolute size won't work)
        grid = GameGrid(size_hint=(None, None), size=(600, 600), handler=GridEventHandler())
        game_view = GameView(name='GameView', grid=grid)
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
    '''Screen where the game actually takes place. Handles keyboard input from the user.'''
    def __init__(self, grid, **kwargs):
        super().__init__(**kwargs)
        self.grid = grid
        #Add the grid to the AnchorLayout defined in kvlang
        self.ids.anchor.add_widget(self.grid)
        #Only request the keyboard when we navigate into this view. 
        self.bind(on_pre_enter=self.get_keyboard) 
        self.bind(on_pre_leave=self._keyboard_closed)
    
    def get_keyboard(self, instance):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self, instance=None): #Todo -- doc why instance is none
        '''Removes the keyboard upon exiting the application or the GameView screen.
        Params:
        -------
        instance: GameView
            Refers to self, the current GameView. Set as a default for error prevention (make these docs better).
        '''
        if self._keyboard != None:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        #Kivy docs: "The function collects all the positional and keyword arguments and passes them on to the handlers."
        #See https://kivy.org/doc/stable/api-kivy.event.html for more info
        handler = self.grid.handler
        
        handler.dispatch('on_key_first_pressed')
        handler.dispatch('on_key_pressed', text)



class GameOverView(Screen):
    '''Screen that appears upon a loss. Displays the user's total score and prompts them to either return to the menu or play again.'''


class GridEventHandler(EventDispatcher): 
    '''Defines and handles custom events for the GameGrid.'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.callbacks = []

        self.clock_cycle = None
        self.register_event_type('on_segments_updated')
        self.register_event_type('on_key_first_pressed')
        self.register_event_type('on_key_pressed')
        self.register_event_type('on_move')
        self.register_event_type('on_loss')

    def on_segments_updated(self, *args):
        pass

    def on_key_first_pressed(self, *args): #Fires only after the key is pressed for the first time, and no more after that.
        pass
        #self.clock_cycle = Clock.schedule_interval(self.dispatch_game_events, 0.5)
        #self.unregister_event_type('on_key_first_pressed') #BUG -- when the user LOSES... this is permanently unbinded, so this should really be a trigger so it calls once, but can be reused later
        #TODO This might be better modeled by binding this fn to a trigger (or something that calls once), rather than this hackish solution
    
    def on_key_pressed(self, *args):
        pass
    
    def dispatch_game_events(self, dt): #FIXME -- this is named kinda badly
        '''Acts as the main loop for a variety of game events. Repeatedly dispatches events for movement and collisons.'''
        self.dispatch('on_move')
    
    def on_move(self, *args):
        pass

    def on_loss(self, *args):
        pass


class GameGrid(GridLayout): 
    '''Represents the main board where the game wil be played. Displays key information about the game, such as
    location of the snake and location of food.''' #finish docs bc yk

    segments = ListProperty() #Whenever food is eaten, fire event to update this and model

    def __init__(self, handler, **kwargs):
        super().__init__(**kwargs)
        self.handler = handler
        self.rows = 10
        self.cols = 10

        #Add cells to the board
        for i in range(self.rows*self.cols):
            self.add_widget(self.create_cell())
        
        #Initialize the snake
        self.segments = [51, 52, 53]#TODO-- change me back to 3, and in the model too

    def create_cell(self): 
        return GridCell() #Violates DI, unfortunately
    
    def get_segments(self):
        return self.segments
    
    def set_segments(self, segments):
        self.segments = segments
    
    def remove_segment(self, index):
        '''Restores the given cell to its graphical default, removing any drawn segments or food.'''
        cells = self.children[::-1]
        rect = (80/255, 140/255, 164/255)
        border = (145/255, 174/255, 193/255)
        #Calling draw cell here, but passing in the default colors.
        cells[index].draw_cell(rect, border)

    def on_segments(self, instance, new_segments): 
        '''Draws new segments on the grid whenever the segments property is modified.'''
        #print(f'New segment at {new_segments}') # Testing statement
        cells = self.children[::-1] #TODO = Add explination for reversing list here

        rect = (10/255, 135/255, 84/255)
        border = (145/255, 174/255, 193/255)

        for i in new_segments:
            cells[i].draw_cell(rect, border)

        self.handler.dispatch('on_segments_updated') #TODO This could just bind to the on segments property, but idrk
        
                    

class GridCell(Widget):
    '''Graphical representation of an individual cell. Consists of a rectangle and a line (for drawing the border).'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rect = (80/255, 140/255, 164/255)
        border = (145/255, 174/255, 193/255)
        self.draw_cell(rect, border)

        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def draw_cell(self, rect_rgb, border_rgb):
        #Before we draw, get rid of any double-draw mistakes by clearing the canvas.
        self.canvas.clear()

        r, g, b = rect_rgb
        with self.canvas:
            Color(r, g, b) #TODO -- fix color
            self.rect = Rectangle(pos=self.pos, size=self.size)

        r, g, b = border_rgb
        with self.canvas:
            Color(r, g, b) # TODO -- fix color
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=2)

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
    