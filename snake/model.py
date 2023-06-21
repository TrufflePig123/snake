import random as r

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

    def check_collision(self, segments, direction):
        #'Neck' here refers to the second segment (right next to the head).
        headpos, neckpos = abs(segments[-1]), abs(segments[-2])

        #Break if the 2 segments are in the same position
        if len(segments) != len(set(segments)): 
            print('\033[91m' + 'Break Game!' + '\033[0m')
            return True
        #As the snake moves up, its given position in the is decreasing. 
        #So the only way the head's position can suddenly increase is if it hits the top and circles back around (which would be a loss).
        if direction == 'w' and headpos < neckpos: #Dirty, could def simplify with DRY
            return 
        elif direction == 's' and headpos > neckpos: 
            return 
        #The Grid's first row goes from 0-9, the second from 10-19, etc. So if the snake is moving right (direction = 'd')
        #The snake's head cannot reach the first column of the board with ids ending in 0. If it does, then it's a collision.
        elif direction == 'd' and  headpos % 10 != 0: #These ifs are a crime against humanity, but it izz what it izz #FIXME, im lazy, but it might be better to extract thr rows and cols from the view here
            return 
        elif direction == 'a' and  headpos % 10 != 9: #Opposite direction, so here going from say, 20 to 19 is the red flag
            return
        else:
            print('\033[91m' + 'Break Game!' + '\033[0m')
            return True
        
    def get_valid_fruit_pos(self, grid_size):
        segments = set(self.snake.segments) #Def a better way to do this, but idc
        all_positions = set(range(grid_size))
        valid_spawns = all_positions.difference(segments)
        
        return r.choice(list(valid_spawns))

    def get_segments(self):
        return self.snake.segments
    
    def set_segments(self, segments):
        self.snake.segments = segments

    def get_last_tail_pos(self):
        return self.snake.last_tail_pos
    
    def get_direction(self):
        return self.snake.direction

    def set_direction(self, direction):
        self.snake.direction = direction

    

#------Data classes begin here------

class Game:
    def __init__(self): 
        self.score = 0
        self.game_started = False
        
    def set_game_state(self, value):
        self.game_started = value

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
        #print(f'Valid key called in setter: {value}')



    @property #This prop mostly for testing
    def segments(self):
        return self._segments
    
    @segments.setter
    def segments(self, value):
        self._segments = value
        #print(f'Model setter called:  {value}')
        #print(self._segments)