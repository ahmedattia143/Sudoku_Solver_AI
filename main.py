from SudokuPreprocess import SudokuPreprocess
from SudokuSolver import SudokuSolver
import sys 
import cv2 as cv 
import matplotlib.pyplot as plt

if __name__ == "__main__":
    #read sudoku image 
    image = cv.imread(sys.argv[1])

    #preprocess the image 
    sp = SudokuPreprocess(image)
    matrix = sp.get_sudoku_matrix()

    #solve the sudoku 
    sv = SudokuSolver(matrix)
    sv.solve_array()
    result = sv.get_matrix()
    
    #print the result
    print(result)

    