
# Sudoku Solver

A web-based Sudoku Solver built with Python and Flask. It implements four different solving approaches, ranging from basic backtracking to constraint-based optimization and human-inspired solving techniques.

The application allows users to enter a Sudoku puzzle, choose a solving algorithm, and watch the solver work through the puzzle with a step-by-step animation.

## Features

- **Interactive Sudoku Grid:** Enter numbers directly into the 9×9 grid.
- **On-Screen Number Pad:** Enter numbers using the built-in 3×3 number pad, with an Erase option.
- **Multiple Solving Algorithms:** Choose between four different solver implementations.
- **Step-by-Step Visualization:** Watch the algorithm place and backtrack numbers while solving.
- **Dark Mode:** Switch between light and dark themes.
- **Solver Statistics:** View the number of nodes explored and the solution status.
- **Original Puzzle Preservation:** Compare the original clues with the numbers filled in by the solver.

## Solving Algorithms

The project implements four different approaches to solving Sudoku.

| Algorithm | Approach |
|---|---|
| Basic Backtracking | Tries possible numbers recursively and backtracks when a contradiction is found. |
| MRV | Uses the Minimum Remaining Values heuristic to select the empty cell with the fewest valid candidates. |
| MRV + Incremental Tracking + LCV | Maintains candidate information incrementally and uses the Least Constraining Value heuristic to improve number selection. |
| Human Techniques + MRV | Applies techniques such as Naked Singles and Hidden Singles before falling back to MRV-based search. |

## Tech Stack

- **Python** – Sudoku-solving algorithms and backend logic.
- **Flask** – Web application framework.
- **HTML5** – Page structure.
- **CSS3** – Styling, responsive layout, and theme support.
- **JavaScript** – Interactive number pad, theme switching, and solving animations.
- **Jinja2** – Dynamic HTML rendering through Flask.

## Project Structure

```text
sudoku_solver/
│
├── app.py
│
├── solvers/
│   ├── basic.py
│   ├── MRV.py
│   ├── MRV_incr.py
│   └── advanced.py
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── static/
│   ├── style.css
│   ├── script.js
│   ├── theme.js
│   └── input.js
│
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/hxvrsh/Sudoku-Solver.git
```

### 2. Navigate to the Project Directory

```bash
cd Sudoku-Solver
```

### 3. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install flask
```

### 5. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## How to Use

1. Open the application in your browser.
2. Enter the Sudoku puzzle into the 9×9 grid.
3. Use the on-screen number pad or your keyboard to enter numbers.
4. Select a solving algorithm from the dropdown.
5. Click **Solve Sudoku**.
6. Watch the algorithm solve the puzzle through the step-by-step animation.
7. Compare the original clues with the numbers filled in by the solver.

## Learning Objectives

This project was developed to explore and understand:

- Recursive backtracking and state-space search.
- Constraint satisfaction problems (CSP).
- Minimum Remaining Values (MRV) heuristic.
- Least Constraining Value (LCV) heuristic.
- Incremental candidate tracking.
- Naked Singles and Hidden Singles.
- Comparing different algorithmic approaches through node exploration and visualization.




