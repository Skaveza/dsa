import os

class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=0, numCols=0):
        if matrixFilePath:
            self.numRows, self.numCols, self.elements = self.read_matrix_from_file(matrixFilePath)
        else:
            self.numRows = numRows
            self.numCols = numCols
            self.elements = {}

    def read_matrix_from_file(self, filePath):
        with open(filePath, 'r') as file:
            lines = file.readlines()
            numRows = int(lines[0].split('=')[1])
            numCols = int(lines[1].split('=')[1])
            elements = {}
            for line in lines[2:]:
                row, col, value = map(int, line.strip()[1:-1].split(','))
                elements[(row, col)] = value
        return numRows, numCols, elements

    def get_element(self, row, col):
        return self.elements.get((row, col), 0)

    def set_element(self, row, col, value):
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)]

    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions do not match for addition.")
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for key in set(self.elements.keys()).union(other.elements.keys()):
            result.set_element(*key, self.get_element(*key) + other.get_element(*key))
        return result

    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions do not match for subtraction.")
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for key in set(self.elements.keys()).union(other.elements.keys()):
            result.set_element(*key, self.get_element(*key) - other.get_element(*key))
        return result

    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrix dimensions do not match for multiplication.")
        result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)
        for (i, k), v in self.elements.items():
            for j in range(other.numCols):
                result.set_element(i, j, result.get_element(i, j) + v * other.get_element(k, j))
        return result

# Usage example
if __name__ == "__main__":
    # Correct relative paths
    matrix1_path = os.path.join(os.path.dirname(__file__), '..', 'sample_inputs', 'sample_input_for_students', 'easy_sample_02_1.txt')
    matrix2_path = os.path.join(os.path.dirname(__file__), '..', 'sample_inputs', 'sample_input_for_students', 'easy_sample_02_2.txt')

    matrix1 = SparseMatrix(matrix1_path)
    matrix2 = SparseMatrix(matrix2_path)

    # Print matrix dimensions for debugging
    print(f"Matrix 1: {matrix1.numRows}x{matrix1.numCols}")
    print(f"Matrix 2: {matrix2.numRows}x{matrix2.numCols}")

    added_matrix = matrix1.add(matrix2)
    subtracted_matrix = matrix1.subtract(matrix2)

    print("Addition result:", added_matrix.elements)
    print("Subtraction result:", subtracted_matrix.elements)

    # Check multiplication compatibility before attempting to multiply
    multiplied_matrix = None
    if matrix1.numCols == matrix2.numRows:
        multiplied_matrix = matrix1.multiply(matrix2)
        print("Multiplication result:", multiplied_matrix.elements)
    else:
        print("Matrix dimensions do not match for multiplication.")
