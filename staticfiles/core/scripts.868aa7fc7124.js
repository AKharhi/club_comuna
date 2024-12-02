// JavaScript para activar la validación de Bootstrap en los formularios
(function () {
    'use strict'

    // Obtener todos los formularios a los que queremos aplicar estilos de validación de Bootstrap
    var forms = document.querySelectorAll('.needs-validation')

    // Evitar el envío del formulario si no pasa la validación
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })
})()

let map;
let markers = [];

// Inicializar el mapa
function initMap() {
    const defaultLocation = { lat: -33.447487, lng: -70.673676 }; // Ubicación inicial
    map = new google.maps.Map(document.getElementById("map"), {
        center: defaultLocation,
        zoom: 12,
    });
}

// Función para agregar un marcador al mapa
function addMarker(lat, lng, title) {
    const marker = new google.maps.Marker({
        position: { lat, lng },
        map: map,
        title: title,
    });
    markers.push(marker);
    map.setCenter({ lat, lng });
    map.setZoom(16); // Acercar el mapa
}

// Manejar clics en las direcciones
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".direccion-link").forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault(); // Evitar redirección
            const lat = parseFloat(this.dataset.lat);
            const lng = parseFloat(this.dataset.lng);
            const title = this.textContent.trim();

            if (!isNaN(lat) && !isNaN(lng)) {
                addMarker(lat, lng, title);
            } else {
                console.error("Coordenadas inválidas:", lat, lng);
            }
        });
    });
});



window.initMap = initMap;






