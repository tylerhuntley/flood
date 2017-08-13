import random
from functools import partial
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.animation import Animation


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


rgb = {'red': (1, 0, 0, 1), 'green': (0, 1, 0, 1), 'blue': (0, 0, 1, 1), 'purple': (1, 0, 1, 1)}
colors = ('red', 'green', 'blue', 'purple')
grid_size = 20


class Tile(Widget):
    color = ListProperty([0, 0, 0, 0])
    points = ListProperty([0, 0, 0, 0, 0, 0, 0, 0])
    
    def __init__(self, board, posx, posy, init_color, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.board = board
        self.color = rgb[init_color]
        (self.posx, self.posy) = (posx, posy)
        self.adjacent = [(posx+1, posy), (posx, posy+1), (posx-1, posy), (posx, posy-1)]
        for tile in self.adjacent[:]:
            if not (tile[0] in range(grid_size) and tile[1] in range(grid_size)):
                self.adjacent.remove(tile)
        self.bind(size=self.align)
    def align(self, *args):
        self.x1, self.y1 = self.pos
        self.x2, self.y2 = self.x1+self.width, self.y1+self.height
        self.x3, self.y3 = self.x1+self.width/2, self.y1+15
        self.y4 = self.y1+self.height+15
        self.points = [self.x1, self.y1, self.x2, self.y1, self.x2, self.y2, self.x1, self.y2]

    @property
    def xy(self):
        return self.posx, self.posy

    def get_color(self):
        return tuple(self.color)

    def get_adj(self):
        temp = []
        for coords in self.adjacent:
            temp.append(self.board.tile(*coords))
        return temp

    def remove_adj(self, coords):
        if coords in self.adjacent:
            self.adjacent.remove(coords)

    def flip(self, new_color):
        offset = 5
        anim = Animation(pos=(self.x-offset, self.y+offset), d=.1, points=(
                         self.x3, self.y3, self.x3, self.y1,
                         self.x3, self.y2, self.x3, self.y4))
        # Swap the corners, to maintain original positions after the flip
        anim += Animation(color=new_color, d=0, points=(
                         self.x3, self.y1, self.x3, self.y3,
                         self.x3, self.y4, self.x3, self.y2))
        anim += Animation(pos=(self.x, self.y), d=.1, points=(
                         self.x1, self.y1, self.x2, self.y1,
                         self.x2, self.y2, self.x1, self.y2))
        anim.start(self)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.board.click(self.get_color())


class Panel(BoxLayout):
    def __init__(self, board, **kwargs):
        super(Panel, self).__init__(**kwargs)
        self.padding = 50
        self.spacing = 5
        for color in rgb:
            but = PanelButton(bg_color=rgb[color], board=board)
            self.add_widget(but)


class PanelButton(Button):
    def __init__(self, bg_color, board, **kwargs):
        super(PanelButton, self).__init__(**kwargs)
        self.background_color = bg_color
        # self.on_release = partial(board.tiles[(0,0)].recolor, bg_color)
        self.on_release = partial(board.click, bg_color)


class Board(GridLayout):
    def __init__(self, **kwargs):
        super(Board, self).__init__(padding=50, spacing=2, cols=grid_size, **kwargs)
        self.tiles = {}
        for x in range(grid_size):
            for y in range(grid_size):
                self.tiles[(x, y)] = Tile(self, x, y, random.choice(colors))
                self.add_widget(self.tiles[(x, y)])
        self.pool = {self.tile(0, 0)}
        # self.border = set(self.linked_tiles(self.tile(0, 0)))
        self.expand_pool()

    def click(self, btn_color):
        self.expand_pool(btn_color)
        for tile in self.pool:
            tile.flip(btn_color)

    def tile(self, x, y):
        return self.tiles[(x, y)]

    # def expand_pool_alt(self, color):
    #     """Adds all adjacent matching tiles to the pool, and updates the new border"""
    #     flag = True
    #     current = self.tile(0, 0).color
    #     while flag:
    #         flag = False
    #         for tile in self.border:
    #             if tile.color == current:
    #                 self.pool.add(tile)
    #                 self.border.update(tile.get_adj())
    #                 self.border.remove(tile)
    #                 flag = True

    def expand_pool(self, color=None):
        """Updates pool with all contiguous, matching tiles
        side-effect: deletes adjacent pointers from Tile() objects"""
        temp = list(self.pool)
        if not color:
            color = temp[0].get_color()
        for root in temp:
            for adj in root.get_adj():
                if adj.get_color() == color:
                    temp.append(adj)
                    adj.remove_adj(root.xy)
                    root.remove_adj(adj.xy)
        self.pool.update(temp)


class App(App):
    def build(self):
        parent = BoxLayout(orientation='vertical')
        board = Board(size_hint=(1,3))
        parent.add_widget(board)
        parent.add_widget(Panel(board))
        return parent
        

if __name__ == '__main__':
    app = App()
    app.run()
