/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

document.addEventListener('DOMContentLoaded', function () {
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function (e) {
            e.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
        });
    }
});


document.getElementById("buscarAtributoBtn").addEventListener("click", function() {
    const atributo = document.getElementById("atributo").value;
    const valor = document.getElementById("valorAtributo").value;

    // Validar campos
    if (!atributo || !valor) {
        alert("Por favor completa ambos campos.");
        return;
    }

    // Redirigir con parámetros por GET
    const url = `/buscar-por-atributo?atributo=${encodeURIComponent(atributo)}&valor=${encodeURIComponent(valor)}`;
    window.location.href = url;
});

function ordenarPorSuma(direccion = 'desc') {
    const tbody = document.getElementById("voluntariosBody");
    const filas = Array.from(tbody.querySelectorAll("tr"));

    const obtenerSuma = (fila) => {
        const constructivo = parseInt(fila.children[3]?.innerText) || 0;
        const social = parseInt(fila.children[4]?.innerText) || 0;
        const genero = parseInt(fila.children[5]?.innerText) || 0;
        return constructivo + social + genero;
    };

    filas.sort((a, b) => {
        const sumaA = obtenerSuma(a);
        const sumaB = obtenerSuma(b);
        return direccion === 'asc' ? sumaA - sumaB : sumaB - sumaA;
    });

    tbody.innerHTML = "";
    filas.forEach(fila => tbody.appendChild(fila));
}
