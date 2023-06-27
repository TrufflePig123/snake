import logging
import random as r
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
        
        handler.bind(on_segments_updated=self.update_segments)
        handler.bind(on_key_pressed=self.set_direction)
        handler.bind(on_key_first_pressed=self.start_movement_loop)
        #Because the user is constantly changing direction, we need to make sure we check for collisions only in the instant, with as little delays as possible.
        handler.bind(on_move=self.check_collision)
        handler.bind(on_move=self.check_fruit_eaten)
        handler.bind(on_move=self.update_segment_positions) #TODO: for the future, please cut down on these events,  
        handler.bind(on_loss=self.reset_on_loss)
        handler.bind(on_loss=self.change_view_on_loss)

        handler.bind(on_fruit_eaten=self.update_score)
        handler.bind(on_fruit_eaten=self.add_snake_segment)
        handler.bind(on_fruit_eaten=self.spawn_fruit) 
       
        #Bound callbacks are stored as weak references in kv, making them open to garbage collection without a direct reference to the function objects.
        #Storing them in a list counts as a reference, so the events trigger as normal.
        #See https://kivy.org/doc/stable/api-kivy.event.html
        cbs = [self.add_snake_segment, self.check_collision, self.check_fruit_eaten, self.spawn_fruit, self.change_view_on_loss, self.reset_on_loss, self.update_segment_positions, 
               self.set_direction, self.start_movement_loop, self.update_score, self.update_segments]

        handler.callbacks.extend(cbs)
    
    
    
    def start_movement_loop(self, instance):
        handler = self.game_view.grid.handler
        game_started = self.model.game.get_game_state()

        if not game_started:
            self.spawn_fruit()
            handler.clock_cycle = Clock.schedule_interval(handler.dispatch_game_events, 0.2)
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

    def spawn_fruit(self, instance=None):
        spawn = self.model.get_valid_fruit_pos(self.game_view.grid.rows**2)
        self.game_view.grid.draw_fruit(spawn)
    
    def check_fruit_eaten(self, instance):
        fruitpos = self.model.get_fruit_pos()
        segments = self.model.get_segments()

        #If the head touches the fruit
        if fruitpos == segments[-1]:
            self.game_view.grid.handler.dispatch('on_fruit_eaten')

    def update_score(self, instance):
        self.model.add_score() #might be better somewhere else but whatev
        score = self.model.get_score()
        self.game_view.counter.set_score(score)

            
    def add_snake_segment(self, instance):
        segments = self.model.get_segments()
        new_segment = self.model.get_new_segment_pos()

        segments.insert(0, new_segment)
        self.model.set_segments(segments)

    def check_collision(self, instance):
        '''Checks to see if the current snake position would classify as a collision, either with the grid boundary or with itself.'''
        segments = self.model.get_segments()
        direction = self.model.get_direction()
        snake_collided = self.model.check_collision(segments, direction)

        if snake_collided:
            self.game_view.grid.handler.dispatch('on_loss')

    def change_view_on_loss(self, instance):
        score = self.model.get_score()
        self.gameover_view.set_score(score)
        self.sm.current = 'GameOverView'
        

    def reset_on_loss(self, instance):
        self.game_view.grid.handler.clock_cycle.cancel() #Terminate the movement loop

        segments = self.model.get_segments()
        grid = self.game_view.grid

        #Because the snake can technically go out of bounds before it collides, we need to filter invalid indeces before passing it to related functions.
        clean_segments = [x for x in segments if x < (grid.rows * grid.cols)]
        #Clear the grid
        for i in clean_segments:
            grid.remove_segment(i)
        
        #Clear fruit from the last game
        fruit = self.model.get_fruit_pos()
        grid.remove_segment(fruit)
        #Reset to a new snake
        self.model.set_segments([51, 52, 53])
        grid.set_segments([51, 52, 53])
        
        self.model.set_direction('d')
        self.model.game.set_game_state(False) #TODO -- need to remove fruit too, might just be better to clear the whole board and draw a new snake or sum
        

   