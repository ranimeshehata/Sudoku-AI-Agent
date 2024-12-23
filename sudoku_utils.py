def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))

def is_valid_move(board, row, col, num):
    if num in board[row]:   # Check same row
        return False
    
    if num in [board[i][col] for i in range(9)]:    # Check same column
        return False
    
    subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)   # Check same subgrid
    for i in range(subgrid_row, subgrid_row + 3):
        for j in range(subgrid_col, subgrid_col + 3):
            if board[i][j] == num:
                return False
    return True

def is_empty_cell(board):    # finds next empty cell with minimum remaining values MRV
    min_remaining_values = float('inf')
    selected_cell = None
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                remaining_values = len(get_domain_values(board, i, j))
                if remaining_values < min_remaining_values:
                    min_remaining_values = remaining_values
                    selected_cell = (i, j)
    return selected_cell

def get_domain_values(board, row, col):
    domain_values = [num for num in range(1, 10) if is_valid_move(board, row, col, num)]
    return domain_values

def is_valid_sudoku(board):
    def is_valid_row(board, row):
        is_found = set()
        for num in board[row]:
            if num != 0:
                if num in is_found:
                    return False
                is_found.add(num)
        return True

    def is_valid_column(board, col):
        seen = set()
        for row in range(9):
            num = board[row][col]
            if num != 0:
                if num in seen:
                    return False
                seen.add(num)
        return True

    def is_valid_subgrid(board, start_row, start_col):
        seen = set()
        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                num = board[row][col]
                if num != 0:
                    if num in seen:
                        return False
                    seen.add(num)
        return True

    for i in range(9):
        if not is_valid_row(board, i) or not is_valid_column(board, i):
            return False

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            if not is_valid_subgrid(board, i, j):
                return False

    return True

# def is_initial_state_valid(board):
#     if not is_valid_sudoku(board):
#         print("The initial state of the Sudoku puzzle is not valid.")
#         return False
#     return True 

def get_filled_cells_range(difficulty):
    if difficulty == "Easy":
        return 36, 45
    elif difficulty == "Moderate":
        return 27, 35
    elif difficulty == "Hard":
        return 17, 26
    else:
        return 0, 81 


