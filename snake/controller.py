#TODO -- controller stuff here
import logging
from kivy.clock import Clock

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class Controller: #might want to create different classes for different controllers, for now, im just gonna have one for the whole app, b/c the only screen that really needs it is #2
    def __init__(self, screenmanager, model):
        self.sm = screenmanager
        self.title = self.sm.title
        self.game_view = self.sm.game_view
        self.gameover_view = self.sm.gameover_view
        self.model = model

        handler = self.game_view.grid.handler
        #Bound callbacks are stored as weak references in kv, making them open to garbage collection without a direct reference to the function object.
        #Without a reference, calling dispatch() in this method fires the model setter, but calling dipatch elsewhere the application does nothing (b/c the callback was garbage collected)
        #See https://kivy.org/doc/stable/api-kivy.event.html
        handler.callbacks.append(self.update_segments)
        handler.bind(on_segments_updated=self.update_segments)
        handler.callbacks.append(self.set_direction) 
        handler.bind(on_key_pressed=self.set_direction)
        handler.callbacks.append(self.start_movement_loop)
        handler.bind(on_key_first_pressed=self.start_movement_loop)
        
        #Because the user is constantly changing direction, we need to make sure we check for collisions only in the instant, with as little delays as possible.
        handler.bind(on_move=self.check_collision)
        handler.bind(on_move=self.update_segment_positions)
        
        #TODO -- this might be simplified better, maybe by appending all callbacks in one
        handler.callbacks.append(self.check_collision)
        handler.callbacks.append(self.update_segment_positions)
    
    def check_collision(self, instance):
        '''Checks to see if the current snake position would classify as a collision, either with the grid boundary or with itself.'''
        segments = self.model.get_segments()
        direction = self.model.get_direction()
        snake_collided = self.model.game.check_collision(segments, direction)

        if snake_collided:
            self.change_view_on_loss()
            self.reset_on_loss()
    
    def start_movement_loop(self, instance):
        handler = self.game_view.grid.handler
        game_started = self.model.game.get_game_state()


        if not game_started:
            handler.clock_cycle = Clock.schedule_interval(handler.dispatch_game_events, 0.5)
            self.model.game.set_game_state(True)
        
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

    def change_view_on_loss(self):
        self.sm.current = 'GameOverView'
        self.game_view.grid.handler.clock_cycle.cancel() #Terminate the movement loop

    def reset_on_loss(self):
        segments = self.model.get_segments()
        grid = self.game_view.grid
        #Clear the grid
        for i in segments:
            grid.remove_segment(i)

        #Reset to a new snake
        self.model.set_segments([51, 52, 53])
        grid.set_segments([51, 52, 53])
        self.model.game.set_game_state(False)
        

   