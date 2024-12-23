import numpy as np
import logging
import copy
from sudoku_utils import get_filled_cells_range, is_valid_move, is_empty_cell

logging.basicConfig(filename='sudoku_agent.log', level=logging.INFO, format='%(message)s', filemode='w')

def backtracking(board, domains=None):

    if domains is None:
        domains, steps = apply_arc_consistency(board)
    mrv_cell = is_empty_cell(board, domains)  # Find mrv cell with min remaining values in domain.
    
    if mrv_cell is None:   # If no mrv cell is found, the board is solved.
        return True

    # print(f"MRV is {mrv_cell}")
    row, col = mrv_cell

    domain_values = domains[row][col]

    # we re-order by least constrained value of domain of mrv
    domain_values.sort(key=lambda num: count_constrained_values(board, row, col, num))

    # print(f"Attempting to fill cell ({row}, {col}) with domain values: {domain_values}")
    logging.info(f"Attempting to fill cell ({row}, {col}) with domain values: {domain_values}")

    for num in domain_values:
        # print(f"Trying value {num} for cell ({row}, {col})")
        logging.info(f"Trying value {num} for cell ({row}, {col})")
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            # print("Applying Arc Consistency")
            logging.info("Applying Arc Consistency")

            # first returned value is domains, it's None if a var domain became empty
            new_domains, steps = apply_arc_consistency(board, domains)
            if new_domains is not None:
                # print("Arc Consistency check is successful")
                logging.info("Arc Consistency check is successful")

                # Recursive call to fill the next cell --> DFS way
                if backtracking(board, new_domains):
                    return True

            # print(f"Value {num} for cell ({row}, {col}) leads to conflict. Backtracking...")
            logging.info(f"Value {num} for cell ({row}, {col}) leads to conflict. Backtracking...")
            board[row][col] = 0
        else:
            # print(f"Value {num} is not valid for cell ({row}, {col}). Skipping...")
            logging.info(f"Value {num} is not valid for cell ({row}, {col}). Skipping...") 

    # print(f"No valid value found for cell ({row}, {col}). Backtracking...")
    logging.info(f"No valid value found for cell ({row}, {col}). Backtracking...")
    return False

def get_domain_values(board, row, col):
    domain_values = [num for num in range(1, 10) if is_valid_move(board, row, col, num)]
    return domain_values

def count_constrained_values(board, row, col, num):
    count = 0
    for i in range(9):
        if i != col and not is_valid_move(board, row, i, num): # check for violation in row
            count += 1
        if i != row and not is_valid_move(board, i, col, num): # check for violation in column
            count += 1
    for i in range(row - row % 3, row - row % 3 + 3):  # check for violation in 3x3
        for j in range(col - col % 3, col - col % 3 + 3):
            if (i != row or j != col) and not is_valid_move(board, i, j, num):
                count += 1
    return count
 
def apply_arc_consistency(board, parent_domains=None):
    queue = []
    # Initialize domains with all possible values
    domains = copy.deepcopy(parent_domains) if parent_domains is not None else [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]
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
            if isinstance(domains[xj[0]][xj[1]], list) and len(domains[xj[0]][xj[1]]) == 1 and value in domains[xj[0]][xj[1]] :
                domains[xi[0]][xi[1]].remove(value)
                removed_values.append(value)
                revised = True
        if revised:
            steps.append(((xi[0], xi[1]), (xj[0], xj[1]), removed_values))
            # print(f"Revised: {removed_values} removed from ({xi[0]}, {xi[1]})'s domain due to ({xj[0]}, {xj[1]})")
            logging.info(f"Revised: {removed_values} removed from ({xi[0]}, {xi[1]})'s domain due to ({xj[0]}, {xj[1]})")
        return revised

    while queue:
        xi, xj = queue.pop(0)
        # print(f"Processing cell ({xi}, {xj})")
        logging.info("=====================================================")
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

        subgrid_row_start = (xi // 3) * 3
        subgrid_col_start = (xj // 3) * 3
        for i in range(subgrid_row_start, subgrid_row_start + 3):
            for j in range(subgrid_col_start, subgrid_col_start + 3):
                if (i != xi or j != xj) and revise((i, j), (xi, xj)):
                    if len(domains[i][j]) == 0:
                        return None, steps
                    queue.append((i, j))

    return domains, steps

## OLD IMPLEMENTATION
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

    # Create a new board with resolved values, and we directly inject values with domain size 1, otherwise we keep it empty (0)
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
