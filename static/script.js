const cells = document.querySelectorAll(".solved-cell");
const skipButton = document.getElementById("skipButton");

const solverData = JSON.parse(
    document.getElementById("solver-data").textContent
);

const moves = solverData.moves;
const solvedBoard = solverData.board;

let currentMove = 0;
let animationStopped = false;

const animationSpeed = 120;


function getCell(row, col) {

    return document.querySelector(
        `.solved-cell[data-row="${row}"][data-col="${col}"]`
    );

}


function clearSelection() {

    cells.forEach(cell => {
        cell.classList.remove("selected-cell");
    });

}


function performMove(move) {

    const cell = getCell(move.row, move.col);

    if (!cell) {
        return;
    }


    if (move.action === "select") {

        clearSelection();

        cell.classList.add("selected-cell");

        return;
    }


    if (move.action === "place") {

        cell.textContent = move.value;

        cell.classList.remove("selected-cell");
        cell.classList.remove("backtracked");

        cell.classList.add("revealed");

        return;
    }


    if (move.action === "backtrack") {

        cell.textContent = "";

        cell.classList.remove("selected-cell");
        cell.classList.add("backtracked");

        return;
    }
    
    if (move.action === "naked_single" || move.action === "hidden_single") {
        cell.textContent = move.value;

        cell.classList.remove("selected-cell");
        cell.classList.remove("backtracked");
        cell.classList.add("revealed");
        return;
    }
}


function playNextMove() {

    if (animationStopped) {
        return;
    }


    if (currentMove >= moves.length) {

        skipButton.disabled = true;
        clearSelection();

        return;
    }


    const move = moves[currentMove];

    performMove(move);

    currentMove++;

    setTimeout(playNextMove, animationSpeed);

}


function skipAnimation() {

    animationStopped = true;

    clearSelection();


    for (let row = 0; row < 9; row++) {

        for (let col = 0; col < 9; col++) {

            const cell = getCell(row, col);

            if (cell) {
                cell.textContent = solvedBoard[row][col];
            }

        }

    }


    skipButton.disabled = true;
}


skipButton.addEventListener("click", skipAnimation);

playNextMove();