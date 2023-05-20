
#TODO -- model stuff here

class Model:
    def __init__(self, game, snake):
        self.game = game
        self.snake = snake

    def get_segments(self):
        return self.snake.segments
    
    def set_segments(self, segments):
        self.snake.segments = segments

    

#Data classes begin here

class Game:
    def __init__(self): 
        self.score = 0


class Snake:
    def __init__(self):
        self.head_pos = 0
        self.direction = 'D'
        self._segments = [51, 52, 53]
    
    @property #These properties mostly for testin'
    def segments(self):
        return self._segments
    
    @segments.setter
    def segments(self, value):
        self._segments = value
        print(f'Model setter called:  {value}')
        print(self._segments)