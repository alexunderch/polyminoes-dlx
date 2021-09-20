import sys
sys.path.append('./src/')
from src.input_processing import InputProcessor, sortkey
from src.dlx import DLX

def main():
    # input_params = {"grid_params": (3, 5), "rectangles": [((2, 2), 1)], "L": [((3, 2), 1), ((2, 2), 2)]} #True
    # input_params = {"grid_params": (3, 5), "rectangles": [], "L": [((3, 3), 3)]} #False
    # input_params = {"grid_params": (14, 14), "rectangles": [((1, 1), 3)], "L": []} #True
    
    proc = InputProcessor(input_params)
    cover = DLX(*proc.process())
    print("Solution exists: {}".format(cover(return_solutions = False, key = sortkey)))

if __name__ == "__main__":
    main()