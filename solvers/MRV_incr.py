nodes = 0
solutions = 0
first_solution = None

moves = []
first_solution_move_count = 0

rows = []
cols = []
boxes = []


# --------------------------------------------------
# Incremental tracking
# --------------------------------------------------

def initialize(board):

    global rows, cols, boxes

    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for row in range(9):
        for col in range(9):

            num = board[row][col]

            if num != 0:

                rows[row].add(num)
                cols[col].add(num)

                box = (row // 3) * 3 + (col // 3)
                boxes[box].add(num)


# --------------------------------------------------
# Get candidates for a cell
# --------------------------------------------------

def get_candidates(row, col):

    numbers = set(range(1, 10))

    box = (row // 3) * 3 + (col // 3)

    candidates = numbers - rows[row] - cols[col] - boxes[box]

    return candidates


# --------------------------------------------------
# MRV
# Find the empty cell with the fewest candidates
# --------------------------------------------------

def find_best_cell(board):

    best_row = -1
    best_col = -1
    best_candidates = None

    for row in range(9):
        for col in range(9):

            if board[row][col] == 0:

                candidates = get_candidates(row, col)

                # Contradiction
                if len(candidates) == 0:
                    return row, col, set()

                # First empty cell
                # OR better MRV cell
                if (
                    best_candidates is None
                    or len(candidates) < len(best_candidates)
                ):

                    best_row = row
                    best_col = col
                    best_candidates = candidates

                    # Can't do better than 1 candidate
                    if len(best_candidates) == 1:
                        return (
                            best_row,
                            best_col,
                            best_candidates
                        )

    return best_row, best_col, best_candidates


# --------------------------------------------------
# Find neighboring empty cells
# --------------------------------------------------

def get_neighbors(board, row, col):

    neighbors = set()

    # Same row
    for c in range(9):

        if c != col and board[row][c] == 0:
            neighbors.add((row, c))

    # Same column
    for r in range(9):

        if r != row and board[r][col] == 0:
            neighbors.add((r, col))

    # Same 3x3 box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3

    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):

            if (
                (r, c) != (row, col)
                and board[r][c] == 0
            ):
                neighbors.add((r, c))

    return neighbors


# --------------------------------------------------
# LCV
# Least Constraining Value
# --------------------------------------------------

def order_candidates(board, row, col, candidates):

    neighbors = get_neighbors(board, row, col)

    scores = []

    for num in candidates:

        impact = 0

        for n_row, n_col in neighbors:

            neighbor_candidates = get_candidates(
                n_row,
                n_col
            )

            if num in neighbor_candidates:
                impact += 1

        scores.append((impact, num))

    # Lower impact = less constraining
    scores.sort()

    return [num for impact, num in scores]


# --------------------------------------------------
# Solver
# --------------------------------------------------

def solve(board):

    global nodes
    global solutions
    global first_solution
    global first_solution_move_count

    nodes += 1

    # Stop after finding 2 solutions
    if solutions >= 2:
        return

    # MRV
    row, col, candidates = find_best_cell(board)

    # No empty cells
    if row == -1:

        solutions += 1

        if solutions == 1:
            first_solution = [r[:] for r in board]
            first_solution_move_count = len(moves)

        return

    # No possible number
    if len(candidates) == 0:
        return

    # Show which cell MRV selected
    moves.append({
        "action": "select",
        "row": row,
        "col": col,
        "candidates": sorted(candidates)
    })

    # LCV
    ordered_candidates = order_candidates(
        board,
        row,
        col,
        candidates
    )

    box = (row // 3) * 3 + (col // 3)

    # Try candidates in LCV order
    for num in ordered_candidates:

        # -----------------------------
        # Make the move
        # -----------------------------

        board[row][col] = num

        rows[row].add(num)
        cols[col].add(num)
        boxes[box].add(num)

        moves.append({
            "action": "place",
            "row": row,
            "col": col,
            "value": num
        })

        # -----------------------------
        # Continue solving
        # -----------------------------

        solve(board)

        # -----------------------------
        # Undo the move
        # -----------------------------

        board[row][col] = 0

        rows[row].remove(num)
        cols[col].remove(num)
        boxes[box].remove(num)

        moves.append({
            "action": "backtrack",
            "row": row,
            "col": col,
            "value": num
        })

        # Stop if two solutions found
        if solutions >= 2:
            return


# --------------------------------------------------
# Flask interface
# --------------------------------------------------

def run(board):

    global nodes
    global solutions
    global first_solution
    global moves
    global first_solution_move_count

    # Reset solver state
    nodes = 0
    solutions = 0
    first_solution = None
    moves = []
    first_solution_move_count = 0

    # Initialize row, column and box sets
    initialize(board)

    # Solve the user's Sudoku
    solve(board)

    # Keep only the moves that led to the first solution
    moves = moves[:first_solution_move_count]

    # Put the first solution into board
    if first_solution is not None:
        board = first_solution

    # Return result to Flask
    return {
        "board": board,
        "nodes": nodes,
        "solutions": solutions,
        "moves": moves
    }   