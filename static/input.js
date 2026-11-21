const inputCells = document.querySelectorAll(".sudoku-grid input");
const numberButtons = document.querySelectorAll(".number-button");
const eraseButton = document.getElementById("eraseButton");

let selectedCell = null;


inputCells.forEach(cell => {

    cell.addEventListener("focus", () => {

        selectedCell = cell;

        inputCells.forEach(input => {
            input.classList.remove("active-cell");
        });

        cell.classList.add("active-cell");

    });

});


numberButtons.forEach(button => {

    button.addEventListener("click", () => {

        if (!selectedCell) {
            return;
        }

        selectedCell.value = button.dataset.number;

        selectedCell.dispatchEvent(new Event("input", {
            bubbles: true
        }));

    });

});


eraseButton.addEventListener("click", () => {

    if (!selectedCell) {
        return;
    }

    selectedCell.value = "";

    selectedCell.dispatchEvent(new Event("input", {
        bubbles: true
    }));

});