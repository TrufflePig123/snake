
class Game:
    def __init__(self): # class is kinda small, could export to new module
        self.score = 0


class Snake:
    def __init__(self):
        self.head_pos = 0
        self.direction = 'D'
        self.segment_ids = []
