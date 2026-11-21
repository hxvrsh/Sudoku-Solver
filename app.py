from flask import Flask, render_template, request

from solvers import basic
from solvers import MRV
from solvers import MRV_incr
from solvers import advanced

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/solve", methods=["POST"])
def solve():

    solver_name = request.form["solver"]

    board = []

    for row in range(9):

        current_row = []

        for col in range(9):

            value = request.form[f"cell_{row}_{col}"]

            if value == "":
                value = 0
            else:
                value = int(value)

            current_row.append(value)

        board.append(current_row)

    original_board = [row[:] for row in board]

    if solver_name == "basic":
        result = basic.run(board)

    elif solver_name == "mrv":
        result = MRV.run(board)

    elif solver_name == "mrv_incr":
        result = MRV_incr.run(board)

    elif solver_name == "advanced":
        result = advanced.run(board)

    else:
        return "Invalid solver selected"

    return render_template(
        "result.html",
        result=result,
        solver=solver_name,
        original_board=original_board
    )


if __name__ == "__main__":
    app.run(debug=True)