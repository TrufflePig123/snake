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
        handler.callbacks.append(self.update_segment_positions)
        handler.bind(on_move=self.update_segment_positions)
    
    def update_segment_positions(self, instance):
        '''Passes the value of the post-movement snake segments to the GameView.'''
        self.model.move_segments()
        segments = self.model.get_segments()
        self.game_view.grid.set_segments(segments)

        lastpos = self.model.get_last_tail_pos()
        self.game_view.grid.remove_segment(lastpos)
    
    def set_direction(self, instance, key):
        self.model.set_direction(key)


    #Old thing, check
    def update_segments(self, instance): #FIXME This should take from model and put into view
        segments = self.game_view.grid.get_segments()
        self.model.set_segments(segments) 

   