#TODO -- controller stuff here
import logging
from kivy.clock import Clock

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class Controller: #might want to create different classes for different controllers, for now, im just gonna have one for the whole app, b/c the only screen that really needs it is #2
    def __init__(self, title_view, game_view, gameover_view, model):
        self.title = title_view
        self.game_view = game_view
        self.gameover_view = gameover_view
        self.model = model

        handler = self.game_view.grid.handler
        #Bound callbacks are stored as weak references in kv, making them open to garbage collection without a direct reference to the function object.
        #Without a reference, calling dispatch() in this method fires the model setter, but calling dipatch elsewhere the application does nothing (b/c the callback was garbage collected)
        #See https://kivy.org/doc/stable/api-kivy.event.html
        handler.callbacks.append(self.update_segments)
        handler.bind(on_segments_updated=self.update_segments)
        handler.callbacks.append(self.set_direction) # Could probably condense these appends
        handler.bind(on_key_pressed=self.set_direction)
        handler.callbacks.append(self.start_game)
        handler.bind(on_key_first_pressed=self.start_game)



    def start_game(self, instance):
        self.model.start_game()
        print('Bad!')
        handler = self.game_view.grid.handler
        handler.unbind(on_key_first_pressed=None) #BUG -- thing isnt unbinding itself
        #handler.callbacks.remove(self.start_game)

    def set_direction(self, instance, key):
        self.model.set_direction(key)

    def update_segments(self, instance): 
        segments = self.game_view.grid.get_segments()
        self.model.set_segments(segments) 

   