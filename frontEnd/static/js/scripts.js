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

