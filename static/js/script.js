const warehouses = JSON.parse(
	document.getElementById('warehouses').textContent
);
const avg_lat = JSON.parse(document.getElementById('avg_lat').textContent);
const avg_long = JSON.parse(document.getElementById('avg_long').textContent);
var map = L.map('map').setView([avg_lat, avg_long], 13);

console.log(warehouses);

window.addEventListener('load', () => {
	L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
		maxZoom: 19,
		attribution:
			'&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
	}).addTo(map);

	// L.Routing.control({
	// 	waypoints: [L.latLng(57.74, 11.94), L.latLng(57.6792, 11.949)],
	// }).addTo(map);

	var markerGroup = [];

	warehouses.forEach((warehouse) => {
		marker = L.marker([warehouse.lat, warehouse.long]);
		marker.addTo(map).bindPopup(warehouse.name);
		markerGroup.push(marker);
	});

	var group = new L.featureGroup(markerGroup);
	map.fitBounds(group.getBounds());
});
