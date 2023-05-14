
#TODO -- model stuff here

class Model:
    def __init__(self, game, snake):
        self.game = game
        self.snake = snake

#Data classes begin here

class Game:
    def __init__(self): 
        self.score = 0


class Snake:
    def __init__(self):
        self.head_pos = 0
        self.direction = 'D'
        self.segments = [32, 33]
