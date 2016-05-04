// initialize the map
var map = L.map('map').setView([37.76, -122.35], 9);
//    -122.354736
//    37.762030
// load a tile layer
L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
}).addTo(map);

L.tileLayer('http://{s}.tile.openstreetmap.se/hydda/roads_and_labels/{z}/{x}/{y}.png', {
    attribution: 'Tiles courtesy of <a href="http://openstreetmap.se/" target="_blank">OpenStreetMap Sweden</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// load GeoJSON from an external file
$.getJSON("php/stationlist.php", function (data) {
    for (var i = 0; i < data.length; i++) {
        var location = new L.LatLng(data[i].latitude, data[i].longitude);
        var id = data[i].id;
        var stationname = data[i].stationname;
        var sensorslist = data[i].sensorslist;
//            console.log(data);

        L.marker(location, {title: stationname, riseOnHover: true}).addTo(map)
            //                    .bindPopup(stationname + '<br>' + sensorslist)
            .on('click', onClick = scopepreserver(id));
    }

    function scopepreserver(id) {
        return function () {
            console.log(id);
            $('#' + id).modal('show')

        };
    }

//        function onClick(e) {
//
////            var theid = this.getAttribute('id');
////console.log(theid);
////            console.log(e.latlng.lat);
////            $('#sfbaypier17a').modal('show')
//
//
////            $('#'+id).modal('show')
//
//        }
});