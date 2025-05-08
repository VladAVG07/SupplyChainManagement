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
		marker = L.marker([warehouse.lat, warehouse.long]);
		marker.addTo(map).bindPopup(warehouse.name);
		markerGroup.push(marker);

		if (warehouse.shipment_data) {
			warehouse.shipment_data.forEach(async (s) => {
				var waypoints = [];
				waypoints.push({
					latLng: L.latLng(warehouse.lat, warehouse.long),
				});
				waypoints.push({ latLng: L.latLng(s.lat, s.long) });

				try {
					const routes1 = await getRoute(waypoints); // Wait for the route to be resolved
					console.log(routes1); // Use routes1 here
					// Example: Add a line to the map
					marker = L.marker(routes1[0]);
					marker.addTo(map);

					var counter = 0;
					var intervalId = setInterval(function () {
						if (counter < routes1.length) {
							marker.setLatLng(routes1[counter]);
							counter += 30;
						} else {
							clearInterval(intervalId);
							counter = 0;
						}
					}, 5000);

					// routes1.forEach((coords, index) => {
					// 	setTimeout(() => {
					// 		marker.setLatLng(coords);
					// 	}, index * 10);
					// });
				} catch (err) {
					console.error('Error fetching route:', err);
				}
			});
		}
	});

	var group = new L.featureGroup(markerGroup);
	map.fitBounds(group.getBounds());
});
