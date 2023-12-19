const colorCards = document.querySelectorAll('.color-click');
const letterColorInput = document.getElementById('letter_color');


colorCards.forEach(card => {
    card.addEventListener('click', function() {
        const selectedColor = this.style.backgroundColor;

        const messageColor = document.getElementById('message-color');
        messageColor.style.backgroundColor = selectedColor

        const textColor = getContrastColor(selectedColor);
        const textArea = document.getElementById('message')
        textArea.style.color = textColor
        letterColorInput.value = selectedColor;
    });
});

function getContrastColor(rgbColor) {
    const rgbValues = rgbColor.match(/\d+/g);

    const red = parseInt(rgbValues[0]);
    const green = parseInt(rgbValues[1]);
    const blue = parseInt(rgbValues[2]);
    const brightness = Math.round((red * 299 + green * 587 + blue * 114) / 1000);

    return brightness > 125 ? 'black' : 'white';
}
