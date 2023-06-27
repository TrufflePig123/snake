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
        segments = set(self.snake._segments) #Def a better way to do this, but idc
        all_positions = set(range(grid_size))
        valid_spawns = all_positions.difference(segments)

        fruitpos = r.choice(list(valid_spawns))
        self.set_fruit_pos(fruitpos)
        
        return fruitpos
    
    def get_new_segment_pos(self):
        segments = self.snake._segments
        tail = segments[0]
        second_to_last = segments [1]

        if second_to_last - tail == 10:
            return tail - 10
        elif second_to_last - tail == -10:
            return tail + 10
        elif second_to_last - tail == 1:
            return tail - 1
        elif second_to_last - tail == -1:
            return tail + 1
    
    def add_score(self):
        self.game.score += 1

    def get_score(self):
        return self.game.score

    def get_segments(self):
        return self.snake._segments
    
    def set_segments(self, segments):
        self.snake._segments = segments

    def get_last_tail_pos(self):
        return self.snake.last_tail_pos
    
    def get_direction(self):
        return self.snake.direction

    def set_direction(self, direction):
        self.snake._direction = direction

    def get_fruit_pos(self):
        return self.game.fruit_pos
    
    def set_fruit_pos(self, pos):
        self.game.fruit_pos = pos
    

#------Data classes begin here------

class Game:
    def __init__(self): 
        self.score = 0
        self.game_started = False
        self.fruit_pos = None
        
    def get_game_state(self):
        return self.game_started
    
    def set_game_state(self, value):
        self.game_started = value
    
    


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

