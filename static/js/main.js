document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("displayButton");
    const textBox = document.getElementById("textBox");

    button.addEventListener("click", () => {
        textBox.textContent = "Hello! You clicked the button!";
    });
});
