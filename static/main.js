var coordinateList = [];
var modelTargetIndex = -1;

$(document).ready(
  () => {
    var map = L.map('mapid', {doubleClickZoom: false}).locate({setView: true, maxZoom: 10});
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	    attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
	  }).addTo(map);
    map.on("click", (e) => {
        //$("#log").append("Lat, Lon : " + e.latlng.lat + ", " + e.latlng.lng + "<br/>");
        coordinateList.push({latlng: e.latlng});
        var coordId = coordinateList.length - 1;
        if (modelTargetIndex == -1) {
          modelTargetIndex = 0;
        }
        $("#coordinateList").append('<div class="custom-control custom-radio"><input name="modelTarget" type="radio" id="coord' + coordId +'" class="custom-control-input"/><label class="custom-control-label" for="coord' + coordId +'">Latituted: ' + e.latlng.lat + ', longitude: ' + e.latlng.lng + '.</label></div>');
    });
  }
);

/*
<div class="custom-control custom-radio">
  <input name="modelTarget" type="radio" id="coord' + coordinateId +'" class='custom-control-input'/>
  <label class="custom-control-label" for="coord' + coordinateId +'">Latituted: ' + e.latlng.lat + ', longitude: ' + e.latlng.lng + '.</label>
</div>

<div class="input-group m-1">
  <div class="input-group-prepend">
    <div class="input-group-text">
      <input name="modelTarget" type="radio" id="coord' + coordinateId + '"/>
    </div>
  </div>
</div>
*/
