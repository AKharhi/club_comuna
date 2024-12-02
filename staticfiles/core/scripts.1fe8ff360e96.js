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
        mapId: '2c506293d4525b2e', // Reemplaza 'TU_MAP_ID' con tu verdadero ID de mapa

    });
    // Agregar todos los marcadores de los negocios al mapa
    const negocios = JSON.parse(document.getElementById("negocios-data").textContent);
    negocios.forEach(negocio => {
        const marker = new google.maps.Marker({
            position: { lat: negocio.latitud, lng: negocio.longitud },
            map: map,
            title: negocio.nombre,
            icon: "https://club-de-la-comuna.s3.sa-east-1.amazonaws.com/logo_club_comuna.PNG", // Icono personalizado
        });
        markers.push(marker);
    });
}

// Función para centrar el mapa en un marcador específico
function centerMap(lat, lng) {
  map.setCenter({ lat, lng });
  map.setZoom(16); // Acercar el mapa
}


function addMarker(lat, lng, title) {
  const marker = new google.maps.Marker({
      position: { lat: parseFloat(lat), lng: parseFloat(lng) },
      map: map,
      title: title,
  });
  markers.push(marker);
  map.setCenter({ lat: parseFloat(lat), lng: parseFloat(lng) });
  map.setZoom(16); // Acercar el mapa
}






// Manejar clics en las direcciones
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".direccion-link").forEach(link => {
      link.addEventListener("click", function (event) {
          event.preventDefault();
          const lat = parseFloat(this.dataset.lat.replace(',', '.'));
          const lng = parseFloat(this.dataset.lng.replace(',', '.'));
          const title = this.textContent.trim();
          console.log("Clic en dirección:", lat, lng);

          if (!isNaN(lat) && !isNaN(lng)) {
              centerMap(lat, lng);
          } else {
              console.error("Coordenadas inválidas:", lat, lng);
          }
      });
  });
});


window.initMap = initMap;

console.log("JS JSJSJSJS")






