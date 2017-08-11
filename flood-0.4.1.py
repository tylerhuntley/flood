import random
from functools import partial
from kivy.app import App
from kivy.lang import Builder
#from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
#from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, ListProperty, NumericProperty, ReferenceListProperty
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from time import sleep

##    self.qx1,self.qy1,self.qx2,self.qy2,self.qx3,self.qy3,self.qx4,self.qy4

Builder.load_string('''
#:kivy 1.10.0
<Tile>:
    canvas:
        Color:
            rgb: self.color
        Quad:
            points: self.points

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
    color = ListProperty([0,0,0,0])
    points = ListProperty([0,0,0,0,0,0,0,0])
    
    def __init__(self, parent, posx, posy, init_color, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.flipped = False
        self.color = rgb[init_color]
        self.coords = (posx, posy)
        self.adjacent = [(posx+1,posy), (posx,posy+1), (posx-1,posy), (posx,posy-1)]
        for tile in self.adjacent[:]:
            if not (tile[0] in range(grid_size) and tile[1] in range(grid_size)):
                self.adjacent.remove(tile)
#        self.bind(size=self.align)
        Clock.schedule_once(self.align, 1)

    def align(self, *args):
        self.x1, self.y1 = self.pos
        self.x2, self.y2 = self.x1+self.width, self.y1+self.height
        self.x3, self.y3 = self.x1+self.width/2, self.y1+15
        self.y4 = self.y1+self.height+15
        self.points = [self.x1,self.y1, self.x2,self.y1, self.x2,self.y2, self.x1,self.y2]

    def recolor(self, new_color, *args):
        self.flipped = True
        self.old_color = self.color
        self.new_color = new_color
        for tile in self.adjacent:
            if (self.parent.tiles[tile].flipped is False and
                (self.parent.tiles[tile].color == self.old_color or
                 self.parent.tiles[tile].color == new_color)):
                    self.parent.tiles[tile].recolor(new_color, *args)
               # self.parent.tiles[tile].flip(self.parent.tiles[tile])

        self.flipped = False
        self.flip(self)

    def flip(self, instance):
        offset = 5
        anim = Animation(pos=(self.x-offset, self.y+offset), d=.1, points=(
                         self.x3, self.y3, self.x3, self.y1,
                         self.x3, self.y2, self.x3, self.y4))
        #Swap the corners, to maintain original positions after the flip
        anim+= Animation(color=self.new_color, d=0, points=(
                         self.x3, self.y1, self.x3, self.y3,
                         self.x3, self.y4, self.x3, self.y2))
        anim+= Animation(pos=(self.x, self.y), d=.1, points=(
                         self.x1, self.y1, self.x2, self.y1,
                         self.x2, self.y2, self.x1, self.y2))

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
        self.rooted, self.frontier = [], []
        self.tiles = {}
        for x in range(grid_size):
            for y in range(grid_size):
                self.tiles[(x,y)] = Tile(self, x, y, random.choice(colors))
                self.tiles[(x,y)].pos = self.tiles[(x,y)].pos
                self.add_widget(self.tiles[(x,y)])                

    def change_color(self, new_color):
        self.tiles[(0,0)].recolor(new_color)

    def search(self, x=0, y=0):
        pass

class App(App):    
    def build(self):
        parent = BoxLayout(orientation='vertical')
        board = Board(size_hint=(1,3))
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


