const warehouses = JSON.parse(
	document.getElementById('warehouses').textContent
);
const avg_lat = JSON.parse(document.getElementById('avg_lat').textContent);
const avg_long = JSON.parse(document.getElementById('avg_long').textContent);
const shipment_data = JSON.parse(
	document.getElementById('shipment_data').textContent
);
var map = L.map('map').setView([avg_lat, avg_long], 13);
var markerGroup = [];

console.log(warehouses);

function sendShipments(coords, id) {
	const shipmentMarker = L.marker(coords[0]);
	shipmentMarker.addTo(map);
	// shipmentMarker.addTo(map).bindPopup(`Shipment to ${shipment.location}`);
	markerGroup.push(shipmentMarker);

	var counter = 0;
	var intervalId = setInterval(async function () {
		if (counter < coords.length) {
			shipmentMarker.setLatLng(coords[counter]);
			const response = await fetch(
				`http://127.0.0.1:8000/update_coords/${id}`,
				{
					method: 'POST',
					body: JSON.stringify({
						latitude: coords[counter].lat,
						longitude: coords[counter].lng,
					}),
				}
			);
			// console.log(response);
			counter += 30;
		} else {
			clearInterval(intervalId);
			const response = await fetch(
				`http://127.0.0.1:8000/update_shipment_state/${id}`,
				{
					method: 'POST',
					body: JSON.stringify({
						status: 'Delivered',
					}),
				}
			);
			counter = 0;
		}
	}, 100);
}

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

	function getRoute(waypoints) {
		return new Promise((resolve, reject) => {
			const router = L.Routing.osrmv1();
			router.route(waypoints, function (err, routes) {
				if (err) {
					reject(err); // Reject the Promise if there's an error
				} else {
					line = L.Routing.line(routes[0]).addTo(map);
					resolve(routes[0].coordinates); // Resolve the Promise with the route coordinates
				}
			});
		});
	}

	warehouses.forEach((warehouse) => {
		const warehouseMarker = L.marker([warehouse.lat, warehouse.long]);
		warehouseMarker.addTo(map).bindPopup(warehouse.name);
		markerGroup.push(warehouseMarker);

		if (warehouse.shipment_data) {
			warehouse.shipment_data.forEach(async (s) => {
				if (s.status == 'In Transit' || s.status == 'Delayed') {
					var waypoints = [];
					waypoints.push({
						latLng: L.latLng(warehouse.lat, warehouse.long),
					});
					waypoints.push({ latLng: L.latLng(s.lat, s.long) });

					try {
						const routes1 = await getRoute(waypoints); // Wait for the route to be resolved
						console.log(routes1); // Use routes1 here
						// Example: Add a line to the map

						sendShipments(routes1, s.id, s.lat, s.long);
						// routes1.forEach((coords, index) => {
						// 	setTimeout(() => {
						// 		marker.setLatLng(coords);
						// 	}, index * 10);
						// });
					} catch (err) {
						console.error('Error fetching route:', err);
					}
				}
			});
		}
	});

	var group = new L.featureGroup(markerGroup);
	map.fitBounds(group.getBounds());
});
