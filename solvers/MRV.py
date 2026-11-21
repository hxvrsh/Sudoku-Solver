nodes = 0
solutions = 0
first_solution = None
moves = []
first_solution_move_count = 0


def get_candidates(board, row, col):

    candidates = set(range(1, 10))

    # Remove numbers from row
    for num in board[row]:
        candidates.discard(num)

    # Remove numbers from column
    for r in range(9):
        candidates.discard(board[r][col])

    # Remove numbers from 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3

    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            candidates.discard(board[r][c])

    return candidates


def find_mrv_cell(board):

    best_cell = None
    best_candidates = None

    for row in range(9):

        for col in range(9):

            if board[row][col] == 0:

                candidates = get_candidates(board, row, col)

                if best_candidates is None or len(candidates) < len(best_candidates):

                    best_cell = (row, col)
                    best_candidates = candidates

                    # Can't get better than one candidate
                    if len(best_candidates) == 1:
                        return best_cell, best_candidates

    return best_cell, best_candidates


def solve(board):

    global nodes
    global solutions
    global first_solution
    global first_solution_move_count

    # Find the empty cell with the fewest candidates
    cell, candidates = find_mrv_cell(board)

    # No empty cells = solution found
    if cell is None:

        solutions += 1

        if first_solution is None:
            first_solution = [row[:] for row in board]
            first_solution_move_count = len(moves)

        return solutions >= 2

    row, col = cell
    
    moves.append({
    "action": "select",
    "row": row,
    "col": col,
    "candidates": sorted(candidates)
    })
    
    # Try each candidate
    for num in candidates:

        nodes += 1

        # Place candidate
        board[row][col] = num

        moves.append({
            "action": "place",
            "row": row,
            "col": col,
            "value": num
        })

        # Continue solving
        stop = solve(board)

        # Stop after finding two solutions
        if stop:
            return True

        # Backtrack
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

    solve(board)

    # Keep only the moves leading to the first solution
    moves = moves[:first_solution_move_count]

    # Restore first solution
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