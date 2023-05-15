#TODO -- controller stuff here

class Controller: #might want to create different classes for different controllers, for now, im just gonna have one for the whole app, b/c the only screen that really needs it is #2
    def __init__(self, title_view, game_view, gameover_view, model):
        self.title = title_view
        self.game_view = game_view
        self.gameover_view = gameover_view
        self.model = model

    def update_segments(self): #We want to update the model segments in here, binded to some sort of event in kv
        self.model.set_segments([33]) #Placeholder value

    def update_snake(self): #We want to notify the view of the new segments her
        segments = self.model.get_segments()
        self.game_view.segments = segments