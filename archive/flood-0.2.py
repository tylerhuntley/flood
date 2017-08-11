import random
from functools import partial
from kivy.app import App
from kivy.lang import Builder
##from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, ListProperty
from kivy.core.window import Window
from kivy.animation import Animation
from time import sleep

Builder.load_string('''
#:kivy 1.10.0
<Tile>:
    canvas:
        Color:
            rgb: self.color
        Rectangle:
            size: self.size
            pos: self.pos
    Label:
        center: self.parent.center
        text: str(round(self.pos[0]))+', '+ str(round(self.pos[1]))

<PanelButton>:
    canvas:
        Color:
            rgb: self.background_color
        Rectangle:
            size: self.width-10, self.height-10
            pos: self.x+5, self.y+5
''')

rgb = {'red':(1,0,0,1), 'green':(0,1,0,1), 'blue':(0,0,1,1), 'purp':(1,0,1,1)}
colors = ('red', 'green', 'blue', 'purp')
grid_size = 7

class Tile(Widget):
    color = ListProperty([1,1,1,1])
    def __init__(self, parent, x, y, init_color, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.flipped = False
        self.color = rgb[init_color]
        self.coords = (x, y)
        self.adjacent = [(x+1,y), (x,y+1), (x-1,y), (x,y-1)]
        for tile in self.adjacent[:]:
            if not (tile[0] in range(grid_size) and tile[1] in range(grid_size)):
                self.adjacent.remove(tile)

    def recolor(self, new_color, *args):
        self.flipped = True
        self.old_color = self.color
        self.color = new_color
        for tile in self.adjacent:
            if (self.parent.tiles[tile].flipped == False and
                (self.parent.tiles[tile].color == self.old_color or                    
                 self.parent.tiles[tile].color == new_color)):
                    self.parent.tiles[tile].recolor(new_color, *args)
##                self.parent.tiles[tile].flip(self.parent.tiles[tile])
                    
        self.flipped = False
        self.flip(self)

    def flip(self, instance):
        original_pos, offset = self.pos[:], 5
        anim = Animation(pos=(self.x-offset, self.y+offset), d=0.05)
        anim+= Animation(pos=(self.x, self.y), d=0.05)
        anim.start(instance)

    def animate(self, board, inst):
        to_flip = []
        to_flip.append(self)
        for tile in self.adjacent:
            if board.tiles[tile].color == self.color:
                to_flip.append(board.tiles[tile])
        

    def on_touch_down(self, touch):
        pass

class Panel(BoxLayout):
    def __init__(self, board, **kwargs):
        super(Panel, self).__init__(**kwargs)
        self.padding = 50
        self.spacing = 5
        for color in rgb:
            but = PanelButton(bg_color=rgb[color], board=board)
            self.add_widget(but)
##            but.on_release = partial(board.tiles[(0,0)].recolor, rgb[i])            

class PanelButton(Button):
    def __init__(self, bg_color, board, **kwargs):
        super(PanelButton, self).__init__(**kwargs)
        self.background_color = bg_color
        self.on_release = partial(board.tiles[(0,0)].recolor, bg_color)

class Board(GridLayout):
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.padding = 50
        self.spacing = 2
        self.cols = 7
        self.tiles = {(0,0):None}
        for x in range(grid_size):
            for y in range(grid_size):
                self.tiles[(x,y)] = Tile(self, x, y, random.choice(colors))
                self.add_widget(self.tiles[(x,y)])

    def change_color(self, new_color):
        self.tiles[(0,0)].recolor(new_color)

class App(App):    
    def build(self):
        parent = BoxLayout(orientation='vertical')
        board = Board()
        parent.add_widget(board)
        parent.add_widget(Panel(board))
        return parent
    
##        buttons = BoxLayout(size_hint=(1,0.3))
##        but1 = Button(text='Red')
##        but1.bind(on_release= partial(board.tiles[(0,0)].recolor, 'red'))
##        but2 = Button(text='Green')
##        but2.bind(on_release= partial(board.tiles[(0,0)].recolor, 'green'))
##        but3 = Button(text='Blue')
##        but3.bind(on_release= partial(board.tiles[(0,0)].recolor, 'blue'))
##        for but in (but1, but2, but3):
##            buttons.add_widget(but)
##        parent.add_widget(buttons)

        
        
        

if __name__ == '__main__':
    app = App()
    app.run()


