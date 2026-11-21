nodes = 0
moves = []


# ==================================================
# CANDIDATE SETS
# ==================================================

def get_candidates(board, row, col):

    numbers = set(range(1, 10))

    # Numbers already in row
    used = set(board[row])

    # Numbers already in column
    for r in range(9):
        used.add(board[r][col])

    # Numbers already in box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3

    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            used.add(board[r][c])

    used.discard(0)

    return numbers - used


# ==================================================
# NAKED SINGLES
# ==================================================

def naked_singles(board):

    changed = False

    for row in range(9):
        for col in range(9):

            if board[row][col] == 0:

                candidates = get_candidates(board, row, col)

                # Exactly one possible number
                if len(candidates) == 1:

                    num = next(iter(candidates))

                    board[row][col] = num

                    moves.append({
                        "action": "naked_single",
                        "row": row,
                        "col": col,
                        "value": num
                    })

                    changed = True

    return changed


# ==================================================
# HIDDEN SINGLES
# ==================================================

def hidden_singles(board):

    changed = False

    # ----------------------------------------------
    # Check rows
    # ----------------------------------------------

    for row in range(9):

        for num in range(1, 10):

            positions = []

            for col in range(9):

                if board[row][col] == 0:

                    candidates = get_candidates(
                        board,
                        row,
                        col
                    )

                    if num in candidates:
                        positions.append(col)

            # Number can only go in one cell
            if len(positions) == 1:

                col = positions[0]

                board[row][col] = num

                moves.append({
                    "action": "hidden_single",
                    "row": row,
                    "col": col,
                    "value": num
                })

                changed = True


    # ----------------------------------------------
    # Check columns
    # ----------------------------------------------

    for col in range(9):

        for num in range(1, 10):

            positions = []

            for row in range(9):

                if board[row][col] == 0:

                    candidates = get_candidates(
                        board,
                        row,
                        col
                    )

                    if num in candidates:
                        positions.append(row)

            # Number can only go in one cell
            if len(positions) == 1:

                row = positions[0]

                board[row][col] = num

                moves.append({
                    "action": "hidden_single",
                    "row": row,
                    "col": col,
                    "value": num
                })

                changed = True


    # ----------------------------------------------
    # Check 3x3 boxes
    # ----------------------------------------------

    for box_row in range(3):

        for box_col in range(3):

            for num in range(1, 10):

                positions = []

                start_row = box_row * 3
                start_col = box_col * 3

                for row in range(
                    start_row,
                    start_row + 3
                ):

                    for col in range(
                        start_col,
                        start_col + 3
                    ):

                        if board[row][col] == 0:

                            candidates = get_candidates(
                                board,
                                row,
                                col
                            )

                            if num in candidates:
                                positions.append(
                                    (row, col)
                                )

                # Number has only one possible cell
                if len(positions) == 1:

                    row, col = positions[0]

                    board[row][col] = num

                    moves.append({
                        "action": "hidden_single",
                        "row": row,
                        "col": col,
                        "value": num
                    })

                    changed = True

    return changed


# ==================================================
# HUMAN-STYLE SOLVING
# ==================================================

def human_solve(board):

    while True:

        changed = False

        # First look for naked singles
        if naked_singles(board):
            changed = True

        # Then look for hidden singles
        if hidden_singles(board):
            changed = True

        # Stop when neither technique makes progress
        if not changed:
            break


# ==================================================
# CHECK WHETHER SOLVED
# ==================================================

def is_solved(board):

    for row in range(9):

        for col in range(9):

            if board[row][col] == 0:
                return False

    return True


# ==================================================
# MRV
# ==================================================

def find_best_cell(board):

    best_row = -1
    best_col = -1
    best_candidates = None

    for row in range(9):

        for col in range(9):

            if board[row][col] == 0:

                candidates = get_candidates(
                    board,
                    row,
                    col
                )

                if len(candidates) == 0:
                    return row, col, set()

                if (
                    best_candidates is None
                    or len(candidates)
                    < len(best_candidates)
                ):

                    best_row = row
                    best_col = col
                    best_candidates = candidates

                    if len(candidates) == 1:
                        return (
                            best_row,
                            best_col,
                            best_candidates
                        )

    return best_row, best_col, best_candidates


# ==================================================
# BACKTRACKING FALLBACK
# ==================================================

def solve(board):

    global nodes

    nodes += 1

    # ----------------------------------------------
    # Apply human-style techniques
    # ----------------------------------------------

    human_solve(board)

    # ----------------------------------------------
    # Check if solved
    # ----------------------------------------------

    if is_solved(board):
        return True

    # ----------------------------------------------
    # MRV
    # ----------------------------------------------

    row, col, candidates = find_best_cell(board)

    # Contradiction
    if len(candidates) == 0:
        return False

    # Show which cell MRV selected
    moves.append({
        "action": "select",
        "row": row,
        "col": col,
        "candidates": sorted(candidates)
    })

    # Save current board before recursion
    saved_board = [r[:] for r in board]

    # ----------------------------------------------
    # Try candidates
    # ----------------------------------------------

    for num in candidates:

        board[row][col] = num

        moves.append({
            "action": "place",
            "row": row,
            "col": col,
            "value": num
        })

        if solve(board):
            return True

        # Restore previous state
        for r in range(9):
            board[r] = saved_board[r]

        board[row][col] = 0

        moves.append({
            "action": "backtrack",
            "row": row,
            "col": col,
            "value": num
        })

    return False


# ==================================================
# FLASK INTERFACE
# ==================================================

def run(board):

    global nodes
    global moves

    # Reset state for every new Sudoku
    nodes = 0
    moves = []

    # Solve the user's Sudoku
    solved = solve(board)

    # Return result to Flask
    return {
        "board": board,
        "nodes": nodes,
        "solved": solved,
        "moves": moves
    }