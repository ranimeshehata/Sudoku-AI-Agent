import pygame
import sys
import time
import copy
import logging
from sudoku import solve_sudoku, generate_random_puzzle
from sudoku_utils import is_valid_sudoku, get_filled_cells_range

logging.basicConfig(filename='sudoku_agent.log', level=logging.INFO, format='%(message)s', filemode='w')
logging.info("Sudoku Agent Log\n")
logging.info("=====================================\n")

pygame.init()

WIDTH, HEIGHT = 1300, 800
BUTTON_WIDTH, BUTTON_HEIGHT = 530, 130
BUTTON_GAP = 100

WHITE = (255, 255, 255) 
MENU_BUTTON_BACKGROUND = (173, 216, 230)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
ERROR = (230, 30, 30)
SELECTED_CELL_COLOR = (255, 255, 0) 
BACKGROUND = (89, 72, 81)
BUTTON_TEXT =(209, 50, 124)
BUTTON_BACKGROUND = (247, 210, 230)

cell_size = 70
cell_margin = 10
board_size = 9 * cell_size + 10 * cell_margin
board_start_x = 15
board_start_y = 15
number_font = pygame.font.SysFont(None, 45)
subgrid_size = 3 * (cell_size+2) + 2 * (cell_margin+5)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")
background_image = pygame.image.load("photo.webp")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 40)
button_font = pygame.font.SysFont(None, 30)

buttons = [
    pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, 100, BUTTON_WIDTH, BUTTON_HEIGHT),
    pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, 300, BUTTON_WIDTH, BUTTON_HEIGHT),
    pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, 500, BUTTON_WIDTH, BUTTON_HEIGHT)
]

button_texts = [
    "Mode 1: AI Agent Solves Randomly Generated Board",
    "Mode 2: AI Agent Solves User Generated Board",
    "Mode 3: User Solves Randomly Generated Board"
]

difficulty_buttons = [
    pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT),
    pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, 260, BUTTON_WIDTH, BUTTON_HEIGHT),
    pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, 320, BUTTON_WIDTH, BUTTON_HEIGHT)
]

difficulty_texts = ["Easy", "Moderate", "Hard"]
selected_difficulty = None
show_select_difficulty_message = False
    
def draw_menu():
        window.blit(background_image, (0, 0))
        for i, button in enumerate(buttons):
            pygame.draw.rect(window, MENU_BUTTON_BACKGROUND, button, border_radius=10)
            text = button_font.render(button_texts[i], True, BLACK)
            text_rect = text.get_rect(center=button.center)
            window.blit(text, text_rect)
            
        for j, diff_button in enumerate(difficulty_buttons):
            
            diff_button.y = buttons[2].y + BUTTON_HEIGHT + 50 
            diff_button.x = (WIDTH - BUTTON_WIDTH) // 2 + j * (BUTTON_WIDTH // 3) 
            if selected_difficulty == j:
                pygame.draw.circle(window, BLACK, (diff_button.x + 15, diff_button.y + 15), 10)
            else:
                pygame.draw.circle(window, WHITE, (diff_button.x + 15, diff_button.y + 15), 10)
                pygame.draw.circle(window, BLACK, (diff_button.x + 15, diff_button.y + 15), 10, 1)
            text = button_font.render(difficulty_texts[j], True, BLACK)
            text_rect = text.get_rect(midleft=(diff_button.x + 30, diff_button.y + 15))
            window.blit(text, text_rect)
            
            if show_select_difficulty_message:
                message = "Please select a difficulty first!"
                message_font = pygame.font.SysFont(None, 40)
                message_text = message_font.render(message, True, ERROR)
                message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                window.blit(message_text, message_rect)
                box_padding = 30
                box_rect = pygame.Rect(
                    message_rect.left - box_padding,
                    message_rect.top - box_padding,
                    message_rect.width + 2 * box_padding,
                    message_rect.height + 2 * box_padding
                )
                pygame.draw.rect(window, (255, 255, 255), box_rect)
                pygame.draw.rect(window, ERROR, box_rect, 2)
                window.blit(message_text, message_rect)
                
                
def count_filled_cells(grid):
    return sum(cell != 0 for row in grid for cell in row)

def draw_sudoku_board(window, board):
    for i in range(9):
        for j in range(9):
            cell_x = board_start_x + j * (cell_size + cell_margin)
            cell_y = board_start_y + i * (cell_size + cell_margin)
            pygame.draw.rect(window, WHITE, (cell_x, cell_y, cell_size, cell_size), border_radius=3)
            pygame.draw.rect(window, (0, 0, 0), (cell_x, cell_y, cell_size, cell_size), 1)
            
            if board[i][j] != 0:
                text_surface = number_font.render(str(board[i][j]), True, BUTTON_TEXT)
                text_rect = text_surface.get_rect(center=(cell_x + cell_size / 2, cell_y + cell_size / 2))
                window.blit(text_surface, text_rect)
            if i % 3 == 0 and j % 3 == 0:
                pygame.draw.rect(window, BLACK, (cell_x - cell_margin +3, cell_y - cell_margin+3, subgrid_size, subgrid_size), 7, border_radius=15)

def mode1():
    mode1_agent = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mode 1: AI Agent Solve Randomized Board")
    puzzle = generate_random_puzzle(difficulty_texts[selected_difficulty])
    elapsed_time = None
    mode1 = True
    error_message = None
    
    while mode1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mode1 = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if solve button is clicked
                if 850 <= event.pos[0] <= 1090 and 500 <= event.pos[1] <= 550:
                    start = time.time()
                    solved_puzzle = solve_sudoku(puzzle)
                    end = time.time()
                    
                    if solved_puzzle is not None:
                        elapsed_time = end - start
                        print(f"Board solved in {elapsed_time:.5f} seconds.")
                        logging.info(f"Board solved in {elapsed_time:.5f} seconds.")
                        puzzle = solved_puzzle
                        error_message = None 
                    else:
                        error_message = "The puzzle is unsolvable."
                        logging.info("The puzzle is unsolvable.")

                # Check if regenerate button is clicked
                elif 850 <= event.pos[0] <= 1090 and 575 <= event.pos[1] <= 625:
                    puzzle = generate_random_puzzle(difficulty_texts[selected_difficulty])
                    error_message = None 
                # Check if back button is clicked
                elif 850 <= event.pos[0] <= 1090 and 650 <= event.pos[1] <= 700:
                    mode1 = False

        mode1_agent.fill(BACKGROUND)
        draw_sudoku_board(mode1_agent, puzzle)
        
        difficulty_font = pygame.font.SysFont(None, 50)
        difficulty_text = difficulty_font.render(f"Difficulty: {difficulty_texts[selected_difficulty]}", True, BLACK)
        mode1_agent.blit(difficulty_text, (850, 50))
        
        min_cells, max_cells = get_filled_cells_range(difficulty_texts[selected_difficulty])
        hint_font = pygame.font.SysFont(None, 30)
        hint_text = hint_font.render(f"Entered between {min_cells} and {max_cells} cells", True, BLACK)
        mode1_agent.blit(hint_text, (850, 100))

        if error_message:
            error_font = pygame.font.SysFont(None, 36)
            error_text = error_font.render(error_message, True, ERROR)
            error_rect = error_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            mode1_agent.blit(error_text, error_rect)
            
        if elapsed_time is not None:
            time_font = pygame.font.SysFont(None, 36)
            time_text = time_font.render(f"Game solved in {elapsed_time:.3f} seconds", True, (0, 0, 0))
            mode1_agent.blit(time_text, (800, 450))

        pygame.draw.rect(mode1_agent, BUTTON_BACKGROUND, (850, 500 - 5, 200, 50), border_radius=20)
        pygame.draw.rect(mode1_agent, BUTTON_BACKGROUND, (850, 575 - 5, 200, 50), border_radius=20)
        pygame.draw.rect(mode1_agent, BUTTON_BACKGROUND, (850, 650 - 5, 200, 50), border_radius=20)
        button_font = pygame.font.SysFont(None, 30)
        regenerate_text = button_font.render("Solve Board", True, BUTTON_TEXT)
        solve_text = button_font.render("Randomize Board", True, BUTTON_TEXT)
        mode1_agent.blit(regenerate_text, (880, 510))
        mode1_agent.blit(solve_text, (860, 585))
        back_text = button_font.render("Back to Menu", True, BUTTON_TEXT)
        mode1_agent.blit(back_text, (880, 655))

        pygame.display.flip()
        

def mode2():
    mode2_agent = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mode 2: AI Agent Solve User Generate Board")
    elapsed_time = None
    puzzle = [[0 for _ in range(9)] for _ in range(9)]
    selected_cell = None
    mode2 = True
    error_message = None 
    invalid_key_message = None
    
    while mode2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mode2 = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if back button is clicked
                if 850 <= event.pos[0] <= 1050 and 650 <= event.pos[1] <= 700:
                    mode2 = False
                elif 850 <= event.pos[0] <= 1050 and 500 <= event.pos[1] <= 550:
                    # Check if the puzzle is valid
                    min_cells, max_cells = get_filled_cells_range(difficulty_texts[selected_difficulty])
                    filled_cells = count_filled_cells(puzzle)
                    if filled_cells < min_cells or filled_cells > max_cells:
                        error_message = f"Please enter between {min_cells} and {max_cells} cells for {difficulty_texts[selected_difficulty]} difficulty."
                    elif is_valid_sudoku(puzzle):   # solve
                        start = time.time()
                        solved_puzzle = solve_sudoku(puzzle)
                        end = time.time()
                        if solved_puzzle is not None:
                            elapsed_time = end - start
                            print(f"Board solved in {elapsed_time:.5f} seconds.")
                            logging.info(f"Board solved in {elapsed_time:.5f} seconds.")
                            
                            puzzle = solved_puzzle
                            error_message = None
                        else:
                            error_message = "The puzzle is unsolvable."
                            logging.info("The puzzle is unsolvable.")

                    else:
                        error_message = "Invalid Sudoku Input. Please Check Game Constraints"
                elif 850 <= event.pos[0] <= 1050 and 575 <= event.pos[1] <= 625:
                    # Reset the puzzle when "Reset Board" button is clicked
                    puzzle = [[0 for _ in range(9)] for _ in range(9)]
                    error_message = None 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the clicked cell position
                    cell_x = (event.pos[0] - board_start_x) // (cell_size + cell_margin) 
                    cell_y = (event.pos[1] - board_start_y) // (cell_size + cell_margin) 
                    # print(f"Clicked position: {event.pos}, Calculated cell: ({cell_x}, {cell_y})")
                    if 0 <= cell_x < 9 and 0 <= cell_y < 9:
                        selected_cell = (cell_x, cell_y)
                        # print(f"Selected cell: {selected_cell}")
                        error_message = None
            elif event.type == pygame.KEYDOWN:
                if selected_cell is not None: 
                    invalid_key_message = None
                # Check if a number key (1-9) is pressed
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        puzzle[selected_cell[1]][selected_cell[0]] = int(event.unicode)
                        # print(f"Updated cell {selected_cell} to {int(event.unicode)}")
                    elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        puzzle[selected_cell[1]][selected_cell[0]] = 0
                        # print(f"Cleared cell {selected_cell}")
                    else:
                        print(f"Invalid key pressed")
                        invalid_key_message = "Invalid key pressed. Please press a number key (1-9) or Backspace/Delete to clear the cell."    

        mode2_agent.fill(BACKGROUND)
        draw_sudoku_board(mode2_agent, puzzle)
        
        difficulty_font = pygame.font.SysFont(None, 50)
        difficulty_text = difficulty_font.render(f"Difficulty: {difficulty_texts[selected_difficulty]}", True, BLACK)
        mode2_agent.blit(difficulty_text, (850, 50))
        
        min_cells, max_cells = get_filled_cells_range(difficulty_texts[selected_difficulty])
        hint_font = pygame.font.SysFont(None, 30)
        hint_text = hint_font.render(f"Enter between {min_cells} and {max_cells} cells", True, BLACK)
        mode2_agent.blit(hint_text, (850, 100))


        if selected_cell is not None:
            cell_x, cell_y = selected_cell
            pygame.draw.rect(mode2_agent, SELECTED_CELL_COLOR, (cell_x * 80 + 12, cell_y * 80 + 12, 73, 73), 5, border_radius=10)
            
        if invalid_key_message:
            invalid_key_font = pygame.font.SysFont(None, 30)
            invalid_key_text = invalid_key_font.render(invalid_key_message, True, ERROR)
            invalid_key_rect = invalid_key_text.get_rect(center=(WIDTH // 2, HEIGHT - 30))  
            box_padding = 20
            box_rect = pygame.Rect(
                invalid_key_rect.left - box_padding,
                invalid_key_rect.top - box_padding,
                invalid_key_rect.width + 2 * box_padding,
                invalid_key_rect.height + 2 * box_padding
            )
            pygame.draw.rect(mode2_agent, (255, 255, 255), box_rect)
            pygame.draw.rect(mode2_agent, ERROR, box_rect, 2)
            mode2_agent.blit(invalid_key_text, invalid_key_rect)
            
        if error_message:
            error_font = pygame.font.SysFont(None, 50)
            error_text = error_font.render(error_message, True, ERROR)
            error_rect = error_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            mode2_agent.blit(error_text, error_rect)            
            box_padding = 50
            box_rect = pygame.Rect(
                error_rect.left - box_padding,
                error_rect.top - box_padding,
                error_rect.width + 2 * box_padding,
                error_rect.height + 2 * box_padding
            )
            pygame.draw.rect(mode2_agent, (255, 255, 255), box_rect)
            pygame.draw.rect(mode2_agent, ERROR, box_rect, 2)
            
            mode2_agent.blit(error_text, error_rect)
            
        if elapsed_time is not None:
            time_font = pygame.font.SysFont(None, 36)
            time_text = time_font.render(f"Game solved in {elapsed_time:.3f} seconds", True, BLACK)
            mode2_agent.blit(time_text, (800, 450))

        pygame.draw.rect(mode2_agent, BUTTON_BACKGROUND, (850, 500, 200, 50), border_radius=20)
        pygame.draw.rect(mode2_agent, BUTTON_BACKGROUND, (850, 575, 200, 50), border_radius=20)
        pygame.draw.rect(mode2_agent, BUTTON_BACKGROUND, (850, 650, 200, 50), border_radius=20)  

        button_font = pygame.font.SysFont(None, 30)
        solve_text = button_font.render("Solve Board", True, BUTTON_TEXT)
        mode2_agent.blit(solve_text, (880, 510))
        reset_text = button_font.render("Reset Board", True, BUTTON_TEXT)
        mode2_agent.blit(reset_text, (880, 585))
        back_text = button_font.render("Back to Menu", True, BUTTON_TEXT)
        mode2_agent.blit(back_text, (880, 660))

        pygame.display.flip()

    return puzzle

def highlight_conflicts(mode3_agent, user_input_grid, solved_puzzle):
    conflict_messages = []
    for y in range(9):
        for x in range(9):
            if user_input_grid[y][x] != 0 and user_input_grid[y][x] != solved_puzzle[y][x]:
                # Highlight the incorrect cell
                pygame.draw.rect(mode3_agent, ERROR, (x * 80 + 12, y * 80 + 12, 72, 72), 5, border_radius=10)
                conflict_message = f"Input at Column ({x+1}), Row ({y+1}) is incorrect"
                conflict_messages.append(conflict_message)
                logging.info(conflict_message)
                print(conflict_message)

                # Highlight the conflicting row
                for col in range(9):
                    if user_input_grid[y][col] == user_input_grid[y][x] and col != x:
                        pygame.draw.rect(mode3_agent, ERROR, (col * 80 + 12, y * 80 + 12, 72, 72), 5, border_radius=10)
                        conflict_message = f"Conflict with cell at Column ({col+1}), Row ({y+1})"
                        conflict_messages.append(conflict_message)
                        logging.info(conflict_message)
                        print(conflict_message)

                # Highlight the conflicting column
                for row in range(9):
                    if user_input_grid[row][x] == user_input_grid[y][x] and row != y:
                        pygame.draw.rect(mode3_agent, ERROR, (x * 80 + 12, row * 80 + 12, 72, 72), 5, border_radius=10)
                        conflict_message = f"Conflict with cell at Column ({x+1}), Row ({row+1})"
                        conflict_messages.append(conflict_message)
                        logging.info(conflict_message)
                        print(conflict_message)

                # Highlight the conflicting subgrid
                subgrid_row, subgrid_col = 3 * (y // 3), 3 * (x // 3)
                for row in range(subgrid_row, subgrid_row + 3):
                    for col in range(subgrid_col, subgrid_col + 3):
                        if user_input_grid[row][col] == user_input_grid[y][x] and (row, col) != (y, x):
                            pygame.draw.rect(mode3_agent, ERROR, (col * 80 + 12, row * 80 + 12, 72, 72), 5, border_radius=10)
                            conflict_message = f"Conflict with cell ({col+1}), Row ({row+1}) in same subgrid"
                            conflict_messages.append(conflict_message)
                            logging.info(conflict_message)
                            print(conflict_message)

    # Display conflict messages on the window
    if conflict_messages:
        font = pygame.font.SysFont(None, 30)
        y_offset = 250
        for message in conflict_messages:
            text_surface = font.render(message, True, ERROR)
            text_rect = text_surface.get_rect(center=(WIDTH // 2 + 340, y_offset))
            box_padding = 20
            box_rect = pygame.Rect(
                text_rect.left - box_padding,
                text_rect.top - box_padding,
                text_rect.width + 2 * box_padding,
                text_rect.height + 2 * box_padding
            )
            pygame.draw.rect(mode3_agent, BUTTON_BACKGROUND, box_rect)
            pygame.draw.rect(mode3_agent, ERROR, box_rect, 2)
            mode3_agent.blit(text_surface, text_rect)
            y_offset += text_rect.height + 40

def mode3():
    mode3_agent = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mode 3: User Solve User Generate Board")
    puzzle = generate_random_puzzle(difficulty_texts[selected_difficulty])
    selected_cell = None
    solved_puzzle = None
    user_input_grid = copy.deepcopy(puzzle)
    mode3 = True
    error_message = None
    invalid_key_message = None
    
    while mode3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mode3 = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if back button is clicked
                if 850 <= event.pos[0] <= 1050 and 650 <= event.pos[1] <= 700:
                    mode3 = False
                elif 850 <= event.pos[0] <= 1050 and 500 <= event.pos[1] <= 550:
                    # Solve the puzzle and store the solution
                    min_cells, max_cells = get_filled_cells_range(difficulty_texts[selected_difficulty])
                    filled_cells = count_filled_cells(user_input_grid)
                    if filled_cells < min_cells or filled_cells > max_cells:
                        print(f"Filled cells: {filled_cells}, Min cells: {min_cells}, Max cells: {max_cells}")
                        logging.info(f"Filled cells: {filled_cells}, Min cells: {min_cells}, Max cells: {max_cells}")
                        error_message = f"Please enter between {min_cells} and {max_cells} cells for {difficulty_texts[selected_difficulty]} difficulty."
                    elif is_valid_sudoku(user_input_grid):
                        # Solve the puzzle when "Solve Board" button is clicked
                        start = time.time()
                        solved_puzzle = solve_sudoku(user_input_grid)
                        end = time.time()
                        if solved_puzzle is not None:
                            elapsed_time = end - start
                            print(f"Board solved in {elapsed_time:.5f} seconds.")
                            logging.info(f"Board solved in {elapsed_time:.5f} seconds.")
                            puzzle = solved_puzzle
                            error_message = None
                        else:
                            error_message = "The puzzle is unsolvable."
                            logging.info("The puzzle is unsolvable.")
                    else:
                        error_message = "Invalid Sudoku Input. Please Check Game Constraints"
                # Check if regenerate button is clicked
                elif 850 <= event.pos[0] <= 1090 and 575 <= event.pos[1] <= 625:
                    puzzle = generate_random_puzzle(difficulty_texts[selected_difficulty])
                    user_input_grid = generate_random_puzzle(difficulty_texts[selected_difficulty])
                    error_message = None 
                else:
                    # Get the clicked cell position
                    cell_x = (event.pos[0] - 10) // 80  
                    cell_y = (event.pos[1] - 10) // 80 
                    if 0 <= cell_x < 9 and 0 <= cell_y < 9:
                        selected_cell = (cell_x, cell_y)
                        # print(f"Selected cell: {selected_cell}")
                        error_message = None
            elif event.type == pygame.KEYDOWN:
                if selected_cell is not None:
                    invalid_key_message = None
                # Check if a number key (1-9) is pressed
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        user_input_grid[selected_cell[1]][selected_cell[0]] = int(event.unicode)
                    elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        user_input_grid[selected_cell[1]][selected_cell[0]] = 0
                    else:
                        print(f"Invalid key pressed")
                        invalid_key_message = "Invalid key pressed. Please press a number key (1-9) or Backspace/Delete to clear the cell."

        mode3_agent.fill(BACKGROUND)
        draw_sudoku_board(mode3_agent, user_input_grid)

        difficulty_font = pygame.font.SysFont(None, 50)
        difficulty_text = difficulty_font.render(f"Difficulty: {difficulty_texts[selected_difficulty]}", True, BLACK)
        mode3_agent.blit(difficulty_text, (850, 50))
        
        min_cells, max_cells = get_filled_cells_range(difficulty_texts[selected_difficulty])
        hint_font = pygame.font.SysFont(None, 30)
        hint_text = hint_font.render(f"Enter between {min_cells} and {max_cells} cells", True, BLACK)
        mode3_agent.blit(hint_text, (850, 100))
        
        Instructions_font = pygame.font.SysFont(None, 30)
        Instructions_text = Instructions_font.render("Click on (Start Solve Board) to start playing ..", True, BLACK)
        mode3_agent.blit(Instructions_text, (800, 150))
        

        if selected_cell is not None:
            cell_x, cell_y = selected_cell
            pygame.draw.rect(mode3_agent, SELECTED_CELL_COLOR, (cell_x * 80 + 12, cell_y * 80 + 12, 72, 72), 5, border_radius=10)
            
        if invalid_key_message:
            invalid_key_font = pygame.font.SysFont(None, 30)
            invalid_key_text = invalid_key_font.render(invalid_key_message, True, ERROR)
            invalid_key_rect = invalid_key_text.get_rect(center=(WIDTH // 2, HEIGHT - 30))  
            box_padding = 20
            box_rect = pygame.Rect(
                invalid_key_rect.left - box_padding,
                invalid_key_rect.top - box_padding,
                invalid_key_rect.width + 2 * box_padding,
                invalid_key_rect.height + 2 * box_padding
            )
            pygame.draw.rect(mode3_agent, (255, 255, 255), box_rect)
            pygame.draw.rect(mode3_agent, ERROR, box_rect, 2)
            mode3_agent.blit(invalid_key_text, invalid_key_rect)
            
        if error_message:
            error_font = pygame.font.SysFont(None, 50)
            error_text = error_font.render(error_message, True, ERROR)
            error_rect = error_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            mode3_agent.blit(error_text, error_rect)            
            box_padding = 50
            box_rect = pygame.Rect(
                error_rect.left - box_padding,
                error_rect.top - box_padding,
                error_rect.width + 2 * box_padding,
                error_rect.height + 2 * box_padding
            )
            pygame.draw.rect(mode3_agent, (255, 255, 255), box_rect)
            pygame.draw.rect(mode3_agent, ERROR, box_rect, 2)
            
            mode3_agent.blit(error_text, error_rect)
        # Compare user input with solver's solution in real-time
        if solved_puzzle is not None:
            highlight_conflicts(mode3_agent, user_input_grid, solved_puzzle)

            # for y in range(9):
            #     for x in range(9):
            #         if user_input_grid[y][x] != 0 and user_input_grid[y][x] != solved_puzzle[y][x]:
            #             # incorrect user input
            #             pygame.draw.rect(mode3_agent, ERROR, (x * 80 + 12, y * 80 + 12, 72, 72), 5, border_radius=10)
            #             print(f"User input at ({x}, {y}) is incorrect")
            #             logging.info(f"User input at ({x}, {y}) is incorrect")
            #             invalid_key_message = (f"Input at Column ({x+1}), Row ({y+1}) is incorrect")


        pygame.draw.rect(mode3_agent, BUTTON_BACKGROUND, (850, 500, 200, 50), border_radius=20)
        pygame.draw.rect(mode3_agent, BUTTON_BACKGROUND, (850, 575, 200, 50), border_radius=20)
        pygame.draw.rect(mode3_agent, BUTTON_BACKGROUND, (850, 650, 200, 50), border_radius=20)  
        button_font = pygame.font.SysFont(None, 30)
        solve_text = button_font.render("Start Solve Board", True, BUTTON_TEXT)
        mode3_agent.blit(solve_text, (860, 510))
        reset_text = button_font.render("Randomize Board", True, BUTTON_TEXT)
        mode3_agent.blit(reset_text, (866, 585))
        back_text = button_font.render("Back to Menu", True, BUTTON_TEXT)
        mode3_agent.blit(back_text, (880, 660))

        pygame.display.flip()

    return user_input_grid

def main():
    # Main loop
    mode1_option = False  
    mode2_option = False  
    mode3_option = False  
    running = True
    global selected_difficulty, show_select_difficulty_message
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        if selected_difficulty is None:
                            show_select_difficulty_message = True
                        else:
                            show_select_difficulty_message = False
                            if i == 0:  
                                mode1_option = True
                                mode2_option = False
                                mode3_option = False
                            elif i == 1:  
                                mode2_option = True
                                mode1_option = False
                                mode3_option = False
                            elif i == 2:  
                                mode3_option = True
                                mode1_option = False
                                mode2_option = False
                for j, button in enumerate(difficulty_buttons):
                    if button.collidepoint(event.pos):
                        selected_difficulty = j
                        logging.info("Selected Difficulty: " + difficulty_texts[selected_difficulty])
                        logging.info("=====================================\n") 
                        show_select_difficulty_message = False

        draw_menu()
        pygame.display.flip()
        
        if mode1_option:
            logging.info("Mode 1: AI Agent Solve Randomized Board")
            logging.info("=====================================\n")             
            mode1_option = False 
            mode1()  

        if mode2_option:
            logging.info("Mode 2: AI Agent Solve User Generate Board")
            logging.info("=====================================\n")
            mode2_option = False  
            mode2()  

        if mode3_option:
            logging.info("Mode 3: User Solve User Generate Board")
            logging.info("=====================================\n")
            mode3_option = False 
            mode3()  
    pygame.quit()

if __name__ == "__main__":
    main()