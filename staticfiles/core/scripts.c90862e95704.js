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


function createMarker(place) {
  if (!place.geometry || !place.geometry.location) return;

  const marker = new google.maps.Marker({
    map,
    position: place.geometry.location,
    icon: {
      url: "https://club-de-la-comuna.s3.sa-east-1.amazonaws.com/logo_club_comuna.PNG", // URL de tu icono personalizado
      scaledSize: new google.maps.Size(40, 40), // Ajuste del tamaño del icono
    },
  });

  // Agregar evento para mostrar el nombre y la opción de obtener direcciones al hacer clic en el marcador
  google.maps.event.addListener(marker, "click", () => {
    // Crear un enlace de Google Maps para obtener direcciones desde la ubicación actual
    const directionsUrl = `https://www.google.com/maps/dir/?api=1&origin=current+location&destination=${place.geometry.location.lat()},${place.geometry.location.lng()}`;

    // Contenido de la ventana de información
    const contentString = `
      <div>
        <strong>Pastelería D'Gustar</strong><br>
        <strong>${place.name || "Negocio Local"}</strong><br>
        <a href="${directionsUrl}" target="_blank">Cómo llegar</a>
      </div>
    `;

    infowindow.setContent(contentString);
    infowindow.open(map, marker);
  });
}

window.initMap = initMap;






