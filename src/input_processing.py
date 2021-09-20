from polymino import GRID_STEP, Grid, Polymino, generate_all_possible_polynominoes

def sortkey(x) -> tuple:
    x = str(x)
    return (len(x), x)

class InputProcessor:
    def __init__(self, input_params: dict) -> None:
        """
        input_params = {"grid_params": [], "rectangles": [], "L": []}
        """
        self.grid = Grid(input_params['grid_params'])
        self.square = input_params['grid_params'][0] * input_params['grid_params'][1]
        self.polyminoes = []
        for element in input_params["rectangles"]:
            for _ in range(element[1]):
                self.square -= element[0][0] * element[0][1]
                assert self.square >= 0, "decrease polyminoes square or increase the grid square"
                self.polyminoes.append(Polymino(element[0], 'RECT'))

        for element in input_params["L"]:
            for _ in range(element[1]):
                self.square -= element[0][0] * element[0][1] - (element[0][0] - 1) * (element[0][1] - 1)
                assert self.square >= 0, "decrease polyminoes square or increase the grid square"
                self.polyminoes.append(Polymino(element[0], 'L'))
        if self.square > 0:
            for _ in range(self.square):
                self.square -= GRID_STEP * GRID_STEP
                self.polyminoes.append(Polymino((None, None), 'HOLE'))
    def print_polyminoes(self) -> None:
        for poly in self.polyminoes:
            print(poly.as_list())

    def process(self) -> tuple:
        """Here is your favourite processing function"""
        polyminoes = list([pol for ind, polymino in enumerate(self.polyminoes) for pol in generate_all_possible_polynominoes([polymino], self.grid, name = str(ind))])
        columns = list(set([element for polymino in polyminoes for element in polymino]))
        columns = sorted(columns, key = sortkey)
        return columns, polyminoes
