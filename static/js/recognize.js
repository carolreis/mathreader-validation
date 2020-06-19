var myBoard = new DrawingBoard.Board('zbeubeu', {
    size: 7,
    controls: [
        { Size: { type: false } },
        { Navigation: { back: false, forward: false } },
        { DrawingMode: { filler: false } }
    ],
    webStorage: 'local'
});

var reconhecer = document.querySelector("#reconhecer");

reconhecer.addEventListener("click", function() {
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
            document.querySelector("#latex").innerText = data.latex;
        })
        .finally(function() {
            reconhecer.classList.remove('--disabled');
        });
    }
});
