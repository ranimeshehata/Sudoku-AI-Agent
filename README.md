# Sudoko AI Agent

This project is a Sudoku solver and generator with a graphical user interface (GUI) built using Pygame. It provides three modes for users to interact with Sudoku puzzles:

1. **Mode 1**: AI Agent solves a randomly generated Sudoku board.
2. **Mode 2**: AI Agent solves a user-generated Sudoku board.
3. **Mode 3**: User solves a user-generated Sudoku board.

## Features

- **Sudoku Solver**: Uses **Backtracking** and **Arc Consistency** techniques to solve Sudoku puzzles.
- **Sudoku Generator**: Generates Sudoku puzzles of varying difficulty levels (Easy, Moderate, Hard).
- **Graphical User Interface**: Built with Pygame, allowing users to interact with the Sudoku Board visually.

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

