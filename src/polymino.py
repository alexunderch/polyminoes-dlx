from copy import deepcopy
from typing import _SpecialForm
from dlx import DLX

GRID_STEP = 1

class Polymino: 

    def __init__(self, size: tuple, poly_type: str):

        NAMES = ['RECT', 'L', 'HOLE']

        self.size = size
        self.name = poly_type
        assert poly_type in NAMES, "no other types implemented"
        
        m, n = size
        if self.name == "RECT":
            self.coords = [(i, j) for i in range(0, m + 1, GRID_STEP) for j in range(0, n + 1, GRID_STEP)]
        elif self.name == "L":
            self.coords = sorted([(0, j) for j in range(0, n + 1, GRID_STEP)] + [(GRID_STEP, j) for j in range(GRID_STEP, n + 1, GRID_STEP)] + \
                  [(i, 0) for i in range(GRID_STEP, m + 1, GRID_STEP)] + [(i, GRID_STEP) for i in range(GRID_STEP + 1, m + 1, GRID_STEP)])
        elif self.name == "HOLE":
            self.coords = [(0,0), (0, GRID_STEP), (GRID_STEP, 0), (GRID_STEP, GRID_STEP)]
        self.min_i, self.min_j = map(min, *self.coords)
        self.max_i, self.max_j = map(max, *self.coords)
        
    def get_size(self) -> list:
        return list(*self.size)

    def as_list(self) -> list:
        return [self.name] + self.coords

    def get_coords(self) -> list:
        return self.coords
    
    def get_boundaries(self) -> list:
        return [self.min_i, self.max_i, self.min_j, self.max_j]

    def update_boundaries(self, coords):
        self.min_i, self.min_j = map(min, *coords)
        self.max_i, self.max_j = map(max, *coords)
    
    def relative_shift(self, delta_x: int, delta_y: int) -> None:
        #deprecated
        self.min_i += delta_x
        self.max_i += delta_x
        self.min_j += delta_y
        self.max_j += delta_y

        self.coords = [(i + delta_x, j + delta_y) for i, j in self.coords]

    def absolute_shift(self, x_0: int, y_0: int) -> None:
        
        self.coords = [(i - self.min_i + x_0, j - self.min_j + y_0) for i, j in self.coords]
        self.max_i += x_0 - self.min_i
        self.max_j += y_0 - self.min_j
        self.min_i = x_0
        self.min_j = y_0

    def rotate_90(self) -> None:
        
        old_min_i, old_min_j =  self.min_i, self.min_j
        self.coords = sorted([(-j, i) for i, j in self.coords])
        self.min_i, self.max_i, self.min_j, self.max_j = -self.max_j, -self.min_j, self.min_i, self.max_i

        self.absolute_shift(old_min_i, old_min_j)

    def __eq__(self, other) -> bool:
        if isinstance(other, Polymino): return (self.name, self.coords) == (other.name, other.coords)
        return False

    def __hash__(self):
        return hash(tuple(self.as_list()))


class Grid:
    def __init__(self, size: tuple):
        m, n = size
        self.size= size
        self.polyminoes = list()
        self.coords = [(i, j) for i in range(0, m + 1, GRID_STEP) for j in range(0, n + 1, GRID_STEP)]
        self.min_i, self.max_i = 0, m 
        self.min_j, self.max_j = 0, n

        self.cells = [[(i, j) for i in range(I, I + 2, GRID_STEP) for j in range(J, J + 2, GRID_STEP)]for I in range(m) for J in range(n)]    


    def get_boundaries(self) -> list:
        return [self.min_i, self.max_i, self.min_j, self.max_j]

    def is_valid_pos(self, polymino: Polymino) -> bool:
        set_polymino = set(polymino.coords)

        if set_polymino.intersection(self.coords) != set_polymino: return False


        for poly in self.polyminoes:
            if set_polymino.intersection(poly.coords): return False

        return True

    def add_polymino(self, polymino: Polymino) -> bool:
        if self.is_valid_pos(polymino = polymino): 
            self.polyminoes.append(polymino)
            return True
        return False



def generate_all_possible_polynominoes(polyminoes: list, grid: Grid, name: str = ''):
    def generate_all_rotations(polyminoes: list):
        for polymino in polyminoes:
            for i in range(4):
                yield deepcopy(polymino)
                polymino.rotate_90()

    for polymino in set(generate_all_rotations(polyminoes)):     
        for i in range(grid.min_i, grid.min_i + grid.size[0], GRID_STEP):
            for j in range(grid.min_j, grid.min_j + grid.size[1], GRID_STEP):
                polymino.absolute_shift(i, j)
                if grid.is_valid_pos(polymino): 
                    yield convert_representation(deepcopy(polymino), grid.cells, name = name)



def convert_representation(polymino: Polymino, representation: dict, name = '') -> list:
    """converts a catesian representation to given, associated with grid cells"""
    set_coords = set(polymino.get_coords())
    result = []
    for ind, repr in enumerate(representation):
        if set(repr).issubset(set_coords): result.append(ind)
    return [polymino.name + name] + result

    


# def make_experiment(): 
    
#     print()
#     cover = DLX(columns, polyminoes)
#     print("Solutions: \n", cover(key = sortkey))
# if __name__ == '__main__':
#     make_experiment()


    #     
    # print(polyminoes.as_list())
    # polyminoes.rotate_90()
    # print(polyminoes.as_list())
    # polyminoes.rotate_90()
    # print(polyminoes.as_list())
    # polyminoes.rotate_90()
    # print(polyminoes.as_list())
    # polyminoes.rotate_90()
    # print(polyminoes.as_list())
    # polyminoes.rotate_90()