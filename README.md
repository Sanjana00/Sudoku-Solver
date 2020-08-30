# Sudoku-Solver
Sudoku solver coded in python. Uses logic to solve easy, medium and hard level Sudoku puzzles, but resorts to backtracking for puzzles with extreme difficulty.

# Usage

Execute the sudoku.py file with the name of the file containing the Sudoku game as a command line argument. If no command line argument is provided, the program looks for a file named 'sudoku.txt' located in the same directory as code file.

# Format for game file

The game is represented in 9 lines for 9 rows and one character for each column in a text file. Empty spaces are represented by '0' and clues are represented by the corresponding digit whose value lies between 1 and 9.

Eg:

306520090

940160083

070400065

030782000

704601032

601350079

103070904

000045008

008010756
