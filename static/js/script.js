const warehouses = JSON.parse(
	document.getElementById('warehouses').textContent
);
const avg_lat = JSON.parse(document.getElementById('avg_lat').textContent);
const avg_long = JSON.parse(document.getElementById('avg_long').textContent);
const shipment_data = JSON.parse(
	document.getElementById('shipment_data').textContent
);
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

		if (warehouse.shipment_data) {
			warehouse.shipment_data.forEach((s) => {
				var router = L.Routing.osrmv1(),
					waypoints = [],
					line;
				waypoints.push({
					latLng: L.latLng(warehouse.lat, warehouse.long),
				});
				waypoints.push({ latLng: L.latLng(s.lat, s.long) });

				router.route(waypoints, function (err, routes) {
					if (line) {
						map.removeLayer(line);
					}

					if (err) {
						alert(err);
					} else {
						line = L.Routing.line(routes[0]).addTo(map);
					}
				});
			});
		}
	});

	var group = new L.featureGroup(markerGroup);
	map.fitBounds(group.getBounds());
});
