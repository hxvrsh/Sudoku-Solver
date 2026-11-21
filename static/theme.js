const themeButton = document.getElementById("themeToggle");

function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);

    if (theme === "dark") {
        themeButton.textContent = "☀ Light mode";
    } else {
        themeButton.textContent = "☾ Dark mode";
    }
}

const currentTheme = localStorage.getItem("sudoku-theme") || "light";
applyTheme(currentTheme);

themeButton.addEventListener("click", () => {
    const currentTheme = document.documentElement.getAttribute("data-theme");

    const newTheme = currentTheme === "dark" ? "light" : "dark";

    applyTheme(newTheme);
    localStorage.setItem("sudoku-theme", newTheme);
});