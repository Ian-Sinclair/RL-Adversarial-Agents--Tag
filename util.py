from math import inf
import numpy as np

class k_quad_tree() :
    def __init__(self, game,  center : tuple, k = 2, min_xy = None, max_xy = None ) :
        x,y = center
        self.c_x , self.c_y = x,y
        if min_xy == None :
            min_xy = (0,0)
        if max_xy == None :
            max_xy = game.size
        x_min, y_min = min_xy
        x_max,y_max = max_xy
        self.min_xy = min_xy
        self.max_xy = max_xy
        self.k = k
        self.data = {
            'data' : None,
            'rank' : inf
        }
        self.children = {}
        if self.k > 0 :
            self.children = {
                (-1,-1) : k_quad_tree(game, ( ( x_min + x)/2 , (y_min + y)/2 )  , k = self.k-1 , min_xy=(x_min,y_min), max_xy=(x,y)) ,
                (-1,1) : k_quad_tree(game, ( (x_min +x) / 2 , y + (abs( y_max - y ) / 2) ) , k = self.k-1 , min_xy=(x_min,y), max_xy=(x,y_max)   ) ,
                (1,-1) : k_quad_tree(game, (  x+ ( abs( x_max-x )/2 )  ,  (y_min + y)/2 )  , k = self.k-1 , min_xy=(x,y_min) , max_xy=(x_max,y)) ,
                (1,1) : k_quad_tree(game, ( x+ (abs( x_max-x )/2 ) , y+(abs( y_max-y )/2) )  , k = self.k-1 , min_xy=(x,y), max_xy=(x_max,y_max))
            }
        else : 
            self.data = { 'data' : game.default_objects[0].symbol.copy(), 'rank' : -2 }

    def add_data(self, game , position : tuple , value = None, rank = None) :
        if self.k > 0 :
            x,y = position
            mod_x , mod_y = -1, -1
            if x >= self.c_x :
                mod_x = 1
            if y >= self.c_y :
                mod_y = 1
            key = (mod_x,mod_y)
            self.children[key].add_data(game, position, value = value, rank = rank)
        else :
            if value == None:
                self.data = self.hierarchySelection(game , position)
            else :
                self.data = {'data' : value, 'rank' : rank}

    def update_data(self, game,  new_pos : tuple, old_pos : tuple, rank) :
        self.add_data(game, old_pos, value = tuple(game.emptySpace.symbol), rank= -1 )
        self.add_data(game , new_pos, value=tuple('A',), rank = rank)
        return self


    def hierarchySelection(self , game , position) :
        hierarchy = {
            -2 : [tuple(s) for s in game.default_symbols],
            -1 : [tuple(game.emptySpace.symbol)]
        }
        x,y = position
        symb = tuple(game.grid[x][y].copy())
        for r,symbols in hierarchy.items() :
            if symb in symbols :
                if r >= self.data['rank'] :
                    return { 'data' : tuple(symb), 'rank' : r }
                else : 
                    return self.data
        return { 'data' : tuple(symb), 'rank' : 0 }
        
    def print_data(self) :
        print(self.extract_data())

    def get_centers(self, out = [] ) :
        out += [(self.c_x , self.c_y)]
        for tree in self.children.values() :
            tree.get_centers(out)
        return out
    
    def get_rect(self, out = []) :
        out += [{
            'center' : (self.c_x, self.c_y),
            'min_xy' : self.min_xy,
            'max_xy' : self.max_xy
        }]
        for tree in self.children.values() :
            tree.get_rect(out)
        return out


    def extract_data(self) :
        if self.k > 0 :
            A = tuple([tree.extract_data() for tree in self.children.values()])
            if np.ndim(A) > 1 :
                A = tuple(np.concatenate(A).flat)
            return A
        else : return str(self.data['rank'])



def test1() :
    import GUI
    from game import game as game_
    game = game_(size=(20,20), walls_prob=0.2, fillFunc='uniformGrid')
    game.print_game()
    k_tree = k_quad_tree(game, (10,10), k=3)
    play = GUI.GUI(game)
    play.demo_tree(game, k_tree.get_rect())
    for i in range(game.size[0]) :
        for j in range(game.size[1]) :
            k_tree.add_data(game,(i,j))
    k_tree.print_data()


if __name__ == "__main__":
    test1()

