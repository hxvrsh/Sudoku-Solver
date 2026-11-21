nodes = 0
solutions = 0
first_solution = None
moves = []
first_solution_move_count = 0

def is_safe(board, row, col, num):

    # Check row
    for c in range(9):
        if board[row][c] == num:
            return False

    # Check column
    for r in range(9):
        if board[r][col] == num:
            return False

    # Check 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3

    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False

    return True


def solve(board):

    global nodes
    global solutions
    global first_solution
    global first_solution_move_count

    # Find an empty cell
    empty_cell = None

    for row in range(9):
        for col in range(9):

            if board[row][col] == 0:
                empty_cell = (row, col)
                break

        if empty_cell:
            break

    # No empty cells = solution found
    if empty_cell is None:

        solutions += 1

        if first_solution is None:
            first_solution = [row[:] for row in board]

            # Remember where the first solution ended
            first_solution_move_count = len(moves)

        return solutions >= 2

    row, col = empty_cell

    # Try numbers 1 to 9
    for num in range(1, 10):

        if is_safe(board, row, col, num):

            nodes += 1

            # Place number
            board[row][col] = num

            moves.append({
                "action": "place",
                "row": row,
                "col": col,
                "value": num
            })

            # Continue solving
            stop = solve(board)

            # If two solutions have been found, stop
            if stop:
                return True

            # Remove number because this path did not work
            board[row][col] = 0

            moves.append({
                "action": "backtrack",
                "row": row,
                "col": col,
                "value": num
            })

    return False

def run(board):

    global nodes
    global solutions
    global first_solution
    global moves
    global first_solution_move_count

    # Reset everything
    nodes = 0
    solutions = 0
    first_solution = None
    moves = []
    first_solution_move_count = 0

    # Solve
    solve(board)

    # Keep only the moves that led to the first solution
    moves = moves[:first_solution_move_count]

    # Restore the first solution
    if first_solution is not None:

        for row in range(9):
            for col in range(9):
                board[row][col] = first_solution[row][col]

    return {
        "board": board,
        "nodes": nodes,
        "solutions": solutions,
        "moves": moves
    }