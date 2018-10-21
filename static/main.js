$(document).ready(
  () => {
    var map = L.map('mapid', {doubleClickZoom: false}).locate({setView: true, maxZoom: 8});
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	    attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
	  }).addTo(map);
    map.on("click", (e) => {
        $("#log").append("Lat, Lon : " + e.latlng.lat + ", " + e.latlng.lng + "<br/>");
    });
  }
);
