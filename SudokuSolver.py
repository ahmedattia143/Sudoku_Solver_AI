

class SudokuSolver:
    
    def __init__(self,matrix):
        self.matrix = matrix
        
    #this function find an empty cell, return indices of the cell  
    def find_empty_grid(self,matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 0:
                    return (i, j)  #return row, col
        return None
    
    #this function checks the constraints
    def possible(self,matrix, num, pos):
        for i in range(len(matrix[0])):
            if matrix[pos[0]][i] == num and pos[1] != i:
                return False
        for i in range(len(matrix)):
            if matrix[i][pos[1]] == num and pos[0] != i:
                return False
            
        x0 = (pos[1] // 3)*3
        y0 = (pos[0] // 3)*3
        for i in range(y0, y0+ 3):
            for j in range(x0, x0 + 3):
                if matrix[i][j] == num and (i,j) != pos:
                    return False
        return True
    
    def solve_array(self):
        find = self.find_empty_grid(self.matrix) #find the empty spaces
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if self.possible(self.matrix, i, (row, col)): #check the constraints
                self.matrix[row][col] = i

                if self.solve_array():
                    return True

                self.matrix[row][col] = 0

        return False
    
    def get_matrix(self):
        return self.matrix