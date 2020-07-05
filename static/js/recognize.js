/* Na validação estava assim:
size: 4,
controls: [
    size.... dropdown
]
*/
var myBoard = new DrawingBoard.Board('zbeubeu', {
    // size: 7,
    // size: 5,
    size: 5, 
    controls: [
        // { Size: { type: 'dropdown' } },
        { Navigation: { back: false, forward: false } },
        { DrawingMode: { filler: false, eraser: false } }
    ],
    // webStorage: 'local'
    webStorage: false
});

var reconhecer = document.querySelector("#reconhecer"),
    loading = document.querySelector("#loading"),
    latexElement = document.querySelector("#latex"),
    errorElement = document.querySelector(".quadro__resultado__error"),
    teste = document.querySelector("#teste");

reconhecer.addEventListener("click", function() {

    latexElement.classList.remove('--error');
    errorElement.classList.remove('--show');
    loading.classList.add('--show');
    teste.innerHTML = "";

    if (!reconhecer.classList.contains('--disabled')) {

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
            } else {
                MathJax.texReset();
                var options = MathJax.getMetricsFor(teste);
                options.display = true;
                MathJax.tex2chtmlPromise(data.latex, options).then(function (node) {
                    teste.appendChild(node);
                    MathJax.startup.document.clear();
                    MathJax.startup.document.updateDocument();
                }).catch(function (err) {
                    teste.innerHTML(document.createElement('pre')).appendChild(document.createTextNode(err.message));
                }).then(function () {
                    // nothing
                });
            }
            
        })
        .finally(function() {
            reconhecer.classList.remove('--disabled');
            loading.classList.remove('--show')
        });
    }
});
