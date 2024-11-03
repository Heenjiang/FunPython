def reverse_list(l: list):
    """
    Reverse a list without using any built-in functions.

    The function should return a reversed list.
    Input l is a list which can contain any type of data.
    """
    reversed_list = []

    # Iterate over the original list in reverse order
    for i in range(len(l) - 1, -1, -1):
        reversed_list.append(l[i])

    # Sort the list using Quick Sort manually
    def quick_sort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)

    # Return the reversed list
    return quick_sort(reversed_list)


def solve_sudoku(matrix):
    """
    Write a program to solve a 9x9 Sudoku board.

    The input matrix is a 9x9 matrix. The goal is to fill a 9×9 grid with numbers so that
    each row, column, and 3×3 section contain all of the digits between 1 and 9.
    """
    # Checke if the input is valid or not
    if not (isinstance(matrix, list) and len(matrix) == 9 and all(
            isinstance(row, list) and len(row) == 9 for row in matrix)):
        raise ValueError("Input must be a 9x9 matrix")

    def is_valid(board, row, col, num):
        # Check if the number is not in the current row or column
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        # Determine the starting indices for the 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)

        # Check if the number is not in the current 3x3 box
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False

        # If the number is not found in the row, column, or box, it's valid
        return True

    def solve(board):
        # Iterate through each cell in the 9x9 board
        for row in range(9):
            for col in range(9):
                # If the cell is empty (denoted by 0), try to fill it
                if board[row][col] == 0:
                    # Try each number from 1 to 9
                    for num in range(1, 10):
                        # Check if placing the number is valid
                        if is_valid(board, row, col, num):
                            board[row][col] = num  # Place the number

                            # Recursively try to solve the rest of the board
                            if solve(board):
                                return True

                            # If placing the number didn't lead to a solution, backtrack
                            board[row][col] = 0

                    # If no number is valid, return False to trigger backtracking
                    return False

        return True

    solve(matrix)

    return matrix

matrix = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solved_matrix = solve_sudoku(matrix)
for row in solved_matrix:
    print(row)
