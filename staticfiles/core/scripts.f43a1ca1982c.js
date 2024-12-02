(function () {
  'use strict';

  // Validación de formularios
  var forms = document.querySelectorAll('.needs-validation');
  Array.prototype.slice.call(forms).forEach(function (form) {
      form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
              event.preventDefault();
              event.stopPropagation();
          }
          form.classList.add('was-validated');
      }, false);
  });
})();

// Inicializar el mapa y marcadores
let map;
let markers = [];

function initMap() {
  const defaultLocation = { lat: -33.4928, lng: -70.6057 }; // Ubicación inicial
  console.log("Mapa inicializado correctamente");

  map = new google.maps.Map(document.getElementById("map"), {
      center: defaultLocation,
      zoom: 12,
      mapId: '2c506293d4525b2e',

      
  });

  // Intentar obtener la ubicación actual del usuario
  if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
          (position) => {
              const userLocation = {
                  lat: position.coords.latitude,
                  lng: position.coords.longitude,
              };
              console.log("Ubicación del usuario obtenida:", userLocation);
              map.setCenter(userLocation);
              map.setZoom(14); // Ajustar el nivel de zoom si se necesita
          },
          () => {
              console.error("No se pudo obtener la ubicación del usuario.");
          }
      );
  } else {
      console.error("Geolocalización no es compatible con este navegador.");
  }

  // Agregar marcadores
  // const negocios = JSON.parse(document.getElementById("negocios-data").textContent);

}

// Centrar el mapa al hacer clic en la dirección
function centerMap(lat, lng) {
  const latLng = new google.maps.LatLng(lat, lng);
  map.setCenter(latLng);
  map.setZoom(16); // Acercar
}

// Manejar clics en las direcciones
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".direccion-link").forEach(link => {
      link.addEventListener("click", function (event) {
          event.preventDefault();

          const lat = parseFloat(this.dataset.lat.replace(',', '.'));
          const lng = parseFloat(this.dataset.lng.replace(',', '.'));
          console.log("Clic en dirección:", lat, lng);

          if (!isNaN(lat) && !isNaN(lng)) {
              centerMap(lat, lng);
          } else {
              console.error("Coordenadas inválidas:", lat, lng);
          }
      });
  });
});


console.log("JS cargado correctamente.");
