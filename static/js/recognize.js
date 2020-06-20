var myBoard = new DrawingBoard.Board('zbeubeu', {
    size: 7,
    controls: [
        { Size: { type: false } },
        { Navigation: { back: false, forward: false } },
        { DrawingMode: { filler: false } }
    ],
    // webStorage: 'local'
    webStorage: false
});

var reconhecer = document.querySelector("#reconhecer");
var latexElement = document.querySelector("#latex");
var errorElement = document.querySelector(".quadro__resultado__error");

reconhecer.addEventListener("click", function() {

    latexElement.classList.remove('--error');
    errorElement.classList.remove('--show');

    if(!reconhecer.classList.contains('--disabled')) {
        reconhecer.classList.add('--disabled');
        var img = myBoard.getImg();
        fetch('ajax/recognize/',{
            method: 'POST',
            headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json' },
            body: JSON.stringify({
                "image": img
            })
        })
        .then(function(response) {
            return response.text()
        })
        .then(function(data) {
            data = JSON.parse(data)
            latexElement.innerText = data.latex;
            if(data.error) {
                latexElement.classList.add('--error')
                errorElement.classList.add('--show');
            }
        })
        .finally(function() {
            reconhecer.classList.remove('--disabled');
        });
    }
});
