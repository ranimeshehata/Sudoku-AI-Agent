# Sudoko AI Agent

This project is a Sudoku solver and generator with a graphical user interface (GUI) built using Pygame. It provides three modes for users to interact with Sudoku puzzles:
![image](https://github.com/user-attachments/assets/dd8eb676-c2a5-43cd-ab23-69f5285fd7e9)

![image](https://github.com/user-attachments/assets/c9822c3e-2b0d-46ac-8f69-fd179d31b63b)

![image](https://github.com/user-attachments/assets/602f3c64-b56d-4030-ba6e-f8df35305427)

![image](https://github.com/user-attachments/assets/fa66fd3b-af3f-4b69-ba1f-fcd2a0ebf455)

![image](https://github.com/user-attachments/assets/bafab339-4dbc-4542-98b8-3d76effc36e8)


1. **Mode 1**: AI Agent solves a randomly generated Sudoku board.
2. **Mode 2**: AI Agent solves a user-generated Sudoku board.
3. **Mode 3**: User solves a user-generated Sudoku board.

## Features

- **Sudoku Solver**: Uses **Backtracking** and **Arc Consistency** techniques to solve Sudoku puzzles.
- **Sudoku Generator**: Generates Sudoku puzzles of varying difficulty levels (Easy, Moderate, Hard).
- **Graphical User Interface**: Built with Pygame, allowing users to interact with the Sudoku Board visually.

## Randomization:

This function generates a randomized Sudoku puzzle based on the specified difficulty level. The randomization involves the following steps:

#### 1. Determine the Range of Pre-Filled Cells

The function get_filled_cells_range(difficulty) returns a tuple (min_filled, max_filled) based on the difficulty level:
Easy: Between 36–45 pre-filled cells.
Moderate: Between 27–35 pre-filled cells.
Hard: Between 17–26 pre-filled cells.
 ```sh
np.random.randint(*filled_range) 
```
selects a random number of cells to fill within the specified range.

#### 2. Generate a Fully Solved Sudoku Board

- A 9x9 empty board (all zeros) is initialized. <br>
- The backtracking algorithm fills the board with valid values to create a complete (solved) Sudoku board. The randomization here comes from the backtracking logic itself: <br>
- MRV (Minimum Remaining Values): The cell with the fewest valid options is chosen. <br>
- LCV (Least Constraining Value): The algorithm tries numbers in the order that creates the least constraints for other cells. <br>
- Recursive backtracking ensures the board remains valid as it is filled.

#### 3. Remove Cells to Match the Difficulty

- The number of cells to remove (num_to_remove) is calculated as the total cells (81) minus the number of pre-filled cells (num_filled).
#### The remove_cells function uses randomization:

- Randomly selects a row and column using np.random.randint(0, 9, size=2). <br>
- If the selected cell is already empty (board[row][col] == 0), it skips removing it and continues until the desired number of cells is removed. <br>
- This random removal ensures that each generated puzzle is unique while adhering to the desired difficulty level.
#### Supporting Randomization in the Backtracking:
- MRV and LCV Logic: <br>
For each unfilled cell, the backtracking algorithm sorts possible values by the "least constraining value." This ensures that even if multiple puzzles are generated with the same difficulty, the paths taken during backtracking differ due to varying constraints.<br>
- Recursive Nature: <br>
The depth-first search (DFS) approach of backtracking inherently introduces variability in the order of exploration.


#### Randomization Key Points:
- Randomized Pre-Fill Count: The number of cells to pre-fill varies based on difficulty. <br>
- Randomized Cell Selection for Removal: Cells to be emptied are randomly selected. <br>
- Randomized Backtracking Path: The LCV and MRV heuristics ensure unique solutions even for identical inputs. <br>
- This combination of strategies ensures the generated puzzles are unique and adhere to the desired difficulty level.


## Project Structure

- `gui.py`: Contains the Pygame GUI implementation and the main game loop.
- `sudoku.py`: Contains the Sudoku solver and generator logic.
- `sudoku_utils.py`: Contains utility functions for Sudoku validation and difficulty settings.
- `sudoku_agent.log`: Log file for the Sudoku solver's actions.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ranimeshehata/Sudoku-AI-Agent.git
    cd sudoku-solver
    ```
2. Run the application:
    ```sh
    python gui.py
    ```

## Usage

### Mode 1: AI Agent Solve Randomized Board

1. Select the difficulty level (Easy, Moderate, Hard).
2. Click on "Mode 1: AI Agent Solve Randomized Board".
3. The AI will generate and solve a Sudoku puzzle based on the selected difficulty.

### Mode 2: AI Agent Solve User Generate Board

1. Select the difficulty level (Easy, Moderate, Hard).
2. Click on "Mode 2: AI Agent Solve User Generate Board".
3. Enter your Sudoku puzzle by clicking on the cells and typing numbers (1-9).
4. Click "Solve Board" to let the AI solve the puzzle.

### Mode 3: User Solve User Generate Board

1. Select the difficulty level (Easy, Moderate, Hard).
2. Click on "Mode 3: User Solve User Generate Board".
3. Enter your Sudoku puzzle by clicking on the cells and typing numbers (1-9).
4. Solve the puzzle manually.

## Logging

The application logs its actions to **[sudoku_agent.log]**. This includes the steps taken by the AI to solve the puzzle and any errors encountered.

