class Model:
    def __init__(self, game, snake):
        self.game = game
        self.snake = snake
    
    def move_segments(self):
        direction = self.snake._direction
        segments = self.snake._segments
        

        headpos = segments[-1]
        #Remove the former tail position (but save its value)
        self.snake.last_tail_pos = segments[0]
        segments.pop(0)
        #Add the new head position
        if direction == 'w':
            segments.append(headpos - 10)
        elif direction == 'a':
            segments.append(headpos - 1)
        elif direction == 's':
            segments.append(headpos + 10)
        elif direction == 'd':
            segments.append(headpos + 1)
        
        
        print(f'Current direction: {direction}; Segments list: {segments}')

    def get_segments(self):
        return self.snake.segments
    
    def set_segments(self, segments):
        self.snake.segments = segments

    def get_last_tail_pos(self):
        return self.snake.last_tail_pos

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
        self.last_tail_pos = 0
    
    @property
    def direction(self): #This prop is actually useful
        return self._direction
    
    @direction.setter
    def direction(self, value):
        valid_keys = ['w', 'a', 's', 'd']

        #Represents invalid pairs of the desired direction (modeled by the key press) and the current direction of the snake.
        invalids = {'w': 's', 'a': 'd', 
                    's': 'w', 'd': 'a' }
        
        if value not in valid_keys:
            return

        #Snake head can't turn into itself. If you wanted to turn up ('w') but the snake is going down ('s')
        #The snake would be turning into itself, which would be invalid.
        if (value, self._direction) in invalids.items(): #TODO Clean this code, it works, but its roundabout and hard to understand
            return
        
        self._direction = value
        print(f'Valid key called in setter: {value}')



    @property #This prop mostly for testing
    def segments(self):
        return self._segments
    
    @segments.setter
    def segments(self, value):
        self._segments = value
        print(f'Model setter called:  {value}')
        #print(self._segments)