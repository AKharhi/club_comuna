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
let service;
let infowindow;

function initMap() {
  // Coordenadas de Macul, Santiago como valor por defecto
  const maculCenter = new google.maps.LatLng(-33.4928, -70.61);

  infowindow = new google.maps.InfoWindow();
  map = new google.maps.Map(document.getElementById("map"), {
    center: maculCenter,
    zoom: 14,
  });

  // Intentar obtener la ubicación actual del usuario
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const userLocation = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };
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

  // Lista de negocios con sus direcciones
  const locations = [
    { name: "Agua Purificada Macul", query: "Las Dalias 2790, Macul, Región Metropolitana" },
    { name: "Vivero Kiarita", query: "Av. Escuela Agrícola 1924, Macul, Región Metropolitana" },
    { name: "Servicios IA", query: "Av. Quilín 4245, Macul, Región Metropolitana" },
    { name: "Dentista Maty", query: "Av. Macul 4122, Macul, Región Metropolitana" },
    { name: "El Talquino", query: "Av. Macul 4041, Macul, Región Metropolitana" },
    { name: "El Alemán Experto", query: "Av. Macul 2955, Macul, Región Metropolitana" },
    { name: "Farmacia Macul", query: "Av. Macul N°2555, Macul, Región Metropolitana" },
    { name: "Floristería Macul", query: "Av. Pedro de Valdivia 6915, Macul, Región Metropolitana" },
    { name: "Verduras Catalina", query: "Los Olmos 3967, Macul, Región Metropolitana" },
    { name: "Pancitos Almendral", query: "Av. Macul 3049, Macul, Región Metropolitana" },
    { name: "Pastelería D’Gustar", query: "Av. Macul 3226, Macul, Región Metropolitana" }
  ];

  service = new google.maps.places.PlacesService(map);

  // Buscar y crear marcadores para cada ubicación
  locations.forEach((location) => {
    service.findPlaceFromQuery({ query: location.query, fields: ["name", "geometry"] }, (results, status) => {
      if (status === google.maps.places.PlacesServiceStatus.OK && results) {
        createMarker(results[0], location.name); // Crear marcador y pasar el nombre del negocio
      }
    });
  });
}

function createMarker(place, businessName) {
  if (!place.geometry || !place.geometry.location) return;

  const marker = new google.maps.Marker({
    map,
    position: place.geometry.location,
    icon: {
      url: "https://club-de-la-comuna.s3.sa-east-1.amazonaws.com/logo_club_comuna.PNG", // URL de tu icono personalizado
      scaledSize: new google.maps.Size(30, 30), // Ajuste del tamaño del icono
    },
  });

  // Agregar evento para mostrar el nombre y la opción de obtener direcciones al hacer clic en el marcador
  google.maps.event.addListener(marker, "click", () => {
    // Crear un enlace de Google Maps para obtener direcciones desde la ubicación actual
    const directionsUrl = `https://www.google.com/maps/dir/?api=1&origin=current+location&destination=${place.geometry.location.lat()},${place.geometry.location.lng()}`;

    // Contenido de la ventana de información con el nombre del negocio
    const contentString = `
      <div>
        <strong>${businessName}</strong><br>
        <a href="${directionsUrl}" target="_blank">Cómo llegar</a>
      </div>
    `;

    infowindow.setContent(contentString);
    infowindow.open(map, marker);
  });
}

window.initMap = initMap;
