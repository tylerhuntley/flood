import random
from functools import partial
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, ListProperty
from kivy.core.window import Window

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
        

<Board>:



''')


rgb = {'red':(1,0,0), 'green':(0,1,0), 'blue':(0,0,1)}
text = {'red':'r', 'green':'g', 'blue':'b'}
colors = ('red', 'green', 'blue')
size = 7

class Tile(Widget):
    color = ListProperty([1,1,1])
    def __init__(self, x, y, init_color, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.flipped = False
        self.color = rgb[init_color]
        self.coords = (x, y)
        self.adjacent = [(x+1,y), (x,y+1), (x-1,y), (x,y-1)]
##        with self.canvas:
##            Label(text=str(self.pos))
##            Color(*self.color, mode='rgb')
##            Rectangle(pos=(x*100,y*100), size=self.size)


    def flip(self, new_color, _):
        print("Flipping: ", new_color)
        self.flipped = True
        self.old_color = self.color
        self.color = new_color
        for tile in self.adjacent:
##            if tile in board.tiles.keys():
##            try:
                if all([board.tiles[tile].flipped == False,
                        board.tiles[tile].color == self.old_color,
                        board.tiles[tile].color != new_color]):            
                    board.tiles[tile].flip(new_color, _)
                    print("Good flip")
##            except:
##                continue
                    
                

class Board(GridLayout):
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.cols = 7
        self.tiles = {}
        for x in range(size):
            for y in range(size):
                self.tiles[(x,y)] = Tile(x, y, random.choice(colors))#, width=50, height=50)
                self.add_widget(self.tiles[(x,y)])

    def change_color(self, new_color):
        self.tiles[(0,0)].flip(new_color)

##    def update(self):
##        for x in range(size):            
##            for y in range(size):
##                print(text[board.tiles[(x,y)].color] + ' ', end='')
##                board.tiles[(x,y)].flipped = False
##            print()



##class Game(Widget):
##    def __init__(self, **kwargs):
##        super(Game, self).__init__(**kwargs)
##        board = Board()
##        self.update



class App(App):
    
    def build(self):
        parent = BoxLayout(orientation='vertical')
        board = Board()
        parent.add_widget(board)
        
##        buttons = BoxLayout()
##        but1 = Button(text='Red')
##        but1.bind(on_release= partial(board.tiles[(0,0)].flip, 'red'))
##        but2 = Button(text='Green')
##        but2.bind(on_release= partial(board.tiles[(0,0)].flip, 'green'))
##        but3 = Button(text='Blue')
##        but3.bind(on_release= partial(board.tiles[(0,0)].flip, 'blue'))
##        for but in (but1, but2, but3):
##            buttons.add_widget(but)
##        parent.add_widget(buttons)
        
##        for x in range(size):
##            board.add_widget(Button())
##            for y in range(size):
##                board.tiles[(x,y)] = Tile(x, y, random.choice(colors))
##                board.add_widget(board.tiles[(x,y)])
        return parent

##board = Board()
app = App()
app.run()


##while True:
##    game.update()
##    new_color = input("Flip to color: ")
##    board.change_color(new_color)
