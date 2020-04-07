# Sudoku Solver using artifidial intelligence 
## Inspiration 
Being a fan of the famous sudoku game, I had the idea to create a program that solves a sudoku puzzle taking as input the puzzle image


## Dependencies
-   python 3.7
-   tensorflow v2.1.0
-   keras 
-   openCV 4.2.0.32

## Usage 
```bash
python main.py "path_to_image"
```

Example:

<img src = "/test_images/sudoku7.jpg" width="250" height="250"/>   <img src="/screenshot1.png" width="250" height="250" /> 

## Files : 
- main.py : main python file that will run the program on sudoku images as described in usage.

- SudokuSolver.py : python class that contains all the logic of solving sudoku puzzle using backtracking.

- SudokuPreprocess.py : python class that contains all the methods needed to extract the sudoku puzzle from an image 
and convert it to a 2d array using the model trained.

- sudoku preprocess.ipynb : python notebook that contain an exampel showing all the steps of image preprocessing from 
finding conours to converting the puzzle image to a 2d array.

- model.ipynb : python notebook to train a convolution neural network on numbers images. 

- dataset : folder that contains all the images used to train the model , images were collected by me from internet.

- model : folder that contains the model trained.

- test_images : images of sudoku puzzle to test on the program . 






