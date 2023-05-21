from kivy.clock import Clock
#TODO -- model stuff here

class Model:
    def __init__(self, game, snake):
        self.game = game
        self.snake = snake

    def start_game(self):
        started = self.game.game_started = True
        if started:
            Clock.schedule_interval(self.test, 0.5)
    
    def test(self, dt):
        pass
        print('Start-game callback called')

    def get_segments(self):
        return self.snake.segments
    
    def set_segments(self, segments):
        self.snake.segments = segments

    def set_direction(self, direction):
        self.snake.direction = direction

    

#------Data classes begin here------

class Game:
    def __init__(self): 
        self.score = 0
        self.game_started = False
    
    def get_game_state(self):
        return self.game_started


class Snake:
    def __init__(self):
        self._head_pos = 0
        self._direction = 'd'
        self._segments = [51, 52, 53]
    
    @property
    def direction(self): #This prop is actually useful
        return self._direction
    
    @direction.setter
    def direction(self, value):
        valid_keys = ['w', 'a', 's', 'd']
        if value in valid_keys:
            self._direction = value
            print(f'Valid key called in setter: {value}')



    @property #This prop mostly for testing
    def segments(self):
        return self._segments
    
    @segments.setter
    def segments(self, value):
        self._segments = value
        #print(f'Model setter called:  {value}')
        #print(self._segments)