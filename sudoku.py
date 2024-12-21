import numpy as np
import logging
import copy
from sudoku_utils import get_filled_cells_range, is_valid_move, is_empty_cell

logging.basicConfig(filename='sudoku_agent.log', level=logging.INFO, format='%(message)s', filemode='w')

def backtracking(board):
    empty_cell = is_empty_cell(board)
    print(f"MRV is {empty_cell}")
    if empty_cell is None:
        return True

    row, col = empty_cell
    domain_values = get_domain_values(board, row, col)
    domain_values.sort(key=lambda num: count_constrained_values(board, row, col, num))

    print(f"Attempting to fill cell ({row}, {col}) with domain values: {domain_values}")
    logging.info(f"Attempting to fill cell ({row}, {col}) with domain values: {domain_values}")


    for num in domain_values:
        print(f"Trying value {num} for cell ({row}, {col})")
        logging.info(f"Trying value {num} for cell ({row}, {col})")
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            print("Applying forward checking")
            logging.info("Applying forward checking")
            if apply_arc_consistency(board) is not None:
                print("Forward checking successful")
                logging.info("Forward checking successful")
                if backtracking(board):
                    return True

            print(f"Value {num} for cell ({row}, {col}) leads to conflict. Backtracking...")
            logging.info(f"Value {num} for cell ({row}, {col}) leads to conflict. Backtracking...")
            board[row][col] = 0
        else:
            print(f"Value {num} is not valid for cell ({row}, {col}). Skipping...")
            logging.info(f"Value {num} is not valid for cell ({row}, {col}). Skipping...") 

    print(f"No valid value found for cell ({row}, {col}). Backtracking...")
    logging.info(f"No valid value found for cell ({row}, {col}). Backtracking...")
    return False


def get_domain_values(board, row, col):
    domain_values = [num for num in range(1, 10) if is_valid_move(board, row, col, num)]
    return domain_values

def count_constrained_values(board, row, col, num):
    count = 0
    for i in range(9):
        if i != col and not is_valid_move(board, row, i, num):
            count += 1
        if i != row and not is_valid_move(board, i, col, num):
            count += 1
    for i in range(row - row % 3, row - row % 3 + 3):
        for j in range(col - col % 3, col - col % 3 + 3):
            if (i != row or j != col) and not is_valid_move(board, i, j, num):
                count += 1
    return count

def forward_checking(board, row, col, num):
    original_board = copy.deepcopy(board)  # copy board before making changes

    #assignment
    board[row][col] = num

    # Check consistency with peers
    for i in range(9):
        if i != col and board[row][i] == num:  # conflicts in the same row
            board[row][col] = 0  # Revert the assignment
            return False
        if i != row and board[i][col] == num:  # conflicts in the same column
            board[row][col] = 0  # Revert the assignment
            return False
    for i in range(row - row % 3, row - row % 3 + 3):
        for j in range(col - col % 3, col - col % 3 + 3):
            if (i != row or j != col) and board[i][j] == num:  # conflicts in the same 3x3 subgrid
                board[row][col] = 0  # Revert the assignment
                return False
    return True  

def apply_arc_consistency(board):
    queue = []
    domains = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]
    steps = []  # List to store the steps of arc consistency

    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                domains[i][j] = [board[i][j]]
                queue.append((i, j))

    def revise(xi, xj):
        revised = False
        removed_values = []
        for value in domains[xi[0]][xi[1]]:
            if isinstance(domains[xj[0]][xj[1]], list) and value in domains[xj[0]][xj[1]]:
                domains[xi[0]][xi[1]].remove(value)
                removed_values.append(value)
                revised = True
        if revised:
            steps.append(((xi[0], xi[1]), (xj[0], xj[1]), removed_values))
            print(f"Revised: {removed_values} removed from ({xi[0]}, {xi[1]})'s domain due to ({xj[0]}, {xj[1]})")
            logging.info(f"Revised: {removed_values} removed from ({xi[0]}, {xi[1]})'s domain due to ({xj[0]}, {xj[1]})")
        return revised

    while queue:
        xi, xj = queue.pop(0)
        print(f"Processing cell ({xi}, {xj})")
        logging.info(f"Processing cell ({xi}, {xj})")
        for i in range(9):
            if i != xi and revise((i, xj), (xi, xj)):
                if len(domains[i][xj]) == 0:
                    return None, steps
                queue.append((i, xj))
        for j in range(9):
            if j != xj and revise((xi, j), (xi, xj)):
                if len(domains[xi][j]) == 0:
                    return None, steps
                queue.append((xi, j))

    return domains, steps


def solve_sudoku(initial_board):
    board = copy.deepcopy(initial_board)

    if not backtracking(board):
        print("The puzzle is unsolvable.")
        logging.info("The puzzle is unsolvable.")
        return None

    domains, steps = apply_arc_consistency(board)
    if domains is None:
        print("Arc consistency failed. The puzzle might be unsolvable.")
        logging.info("Arc consistency failed. The puzzle might be unsolvable.")
        return None

    # Create a new board with resolved values
    solved_board = [[domains[i][j][0] if isinstance(domains[i][j], list) and len(domains[i][j]) == 1 else 0 for j in range(9)] for i in range(9)]

    return solved_board

def generate_random_puzzle(difficulty):
    def remove_cells(board, num_to_remove):
        removed = 0
        while removed < num_to_remove:
            row, col = np.random.randint(0, 9, size=2)
            if board[row][col] != 0:
                board[row][col] = 0
                removed += 1

    filled_range = get_filled_cells_range(difficulty)
    num_filled = np.random.randint(*filled_range)

    board = np.zeros((9, 9), dtype=int)
    if not backtracking(board):
        print("Failed to generate a complete board.")
        logging.info("Failed to generate a complete board.")
        return None

    # Remove cells to match difficulty
    num_to_remove = 81 - num_filled
    remove_cells(board, num_to_remove)

    return board
    # Create an empty Sudoku board
    # board = np.zeros((9, 9), dtype=int)
    
    # if difficulty == "Easy":
    #     # Fill random places of the puzzle
    #     for _ in range(np.random.randint(36, 46)):
    #         row, col, num = np.random.randint(9, size=3)
    #         while not is_valid_move(board, row, col, num + 1):
    #             row, col, num = np.random.randint(9, size=3)
    #         board[row][col] = num + 1
    # elif difficulty == "Medium":
    #     # Fill random places of the puzzle
    #     for _ in range(np.random.randint(27, 36)):
    #         row, col, num = np.random.randint(9, size=3)
    #         while not is_valid_move(board, row, col, num + 1):
    #             row, col, num = np.random.randint(9, size=3)
    #         board[row][col] = num + 1
    # elif difficulty == "Hard":
    #     # Fill random places of the puzzle
    #     for _ in range(np.random.randint(17, 27)):
    #         row, col, num = np.random.randint(9, size=3)
    #         while not is_valid_move(board, row, col, num + 1):
    #             row, col, num = np.random.randint(9, size=3)
    #         board[row][col] = num + 1
            
    # return board

    # # Fill random places of the puzzle
    # for _ in range(np.random.randint(12, 25)):  # Adjust the range for puzzle difficulty
    #     row, col, num = np.random.randint(9, size=3)
    #     while not is_valid_move(board, row, col, num + 1):
    #         row, col, num = np.random.randint(9, size=3)
    #     board[row][col] = num + 1

    # return board
    




 